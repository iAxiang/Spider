from wordcloud import WordCloud, ImageColorGenerator
from pyecharts import Geo, Bar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import jieba

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 显示10行
pd.set_option('display.max_rows', 10)

# 读取数据
df = pd.read_csv('subways.csv', header=None, names=['city', 'line', 'station'], encoding='gbk')

# 各个城市地铁线路情况
df_line = df.groupby(['city', 'line']).count().reset_index()
# print(df_line)

# 哪个城市哪条线路地铁站最多
# print(df_line.sort_values(by='station', ascending=False))

# 去除重复换乘站的地铁数据
df_station = df.groupby(['city','station']).count().reset_index()
# print(df_station)

# 统计每个城市包含地铁站数(已去除重复换乘站)
# print(df_station.groupby(['city']).count().reset_index().sort_values(by='station', ascending=False))

# 各个城市地铁线路数
df_city = df_line.groupby(['city']).count().reset_index().sort_values(by='line', ascending=False)
# print(df_city)

# attr：标签名称（在例子里面就是地点）
# value：数值（在例子里就是流动人员）
# visual_range：可视化的数值范围
# symbol_size：散点的大小
# visual_text_color：标签颜色
# is_piecewise ：颜色是否分段显示（False为渐变，True为分段）
# is_visualmap：是否映射（数量与颜色深浅是否挂钩）
# maptype ：地图类型，可以是中国地图，省地图，市地图等等
# visual_split_number ：可视化数值分组
# geo_cities_coords：自定义的经纬度
def create_map(df):
    # 绘制地图
    value = [i for i in df['line']]
    attr = [i for i in df['city']]
    geo = Geo("已开通地铁城市分布情况", title_pos='center', title_top='0', width=1024, height=500, title_color="#fff",
              background_color="#404a59")
    geo.add("", attr, value, is_visualmap=True, visual_range=[0, 25], visual_text_color="#fff", symbol_size=15, type="effectScatter")
    geo.render("已开通地铁城市分布情况.html")

def create_line(df):
    """
    生成城市地铁线路数量分布情况
    """
    title_len = df['line']
    bins = [0,5,10,15,20,25]
    level = ['0-5','5-10','10-15','15-20','20以上']
    len_stage = pd.cut(title_len, bins=bins, labels=level).value_counts().sort_index()
    # 生成柱状图
    attr = len_stage.index
    v1 = len_stage.values
    bar = Bar("各城市地铁线路数量分布", title_pos='center', title_top='18', width=1024, height=968)
    bar.add("", attr, v1, is_stack=True, is_label_show=True)
    bar.render("各城市地铁线路数量分布.html")

# create_map(df_city)
# create_line(df_city)

def create_wordcloud(df):
    """
    生成地铁名词云
    """
    # 分词
    text =''
    for line in df['station']:
        text +=' '.join(jieba.cut(line, cut_all=False))
        text +=' '
        backgroud_Image = plt.imread('dt.jpeg')
        wc = WordCloud(
            background_color='white',
            mask=backgroud_Image,
            font_path='C:\Windows\Fonts\微软雅黑.TTF',
            max_words=1000,
            max_font_size=150,
            min_font_size=15,
            prefer_horizontal=1,
            random_state=50,
        )
        wc.generate_from_text(text)
        img_colors = ImageColorGenerator(backgroud_Image)
        wc.recolor(color_func=img_colors)
        # 看看词频高的有哪些
        process_word = WordCloud.process_text(wc, text)
        sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
        print(sort[:50])
        plt.imshow(wc)
        plt.axis('off')
        wc.to_file("地铁名词云.jpg")
    print('生成词云成功!')

# create_wordcloud(df_station)