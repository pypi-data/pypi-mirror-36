import singer
from singer import metrics, metadata, Transformer

from tap_listrak.schema import PKS

def write_schema(catalog, stream_id):
    stream = catalog.get_stream(stream_id)
    schema = stream.schema.to_dict()
    key_properties = PKS[stream_id]
    singer.write_schema(stream_id, schema, key_properties)

def persist_records(catalog, stream_id, records):
    stream = catalog.get_stream(stream_id)
    schema = stream.schema.to_dict()
    stream_metadata = metadata.to_map(stream.metadata)
    with metrics.record_counter(stream_id) as counter:
        for record in records:
            with Transformer() as transformer:
                record = transformer.transform(record,
                                               schema,
                                               stream_metadata)
            singer.write_record(stream_id, record)
            counter.increment()

def nested_get(dic, keys, default_value):
    cur_dic = dic
    for key in keys[:-1]:
        if key in cur_dic:
            cur_dic = cur_dic[key]
        else:
            return default_value

    if keys[-1] in cur_dic:
        return cur_dic[keys[-1]]

    return default_value

def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

def get_selected_streams(catalog):
    selected_streams = set()
    for stream in catalog.streams:
        mdata = metadata.to_map(stream.metadata)
        root_metadata = mdata.get(())
        if root_metadata and root_metadata.get('selected') is True:
            selected_streams.add(stream.tap_stream_id)
    return list(selected_streams)

def sync_lists(client, catalog, persist):
    lists, _ = client.get('/List', endpoint='lists')
    if lists and persist:
        write_schema(catalog, 'lists')
        persist_records(catalog, 'lists', lists)
    return lists

def sync_campaigns(client, catalog, list_id):
    campaigns, _ = client.get('/List/{}/Campaign'.format(list_id), endpoint='campaigns')
    def transform_campaign(row):
        row['listId'] = list_id
        return row
    campaigns = map(transform_campaign, campaigns)
    if campaigns:
        write_schema(catalog, 'campaigns')
        persist_records(catalog, 'campaigns', campaigns)

def sync_contact_page(client, list_id, subscription_state, start_date, next_token):
    return client.get(
        '/List/{}/Contact'.format(list_id),
        params={
            'cursor': next_token,
            'subscriptionState': subscription_state,
            'startDate': start_date,
            'count': 5000
        },
        endpoint='contacts')

def get_contacts_bookmark(state, list_id, contact_state, start_date):
    return nested_get(state, ['bookmarks', list_id, 'contacts', contact_state], start_date)

def write_contacts_bookmark(state, list_id, contact_state, max_date):
    nested_set(state, ['bookmarks', list_id, 'contacts', contact_state], max_date)
    singer.write_state(state)

def sync_contacts_subscription_state(state, client, catalog, start_date, list_id, subscription_state):
    if subscription_state == 'Subscribed':
        date_key = 'subscribeDate'
    else:
        date_key = 'unsubscribeDate'

    def contacts_transform(contact):
        contact['listId'] = list_id
        return contact

    max_date = start_date
    next_token = 'Start'
    while next_token is not None:
        contacts, next_token = sync_contact_page(client,
                                                 list_id,
                                                 subscription_state,
                                                 start_date,
                                                 next_token)
        if contacts:
            contacts = list(map(contacts_transform, contacts))
            persist_records(catalog, 'contacts', contacts)

            max_data_date = max(contacts, key=lambda x: x[date_key])[date_key]
            if max_data_date > max_date:
                max_date = max_data_date

    # stream is not ordered, so we have to persist state at the end
    write_contacts_bookmark(state, list_id, subscription_state, max_date)

def sync_contacts(client, catalog, state, start_date, list_id):
    write_schema(catalog, 'contacts')

    subscribed_last_date = get_contacts_bookmark(state, list_id, 'Subscribed', start_date)
    sync_contacts_subscription_state(state,
                                     client,
                                     catalog,
                                     subscribed_last_date,
                                     list_id,
                                     'Subscribed')

    unsubscribed_last_date = get_contacts_bookmark(state, list_id, 'Unsubscribed', start_date)
    sync_contacts_subscription_state(state,
                                     client,
                                     catalog,
                                     unsubscribed_last_date,
                                     list_id,
                                     'Unsubscribed')

def get_messages(client, list_id, message_ids):
    messages = []
    for message_id in message_ids:
        message, _ = client.get(
            '/List/{}/Message/{}'.format(list_id, message_id),
            endpoint='messages')
        messages.append(message)
    return messages

