#coding=utf-8
import re
import json
import time

import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
s = requests.session()
# 设置超时重试次数
s.mount('https://', HTTPAdapter(max_retries=3))


# 获取cid
def get_cid(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(bvid)
    html = s.get(url, headers=headers).text
    jhtml = json.loads(html)

    data = jhtml['data']
    cid = data[0]['cid']
    return cid

# 获取弹幕
def get_barrages(cid):
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
    response = s.get(url, headers=headers)
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'lxml')
    d = soup.find_all('d')
    barrages = [i.text for i in d]
    print(barrages)

    return barrages


if __name__ == '__main__':
    video_info = pd.read_excel('titleAndlink.xlsx')
    links = video_info['链接'].tolist()
    # 提取bvid
    bvid = [re.findall(r'https://www.bilibili.com/video/(.*)', str(i))[0] for i in links]

    # 获取所有的cid
    cids = []
    for bv in bvid:
        cids.append(get_cid(bv))

    # 保存结果
    result = []
    for cid in cids:
        result.append(get_barrages(cid))
        time.sleep(1)
    result = sum(result, [])
    print(result)
    with open('barrages.comments', 'a+', encoding='utf-8') as f:
        for i in result:
            print(i)
            f.write(str(i) + '\n')

    print('Sucess')