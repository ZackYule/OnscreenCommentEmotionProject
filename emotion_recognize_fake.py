#!/usr/bin/env python
# coding: utf-8

# # 情感分析（使用baidu-api）

# ## 预处理

# In[136]:


import pandas as pd
from aip import AipNlp
import time
from utils import *


# ## 函数工具


# In[142]:


def get_sentiment_result(text, client):
    # return {'confidence': 0.1, 'negative_prob': 0.2, 'positive_prob': 0.3, 'sentiment': 0}
    result = client.sentimentClassify(text)
    if 'items' in result and len(result['items']) > 0:
        return result['items'][0]
    return None


# In[184]:


def get_sentiment_data_frame(df, content_column_name, client):
    sentiment_data = []
    for i, content in df[content_column_name].items():
        try:
            sentiment_item = get_sentiment_result(content, client)
        except Exception as err:
            print(f'🌈GET_SENTIMENT_ERROR!!--->{err=}, {type(err)=}')
            sentiment_item = {'index':pd.NA, 'confidence': pd.NA, 'negative_prob': pd.NA, 'positive_prob': pd.NA, 'sentiment': pd.NA, 'sentiment_processed': 0}
        if sentiment_item:
                sentiment_item['index'] = i     
        else:
            sentiment_item = {'index':pd.NA, 'confidence': pd.NA, 'negative_prob': pd.NA, 'positive_prob': pd.NA, 'sentiment': pd.NA, 'sentiment_processed': 1}
        sentiment_data.append(sentiment_item)
        time.sleep(0.5)
    return df.join(pd.DataFrame(data=sentiment_data).set_index('index',drop=True))


# In[211]:

# 弥补情感识别失败的弹幕
def supplement_sentiment_data_frame(df, content_column_name, client):
    sentiment_data = []
    for i, content in df[df[content_column_name+'_processed'] == 0][content_column_name].items():
        try:
            sentiment_item = get_sentiment_result(content, client)
        except Exception as err:
            print(f'🌈GET_SENTIMENT_ERROR!!--->{err=}, {type(err)=}')
            sentiment_item = {'index':pd.NA, 'confidence': pd.NA, 'negative_prob': pd.NA, 'positive_prob': pd.NA, 'sentiment': pd.NA, 'sentiment_processed': 0}
        if sentiment_item:
                sentiment_item['index'] = i     
        else:
            sentiment_item = {'index':pd.NA, 'confidence': pd.NA, 'negative_prob': pd.NA, 'positive_prob': pd.NA, 'sentiment': pd.NA, 'sentiment_processed': 1}
        sentiment_data.append(sentiment_item)
        time.sleep(0.5)
    supplementary_sentiment_data_frame = pd.DataFrame(data=sentiment_data).set_index('index',drop=True)
    df.loc[df[df['sentiment_processed'] == 0].index, ['confidence','negative_prob','positive_prob','sentiment', 'sentiment_processed']] = supplementary_sentiment_data_frame[['confidence','negative_prob','positive_prob','sentiment', 'sentiment_processed']]
    return df


if __name__ == "__main__":

    # In[137]:

    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


    for num in range(6,7):
            
        # In[138]:

        DataFilePath = f'data/subtitle{num}.pkl'

        # ## 数据读取
                    
        # In[208]:


        data = pd.read_pickle(DataFilePath)


        # ## 数据处理

        # In[168]:


        data = get_sentiment_data_frame(data, 'content', client)


        # ## 数据保存

        # In[206]:


        OutFilePath = get_new_path(DataFilePath, 'sentiment')


        # In[207]:


        data.to_pickle(OutFilePath)

