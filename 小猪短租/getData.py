'''
获取每个城市的url
'''
import multiprocessing
import  re
import pymysql
import requests
import pandas as pd
from lxml import etree
from requests.adapters import HTTPAdapter
from Spider.小猪短租.city_to_province import city_to_province


'''
省份 Province
城市 City
标题 Title
价格 Price
地址 Address
图片 Picture
房东 FangDong
房东链接 FangDongLink
'''

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
}
url = 'http://jci.xiaozhustatic1.com/e17061601/xzjs?k=Front_Search&httphost=bj.xiaozhu.com'     #获取城市名称的链接

#通过上面提供的url来爬取每个省份的拼音
html = requests.get(url).text

def choose_area():
    city_tup = re.compile('citys[[0-9]\d*]=new Array(.*?);').findall(html)
    #print(city_tup)
    for city_name in city_tup[29:]:
        #print(city_name)
        city_time = re.compile('[0-9]\d*:[0-9]\d*').findall(city_name)
        if len(city_time) == 0:
            city = re.compile('[\u4E00-\u9FA5]+').findall(city_name)[0]  # 城市名称
            city_jc = re.compile('[a-z]\w*').findall(city_name)[1]  # 城市拼音
            city_zf = re.compile('[0-9]\d*').findall(city_name)[0]  # 城市租房数量
            city_dic = {city: [city_jc, city_zf]}
            yield city_dic
        else:
            pass

def get_url(city_jc,page):  #提供省份的名称和页码来构建需要爬取的url
    url = 'http://{}.xiaozhu.com/search-duanzufang-p{}-0/'.format(city_jc,page)
    return url

#根据你提供的省份名称来判断，这个省份有多少房源，但是每个省份的房源只显示13页的数据，所有做个判断，超过了的话就只显示13页，没有超过的话就有几页就显示几页
def url_list():
    dic = choose_area()
    for i in dic:
        for j in i.items():
            city_name = j[0]
            city = j[1][0]
            total_page = j[1][1]
            # print(city, page)
            if int(total_page) > 13:
                for page in range(1, 14):
                    yield get_url(city, page), city_name
            elif int(total_page) <= 13:
                for page in range(1, int(total_page) + 1):
                    yield get_url(city, page), city_name

def get_html(url):      #获取网页的html内容
    s = requests.session()
    s.mount('https://', HTTPAdapter(max_retries=5))
    response = s.get(url,headers=headers)
    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        html = response.text
        return html
    else:
        print('没有获取到HTML')


# 获取详情页的url
def get_zf_url(url, city_name):
    html = get_html(url)
    links = etree.HTML(html).xpath('//*[@id="page_list"]/ul/li/a/@href')
    return links, city_name

def get_zf_message(zf_list):
    # print(zf_list)
    dic_list = []
    for url in zf_list[0]:
        print(url)
        html = get_html(url)
        area = etree.HTML(html).xpath('//div[@class="pho_info"]/p/@title')[0]
        h_image = etree.HTML(html).xpath('//*[@id="curBigImage"]/@src')[0]
        #//*[@id="floatRightBox"]/div[3]/div[3]/h6/a
        #因为用lxml获取不到房东姓名，不知道为什么，但是用正则就可以
        fd_name = re.compile('<a class="lorder_name" href=".*?" title="(.*?)" target="_blank">.*?</a>').findall(html)[0]
        #fd_name = etree.HTML(html).xpath('//a[class="lorder_name"]/text()')
        fd_link = re.compile('<a class="lorder_name" href="(.*?)" title=".*?" target="_blank">.*?</a>').findall(html)[0]
        zf_price = etree.HTML(html).xpath('//*[@id="pricePart"]/div[1]/span/text()')[0]
        zf_title = etree.HTML(html).xpath('//div[@class="pho_info"]/h4/em/text()')[0]
        data = {
            'Province': city_to_province(zf_list[1]),
            'CityName': zf_list[1],
            'Title': zf_title,
            'Price': zf_price,
            'Address': area,
            'Picture': h_image,
            'FangDong': fd_name,
            'FangDongLink': fd_link,
        }
        print(data)
        cursor = con.cursor()
        sql = 'insert into dz_info(Province, CityName, Title, Price, Address, Picture, FangDong, FangDongLink) values("%s", "%s","%s", "%s","%s", "%s","%s", "%s")'% (city_to_province(zf_list[1]), zf_list[1], zf_title, zf_price, area, h_image, fd_name, fd_link)
        cursor.execute(sql)
        # dic_list.append(data)
        # df = pd.DataFrame(dic_list)
        # df.to_csv('xzdz.csv', mode='a', index=False, header=None)


def getData(url):
    zf_list = get_zf_url(url[0], url[1])
    # print(zf_list[0])
    try:
        get_zf_message(zf_list)
        # print(zf_message)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    con = pymysql.connect('localhost', 'root', 'root', 'xzdz')
    pool = multiprocessing.Pool(processes=5)
    # 遍历所有短租房的url
    for url in url_list():
        # getData(url)
        pool.apply_async(getData, (url, ))
    pool.close()
    pool.join()
    con.close()
    print('Success')