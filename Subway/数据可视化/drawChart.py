from pyecharts import Geo, Bar, Pie, Page
import pandas as pd
import pymysql

dbconn = pymysql.connect(
    host = "localhost",
    database = "subway_db",
    user = "root",
    password = "root",
    port = 3306
)
sql = "select * from line_number"
data_one = pd.read_sql(sql, dbconn)

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 读取数据
# data_one = pd.read_excel('line_number.xlsx')
data_two = pd.read_excel('most_station.xlsx')
data_three = pd.read_excel('station_number.xlsx')
data_four = pd.read_excel('subway_store.xlsx')
data_five = pd.read_excel('city_store_number.xlsx')

def drawChart():
    page = Page()
    """
    城市地铁分布情况  绘制地图
    """
    value = [i for i in data_one['line']]
    attr = [i for i in data_one['ct']]
    geo = Geo("已开通地铁城市分布情况", title_pos='center', title_top='0', width=1600, height=650, title_color="#fff",
              background_color="#404a59")
    geo.add("", attr, value, is_visualmap=True, visual_range=[0, 25], visual_text_color="#fff", symbol_size=15, type="effectScatter")
    page.add(geo)

    """
    全国地铁站附近2公里的餐饮店铺
    """
    geo_cities_coords = {
        data_four.iloc[i]['name']: [data_four.iloc[i]['lng'], data_four.iloc[i]['lat']]
        for i in range(len(data_four))
    }
    geo_cities_coords2 = {
        data_four.iloc[i]['sitename']: [data_four.iloc[i]['longitude'], data_four.iloc[i]['latitude']]
        for i in range(len(data_four))
    }
    geo_cities_coords2.update(geo_cities_coords)
    data_four_sitename = list(data_four['sitename'])
    data_four_name = list(data_four['name'])
    geo2 = Geo('全国地铁站附近2公里的餐饮店铺', title_pos='center', title_top='0', width=1600, height=650, title_color="#fff",
               background_color="#404a59")
    geo2.add('', data_four_sitename, data_four_name, visual_range=[0, 40], visual_text_color="#fff",
             symbol_size=5, is_visualmap=True, geo_cities_coords=geo_cities_coords2)
    page.add(geo2)

    """
    生成城市地铁线路数量分布情况
    """
    data_one_city = [i for i in data_one['ct']]
    data_one_linenumber = [i for i in data_one['line']]
    bar = Bar("各城市地铁线路数量分布", title_top='20', width=1600, height=650)
    bar.add("城市", data_one_city, data_one_linenumber, is_stack=True, is_label_show=True, xaxis_rotate=45)
    page.add(bar)

    """
    全国每个已开通地铁的城市的地铁站数
    """
    data_three_city = [i for i in data_three['city']]
    data_three_station = [i for i in data_three['station']]
    bar2 = Bar('全国每个已开通地铁的城市的地铁站数', width=1600, height=650)
    bar2.add('城市', data_three_city, data_three_station, is_stack=True, is_label_show=True, legend_text_size=18, is_convert=False, xaxis_rotate=45)
    page.add(bar2)

    """
    全国每个城市的地铁站附近2公里的餐饮店铺数
    """
    data_five_city = [i for i in data_five['city']]
    data_five_storenumber = [i for i in data_five['storenumber']]
    bar3 = Bar('全国每个城市的地铁站附近2公里的餐饮店铺数', width=1600, height=650)
    bar3.add('城市', data_five_city, data_five_storenumber, is_stack=True,  is_label_show=True, legend_text_size=18, is_convert=False, xaxis_rotate=45)
    page.add(bar3)

    """
    每个城市最多地铁站的线路
    """
    data_two_cityLine = list(data_two['ct'] + data_two['line'])
    bar4 = Bar('每个城市最多地铁站的线路', width=1600, height=700)
    bar4.add('城市/线路', data_two_cityLine, [i for i in data_two['station']], is_stack=True,  is_label_show=False, legend_text_size=12, is_convert=False, xaxis_rotate=-90, is_datazoom_show=True)
    page.add(bar4)

    return  page

if __name__ == '__main__':
    drawChart().render('可视化.html')