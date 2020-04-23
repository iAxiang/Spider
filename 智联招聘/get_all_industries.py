#coding=utf-8
import time
import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

'''
智联招聘 
爬取范围：所有行业 前六页的数据
爬取字段：岗位、公司、薪资、地区
时间：2020.4.20
'''

def get_data(url):
    # 设置浏览器
    option = webdriver.ChromeOptions()
    # 不加载图形界面
    # option.add_argument('--headless')
    # 不加载图片, 提升速度
    # option.add_argument('blink-settings=imagesEnabled=false')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    )
    option.add_argument('User-Agent=%s' % user_agent)
    # 加载本地cookie配置
    option.add_argument('--user-data-dir=C:\\Users\\KinYohi\\AppData\\Local\\Google\\Chrome\\User Data')

    # 启动浏览器
    browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=option)
    # 防止JS检测
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    browser.get(url)
    time.sleep(10)
    WebDriverWait(browser, 10)
    data = etree.HTML(browser.page_source)
    job, company, salary, area = [], [], [], []
    box = data.xpath('//div[@id="listContent"]')
    for i in box:
        # 岗位字段
        job = i.xpath('div/div/a/div[1]/div[1]/span/@title')
        # 公司字段
        company = i.xpath('div/div/a/div[1]/div[2]/a/text()')
        # 薪资字段
        salary = i.xpath('div/div/a/div[2]/div[1]/p/text()')
        # 地区字段
        area = i.xpath('div/div/a/div[2]/div[1]/ul/li[1]/text()')

    for i in range(0, len(job)):
        print([job[i], company[i], salary[i], area[i]])
        result.append([job[i], company[i], salary[i], area[i]])
    browser.close()

if __name__ == '__main__':
    result = []
    urls = []
    for page in range(100000000, 1600000000, 100000000):
        url = '&in={}'.format(page)
        for i in range(1, 7):
            last_url = 'https://sou.zhaopin.com/?p={}&jl=765'.format(i) + url
            urls.append(last_url)
    # urls = ['https://sou.zhaopin.com/?p={}&jl=779&kw=python&kt=3'.format(i) for i in range(1, 3)]
    for url in urls:
        print('Scraping %s' % url)
        data = get_data(url)
        if data != None:
            result.append(data)
    df = pd.DataFrame(result, columns=['岗位', '公司', '薪资', '地区'])
    print(df)
    df.to_excel('python.xls', index=False, encoding='utf-8')
    print('Success')