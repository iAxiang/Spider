#coding=utf-8
import re
import random
import asyncio
import aiohttp
import pymysql
from bs4 import BeautifulSoup

'''
爬取字段：城市、酒店名称、星级、经度、纬度、开业时间
爬取范围：湖南省(14个市)
存储方式：数据库(由于数据量过大，直接存储到Excel IO操作过多),存入数据库后可以导出成Excel
'''
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
# 代理ip池
proxies = ['http://125.71.212.25:9000', 'http://202.109.157.47:9000', 'http://47.94.169.110:80','http://111.40.84.73:9999', 'http://114.245.221.21:8060', 'http://117.131.235.198:8060']
cookie = '_abtest_userid=135b1a89-b8c3-4a6b-aa20-12b7d9447134; _RSG=kbKV2_tu66ErdoTa9jfGu9; _RDG=288ec656aa36b8234b0e6c46657d90e7d2; _RGUID=e186e37f-c27d-496e-9e10-a6d2647729f5; _ga=GA1.2.1307489671.1569806955; magicid=kKNQ1cufAeVA3mWG0BOu3iAd0GXWkP6zort3XwkAONHBaLSQv4yIN4/TI76Mhhde; MKT_CKID=1578662165871.6m3n3.wz8s; __utma=1.1307489671.1569806955.1578727228.1578727228.1; __utmz=1.1578727228.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _RF1=119.141.255.230; MKT_CKID_LMT=1587460976433; _gid=GA1.2.1564865779.1587460977; MKT_Pagesource=PC; HotelCityID=206split%E9%95%BF%E6%B2%99splitChangshasplit2020-4-21split2020-04-22split5; appFloatCnt=21; Union=AllianceID=1881&SID=2209&OUID=4ABC074DA6A410F5759D786501EF3890%7C100.1030.00.000.00; Session=SmartLinkCode=U2209&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; login_uid=FC2750C64CE856B21F8B45F3C1A27E9F; login_type=0; cticket=3378DD845719416A2E2A3ED98742AF7A4BEC3DE0F9E812191885AF9CAE85D4AA; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojcF3D39+yMCrlYcU3CO/Ua0Xm+VtMwTSGfP6+OngY4tn9qo72FnnCMRAyhlAHCXMj+aqakXOGyqnI1/+lE5hcBn2gKmTKqeTBxFnyZn89o6HxwnAGEFskVT0gBDY9UrSjRRbkcT2DUhYNiuVuj2mvJkEh+WYzewG4TcBjHYv/8ZPrbJtdKSkUDrQn7wmuktsdWm9vZCVMbLrpsrvVA6EEMZpree59cRLva0UeFDiv9vmGmSPrkM6CkOviGP+iZgZq1UFqVTpF7oc=; DUID=u=FC2750C64CE856B21F8B45F3C1A27E9F&v=0; IsNonUser=u=FC2750C64CE856B21F8B45F3C1A27E9F&v=0; IsPersonalizedLogin=F; UUID=DE49A91E9811497DADFC55E376FED45B; hoteluuid=OT9hVAlOQdoHuXm5; ASP.NET_SessionId=egjz5fg1ku2jff0v1iqkjzaf; OID_ForOnlineHotel=15698069522962qgqxx1587506685368102032; _gat=1; fcerror=527903195; _zQdjfing=49d83b7fa0a05cd025310a2c2b024d2f85cb660e34310a2c49d83b; _HGUID=uAHFuCGv%3DsBGt%3DDIFu%3DIuA@%3DqFtBFDGGBIvE; HotelDomesticVisitedHotels1=43132880=0,0,4.9,1022,/200p16000000zvzl72DA4.jpg,&47985594=0,0,4.9,363,/20081800000159lh2DC96.jpg,&1230593=0,0,0,2,/200k0i000000974peAECC.jpg,&6806950=0,0,4.7,601,/2007170000013brh06FAE.jpg,&998749=0,0,4.5,11,/t1/hotel/999000/998750/2022e7af295c41d29d3165d4fec38f4a.jpg,&3385576=0,0,4.3,25,/20020t000000ix5cr467D.jpg,; MjAxNS8wNi8yOSAgSE9URUwgIERFQlVH=OceanBall; _bfi=p1%3D102003%26p2%3D102002%26v1%3D1910%26v2%3D1909; _jzqco=%7C%7C%7C%7C1587461015541%7C1.1246233261.1569806955195.1587507004515.1587507011166.1587507004515.1587507011166.undefined.0.0.232.232; __zpspc=9.11.1587505700.1587507011.19%232%7Csp0.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%25E7%25BD%2591%7C%23; hoteluuidkeys=164KQXEBgeacEGzWMYNYMXYm6EOYDYb4etFEoBjBcWHYdYGkxsfwz8vfZj7YtYUqJnzw87isOjMYzYFBrnkwlHvXFjGY6YZfvfoYB7yGAjOsvc3eqfY96rN5y0YBY4zR8LKcbYNZwAgIqgepsiOsYXYMYdYkYF8vbDe1MI4sistYAYdYBYnYmpE8hKT9wzkidoRnhjXrkQYgoJcGyUrhkYMqWFavn4x0Xe1dYDNxM6xXSYkUi95wHGjNcE35JpnWhbjOrO4JnOi9lwFgvQZRSzjN7YGUjkrD5yqciGdw8oR1HEHpjXqxdOxLOE3tEtOESNW80e7awcTE0djldegGiAQYQGr3fezXeGlxlqi4ci9Gxs0W4qj6PeBUwsmKt0wLkibnRTLjc9e8mELbyq7v0li1gEHLy4AvHzKlzENfKzgw8fiZzRMXjHrh0YGHJfhyMrFljs0eLOjdmKBZjnkwakxnoxUaxmLxF4EcmE3pE7PWmSeNOwbTEcTj3ZemSiLaYDkropEAdy3pvZbi9zEcayBtvHbKF0WFDEsMjSneHTxNfjgrUfEDnWM3et0jdfYhOjnoxzsx93xbNxLXEdFE1mEzkW03eB3wlPEoBjFNecUiO0YLlrbQedqeD6YptE17wXZWhZiXXKHDEqsEogE8LWmFeMFwboEfMjFqeadiUGYz4rzHeFdecZEm5Y5TEUGwTGWaGiDYBY95YH7iO5imbi4Uj9YTYS9y4kwp0yAdwlPiO3j9Fw1OyoYzYg7RLmJNljDAySqJFgW6Ny8OWMsRL7jbAEGDW81E7YoY1LRBpwgFvm9KSMj1UYAMWZdRBMiZ6ycNikQvaQvZZxLMRZ0J9YDY7zR8GJn0wpUvgbjNUWlGw5HvF8JTUYfDY8zvtZwMYlYqbjHawkovfl; hotelhst=171577189; _bfa=1.1569806952296.2qgqxx.1.1587469545675.1587479299716.7.1911; _bfs=1.1781'
# 设置并发量, 不宜设置过大。
CONCURRENCY = 5
# 声明信号量，控制最大并发量
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

