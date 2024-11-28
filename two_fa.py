import pyotp  # pip install pyotp
import time
import qrcode # pip install qrcode
import re
from flask import request

def gen_key():
    return pyotp.random_base32()

def gen_url(key):
    return pyotp.totp.TOTP(key).provisioning_uri(name="bob", issuer_name = '2fa App')

def verify_code(key: str, code: str):
    totp = pyotp.TOTP(key)
    return totp.verify(code)

def get_2fa():
    key = gen_key()
    uri = gen_url(key)
    qrcode.make(uri).save("static/images/2fa_pics/newCode.png")
    return key

def check_2fa(code: str):
    while True:
        if code == request.form["code"]:
            return True
        else:
            return False
