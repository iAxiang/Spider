#coding=utf-8
import os
import time
import pandas as pd
import xlwt
import xlrd
from xlutils.copy import copy
from selenium import webdriver
from lxml import etree

'''
爬取字段：
岗位
薪资
岗位描述
公司介绍
公司地址
'''

class ZhiPinSpider():
    def __init__(self):
        # 设置浏览器
        self.option = webdriver.ChromeOptions()
        # 不加载图形界面
        self.option.add_argument('headless')
        # 不加载图片, 提升速度
        # option.add_argument('blink-settings=imagesEnabled=false')
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 添加请求头
        self.option.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"')
        # 添加启动配置文件,调用本地chrome的cookie文件,实现自动登录,前提是该网站的登录cookie已保存在本地
        # self.option.add_argument('--user-data-dir=C:\\Users\\KinYohi\\AppData\\Local\\Google\\Chrome\\User Data')


    # 创建xls
    def createXls(self, fileName):
        if os.path.exists(fileName + '.xls') == False:
            workbook = xlwt.Workbook(encoding='utf-8')
            sheet1 = workbook.add_sheet(fileName)
            sheet1.write(0, 0, '岗位')
            sheet1.write(0, 1, '薪资')
            sheet1.write(0, 2, '岗位介绍')
            sheet1.write(0, 3, '公司介绍')
            sheet1.write(0, 4, '公司地址')
            workbook.save(fileName + '.xls')
            print('%s.xls创建成功' % fileName)
        else:
            print('文件已存在!')



    # 获取详情页的url
    def getUrl(self, url):
        # 启动浏览器
        browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=self.option)
        # 防止JS检测
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        # 打开网址
        browser.get(url)
        # 解析页面
        data = etree.HTML(browser.page_source)
        links = data.xpath('//div[@class="job-title"]/span[1]/a/@href')
        return links



    # 获取数据
    def getData(self, url, fileName):
        # 启动浏览器
        browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=self.option)
        # 防止JS检测
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        # 打开网址
        browser.get(url)
        time.sleep(2)
        # print(self.browser.page_source)
        data = etree.HTML(browser.page_source)

        # result = []
        # 岗位名称
        job_name = data.xpath('//div[@class="info-primary"]/div[@class="name"]/h1/text()')[0]
        # 岗位薪资
        job_zixin = data.xpath('//div[@class="info-primary"]/div[@class="name"]/span/text()')[0]
        # print(job_name, job_zixin)

        # 职位描述
        job_sec = data.xpath('//div[@class="detail-content"]/div[1]/div[@class="text"]/text()')
        job_sec = ''.join(job_sec).strip()
        # 公司介绍
        company_info = data.xpath('//div[@class="detail-content"]/div[2]/div[@class="text"]/text()')
        company_info = ''.join(company_info).strip()
        if company_info == '':
            try:
                company_info = data.xpath('//div[@class="detail-content"]/div[3]/div[@class="text"]/text()')
                company_info = ''.join(company_info).strip()
            except:
                company_info = 'None'

        # 公司地址
        company_address = data.xpath('//div[@class="location-address"]/text()')[0]
        print(job_name)
        print(job_zixin)
        print(job_sec)
        print(company_info)
        print(company_address)
        # result.append([job_name, job_zixin, job_sec, company_info, company_address])
        # 写入excel
        try:
            values = []
            values.append([job_name, job_zixin, job_sec, company_info, company_address])
            # 打开工作簿
            workbook = xlrd.open_workbook(fileName + '.xls')
            # 获取工作簿中的所有表格
            sheets = workbook.sheet_names()
            # 获取工作簿中所有表格中的的第一个表格
            worksheet = workbook.sheet_by_name(sheets[0])
            # 获取表格中已存在的数据的行数
            rows_old = worksheet.nrows
            # 将xlrd对象拷贝转化为xlwt对象
            new_workbook = copy(workbook)
            # 获取转化后工作簿中的第一个表格
            new_worksheet = new_workbook.get_sheet(0)
            for i in range(0, len(values)):
                for j in range(0, len(values[i])):
                    # 追加写入数据，注意是从i+rows_old行开始写入
                    new_worksheet.write(i + rows_old, j, values[i][j])
            # 保存工作簿
            new_workbook.save(fileName + '.xls')
        except:
            print('此条链接数据写入失败：' + url)
        browser.close()
        print(job_name + '写入成功')
        print('=='*60)


if __name__ == '__main__':
    fileName = 'python'
    zpSpider = ZhiPinSpider()
    zpSpider.createXls(fileName)
    for page in range(1, 16):
        url = 'https://www.zhipin.com/c101281600/?query=python&page=' + str(page)
        links = zpSpider.getUrl(url)

        for link in links:
            link = 'https://www.zhipin.com' + link
            # print(link)
            print('开始爬取：' + link)
            result = zpSpider.getData(link, fileName)
            # df = pd.DataFrame(result, columns = ['职位', '资薪', '职位介绍', '公司介绍', '公司地址'])
            # df.to_csv('boss.csv', mode='a', index=False, header=None, encoding='utf_8_sig')
