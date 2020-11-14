import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from django.conf import settings
from mattermostdriver import Driver


def decrypt(text):
    b64_string = base64.b64decode(text)
    key = RSA.importKey(settings.VERIFYING_KEY)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(b64_string)


def get_driver(username, password):
    return Driver({
        'url': settings.MATTERMOST_API_ENDPOINT,
        'login_id': username,
        'password': password,
        'scheme': 'http',
        'port': 8065,
        'basepath': '/api/v4',
        # 'verify': True,
        # 'mfa_token': 'YourMFAToken',
        # 'auth': None,
        'timeout': 30,
        'request_timeout': None,
        'debug': False,
    })
