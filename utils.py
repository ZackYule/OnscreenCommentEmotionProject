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


def time_serialization(df, time_column_name):
    df = df[df[time_column_name].notna()]
    df.sort_values(by=time_column_name, inplace=True)
    df = df.reset_index(drop=True)
    df[time_column_name] = df[time_column_name].astype('Int64')
    return df


if __name__ == "__main__":
    print(remove_abnormal_symbols("曾经大学课间放送的٩(`Д)۶lpl冲鸭"))