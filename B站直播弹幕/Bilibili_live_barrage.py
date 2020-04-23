#coding=utf-8
import time
import json
import requests
import pandas as pd

'''
Bilibili直播弹幕获取
'''

def getData():
    url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
    headers = {
        'Host': 'api.live.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

    from_data = {
        'roomid': 21144080,
        'csrf_token': '',
        'csrf': '',
        'visit_id': ''
    }

    response = requests.post(url, headers=headers, data=from_data)
    dic = json.loads(response.text)
    info_dic = dic['data']['room']

    result = []
    for i in info_dic:
        userid = i['uid']
        username = i['nickname']
        danmu = i['text']
        timeline = i['timeline']
        result.append([userid, username, danmu, timeline])
    return result

if __name__ == '__main__':
    result = []
    start = time.time()
    print('开始时间：%s' % start)
    while True:
        info = getData()
        for i in info:
            print('%s:%s' % (i[1], i[2]))
            # if i not in result:
            #     result.append(i)
        time.sleep(1.5)
        end = time.time()
        if (end-start) > 60:
            break
    end = time.time()
    print('耗时：%s' % (end-start))
    # df = pd.DataFrame(result, columns=['用户ID', '用户名', '弹幕信息', '发送时间'], index=None)
    # print(df)