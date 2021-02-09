#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串，自动提现需要自己抓包
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可
cookies1 = {
    'YOUTH_HEADER': {
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Host": "kd.youth.cn",
        "Accept-Language": "zh-cn",
        "Content-Type": "Accept-Encoding",
        "Referer": "https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=ab46e88671178fe4555e7ccc73a96cf8&sign=4aa2cc35a3431e039abbb57984ac2091&channel_code=80000000&uid=53066217&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=e9b684fc6349523ddf5ee4bede36407a&openudid=ab46e88671178fe4555e7ccc73a96cf8&device_type=1&device_brand=iphone&sm_device_id=202012291619596aff9a650cb13c41a8a1d5079b3ea8a2010c76d9275ba375&device_id=49293647&version_code=200&os_version=14.3&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3XVrhaJ-3q_eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfsKm2qoKvl2mEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3XVrhaJ-3q_eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfsKm2qoKvl2mEY2Ft&cookie_id=e9b684fc6349523ddf5ee4bede36407a",
        "Cookie": "sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2253066217%22%2C%22%24device_id%22%3A%221778569f5db2a0-0f82e829dd7f1e8-754c1451-370944-1778569f5dceee%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221778569f5db2a0-0f82e829dd7f1e8-754c1451-370944-1778569f5dceee%22%7D; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1612851052,1612851275; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1612851053; sajssdk_2019_cross_new_user=1"
    },
    'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTckY1lFLggiEWDV0Pl36lE9-o1Y1oiXpMyIsc_2RKYiiWsEnbGBFcJZD1cOG8xFl959zxJ9-hk-yEakaE4Wih8u3mTvcBhBKwJfiqRy4Gw-O0B3DN2eyh_pM0helbWDGAD4XuxTdNdq1nVkGjYR4uA_xsdJX76XR3quuTlERRKRrcjSxijVMRGaT_F1mBOG6xEpfQVkAuE5Iexx2Xp72K4kaKC90BtESzUmOVIhazt0k4F_DJx3NMoLPW9E2jHbi5paMAT3d6swFUcAsqlwEGjtXID_1D-q58ijpBVAgO5uDVrjSQ4cY3YdoPpMQsMk79HlM2veZ7p2Ocdx1-oj1IpeeFPOxfG-3udGyUqjsCCvG4BqdSAL1zJE4-dR6vSWrYjikzSzhMwZqT0A_uth9r9eDfCu2eQXzzBkucSWWEZauj_tKxA3X8wB_vbi1RlLQcrSXUY9tGWBj6AJm9pR7cL5qHBxsCVEYvm7ZwYyQBTN1ebCoDLPbgCf1j9OUpWtjyDUVcopDsulQn5mqGtRA4e8AKfF5qwqsFaFVPLPVzPC6TkEyxHlsdjZuwpwbo6KCN97naUUkqyqiAP1vSPnLHsRJuKe6XdzwkxazRjVUV4h44TN0gqTJopVULuSuuoDs-CFuSwTmS4_biOs46eUAftm77sXxHNadeaeDlz_dvMHwQ%3D%3D',
    'YOUTH_REDBODY': "p=9NwGV8Ov71o%3DgW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o1vMtEls8mPJh514T6M7mT424qvh8QrkxvplMO-SYOVD8eel3ty7vwxe_wa7ZfSZfXdjTiw3cbhIZT-OnIao6ZrF_hSdmQipG4Rvvz3nXQ6gK5CyHYI1D1-baeHBTpn7ijSSnjFXoXswynYfcRFREAHJ6YIfERMd5gNvOt1Z-2qhW6HeOfKfDXt51mbvvtHfKY4mqICm0RFyaEkPVSFOr36byvRw4XtAO6ApmJvbjdYTWmAslf9KwrCPfoepxHo0iaVfKmZTFTDdyuT3DtLuLy_aRfXYVPNJys9CuiuFyzJmLX7BJZFTKcCKYKlRAQBwO9RX3p-byFzGgvOZq5nzU9gJSlbgu_880HtwzanJxsIGdaNdq5PB8YOdt-g_5MvaMS6VadvfSIJ8QFet6GyjXt18r2qXql5QAhKnXQm5SE8w36f4hD82cqJtbo0u5EhKRR2SY4maOLgEv0_U26WRMaDiLy-g0qXKz_x0pfndT81WgLhFEvpoSmgpt021ytVB5tOyD3U7cN22BloWYzVwQPkJeKU7LuIEw-XlxIqA0YZie7E2Q4S8g04VrtP_UUeC0lUsDIHugnuUPP6LxCEMTQyRjSER-CKEjsR9Z-xcFAs82rcr0zBYrRDcnILIT3U2HKvLYOkC8qkCiaT_QWQOeGOeVvSAJsJ2IvUDmJJm_DWdqqCIZ3SCOeevvh-TEYBBHiA2F4M8qcYumz2b1LJVsMknjymTX96u9dwo1lWYN1rp-_r_0CCG3emRFS5epj8Y7UkShzfNB48Zu3K2E6sRE7Q%3D%3D",
    'YOUTH_READTIMEBODY': "p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTckY1lFLggiEWDV0Pl36lE9-o1Y1oiXpMyIsc_2RKYiiWsEnbGBFcJZD1cOG8xFl959zxJ9-hk-yEakaE4Wih8u3mTvcBhBKwLGd7raA5l_2WAGCgVQhBk9bQlypoAFK6jzt88pRjQkQXJ1Iyf1uCR-0EBBulU0GmtfYFG8h0r9kEPW_g60U34a7pySPR813N3pFWSEhxJpzmEqBc2syBrudiPVzCySIWvrK16UpxfJIiWq2WTlAVodVlGSqJCLA61qQA3E1UErbF8WEE4lABbijLTnpUDBzSnS6oo76iMvQdv68PK65g38mVkSelu6AXrP55HRdR19P-hGG6f7mUKV-46Sq9CqYh7F9lZNwZdgm261Jqy4ZSlcYkNBYgqbciY7bAilWvyJauoMeY_WJo2yWHOyew1m6YWIeL_nApGBZUIxPZoYeQ5JjVPThz7sZFk9LfX7lwf9vNetJmutpPoqj26H53G3hCJRrD6gfxosjGl6XriGCRY8yON0q_IsgfCtSdW9kcsIGly-ks_YKhlNE9UjGoFKS96UskB8C0CsUlF__4rrmxhEZmpQ1EaPVld5myuVm1tDKdH29OzamKGMStxTeM2fNE4CXTxv_OTPHEXIUL03ASc5aBGAYuo5RSO0pL2coGVkhLFCXNvOIjfqzhLwNlSy_00%3D",
    'YOUTH_WITHDRAWBODY': ''
}
cookies2 = {
    'YOUTH_HEADER': {
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Host": "kd.youth.cn",
        "Accept-Language": "zh-cn",
        "Content-Type": "Accept-Encoding",
        "Cookie": "Hm_lpvt_6c30047a5b80400b0fd3f410638b8f0c=1612858063; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1612858063; Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775=1612858063; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1612858063; sajssdk_2019_cross_new_user=1; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2252522971%22%2C%22%24device_id%22%3A%2217785d4ef415e2-03f00efa27b5bd8-754c1451-370944-17785d4ef421139%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217785d4ef415e2-03f00efa27b5bd8-754c1451-370944-17785d4ef421139%22%7D",
        "Referer": "https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=ab46e88671178fe4555e7ccc73a96cf8&sign=0d37654ec5f3f268fd2efb9eb5da42e8&channel_code=80000000&uid=52522971&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=be63b00c0858f16554caaff49a1a9180&openudid=ab46e88671178fe4555e7ccc73a96cf8&device_type=1&device_brand=iphone&sm_device_id=202012291619596aff9a650cb13c41a8a1d5079b3ea8a2010c76d9275ba375&device_id=49293647&version_code=200&os_version=14.3&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwzYmyhKKgma64qmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfsKm2ZoOJm2qEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwzYmyhKKgma64qmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfsKm2ZoOJm2qEY2Ft&cookie_id=be63b00c0858f16554caaff49a1a9180"
    },
    'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_kF97hamPuz4ZZk3rmRrVU_m2Z51XN3szZYaCPxNG07BYjyjwYkBVGTfTGYPVecze9u-jGHCQmfvey4yZrPyKR-cA01PbV3h61GBiHFc-skGrpoDK0eliCfJPX7f9_IVT-MEKcW_xpZDYqzKjXUHiQkSn-3pNKb-EYY2QNhdT3MWjveQRbvBByg87wRk9ezItIlsZoas242dX-emdrYOrxHGfLb7_Gpsdg3Af3nlqLBNr9-E78gZSpJEWwDoS9rEuyg3rMqgNQoibB3nwueBjqBXenBdhSgUpEhIp8WQodCKv8bhNN7Nx2nKK-N3YLgZhpuI8lOEfmNfyvORT7bc3RU1TT94XB79eXuLCg5SbvPHCmbjEiPPFpMBdt2EI6lcaaKFkWi4m8bY-s7aky3HAHojLIKfGhK_zVC4zEIkJjrxwWUphtUSqedzj2e3kcqqfVEJhrzFIPHFMZAAO92z9dZ8S1EARKaNQDYw1ZI5E69KGteMLQkiHv6OlxwBULW-mVsIOK_dLahVh7P0eOc5zi1fscyRVSVNdlFC54NaBDEiAQrIGoGIf2xYnE8_Q9FvMxGQc_OXtYpexo4WcxJsYSzCd86Mqbuopftvf2Z-O7Hy7tCW-2Zfu4V8YEXg-x1dXs1a9qdTl2wKxcncq5s7ohkBqKxfWx51MlHoWnZI6tVMzXwKvjVlvLcr5LX4TFWDc5sdeh3UIfyZLLMI3MOTvwbDkKHhwUSaV0mB5T--UNV2QAGj1bzU7Zi9D5_fuJiL5ZiqiqOKnxbhuvbHdvaAptS3MWs_OZBYI-QdVNKnQ9uiAPTIy6dlopQ%3D%3D',
    'YOUTH_REDBODY': "p=9NwGV8Ov71o%3DgW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o1vMtEls8mPJh514T6M7mT424qvh8QrkxvplMO-SYOVD8eel3ty7vwxe_wa7ZfSZfXdjTiw3cbhIZT-OnIao6ZrF_hSdmQipG4Rvvz3nXQ6gK5CyHYI1D1-baeHBTpn7ijSSnjFXoXswynYfcRFREAHJ6YIfERMd5gNvOt1Z-2qhW6HeOfKfDXt51mbvvtHfKY4mqICm0RFyaEkPVSFOr36byvRw4XtAO6ApmJvbjdYTWmAslf9KwrCPfoepxHo0iaVfKmZTFTDdyuT3DtLuLy_aRfXYVPNJys9CuiuFyzJmLX7BJZFTKcCKYKlRAQBwO9RX3p-byFzGgvOZq5nzU9gJSlbgu_880HtwzanJxsIGdaNdq5PB8YOdt-g_5MvaMS6VadvfSIJ8QFet6GyjXt18r2qXql5QAhKnXQm5SE8w36f4hD82cqJtbo0u5EhKRR2SY4maOLgEv0_U26WRMaDiLy-g0qXKz_x0pfndT81WgLhFEvpoSmgpt021ytVB5tOyD3U7cN22BloWYzVwQPkJeKU7LuIEw-XlxIqA0YZie7E2Q4S8g04VrtP_UUeC0lUsDIHugnuUPP6LxCEMTQyRjSER-CKEjsR9Z-xcFAs82rcr0zBYrRDcnILIT3U2HKvLYOkC8qkCiaT_QWQOeGOeVvSAJsJ2IvUDmJJm_DWdqqCIZ3SCOeevvh-TEYBBHiA2F4M8qcYumz2b1LJVsMknjymTX96u9dwo1lWYN1rp-_r_0CCG3emRFS5epj8Y7UkShzfNB48Zu3K2E6sRE7Q%3D%3D",
    'YOUTH_READTIMEBODY': "p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_kF97hamPuz4ZZk3rmRrVU_m2Z51XN3szZYaCPxNG07BYjyjwYkBVGTfTGYPVecze9u-jGHCQmfvey4yZrPyKR-cA01PbV3h61GBiHFc-skGrpoDK0eliCfJPX7f9_IVT-MEKcW_xpZDYqzKjXUHiQkSn-3pNKb-EYY2QNhdT3MWjveQRbvBByg87wRk9ezItIlsZoas242dX-emdrYOrxHGfLb7_Gpsdg3Af3nlqLBM0UH6tbW_9NuzupICB93eMUBJUD_fJnl8koCiMCnn5CegEyfly64GnelNYutgpoFYEj5Z0QeP1YI3peAIG67RXzBrHtFQ-2sXzIt3ws2h0AfUIg-Vyw_Hih2a4vBUXUNhzRFcNkuU-hBaneqh_VHbluw5jMIxbqJDW6wJSztNqxBl16oDeLL_m4E4JYJTMetR_czVbvxnwncA5dYB2oNXYVRaY3s5BrauO7q2d4zFm-RkJV2a33EM--R6C9J-KTp_y_mpItgoujcbGSNXPk-R8hDB3ROqZxrmeeKpvhRoRWgv_O5u4SZeakNg9X9wHkVsLLd0uS8SerHclHVggUFpx9XTvRHqnB1rnEamPXDTy2Fw6Ik3wNjaO53uCw7U1gmk8UitH9sXtWV8v_rhVb54XLI2EhJS05Y3L7C8AXS4pSknuy_UK0XOYbgh_GJkzRx_VUUGWDLwYT8aEi6ic-6_sNS1c8l_YOkFu3psEIlGwBJTy3nWbKB3jzDgPpo1t1sptV9lqNqCvl9_sGnNGdqBiWlF8lEiNY0HBH0-zDyGSaeHZbikYDq5QXaaSf4YElVM%3D",
    'YOUTH_WITHDRAWBODY': ''
}

