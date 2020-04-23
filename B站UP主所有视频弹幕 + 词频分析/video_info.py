#coding=utf-8
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

'''
倒霉侠刘背实
%E5%80%92%E9%9C%89%E4%BE%A0%E5%88%98%E8%83%8C%E5%AE%9E(urlencode)
'''

# 获取标题和视频链接
def getData(page):
    url = 'https://search.bilibili.com/all?keyword=%E5%80%92%E9%9C%89%E4%BE%A0%E5%88%98%E8%83%8C%E5%AE%9E&page={}'.format(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    a_box = soup.find_all('a', class_='title')
    result = []
    for i in a_box[1:21]:
        href = "https:" + i["href"].replace("?from=search", "")
        result.append([i['title'], href])
    print(result)
    return result


if __name__ == '__main__':
    result = []
    for page in range(1, 11):
        result.append(getData(page))
    result = sum(result, [])
    df = pd.DataFrame(result)
    df.columns = ['标题', '链接']
    df.to_excel('titleAndlink.xlsx', index=False)
    print('Sucess')