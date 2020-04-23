from pyecharts import Bar
import pandas as pd
import numpy as np

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 显示10行
pd.set_option('display.max_rows', 10)

# 读取数据
df = pd.read_csv('subways.csv', header=None, names=['city', 'line', 'station'], encoding='gbk')

words = []
for line in df['station']:
    for i in line:
        # 将字符串输出一个个中文
        words.append(i)

def all_np(arr):
    """
    统计单字频率
    """
    arr = np.array(arr)
    key = np.unique(arr)
    result = {}
    for k in key:
        mask = (arr == k)
        arr_new = arr[mask]
        v = arr_new.size
        result[k] = v
    return result

def create_word(word_message):
    """
    生成柱状图
    """
    attr = [j[0] for j in word_message]
    v1 = [j[1] for j in word_message]
    bar = Bar("中国地铁站最爱用的字", title_pos='center', title_top='18', width=800, height=400)
    bar.add("", attr, v1, is_stack=True, is_label_show=True)
    bar.render("中国地铁站最爱用的字.html")

word = all_np(words)
word_message = sorted(word.items(), key=lambda x: x[1], reverse=True)[:10]
create_word(word_message)