def sync_messages(client, catalog, list_id, persist):
    write_schema(catalog, 'messages')

    message_ids = []

    def messages_transform(message):
        message['listId'] = list_id
        return message

    next_token = 'Start'
    while next_token is not None:
        messages_list, next_token = client.get(
            '/List/{}/Message'.format(list_id),
            params={
                'cursor': next_token,
                'count': 5000
            },
            endpoint='messages_list')
        page_message_ids = list(map(lambda x: x['messageId'], messages_list))
        message_ids += page_message_ids

        if messages_list and persist:
            messages = get_messages(client, list_id, page_message_ids)
            messages = list(map(messages_transform, messages))
            persist_records(catalog, 'messages', messages)

    return message_ids

def sync_message_activity(client, catalog, state, start_date, list_id, message_id):
    write_schema(catalog, 'message_activity')

    bookmark_path = ['bookmarks',
                     list_id,
                     'messages',
                     message_id,
                     'message_activity']
    activity_start_date = nested_get(state,
                                     bookmark_path,
                                     start_date)

    def activity_transform(activity):
        activity['listId'] = list_id
        activity['messageId'] = message_id
        return activity

    max_date = activity_start_date
    next_token = 'Start'
    while next_token is not None:
        activities, next_token = client.get(
            '/List/{}/Message/{}/Activity'.format(
                list_id,
                message_id),
            params={
                'cursor': next_token,
                'count': 5000,
                'dateType': 'Activity',
                'startDate': activity_start_date
            },
            endpoint='message_activity')

        if activities:
            page_max_date = max(filter(lambda x: x is not None,
                                       map(lambda x: x['activityDate'], activities)))
            if page_max_date > max_date:
                max_date = page_max_date

            activities = list(map(activity_transform, activities))
            persist_records(catalog, 'message_activity', activities)

    nested_set(state, bookmark_path, max_date)
    singer.write_state(state)

def sync_message_links(client, catalog, list_id, message_id, persist):
    write_schema(catalog, 'message_links')

    message_link_ids = []

    def message_links_transform(message_link):
        message_link['listId'] = message_id
        message_link['messageId'] = message_id
        return message_link

    next_token = 'Start'
    while next_token is not None:
        message_links, next_token = client.get(
            '/List/{}/Message/{}/Link'.format(list_id, message_id),
            params={
                'cursor': next_token,
                'count': 5000
            },
            endpoint='message_links')
        message_link_ids += list(map(lambda x: x['linkId'], message_links))

        if message_links and persist:
            message_links = list(map(message_links_transform, message_links))
            persist_records(catalog, 'message_links', message_links)

    return message_link_ids

def sync_message_link_clickers(client, catalog, list_id, message_id, message_link_ids):
    write_schema(catalog, 'message_link_clickers')

    for message_link_id in message_link_ids:
        def message_link_clicker_transform(message_link_clicker):
            message_link_clicker['listId'] = list_id
            message_link_clicker['messageId'] = message_id
            message_link_clicker['linkId'] = message_link_id
            return message_link_clicker

        next_token = 'Start'
        while next_token is not None:
            message_link_clickers, next_token = client.get(
                '/List/{}/Message/{}/Link/{}/Clicker'.format(
                    list_id,
                    message_id,
                    message_link_id),
                params={
                    'cursor': next_token,
                    'count': 5000
                },
                endpoint='message_link_clickers')
            if message_link_clickers:
                message_link_clickers = list(map(message_link_clicker_transform, message_link_clickers))
                persist_records(catalog, 'message_link_clickers', message_link_clickers)

def sync_conversations(client, catalog, list_id, persist):
    write_schema(catalog, 'conversations')

    conversations, _ = client.get(
        '/List/{}/Conversation'.format(list_id),
        endpoint='conversations')

    if conversations and persist:
        def transform_conversation(conversation):
            conversation['listId'] = list_id
            return conversation
        conversations = list(map(transform_conversation, conversations))
        persist_records(catalog, 'conversations', conversations)

    return list(map(lambda x: x['conversationId'], conversations))

def sync_conversation_messages(client, catalog, list_id, conversation_id, persist):
    write_schema(catalog, 'conversation_messages')

    def transform_message(message):
        message['listId'] = list_id
        message['conversationId'] = conversation_id
        return message

    next_token = 'Start'
    while next_token is not None:
        conversation_messages, next_token = client.get(
            '/List/{}/Conversation/{}/Message'.format(
                list_id,
                conversation_id),
            params={
                'cursor': next_token,
                'count': 5000
            },
            endpoint='conversation_messages')

        message_ids = list(map(lambda x: x['messageId'], conversation_messages))

        if message_ids and persist:
            messages = []
            for message_id in message_ids:
                message, _ = client.get(
                    '/List/{}/Conversation/{}/Message/{}'.format(
                        list_id,
                        conversation_id,
                        message_id),
                    endpoint='conversation_message')
                messages.append(message)

            messages = list(map(transform_message, messages))
            persist_records(catalog, 'conversation_messages', messages)

        for message_id in message_ids:
            yield message_id

