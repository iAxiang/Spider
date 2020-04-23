#coding=utf-8
import pandas as pd

data = pd.read_excel('./Game-Data.xls')
score = list(data['评分'])
download_values = list(data['累计下载'])
# 选取不包括累计下载列中值为暂无下载量的行
data = data[~data['累计下载'].isin(['暂无下载量'])]

pop_games,upop_games=[],[]
for i in range(len(score)):
    if int(download_values[i]) > 100000:
        pop_games.append([score[i], download_values[i]])
    if int(download_values[i]) < 100000:
        upop_games.append([score[i], download_values[i]])

# 写入Excel
pop_df=pd.DataFrame(pop_games,columns=['评分','下载量'])
upop_df=pd.DataFrame(upop_games,columns=['评分','下载量'])
pop_df.to_excel('pop-game.xls')
upop_df.to_excel('upop-game.xls')