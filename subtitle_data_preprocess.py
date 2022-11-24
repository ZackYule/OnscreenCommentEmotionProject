#!/usr/bin/env python
# coding: utf-8

# # 处理尝试

# ## 预处理

import pandas as pd
import pysubs2
from utils import content_clean
# ## 数据处理

# In[54]:

def time_serialization(df, time_column_name):
    df = df[df[time_column_name].notna()]
    df.sort_values(by=time_column_name,inplace=True)
    df = df.reset_index(drop=True)
    df[time_column_name] = df[time_column_name].astype('Int64')
    return df


# ## 数据展示

# In[57]:

if __name__ == "__main__":
    for num in range(1, 7):
        DataFilePath = f'data/subtitles/美丽中国.Wild.China.EP{num}.chs.srt'
        OutFilePath = f'data/subtitle{num}.pkl'
        subs = pysubs2.load(DataFilePath)
        texts = [sub.plaintext for sub in subs]
        time_start = [sub.start for sub in subs]
        time_end = [sub.end for sub in subs]
        data = pd.DataFrame({'content':texts,'progress':time_start,'progress_end':time_end})
        data['content'] = data['content'].apply(content_clean)
        data = time_serialization(data, 'progress')
        data.to_pickle(OutFilePath)



    