COOKIELIST = [cookies1, cookies2]  # 多账号准备

# # ac读取环境变量
# if "YOUTH_HEADER1" in os.environ:
#     COOKIELIST = []
#     for i in range(5):
#         headerVar = f'YOUTH_HEADER{str(i+1)}'
#         readBodyVar = f'YOUTH_READBODY{str(i+1)}'
#         redBodyVar = f'YOUTH_REDBODY{str(i+1)}'
#         readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
#         withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
#         if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and redBodyVar in os.environ and os.environ[redBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
#             globals()['cookies'+str(i + 1)
#                       ]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
#             globals()['cookies'+str(i + 1)
#                       ]["YOUTH_READBODY"] = os.environ[readBodyVar]
#             globals()['cookies'+str(i + 1)
#                       ]["YOUTH_REDBODY"] = os.environ[redBodyVar]
#             globals()['cookies' + str(i + 1)
#                       ]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
#             globals()['cookies' + str(i + 1)
#                       ]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
#             COOKIELIST.append(globals()['cookies'+str(i + 1)])
#     print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"


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


def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))


def sign(headers):
    """
    签到
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://kd.youth.cn/TaskCenter/sign'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('签到')
        print(response)
        if response['status'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def signInfo(headers):
    """
    签到详情
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://kd.youth.cn/TaskCenter/getSign'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('签到详情')
        print(response)
        if response['status'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def punchCard(headers):
    """
    打卡报名
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}PunchCard/signUp'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('打卡报名')
        print(response)
        if response['code'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def doCard(headers):
    """
    早起打卡
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}PunchCard/doCard'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('早起打卡')
        print(response)
        if response['code'] == 1:
            shareCard(headers=headers)
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def shareCard(headers):
    """
    打卡分享
    :param headers:
    :return:
    """
    time.sleep(0.3)
    startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
    endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
    try:
        response = requests_session().post(
            url=startUrl, headers=headers, timeout=30).json()
        print('打卡分享')
        print(response)
        if response['code'] == 1:
            time.sleep(0.3)
            responseEnd = requests_session().post(
                url=endUrl, headers=headers, timeout=30).json()
            if responseEnd['code'] == 1:
                return responseEnd
        else:
            return
    except:
        print(traceback.format_exc())
        return


