#coding=utf-8
import re
import time
import requests

def getLinks(page):
    # 获取链接，伪装headers
    # https://www.taptap.com/ajax/search/tags?&kw=%E5%8A%A8%E4%BD%9C&sort=hits&page=2
    url = 'https://www.taptap.com/ajax/search/tags?&kw=%E5%8A%A8%E4%BD%9C&sort=hits&page=' + str(page)
    headers = {
        'Referer': 'https://www.taptap.com/tag/%E5%8A%A8%E4%BD%9C',
        'Cookie': 'acw_tc=3ccdc15015640423273401909e4a19ecd3abe73da9ddef32aaae41bf4de7c6; _ga=GA1.2.328004356.1564042402; _gid=GA1.2.2082280361.1564042402; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c28311843503-074af37e761bd-c343162-1327104-16c283118447ec%22%2C%22%24device_id%22%3A%2216c28311843503-074af37e761bd-c343162-1327104-16c283118447ec%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; bottom_banner_hidden=1; XSRF-TOKEN=eyJpdiI6Im5HSmhMdUN1SmM3S0dmTkdnXC9ObGxnPT0iLCJ2YWx1ZSI6ImJGQVI3clVnNDlaTzNpRHpCbFRcL0dIbDRBUzNDZVM1VnNsSEJRU2toRGFwelwvQUxIbTZrMEhTOVJiejlTRXFoUmxxYnh2dVpVUkQ1WmwrWHNxTlV0QWc9PSIsIm1hYyI6IjRhMmVkOGI5OGNhZmQ5ZjczYzFmZGYxOGE0MTcxMWFiMWUyOTQ0OGZmYTg4ZGY5NzAwOTExMGU0N2IwMjQ5YjUifQ%3D%3D; tap_sess=eyJpdiI6IjNMWVRNS0Q0VWxrQk5OY3lLSm5aeFE9PSIsInZhbHVlIjoiQ2xQUnozNSs5WHhMOUQrSVE4eXk3eGhnS1NVczdMelhMZGFHcEpmbVZcLzhSdk51TUhRZGxmaXFjbkJnanJIbitQd094ODNQaXJlY0hEbUw1RGZ1cVp3PT0iLCJtYWMiOiIwYWVlNjExMmJmNjM3YmIxZjg1ZjZiZmVmY2U3MjIwODEwY2E0MDRiNGFlM2Y3MjNmNTc2ZTIwYWE5MzdkZTUxIn0%3D; _gat=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    # 发送请求，获取源码
    response = requests.get(url, headers=headers)
    html = response.text

    # 过滤多余的反斜杠，正则找出link
    html = re.sub(r'\\', '', html)
    links = re.findall('href="(https://www.taptap.com/app/[0-9]+)"', html)

    #去重
    links=list(set(links))

    # 保存结果
    for link in links:
        with open('links.txt', 'a+', encoding='utf-8') as file:
            file.write(link + '\n')
    print('写入第%s组成功' % page)

if __name__ == '__main__':
    #一页有10条，最多1000页，这里选择了30页
    pages=[i for i in range(1,31)]
    for page in pages:
        getLinks(page)
        time.sleep(1)