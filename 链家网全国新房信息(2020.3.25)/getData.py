#coding=utf-8
import math
import multiprocessing
import random
import re
import socket
import time
import requests
import pymysql
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
from requests.adapters import HTTPAdapter

'''
保定 北海 保亭 北京
长春 滁州 长沙 澄迈 重庆 成都
大连 东莞 儋州 东方 德阳 大理
佛山 防城港
广州 桂林 贵阳
呼和浩特 杭州 湖州 合肥 惠州 海口
晋中 嘉兴 济南
昆明
廊坊 临高 乐东 陵水 乐山
眉山
南京 南通 宁波 南昌 南宁
秦皇岛 泉州 青岛 清远 琼海
石家庄 沈阳 上海 苏州 绍兴 三门峡 深圳 三亚
天津 太原
无锡 威海 武汉 五指山 文昌 万宁
徐州 厦门 西双版纳 西安 咸阳
烟台
张家口 镇江 漳州 郑州 珠海 中山
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

citys = [
    'bd', 'bh', 'bt', 'bj',
    'cc', 'cz', 'cs', 'cm', 'cq', 'cd',
    'dl', 'dg', 'dz', 'dongfang', 'dy', 'dl',
    'fs', 'fcg',
    'gz', 'gl', 'gy',
    'hhht', 'hz', 'huzhou', 'hf', 'hui', 'hk',
    'jz', 'jx', 'jn',
    'km',
    'lf', 'lg', 'ld', 'ls', 'leshan',
    'ms',
    'nj', 'nt', 'nb', 'nc', 'nn',
    'qhd', 'qz', 'qd', 'qy', 'qh',
    'sjz', 'sy', 'sh', 'sz', 'sx', 'smx', 'sz', 'san',
    'tj', 'ty',
    'wx', 'wh', 'wh', 'wzs', 'wc', 'wn',
    'xz', 'xm', 'xsbn', 'xa', 'xianyang',
    'yt',
    'zjk', 'zj', 'zhangzhou', 'zz', 'zs'
]
urls = ['https://{}.fang.lianjia.com/loupan/pg'.format(str(i)) for i in citys]


'''
城市 City
房名 fName
类型 fType
是否在售 isSell
价格 price
'''
def getData(url, page):
    cityName, fName, fType, isSell, price = [], [], [], [], []
    for i in range(1, page + 1):
        time.sleep(round(random.uniform(1, 3), 1))
        last_url = url + str(i)
        response = s.get(last_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')

        for i in soup.find('a', class_="s-city"):
            cityName.append(i)
        for i in soup.find_all('div', class_='resblock-name'):
            fName.append(re.findall(r'<a .*?>(.*?)</a>', str(i))[0])
            fType.append(re.findall(r'<span class="resblock-type" style=".*?">(.*?)</span>', str(i))[0])
            isSell.append(re.findall(r'<span class="sale-status" style=".*?">(.*?)</span>', str(i))[0])
        for i in soup.find_all('div', class_="main-price"):
            try:
                price.append(str(re.findall(r'<span class="number">(.*?)</span>', str(i))[0]) + str(
                    re.findall(r'<span class="desc">(.*?)</span>', str(i))[0]))
            except:
                price.append(str(re.findall(r'<span class="number">(.*?)</span>', str(i))[0]))
        print('--------------------------------------------开始爬取--------------------------------------------')
        print('省份：' + cityName[0])
        print('Url：'+ last_url)
        print('--------------------------------------------爬取完成--------------------------------------------')

    cursor = connect.cursor()
    for i in range(len(fName)):
        sql = """insert into lianjia_info (City, Name, Type, isSell, Price) values('%s', '%s', '%s', '%s', '%s')""" % (cityName[0], fName[i], fType[i], isSell[i], price[i])
        # print(sql)
        cursor.execute(sql)
    cursor.close()


if __name__ == '__main__':
    s = requests.session()
    # 设置超时重试
    s.mount('https://', HTTPAdapter(max_retries=3))
    connect = pymysql.connect('localhost', 'root', 'root', 'lianjia')
    try:
        start = time.time()
        for url in urls:
            socket.setdefaulttimeout(5)
            response = s.get(url, headers=headers, timeout=10)
            data = etree.HTML(response.text)

            total_page = data.xpath('//div[@class="page-box"]/@data-total-count')[0]
            page = math.ceil(int(total_page) / 10)

            getData(url, page)
        end = time.time()
        print('耗时：%s' % (end-start))
    except Exception as e:
        print(e)
    connect.close()
    print('--------------------------------------------Success--------------------------------------------')