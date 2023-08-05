
import PureCloudPlatformApiSdk

# For fetching historical adherence
import asyncio
import websockets
import threading
import json
import time

import singer
logger = singer.get_logger()

MAX_TRIES = 5
WEBHOOK_WAIT = 5
ADHERENCE_CHANNEL = 'v2.users.{}.workforcemanagement.historicaladherencequery'

async def get_websocket_msg(uri):
    async with websockets.connect(uri) as websocket:
        for i in range(MAX_TRIES):
            logger.info("Blocking to receive data on websocket for {}".format(uri))
            resp = await websocket.recv()
            data = json.loads(resp)
            body = data.get('eventBody', {})

            logger.info("Received websocket data with keys: {}".format(body.keys()))
            if body.get('id'):
                return body
            else:
                logger.info("Non-result response: {}".format(resp))

        raise RuntimeError("Did not find expected message")

def get_historical_adherence(config, result_reference, unit_id):
    api = PureCloudPlatformApiSdk.NotificationsApi()
    try:
        api_response = api.post_channels()
    except PureCloudPlatformClientV2.rest.ApiException as e:
        time.sleep(10)
        api_response = api.post_channels()

    client_id = config.get('client_id')
    channel_id = ADHERENCE_CHANNEL.format(client_id)

    topic = PureCloudPlatformApiSdk.ChannelTopic()
    topic.id = channel_id

    try:
        notification_resp = api.post_channels_channel_id_subscriptions(api_response.id, [topic])
    except PureCloudPlatformClientV2.rest.ApiException as e:
        time.sleep(10)
        notification_resp = api.post_channels_channel_id_subscriptions(api_response.id, [topic])

    logger.info("Listening on topic {}".format(channel_id))

    def loop_in_thread(loop, websocket_uri, res):
        asyncio.set_event_loop(loop)
        func = get_websocket_msg(websocket_uri)
        val = loop.run_until_complete(func)
        result_reference.update(val)

    websocket_uri = api_response.connect_uri
    loop = asyncio.get_event_loop()

    thread = threading.Thread(target=loop_in_thread, args=(loop, websocket_uri, result_reference))
    thread.start()
    return thread
