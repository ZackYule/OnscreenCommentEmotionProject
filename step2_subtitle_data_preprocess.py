#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pysubs2
from utils import *

if __name__ == "__main__":
    OutFilePath = 'data/subtitle.pkl'

    df_list = []
    for num in range(1, 7):
        DataFilePath = f'data/subtitles/美丽中国.Wild.China.EP{num}.chs.srt'
        subs = pysubs2.load(DataFilePath)
        texts = [sub.plaintext for sub in subs]
        time_start = [sub.start for sub in subs]
        time_end = [sub.end for sub in subs]
        data_temp = pd.DataFrame({
            'content': texts,
            'progress': time_start,
            'progress_end': time_end,
            'episode': num
        })
        data_temp = time_serialization(data_temp, 'progress')
        df_list.append(data_temp)

    data = pd.concat(df_list, axis=0)
    data['content'] = data[data['content'].notna()]['content'].apply(
        remove_abnormal_symbols)
    data.to_pickle(OutFilePath)
