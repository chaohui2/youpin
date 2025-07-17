# -*- coding: UTF-8 -*-
import json
import base64

import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import time

PRIVATE_KEY = 'your private_key'
APP_KEY = "your appkey"
ENDPOINT="https://gw-openapi.youpin898.com"

def b64encode(bytes: bytes) -> bytes:
    return base64.b64encode(bytes)

def b64decode(private_key: str) -> bytes:
    return base64.b64decode(private_key)

def ordered_data_params(data) -> str:
    params = ""
    for key in sorted(data):
        value = json.dumps(data[key], separators=(',', ':'))
        if value:
            params += f"{key}{value}"
    return params

def encrypt(string: str) -> str:

    private_keyBytes = b64decode(PRIVATE_KEY)
    priKey = RSA.importKey(private_keyBytes)
    signer = PKCS1_v1_5.new(priKey)
    hash_obj = SHA256.new(bytearray(string, encoding='utf-8'))
    signature = b64encode(signer.sign(hash_obj))
    return signature.decode()


def post(url, params):
    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "appKey": APP_KEY
    }
    data.update(params)

    # 字典排序
    params = ordered_data_params(data)
    # 生成验签
    sign = encrypt(string=params)
    data["sign"] = sign
    response = requests.post(url=f"{ENDPOINT}{url}", data=json.dumps(data), timeout=5)
    response.raise_for_status()
    return response.json()





