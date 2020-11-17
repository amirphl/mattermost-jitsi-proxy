import os
import asyncio
import multiprocessing

from aiohttp import web
from mattermostdriver import Driver

url = os.getenv('MATTERMOST_API_URL')
assert url is not None


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


def handler_thread(*args):
    data = args[0]
    d = get_driver(access_token=data['access_token'])
    d.login()
    asyncio.set_event_loop(asyncio.new_event_loop())

    async def event_handler(message):
        print(message)
        print(data)

    d.init_websocket(event_handler)


routes = web.RouteTableDef()

handler_processes = {}


@routes.post('/connections/')
async def handle(request):
    text = await request.text()
    params = text.split('&')
    data = {}
    for s in params:
        key, value = s.split('=')
        data[key] = value
    room_id = data['room_id']

    if room_id in handler_processes.keys():
        handler_processes[room_id].terminate()

    process = multiprocessing.Process(target=handler_thread, args=(data,))
    handler_processes[room_id] = process
    process.start()
    return web.json_response()


app = web.Application()
app.add_routes(routes)
web.run_app(app)
