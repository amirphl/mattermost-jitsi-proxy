#!/usr/bin/python3
import os
import sys
import requests

APIS_URL = os.getenv('MATTERMOST_JITSI_PROXY_ADDRESS')
assert APIS_URL is not None


def send_message(room_id, message):
    if message[:7] == '/login ':
        res = requests.post(url=APIS_URL + '/api/v1/login/', headers={'AUTH-TOKEN': message[7:]})
        print(res.status_code)
    elif message[:9] == '/message ':
        res = requests.post(url=APIS_URL + '/api/v1/rooms/' + room_id + '/messages/',
                            data={'message': message[9:]})
        print(res.status_code)
    else:
        print('invalid command')


if __name__ == "__main__":
    send_message(*sys.argv[1:])
