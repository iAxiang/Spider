#coding=utf-8
import os
import xlwt
import xlrd
import aiohttp
import asyncio
from lxml import etree
from xlutils.copy import copy

'''
游戏名称、累计下载、总评论数、评分
'''
headers = {
        'Referer': 'https://www.taptap.com/tag/%E5%8A%A8%E4%BD%9C',
        'Cookie': 'acw_tc=3ccdc15015640423273401909e4a19ecd3abe73da9ddef32aaae41bf4de7c6; _ga=GA1.2.328004356.1564042402; _gid=GA1.2.2082280361.1564042402; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c28311843503-074af37e761bd-c343162-1327104-16c283118447ec%22%2C%22%24device_id%22%3A%2216c28311843503-074af37e761bd-c343162-1327104-16c283118447ec%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; bottom_banner_hidden=1; XSRF-TOKEN=eyJpdiI6Im5HSmhMdUN1SmM3S0dmTkdnXC9ObGxnPT0iLCJ2YWx1ZSI6ImJGQVI3clVnNDlaTzNpRHpCbFRcL0dIbDRBUzNDZVM1VnNsSEJRU2toRGFwelwvQUxIbTZrMEhTOVJiejlTRXFoUmxxYnh2dVpVUkQ1WmwrWHNxTlV0QWc9PSIsIm1hYyI6IjRhMmVkOGI5OGNhZmQ5ZjczYzFmZGYxOGE0MTcxMWFiMWUyOTQ0OGZmYTg4ZGY5NzAwOTExMGU0N2IwMjQ5YjUifQ%3D%3D; tap_sess=eyJpdiI6IjNMWVRNS0Q0VWxrQk5OY3lLSm5aeFE9PSIsInZhbHVlIjoiQ2xQUnozNSs5WHhMOUQrSVE4eXk3eGhnS1NVczdMelhMZGFHcEpmbVZcLzhSdk51TUhRZGxmaXFjbkJnanJIbitQd094ODNQaXJlY0hEbUw1RGZ1cVp3PT0iLCJtYWMiOiIwYWVlNjExMmJmNjM3YmIxZjg1ZjZiZmVmY2U3MjIwODEwY2E0MDRiNGFlM2Y3MjNmNTc2ZTIwYWE5MzdkZTUxIn0%3D; _gat=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
# 设置并发量
CONCURRENCY = 100
# 声明信号量，控制最大并发量
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

def creatXls(fileName):
    if os.path.exists(fileName + '.xls'):
        print('文件已存在')
    else:
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet(fileName)
        sheet1.write(0, 0, '游戏名称')
        sheet1.write(0, 1, '累计下载')
        sheet1.write(0, 2, '总评论数')
        sheet1.write(0, 3, '评分')
        workbook.save(fileName)
        print('%s创建成功！' % fileName)


async def getDatas(url, fileName):
#     url = url.strip()
    async with semaphore:
        async with session.get(url, headers=headers) as response:
            await asyncio.sleep(3)
            html = await response.text()
            data = etree.HTML(html)

            name = data.xpath('//div[@class="base-info-wrap"]/h1/text()')[0].strip()
            print('游戏名称：%s' % name)
            try:
                stats = data.xpath('//span[@class="count-stats"][1]/text()')[0]
                stats = stats.replace('人安装', '')
                stats = stats.replace('人关注', '')
                stats = stats.replace('人购买', '')
            except:
                stats = '暂无下载量'
            print('下载数量：%s' % stats)

            try:
                reviews = data.xpath('//ul/li[2]/a/small/text()')[0]
            except:
                reviews = '暂无评论'
            print('总评论数：%s' % reviews)

            try:
                score = data.xpath('//span[@class="app-rating-container"]/span/text()')[0]
            except:
                score = '暂无评分'
            print('评分：%s' % score)

            try:
                # 写入Excel
                values = []
                values.append([name, stats, reviews, score])
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

async def main(urls):
    global session
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    # 创建task对象执行get_url函数，返回存储task对象的列表。task对象保存了协程运行后的状态
    tasks = [asyncio.ensure_future(getDatas(url.strip(), fileName)) for url in urls]
    # 返回已完成task的result
    await asyncio.gather(*tasks)
    await session.close()


if __name__ == '__main__':
    fileName = 'Game-Data.xls'
    creatXls(fileName)
    with open('links.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
    asyncio.get_event_loop().run_until_complete(main(urls))

    print('爬取完成')