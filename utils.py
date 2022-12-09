# ## 函数工具
import pandas as pd
import re


def get_new_path(old_path, new_tag):
    path_list = old_path.rsplit('.', 1)
    path_list[0] += '_' + new_tag
    return '.'.join(path_list)


def remove_abnormal_symbols(content):
    res = re.sub('\xb4|\u200b|٩|`|Д|۶|๓|╰|╯|♡|◦|˙|ò|ᆺ|ó|➕|•̥́|ˍ|•̀ू|✂|✪|▽', '',
                 str(content))
    return res


def apply_and_concat(df, field, func, args, column_names):
    return pd.concat((df, df[field].apply(
        lambda cell: pd.Series(func(cell, *args), index=column_names))),
                     axis=1)


def time_serialization(df_has_progress_column):
    df_has_progress_column = df_has_progress_column[
        df_has_progress_column['progress'].notna()]
    df_has_progress_column.sort_values(by='progress', inplace=True)
    df_has_progress_column = df_has_progress_column.reset_index(drop=True)
    df_has_progress_column['progress'] = df_has_progress_column[
        'progress'].astype('Int64')
    return df_has_progress_column


if __name__ == "__main__":
    print(remove_abnormal_symbols("曾经大学课间放送的٩(`Д)۶lpl冲鸭"))