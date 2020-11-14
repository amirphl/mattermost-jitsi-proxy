import json
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from proxy.cache_repo import CacheRepository
from proxy.utils import decrypt


class LoginView(APIView):
    MATTER_MOST_LOGIN_ENDPOINT = settings.MATTERMOST_API_ENDPOINT + '/api/v4/users/login'

    def post(self, *args, **kwargs):
        try:
            auth_token = self.request.META['headers']['HTTP_AUTH_TOKEN']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'HTTP_AUTH_TOKEN header not found'})

        try:
            credentials = json.loads(decrypt(auth_token))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'received invalid token'})

        try:
            channel = credentials['channel']
            team = credentials['team']
            room_id = credentials['room_id']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'team, channel or room_id not provided'})

        payload = {'login_id': credentials.get('login_id', None),
                   'password': credentials.get('password', None)}
        res = requests.post(url=self.MATTER_MOST_LOGIN_ENDPOINT, data=payload)

        if res.status_code == status.HTTP_201_CREATED:
            data = {'access_token': res.headers.get('Token'),
                    'channel': channel,
                    'team': team}
            CacheRepository.store(room_id, data, 300000)  # todo fix it
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=res.status_code, data=res.json())
