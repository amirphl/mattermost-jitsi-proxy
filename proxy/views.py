import json
import ast
import requests
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from proxy.cache_repo import CacheRepository
from proxy.utils import decrypt, get_driver, encrypt


class LoginView(APIView):

    def post(self, *args, **kwargs):
        try:
            auth_token = self.request.META.get('HTTP_AUTH_TOKEN')
            if auth_token is None:
                auth_token = self.request.META['headers']['HTTP_AUTH_TOKEN']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'HTTP_AUTH_TOKEN header not found'})

        try:
            text = decrypt(auth_token).decode('utf-8').replace('\'', '"')
            credentials = json.loads(text)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'received invalid token'})

        try:
            channel_name = credentials['channel']
            team_name = credentials['team']
            room_id = credentials['room_id']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'team, channel or room_id not provided'})

        try:
            user = credentials.get('login_id', None)
            password = credentials.get('password', None)
            driver = get_driver(user, password)
            driver.login()
            team = driver.teams.get_team_by_name(team_name)
            team_id = team['id']
            channel = driver.channels.get_channel_by_name(team_id, channel_name)
            room_data = {
                'access_token': driver.client.token,
                'user': user,
                'channel_id': channel['id'],
                'team_id': team_id
            }
            print('adding credentials to redis ...')
            CacheRepository.store(room_id, json.dumps(room_data), 30 * 60)
            room_data['room_id'] = room_id
            print('initiating a websocket event handler ...')
            requests.post(url=settings.EVENT_HANDLER_ADDRESS,
                          data=room_data,
                          headers={'Content-type': 'application/json'})
            print('done')
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MessageView(APIView):
    def post(self, *args, **kwargs):
        room_id = kwargs['room_id']
        try:
            plain_data = CacheRepository.get(room_id)
            data = json.loads(plain_data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if 'message' not in self.request.data.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'message not found'})
        message = self.request.data['message'].strip()

        if message == '':
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'message is empty'})

        try:
            driver = get_driver(access_token=data['access_token'])
            driver.login()
            driver.posts.create_post(options={
                'channel_id': data['channel_id'],
                'message': message
            })
            return Response(status=201)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class MakeEncryptionView(APIView):
    def post(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']
        room_id = self.request.data['room_id']
        channel = self.request.data['channel_id']
        team = self.request.data['team_id']
        data = {
            "login_id": username,
            "password": password,
            "room_id": room_id,
            "channel": channel,
            "team": team
        }
        token = encrypt(data)
        return Response(status=status.HTTP_200_OK, data={'token': token})
