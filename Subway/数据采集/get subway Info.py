import requests
from bs4 import BeautifulSoup
import json


#伪装headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

#获取路线信息，保存为subways.csv，GBK编码/subways.comments, utf-8
def get_data(ID, cityname, name):
    url = 'http://map.amap.com/service/subway?_1570608989615&srhdata=' + ID + '_drw_' + cityname + '.json'
    res = requests.get(url = url, headers = headers)
    html = res.text
    result = json.loads(html)

    for i in result['l']:
        for j in i['st']:
            if len(i['la']) > 0:
                print(name, j['si'], i['ln'] + '(' + i['la'] + ')', j['n'], j['sl'], j['su'])
                # with open('subways.csv', 'a+', encoding='gbk') as f:
                #     f.write(name + ',' + j['si'] + ',' + i['ln'] + '(' + i['la'] + ')' + ',' + j['n'] + ',' + j['sl'] + ',' + j['su'] + '\n')
                with open('subways.comments', 'a+', encoding='utf-8') as f:
                    f.write(name + ',' + j['si'] + ',' + i['ln'] + '(' + i['la'] + ')' + ',' + j['n'] + ',' + j['sl'] + ',' + j['su'] + '\n')
            else:
                print(name, j['si'], i['ln'], j['n'], j['sl'], j['su'])
                with open('subways.comments', 'a+', encoding='utf-8') as f:
                    # name + ',' + j['si'] + ',' + i['ln'] + ',' + j['n'] + ',' + j['sl'] + ',' + j['su'] + '\n'
                    f.write(name + ',' + j['si'] + ',' + i['ln'] + ',' + j['n'] + ',' + j['sl'] + ',' + j['su'] + '\n')


#获取城市信息后调用get_data()方法获取数据
def get_city():
    url = 'http://map.amap.com/subway/index.html?&1100'
    res = requests.get(url=url, headers=headers)
    html = res.text
    html = html.encode('ISO-8859-1')
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    res1 = soup.find_all(class_="city-list fl")[0]
    res2 = soup.find_all(class_="more-city-list")[0]
    for i in res1.find_all('a'):
        ID = i['id']
        cityname = i['cityname']
        name = i.get_text()
        get_data(ID, cityname, name)
    for i in res2.find_all('a'):
        ID = i['id']
        cityname = i['cityname']
        name = i.get_text()
        get_data(ID, cityname, name)

if __name__ == '__main__':
    get_city()