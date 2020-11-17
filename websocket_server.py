import json
import os
import asyncio
import multiprocessing
import aiohttp

from aiohttp import web
from mattermostdriver import Driver

url = os.getenv('MATTERMOST_API_URL')
assert url is not None

xmpp_client_url = 'http://xmpp_client:8080/messages'


def get_driver(access_token=None):
    defaults = {
        'url': url,
        'scheme': 'http',
        'port': 8065,
        'basepath': '/api/v4',
        # 'verify': True,
        # 'mfa_token': 'YourMFAToken',
        # 'auth': None,
        'timeout': 30,
        'request_timeout': None,
        'debug': False,
        'token': access_token
    }
    return Driver(defaults)


def long_running_websocket(*args):
    data = args[0]
    d = get_driver(access_token=data['access_token'])
    d.login()
    asyncio.set_event_loop(asyncio.new_event_loop())

    async def event_handler(message):
        message = json.loads(message)

        if 'event' in message.keys() and message['event'] == 'posted':
            new_obj = json.loads(message['data']['post'])
            my_channel_id = data['channel_id']
            my_team_id = data['team_id']
            if new_obj['channel_id'] == my_channel_id and message['data']['team_id'] == my_team_id:
                async with aiohttp.ClientSession() as session:
                    print('sending post event to xmpp client ...')
                    payload = {
                        'message': new_obj['message'],
                        'user': message['data']['sender_name'],
                        'room_id': data['room_id']
                    }
                    await session.post(xmpp_client_url, json=payload)
                    print('sent ' + str(payload))

    d.init_websocket(event_handler)


routes = web.RouteTableDef()

websocket_processes = {}


# creating a websocket to mattermost and listening for events
@routes.post('/connections/')
async def add_connection(request):
    print('got a new request ...')
    text = await request.text()
    params = text.split('&')
    data = {}
    for s in params:
        key, value = s.split('=')
        data[key] = value
    room_id = data['room_id']

    # disallow creating duplicate sessions for one room (or equally a user)
    if room_id in websocket_processes.keys():
        print(room_id + ' is already logged in, destroying previous session ...')
        websocket_processes[room_id].terminate()

    print('creating new session ...')
    process = multiprocessing.Process(target=long_running_websocket, args=(data,))
    process.start()
    websocket_processes[room_id] = process
    print('new session created for ' + room_id)
    return web.json_response()


app = web.Application()
app.add_routes(routes)
web.run_app(app)
