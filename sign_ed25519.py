#!/usr/bin/env python3

import base64
import time
import json
import traceback

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from websocket import create_connection

# 设置身份验证：
API_KEY='wHzEsV4gCAu1zWpuhjOtMmf3LENj6LaDHyfqRyWn9IsFSBPgU2MGgMi7JT2tAJab'
PRIVATE_KEY_PATH='id_ed25519.pem'

# 加载 private key。
# 在这个例子中，private key 没有加密
# 但我们建议使用强密码以提高安全性。
try:
    with open(PRIVATE_KEY_PATH, 'rb') as f:
      private_key = load_pem_private_key(data=f.read(), password=None)

    # 设置请求参数：
    params = {
    "symbol": "BNBFDUSD",
    "apiKey": API_KEY
    }


    # 参数中加时间戳：
    timestamp = int(time.time() * 1000) # UNIX timestamp in milliseconds
    params['timestamp'] = timestamp

    # 按参数名称的字母顺序进行排序
    params = dict(sorted(params.items()))

    # 计算签名有效负载
    payload = '&'.join([f"{k}={v}" for k,v in params.items()]) # no percent encoding here!

    # 对请求进行签名
    signature = base64.b64encode(private_key.sign(payload.encode('UTF-8')))
    params['signature'] = signature.decode('ASCII')

    # 发送请求，查询BNBFDUSD当前所有挂单
    request = {
        'id': 'my_new_order',
        'method': 'openOrders.status',
        'params': params
    }

    ws = create_connection("wss://ws-api.binance.com:443/ws-api/v3")
    ws.send(json.dumps(request))
    result =  ws.recv()
    ws.close()

    print(result)
except Exception:
    print(traceback.format_exc())