import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from django.conf import settings


def decrypt(text):
    b64_string = base64.b64decode(text)
    key = RSA.importKey(settings.VERIFYING_KEY)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(b64_string)
