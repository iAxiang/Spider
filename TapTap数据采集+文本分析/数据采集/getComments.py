# coding=utf-8
import os
import re
import xlwt
import xlrd
import requests
from xlutils.copy import copy
from bs4 import BeautifulSoup

headers = {
    'Referer': 'https://www.taptap.com/tag/%E5%8A%A8%E4%BD%9C',
    'Cookie': 'acw_tc=3ccdc15015640423273401909e4a19ecd3abe73da9ddef32aaae41bf4de7c6; _ga=GA1.2.328004356.1564042402; _gid=GA1.2.2082280361.1564042402; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c28311843503-074af37e761bd-c343162-1327104-16c283118447ec%22%2C%22%24device_id%22%3A%2216c28311843503-074af37e761bd-c343162-1327104-16c283118447ec%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; bottom_banner_hidden=1; XSRF-TOKEN=eyJpdiI6Im5HSmhMdUN1SmM3S0dmTkdnXC9ObGxnPT0iLCJ2YWx1ZSI6ImJGQVI3clVnNDlaTzNpRHpCbFRcL0dIbDRBUzNDZVM1VnNsSEJRU2toRGFwelwvQUxIbTZrMEhTOVJiejlTRXFoUmxxYnh2dVpVUkQ1WmwrWHNxTlV0QWc9PSIsIm1hYyI6IjRhMmVkOGI5OGNhZmQ5ZjczYzFmZGYxOGE0MTcxMWFiMWUyOTQ0OGZmYTg4ZGY5NzAwOTExMGU0N2IwMjQ5YjUifQ%3D%3D; tap_sess=eyJpdiI6IjNMWVRNS0Q0VWxrQk5OY3lLSm5aeFE9PSIsInZhbHVlIjoiQ2xQUnozNSs5WHhMOUQrSVE4eXk3eGhnS1NVczdMelhMZGFHcEpmbVZcLzhSdk51TUhRZGxmaXFjbkJnanJIbitQd094ODNQaXJlY0hEbUw1RGZ1cVp3PT0iLCJtYWMiOiIwYWVlNjExMmJmNjM3YmIxZjg1ZjZiZmVmY2U3MjIwODEwY2E0MDRiNGFlM2Y3MjNmNTc2ZTIwYWE5MzdkZTUxIn0%3D; _gat=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


def creatXls(fileName):
    if os.path.exists(fileName + '.xls'):
        print('文件已存在')
    else:
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet(fileName)
        sheet1.write(0, 0, '游戏名称')
        sheet1.write(0, 1, '评论时间')
        sheet1.write(0, 2, '评论评分')
        sheet1.write(0, 3, '评论内容')
        workbook.save(fileName)
        print('%s创建成功！' % fileName)


def getComments(url, fileName):
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    box = soup.find('div', class_='taptap-review-none')
    if box == None:
        # 游戏名称字段
        name = soup.find(itemprop='name').text.strip()
        print('游戏名称：%s' % name)

        # 评论时间字段
        comment_times = []
        date_times = soup.find_all(class_='text-header-time')
        for i in range(len(date_times)):
            temp = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', date_times[i].text.strip())[0]
            comment_times.append(temp)
        print('评论时间数组长度：%s' % len(comment_times))

        # 评论评分字段
        comment_score = []
        score = soup.find_all('div', class_='item-text-score')
        for i in range(len(score)):
            temp = re.findall(r'<i class="colored" style="width: ([0-9]{2})px"></i>', str(score[i]))[0]
            comment_score.append(int(temp) / 14)
        print('评论评分数组长度：%s' % len(comment_score))

        # 评论内容字段
        comments = []
        content = soup.find_all('div', class_='item-text-body')
        for i in range(len(content)):
            comment = content[i].text.strip()
            comments.append(comment)
        print('评论数组长度：%s' % len(comments))

        for i in range(20):
            try:
                # 写入Excel
                values = []
                values.append([name, comment_times[i], comment_score[i], comments[i]])
                index = len(values)
                workbook = xlrd.open_workbook(fileName)
                sheets = workbook.sheet_names()
                worksheet = workbook.sheet_by_name(sheets[0])
                rows_old = worksheet.nrows
                new_workbook = copy(workbook)
                new_worksheet = new_workbook.get_sheet(0)
                for i in range(0, index):
                    for j in range(0, len(values[i])):
                        new_worksheet.write(i + rows_old, j, values[i][j])
                new_workbook.save(fileName)
            except:
                print('写入失败!')


if __name__ == '__main__':
    fileName = 'Game-Comments.xls'
    creatXls(fileName)

    with open('links.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()

    for url in urls:
        url = url.strip()
        for page in range(1, 11):
            last_url = url + '/review?order=hot&page=' + str(page)
            print('爬取链接: %s' % last_url)
            getComments(last_url, fileName)
    print('爬取完成')