# -*- coding: utf-8 -*-

import json
import sys
import requests
import time

# 你复制的webhook地址，需要替换成你自己的机器人的webhook地址
url = "https://open.feishu.cn/open-apis/bot/v2/hook/0e5e29d4-5db9-425f-8cc6-d3c8a06f0b6d"


def send_message(message):
    # 构建发送消息的数据格式
    payload_message = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送POST请求，向飞书机器人发送消息
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload_message))
    return response


if __name__ == '__main__':
    # 无限循环，每隔1分钟发送一次消息
    while True:
        text = 'hello'
        send_message(text)

        # 等待60秒，即1分钟
        time.sleep(60)