async def getData(url):
    try:
        # 从user_agent池中随机生成headers
        random_user_agent = random.choice(user_agent)
        # 从代理ip池中随机生成proxies
        random_proxies = random.choice(proxies)
        headers = {
            'origin': 'https://hotels.ctrip.com',
            'referer': 'https://hotels.ctrip.com/hotel/',
            'user-agent': random_user_agent,
            'cookie':cookie
        }
        async with semaphore:
            async with session.get(url, headers=headers) as response:
                await asyncio.sleep(3)
                print('开始采集：' + url)
                html = await response.text()
                # 解析html
                soup = BeautifulSoup(html, 'lxml')

                # 城市字段
                city = soup.find('span', id='ctl00_MainContentPlaceHolder_commonHead_lnkCity').text
                # 酒店名称
                new = '新店'
                name = soup.find('h2', class_='cn_n').text
                if new in name:
                    name = name.replace(new, '').strip()
                # 星级
                star = '经济型'
                try:
                    starBox = soup.find('span', id='ctl00_MainContentPlaceHolder_commonHead_imgStar').get('class')[0]
                    if starBox == 'hotel_diamond05':
                        star = '五星'
                    if starBox == 'hotel_diamond04':
                        star = '四星'
                    if starBox == 'hotel_diamond03':
                        star = '三星'
                    if starBox == 'hotel_diamond02':
                        star = '二星'
                    if starBox == 'hotel_diamond01':
                        star = '经济型'
                except:
                    star = '经济型'

                # 经度
                lon = soup.find('meta', itemprop='longitude').get('content')
                # 纬度
                lat = soup.find('meta', itemprop='latitude').get('content')

                # 获取开业时间内容
                textBox = soup.find('div', id='htlDes')
                try:
                    # 使用re匹配出开始时间
                    practice = re.findall(r'([0-9]{4})年开业', str(textBox))[0]
                except:
                    practice = '无开业时间'

                try:
                    # 开始写入mysql
                    cursor = connect.cursor()
                    print(city, name, star, lon, lat, practice)
                    sql = """insert into wine_shop (city, name, star, lon, lat, practice) values('%s', '%s', '%s', '%s', '%s', '%s')""" % (city, name, star, lon, lat, practice)
                    # 执行sql语句
                    cursor.execute(sql)
                    cursor.close()
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


async def main(urls):
    global session
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    # 创建task对象执行get_url函数，返回存储task对象的列表。task对象保存了协程运行后的状态
    tasks = [asyncio.ensure_future(getData(url)) for url in urls]
    # 返回已完成task的result
    await asyncio.gather(*tasks)
    await session.close()

if __name__ == '__main__':
    # 打开湖南省所有酒店的详情链接
    with open('links.txt') as f:
        links = f.readlines()
    urls = [link.strip() for link in links]
    # 连接mysql
    connect = pymysql.connect('localhost', 'root', 'root', 'xc_wine_shop')
    asyncio.get_event_loop().run_until_complete(main(urls))
    # 关闭mysql
    connect.close()