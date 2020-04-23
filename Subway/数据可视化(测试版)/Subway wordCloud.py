from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
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

# 去除重复换乘站的地铁数据
df_station = df.groupby(['city','station']).count().reset_index()
# print(df_station)


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
            font_path='simhei.ttf',
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

create_wordcloud(df_station)