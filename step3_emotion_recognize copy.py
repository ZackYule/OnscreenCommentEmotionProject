#!/usr/bin/env python
# coding: utf-8

# # 情感分析（使用baidu-api）

import pandas as pd
from aip import AipNlp
import time
from utils import *


def get_sentiment_result(text, client):
    result = client.sentimentClassify(text)
    if 'items' in result and len(result['items']) > 0:
        return result['items'][0]
    return None


def get_sentiment_data_frame(df, content_column_name, client):
    sentiment_data = []
    for i, content in df[content_column_name].items():
        try:
            sentiment_item = get_sentiment_result(content, client)
        except Exception as err:
            print(f'🌈GET_SENTIMENT_ERROR!!--->{err=}, {type(err)=}')
            sentiment_item = {
                'index': pd.NA,
                'confidence': pd.NA,
                'negative_prob': pd.NA,
                'positive_prob': pd.NA,
                'sentiment': pd.NA,
                'sentiment_processed': 0
            }
        if sentiment_item:
            sentiment_item['index'] = i
        else:
            sentiment_item = {
                'index': pd.NA,
                'confidence': pd.NA,
                'negative_prob': pd.NA,
                'positive_prob': pd.NA,
                'sentiment': pd.NA,
                'sentiment_processed': 1
            }
        sentiment_data.append(sentiment_item)
        time.sleep(0.5)
    return df.join(
        pd.DataFrame(data=sentiment_data).set_index('index', drop=True))


# 再次遍历，找出情感识别失败的弹幕进行识别，补充数据
def supplement_sentiment_data_frame(df, content_column_name, client):
    sentiment_data = []
    for i, content in df[df[content_column_name +
                            '_processed'] == 0][content_column_name].items():
        try:
            sentiment_item = get_sentiment_result(content, client)
        except Exception as err:
            print(f'🌈GET_SENTIMENT_ERROR!!--->{err=}, {type(err)=}')
            sentiment_item = {
                'index': pd.NA,
                'confidence': pd.NA,
                'negative_prob': pd.NA,
                'positive_prob': pd.NA,
                'sentiment': pd.NA,
                'sentiment_processed': 0
            }
        if sentiment_item:
            sentiment_item['index'] = i
        else:
            sentiment_item = {
                'index': pd.NA,
                'confidence': pd.NA,
                'negative_prob': pd.NA,
                'positive_prob': pd.NA,
                'sentiment': pd.NA,
                'sentiment_processed': 1
            }
        sentiment_data.append(sentiment_item)
        time.sleep(0.5)
    supplementary_sentiment_data_frame = pd.DataFrame(
        data=sentiment_data).set_index('index', drop=True)
    df.loc[df[df['sentiment_processed'] == 0].index, [
        'confidence', 'negative_prob', 'positive_prob', 'sentiment',
        'sentiment_processed'
    ]] = supplementary_sentiment_data_frame[[
        'confidence', 'negative_prob', 'positive_prob', 'sentiment',
        'sentiment_processed'
    ]]
    return df


if __name__ == "__main__":
    BulletDataFilePath = 'data/bullet_chats.pkl'
    SubtitleDataFilePath = 'data/subtitle.pkl'

    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    # 识别弹幕
    data = pd.read_pickle(BulletDataFilePath)
    data = get_sentiment_data_frame(data, 'content', client)
    data.to_pickle(get_new_path(BulletDataFilePath, 'sentiment'))

    # 识别字幕
    data = pd.read_pickle(SubtitleDataFilePath)
    data = get_sentiment_data_frame(data, 'content', client)
    data.to_pickle(get_new_path(SubtitleDataFilePath, 'sentiment'))
