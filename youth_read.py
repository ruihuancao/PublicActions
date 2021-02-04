#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import traceback
import time
import sys
import os
import json
from util import send, requests_session
from datetime import datetime, timezone, timedelta


def get_standard_time():
    """
    获取utc时间和北京时间
    :return:
    """
    # <class 'datetime.datetime'>
    utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
    beijing_datetime = utc_datetime.astimezone(
        timezone(timedelta(hours=8)))  # 北京时间
    return beijing_datetime


def read(body, i):
    """
    :param body:
    :return:
    """
    try:
        url = 'https://ios.baertt.com/v5/article/complete.json'
        headers = {
            'User-Agent': 'KDApp/1.7.8 (iPhone; iOS 14.0; Scale/3.00)',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        response = requests_session().post(
            url=url, headers=headers, data=body, timeout=30).json()
        print(response)
        if response['error_code'] == '0':
            if 'read_score' in response['items']:
                print(
                    f"\n本次阅读获得{response['items']['read_score']}个青豆，请等待30s后执行下一次阅读\n")
            elif 'score' in response['items']:
                print(f"\n本次阅读获得s{response['items']['score']}个青豆，即将开始下次阅读\n")
            elif 'max_notice' in response['items']:
                print(
                    f"\n本次阅读获得m{response['items']['max_notice']}个青豆，即将开始下次阅读\n")
        elif response['success'] == False:
            print(f'\n第{i}次阅读请求有误，请删除此请求\n')
        return
    except:
        print(traceback.format_exc())
        return


def readBodys():
    bodys = []
    with open('json/youth_read.json') as f:
        bodys = json.load(f)["bodys"]
    return bodys


def main():
    print("开始阅读")
    beijing_datetime = get_standard_time()
    bodyList = list(set(readBodys()))
    print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'\n【中青看点】总共{len(bodyList)}个body')
    for i in range(0, len(bodyList)):
        print(f'\n开始中青看点第{i+1}次阅读')
        read(body=bodyList[i], i=i+1)
        time.sleep(30)
        print(f'\n【中青结束】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
    print("阅读完成")


if __name__ == '__main__':
    main()
