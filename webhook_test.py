# -*- coding: utf-8 -*-

import json
import sys
import datetime
import requests
import time

# 你复制的webhook地址，需要替换成你自己的机器人的webhook地址
url = "https://open.feishu.cn/open-apis/bot/v2/hook/0e5e29d4-5db9-425f-8cc6-d3c8a06f0b6d"


def next_weekend():
    today = datetime.date.today()
    # 0表示周一，1表示周二，依此类推，5表示周六，6表示周日
    weekday = 4
    # 如果今天是周一至周四，下个周末就是周六，也就是5
    if weekday < 4:
        days_ahead = 5 - weekday
    # 如果今天是周五，下个周末就是明天
    elif weekday == 4:
        days_ahead = 1
    # 如果今天是周末，下个周末就是下周的周六
    else: 
        days_ahead = 5 - weekday + 7
    next_weekend = today + datetime.timedelta(days=days_ahead)
    print("today:",today)
    print("weekday:",weekday)
    print("days_ahead:",days_ahead)
    print("next_weekend:",next_weekend)
    print("over:",datetime.datetime.combine(next_weekend, datetime.time()))

    # return datetime.datetime.combine(next_weekend, datetime.time())

def countdown_timer(end_time):
    diff = end_time - datetime.datetime.now()
    if diff.days < 0:
        print("Countdown结束") 
    else:
        days, seconds = diff.days, diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        
        return "距离周末还有: {}天 {}小时 {}分钟 {}秒".format(days, hours, minutes, seconds)
       



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
    # next_weekend()
    text = countdown_timer(next_weekend())
    send_message(text)
    print(text)