def sync_conversation_message_activity(client,
                                       catalog,
                                       list_id,
                                       conversation_id,
                                       conversation_message_id):
    write_schema(catalog, 'conversation_message_activity')

    def transform_message_activity(activity):
        activity['listId'] = list_id
        activity['conversationId'] = conversation_id
        activity['conversationMessageId'] = conversation_message_id
        return activity

    next_token = 'Start'
    while next_token is not None:
        activities, next_token = client.get(
            '/List/{}/Conversation/{}/Message/{}/Activity'.format(
                list_id,
                conversation_id,
                conversation_message_id),
            params={
                'cursor': next_token,
                'count': 5000
            },
            endpoint='conversation_message_activity')

        if activities:
            activities = list(map(transform_message_activity, activities))
            persist_records(catalog, 'conversation_message_activity', activities)

def sync_transactional_messages(client, catalog, list_id):
    write_schema(catalog, 'transactional_messages')

    transactional_messages, _ = client.get(
        '/List/{}/TransactionalMessage'.format(list_id),
        endpoint='transactional_messages')

    if transactional_messages:
        def transform_transactional_message(transactional_message):
            transactional_message['listId'] = list_id
            return transactional_message

        transactional_messages = list(map(transform_transactional_message, transactional_messages))
        persist_records(catalog, 'transactional_messages', transactional_messages)

def should_sync_stream(stream_and_dependencies, selected_streams, last_stream):
    if isinstance(stream_and_dependencies, str):
        stream_and_dependencies = [stream_and_dependencies]
    if last_stream in stream_and_dependencies:
        return True
    for stream in stream_and_dependencies:
        if stream in selected_streams:
            return True
    return False

def update_last_stream(state, stream):
    state['last_stream'] = stream
    singer.write_state(state)

def sync(client, catalog, state, start_date):
    selected_streams = get_selected_streams(catalog)

    if not selected_streams:
        return

    lists = sync_lists(client, catalog, 'lists' in selected_streams)

    list_ids = sorted(map(lambda x: x['listId'], lists)) # sort for last_list_id

    last_list_id = state.get('last_list_id')
    last_stream = state.get('last_stream')

    for list_id in list_ids:
        if last_list_id:
            if list_id == last_list_id:
                last_list_id = None
            else:
                continue
        else:
            state['last_list_id'] = list_id
            update_last_stream(state, None)

        if should_sync_stream('campaigns', selected_streams, last_stream):
            sync_campaigns(client, catalog, list_id)
            last_stream = None
            update_last_stream(state, 'campaigns')

        if should_sync_stream('contacts', selected_streams, last_stream):
            sync_contacts(client, catalog, state, start_date, list_id)
            last_stream = None
            update_last_stream(state, 'contacts')

        if should_sync_stream(
            [
                'messages',
                'message_activity',
                'message_links',
                'message_link_clickers'
            ],
            selected_streams,
            last_stream):

            if last_stream is None or last_stream == 'messages':
                message_ids = sync_messages(client, catalog, list_id, 'messages' in selected_streams)

                for message_id in message_ids:
                    if 'message_activity' in selected_streams:
                        sync_message_activity(client, catalog, state, start_date, list_id, message_id)

                    if should_sync_stream(['message_links', 'message_link_clickers'],
                                          selected_streams,
                                          None):
                        message_link_ids = sync_message_links(client,
                                                              catalog,
                                                              list_id,
                                                              message_id,
                                                              'message_links' in selected_streams)

                    if should_sync_stream('message_link_clickers', selected_streams, None):
                        sync_message_link_clickers(client,
                                                   catalog,
                                                   list_id,
                                                   message_id,
                                                   message_link_ids)

                last_stream = None
                update_last_stream(state, 'messages')

        if should_sync_stream(
            [
                'conversations',
                'conversation_messages',
                'conversation_message_activity'
            ],
            selected_streams,
            last_stream):
            conversation_ids = sync_conversations(client,
                                                  catalog,
                                                  list_id,
                                                  'conversations' in selected_streams)

            if should_sync_stream(['conversation_messages', 'conversation_message_activity'], selected_streams, None): 
                for conversation_id in conversation_ids:
                    message_ids = sync_conversation_messages(client,
                                                             catalog,
                                                             list_id,
                                                             conversation_id,
                                                             'conversation_messages' in selected_streams)

                    if should_sync_stream('conversation_message_activity', selected_streams, None):
                        for conversation_message_id in message_ids:
                            sync_conversation_message_activity(client,
                                                               catalog,
                                                               list_id,
                                                               conversation_id,
                                                               conversation_message_id)
                    else:
                        list(message_ids) # force generator eval

            last_stream = None
            update_last_stream(state, 'conversations')

        if should_sync_stream('transactional_messages', selected_streams, last_stream):
            sync_transactional_messages(client, catalog, list_id)
            last_stream = None
            update_last_stream(state, 'transactional_messages')

    state['last_list_id'] = None
    update_last_stream(state, None)
