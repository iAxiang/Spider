#coding=utf-8
import jieba
import warnings
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
warnings.filterwarnings("ignore")

# 读取excel
data = pd.read_excel('Game-Comments.xls')
# 读取评论评分列并转换成list
scores = list(data['评论评分'])
# 读取评论内容列并转换层list
comments = list(data['评论内容'])
# 正面评论和负面评论
positive_comments, negative_comments = [], []

for i in range(len(scores)):
    if scores[i] >= 4:
        positive_comments.append(comments[i])
    if scores[i] < 4:
        negative_comments.append(comments[i])
print('Positive Comments:',len(positive_comments))
print('Negative Comments:',len(negative_comments))


# jieba分词
# 正面评论分词
positive_cut = [' '.join(jieba.cut(str(s), cut_all=False)) for s in positive_comments]
# 负面评论分词
negative_cut = [' '.join(jieba.cut(str(s), cut_all=False)) for s in negative_comments]

# 读取停用词表
with open('stopwords.txt', 'r') as f:
    stop_wrods = f.read().encode('utf-8').decode('utf-8')
stop_wrods = stop_wrods.split('\n')
# 去重
stop_wrods = list(set(stop_wrods))
# 过滤空值
stop_wrods = list(filter(None, stop_wrods))

# 定义对象，设置停用词
vectorizer = TfidfVectorizer(stop_words=stop_wrods)
# 学习词汇表和idf，返回文档词矩， toarray 将词矩抽出
weight = vectorizer.fit_transform(positive_cut).toarray()
# 获取所有文本的关键词
word = vectorizer.get_feature_names()
print('正面评论的TF-IDF词频矩阵：')
print(weight)

positive_result = []
for i in range(len(weight)):
    for j in range(len(word)):
        temp = [word[j], weight[i][j]]
        if temp[1] != 0.0 : positive_result.append(temp)
positive_df = pd.DataFrame(positive_result, columns=['Word', 'Weight'])
# 根据Weight列排序，False表示降序 [:100]表示取前100个
positive_df = positive_df.sort_values('Weight', ascending=False)[:100]
print(positive_df)

vectorizer2 = TfidfVectorizer(stop_words=stop_wrods)
weight2 =vectorizer2.fit_transform(negative_cut).toarray()
word2 = vectorizer2.get_feature_names()
print('负面评论的TF-IDF词频矩阵：')
print(weight2)

negative_result = []
for i in range(len(weight2)):
    for j in range(len(word2)):
        temp = [word2[j], weight2[i][j]]
        if temp[1] != 0.0 : negative_result.append(temp)
negative_df = pd.DataFrame(negative_result, columns=['Word', 'Weight'])
negative_df = negative_df.sort_values('Weight', ascending=False)[:100]
print(negative_df)

# 存储到Excel
positive_df.to_excel('positive_result.xls', encoding="utf-8")
negative_df.to_excel('negative_result.xls', encoding="utf-8")