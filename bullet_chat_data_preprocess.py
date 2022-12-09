#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from utils import *

if __name__ == "__main__":
    OutFilePath = 'data/bullet_chats.pkl'

    df_list = []
    for i in range(6):
        num = i + 1
        DataFilePath = f'data/bullet_chats/美丽中国 - {num}.json'
        data_temp = pd.read_json(DataFilePath)
        data_temp['episode'] = num
        data_temp = time_serialization(data_temp)
        df_list.append(data_temp)
    data = pd.concat(df_list, axis=0)

    data['content'] = data[data['content'].notna()]['content'].apply(
        remove_abnormal_symbols)

    data.to_pickle(OutFilePath)
