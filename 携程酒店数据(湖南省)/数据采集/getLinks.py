#coding=utf-8
import time
import random
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 请求头池
user_agent = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50 ',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
]


def get_data(url):
    try:
        # 从user_agent池中随机生成headers
        random_user_agent = random.choice(user_agent)
        # 设置浏览器
        option = webdriver.ChromeOptions()
        # 不加载图形界面
        option.add_argument('--headless')
        # 不加载图片, 提升速度
        # option.add_argument('blink-settings=imagesEnabled=false')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('User-Agent=%s' % random_user_agent)
        # 加载本地cookie配置,路径为个人的谷歌浏览器的cookie存放路径
        option.add_argument('--user-data-dir=C:\\Users\\KinYohi\\AppData\\Local\\Google\\Chrome\\User Data')

        # 启动浏览器
        browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=option)
        # 防止JS检测
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        browser.get(url)
        time.sleep(5)

        count_page = 1
        while True:
            try:
                # 显示等待，最长20s
                wait = WebDriverWait(browser, 20)
                # 等待下一页出现
                wait.until(EC.presence_of_element_located((By.ID, 'downHerf')))
                # 解析HTML
                data = etree.HTML(browser.page_source)
                # 获取总页数,当当前页数处于总页数量的中间位置是a的位置应该为9,但目前设置为8不影响最终结果
                total_page = int(data.xpath('//div[@class="c_page_list layoutfix"]/a[8]/text()')[0])
                print('当前页数：%s' % count_page)
                print('总页数：%s' % total_page)
                # 执行js将屏幕滚动到底部
                browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                # 酒店名称
                title = data.xpath('//a[@class="hotel_item_pic  haspic"]/@title')
                # 酒店的详情url
                links = data.xpath('//a[@class="hotel_item_pic  haspic"]/@href')
                for i in title: print(i)
                print('--' * 60)
                # 将获取的详情页链接写入txt
                with open('links.txt', 'a+', encoding='utf-8') as f:
                    for link in links:
                        f.write('https://hotels.ctrip.com' + link + '\n')
                if count_page >= total_page: break
                count_page += 1
                # 点击下一页
                browser.find_element_by_id('downHerf').click()
                # 随机等待,模拟用户。防止被禁
                time.sleep(random.randrange(40, 60))
            except:
                new_url = url + '/p' + str(count_page)
                browser.get(new_url)
        browser.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    with open('hunan_list.txt', 'r', encoding='utf-8') as f:
        links  = f.readlines()
    urls = [link.strip() for link in links]
    for url in urls:
        get_data(url)
        time.sleep(30)
    print('爬取完成')
    url = 'https://hotels.ctrip.com/hotel/changsha206'
    get_data(url)