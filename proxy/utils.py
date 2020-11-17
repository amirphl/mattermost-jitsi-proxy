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


def get_driver(username=None, password=None, access_token=None):
    defaults = {
        'url': settings.MATTERMOST_API_URL,
        'scheme': 'http',
        'port': 8065,
        'basepath': '/api/v4',
        # 'verify': True,
        # 'mfa_token': 'YourMFAToken',
        # 'auth': None,
        'timeout': 30,
        'request_timeout': None,
        'debug': False,
    }
    if access_token is None:
        defaults.update({
            'login_id': username,
            'password': password
        })
    else:
        defaults.update({
            'token': access_token,
        })
    return Driver(defaults)
