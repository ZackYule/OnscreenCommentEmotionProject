#!/usr/bin/env python
# coding: utf-8

# # 处理尝试

# ## 预处理

import pandas as pd
from utils import content_clean
# ## 数据处理

# In[54]:

def time_serialization(df_has_progress_column):
    df_has_progress_column = df_has_progress_column[df_has_progress_column['progress'].notna()]
    df_has_progress_column.sort_values(by='progress',inplace=True)
    df_has_progress_column = df_has_progress_column.reset_index(drop=True)
    df_has_progress_column['progress'] = df_has_progress_column['progress'].astype('Int64')
    return df_has_progress_column


# ## 数据展示

# In[57]:

if __name__ == "__main__":
    for num in range(1, 7):
        DataFilePath = f'data/美丽中国 - {num}.json'
        OutFilePath = f'data/episode{num}.pkl'
        data = pd.read_json(DataFilePath)
        data['content'] = data['content'].apply(content_clean)
        data = time_serialization(data)
        data.to_pickle(OutFilePath)



    