def luckDraw(headers):
    """
    打卡分享
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}PunchCard/luckdraw'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('七日签到')
        print(response)
        if response['code'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def timePacket(headers):
    """
    计时红包
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}TimePacket/getReward'
    try:
        response = requests_session().post(url=url,
                                           data=f'{headers["Referer"].split("?")[1]}', headers=headers, timeout=30).json()
        print('计时红包')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def watchWelfareVideo(headers):
    """
    观看福利视频
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
    try:
        response = requests_session().get(url=url, headers=headers, timeout=30).json()
        print('观看福利视频')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def shareArticle(headers):
    """
    分享文章
    :param headers:
    :return:
    """
    url = 'https://ios.baertt.com/v2/article/share/put.json'
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    body = 'access=WIFI&app_version=1.8.2&article_id=36240926&channel=80000000&channel_code=80000000&cid=80000000&client_version=1.8.2&device_brand=iphone&device_id=49068313&device_model=iPhone&device_platform=iphone&device_type=iphone&from=7&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=c18a9d1f15212eebb9b8dc4c2adcc563&os_version=14.3&phone_code=c18a9d1f15212eebb9b8dc4c2adcc563&phone_network=WIFI&platform=3&request_time=1612771954&resolution=750x1334&sign=67399e61370b3fa383a34ae8025d21cb&sm_device_id=202012191748479a7e5e957ab8f5f116ea95b19fd9120d012db4c3f2b435be&stype=WEIXIN&szlm_ddid=D2U6jGsDnrrijvOmzrEwZMyw/D7WvldETrECXmh7wlq7AXd0&time=1612771954&uid=52289573&uuid=c18a9d1f15212eebb9b8dc4c2adcc563'
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('分享文章')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def threeShare(headers, action):
    """
    三餐分享
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}ShareNew/execExtractTask'
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    body = f'{headers["Referer"].split("?")[1]}&action={action}'
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('三餐分享')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def openBox(headers):
    """
    开启宝箱
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}invite/openHourRed'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('开启宝箱')
        print(response)
        if response['code'] == 1:
            share_box_res = shareBox(headers=headers)
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def shareBox(headers):
    """
    宝箱分享
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}invite/shareEnd'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('宝箱分享')
        print(response)
        if response['code'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def friendList(headers):
    """
    好友列表
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
    try:
        response = requests_session().get(url=url, headers=headers, timeout=30).json()
        print('好友列表')
        print(response)
        if response['error_code'] == '0':
            if len(response['data']['active_list']) > 0:
                for friend in response['data']['active_list']:
                    if friend['button'] == 1:
                        time.sleep(1)
                        friendSign(headers=headers, uid=friend['uid'])
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def friendSign(headers, uid):
    """
    好友签到
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
    try:
        response = requests_session().get(url=url, headers=headers, timeout=30).json()
        print('好友签到')
        print(response)
        if response['error_code'] == '0':
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def sendTwentyScore(headers, action):
    """
    每日任务
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
    try:
        response = requests_session().get(url=url, headers=headers, timeout=30).json()
        print(f'每日任务 {action}')
        print(response)
        if response['status'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def watchAdVideo(headers):
    """
    看广告视频
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    try:
        response = requests_session().post(url=url, data="type=taskCenter",
                                           headers=headers, timeout=30).json()
        print('看广告视频')
        print(response)
        if response['status'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def watchGameVideo(body):
    """
    激励视频
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    try:
        response = requests_session().post(
            url=url, headers=headers, data=body, timeout=30).json()
        print('激励视频')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def visitReward(body):
    """
    回访奖励
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/mission/msgRed.json'
    headers = {
        'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('回访奖励')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def articleRed(body):
    """
    惊喜红包
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/article/red_packet.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('惊喜红包')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def readTime(body):
    """
    阅读时长
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/user/stay.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('阅读时长')
        print(response)
        if response['error_code'] == '0':
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def rotary(headers, body):
    """
    转盘任务
    :param headers:
    :return:
    """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('转盘任务')
        print(response)
        return response
    except:
        print(traceback.format_exc())
        return


def rotaryChestReward(headers, body):
    """
    转盘宝箱
    :param headers:
    :return:
    """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('转盘宝箱')
        print(response)
        if response['status'] == 1:
            i = 0
            while (i <= 3):
                chest = response['data']['chestOpen'][i]
                if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
                    time.sleep(1)
                    runRotary(headers=headers, body=f'{body}&num={i+1}')
                i += 1
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def runRotary(headers, body):
    """
    转盘宝箱
    :param headers:
    :return:
    """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('领取宝箱')
        print(response)
        if response['status'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def doubleRotary(headers, body):
    """
    转盘双倍
    :param headers:
    :return:
    """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
    try:
        response = requests_session().post(
            url=url, data=body, headers=headers, timeout=30).json()
        print('转盘双倍')
        print(response)
        if response['status'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def incomeStat(headers):
    """
    收益统计
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
    try:
        response = requests_session().get(url=url, headers=headers, timeout=50).json()
        print('收益统计')
        print(response)
        if response['status'] == 0:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def withdraw(body):
    """
    自动提现
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
    headers = {
        'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(
            url=url, headers=headers, data=body, timeout=30).json()
        print('自动提现')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def bereadRed(headers):
    """
    时段红包
    :param headers:
    :return:
    """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}Task/receiveBereadRed'
    try:
        response = requests_session().post(url=url, headers=headers, timeout=30).json()
        print('时段红包')
        print(response)
        if response['code'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def run():
    title = f'📚中青看点'
    content = ''
    result = ''
    beijing_datetime = get_standard_time()
    print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
    hour = beijing_datetime.hour
    for i, account in enumerate(COOKIELIST):
        headers = account['YOUTH_HEADER']
        readBody = account['YOUTH_READBODY']
        redBody = account['YOUTH_REDBODY']
        readTimeBody = account['YOUTH_READTIMEBODY']
        withdrawBody = account['YOUTH_WITHDRAWBODY']
        rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'
        sign_res = sign(headers=headers)
        if sign_res and sign_res['status'] == 1:
            content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
        elif sign_res and sign_res['status'] == 2:
            send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
            continue

        sign_info = signInfo(headers=headers)
        if sign_info:
            content += f'\n【账号】：{sign_info["user"]["nickname"]}'
            content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
            result += f'【账号】: {sign_info["user"]["nickname"]}'
        friendList(headers=headers)
        if hour > 12:
            punch_card_res = punchCard(headers=headers)
            if punch_card_res:
                content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
        if hour >= 5 and hour <= 8:
            do_card_res = doCard(headers=headers)
            if do_card_res:
                content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
        luck_draw_res = luckDraw(headers=headers)
        if luck_draw_res:
            content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
        visit_reward_res = visitReward(body=readBody)
        if visit_reward_res:
            content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
        shareArticle(headers=headers)
        for action in ['beread_extra_reward_one', 'beread_extra_reward_two', 'beread_extra_reward_three']:
            time.sleep(5)
            threeShare(headers=headers, action=action)
        open_box_res = openBox(headers=headers)
        if open_box_res:
            content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
        watch_ad_video_res = watchAdVideo(headers=headers)
        if watch_ad_video_res:
            content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
        watch_game_video_res = watchGameVideo(body=readBody)
        if watch_game_video_res:
            content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
        # article_red_res = articleRed(body=redBody)
        # if article_red_res:
        #   content += f'\n【惊喜红包】：+{article_red_res["score"]}个青豆'
        read_time_res = readTime(body=readTimeBody)
        if read_time_res:
            content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
        if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
            beread_red_res = bereadRed(headers=headers)
            if beread_red_res:
                content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
        for i in range(0, 5):
            time.sleep(5)
            rotary_res = rotary(headers=headers, body=rotaryBody)
            if rotary_res:
                if rotary_res['status'] == 0:
                    break
                elif rotary_res['status'] == 1:
                    content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
                    if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
                        double_rotary_res = doubleRotary(
                            headers=headers, body=rotaryBody)
                        if double_rotary_res:
                            content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

        rotaryChestReward(headers=headers, body=rotaryBody)
        for i in range(5):
            watchWelfareVideo(headers=headers)
        timePacket(headers=headers)
        for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward', 'first_share_article']:
            time.sleep(5)
            sendTwentyScore(headers=headers, action=action)
        stat_res = incomeStat(headers=headers)
        if stat_res['status'] == 0:
            for group in stat_res['history'][0]['group']:
                content += f'\n【{group["name"]}】：+{group["money"]}青豆'
            today_score = int(stat_res["user"]["today_score"])
            score = int(stat_res["user"]["score"])
            total_score = int(stat_res["user"]["total_score"])

            if score >= 300000 and withdrawBody:
                with_draw_res = withdraw(body=withdrawBody)
                if with_draw_res:
                    result += f'\n【自动提现】：发起提现30元成功'
                    content += f'\n【自动提现】：发起提现30元成功'
                    send(title=title,
                         content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

            result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
            content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
            result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
            content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
            result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
            content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

    print(content)

    # 每天 23:00 发送消息推送
    if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
        send(title=title, content=result)
    elif not beijing_datetime.hour == 23:
        print('未进行消息推送，原因：没到对应的推送时间点\n')
    else:
        print('未在规定的时间范围内\n')


if __name__ == '__main__':
    run()
