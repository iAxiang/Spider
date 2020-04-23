#coding=utf-8
from collections import Counter

# 打开文件
with open('barrages.comments', 'r', encoding='utf-8') as f:
    barrages = f.read().split('\n')

# 统计词频
barrages_count = Counter(barrages)

# 找出出现频率最高的100个元素
result = barrages_count.most_common(100)

# 保存结果
with open('barrages_100.comments', 'a+', encoding='utf-8') as f:
    for i in result:
        temp = ':'.join([i[0], str(i[1])])
        f.write(temp + '\n')