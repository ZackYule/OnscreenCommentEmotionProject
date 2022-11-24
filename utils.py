# ## 函数工具
import pandas as pd
import re

def get_new_path(old_path, new_tag):
    path_list = old_path.rsplit('.', 1)
    path_list[0] += '_'+new_tag
    return '.'.join(path_list)


def content_clean(text):
    res = re.sub('\xb4|٩|`|Д|۶|๓|╰|╯|♡|◦|˙|▽|ò|ᆺ|ó|➕|•̥́|ˍ|•̀ू|✂|✪|▽', '', text)
    return res

def apply_and_concat(df, field, func, args, column_names):
    return pd.concat((
        df,
        df[field].apply(
            lambda cell: pd.Series(func(cell, *args), index=column_names))), axis=1)


if __name__ == "__main__":
    print(content_clean("曾经大学课间放送的٩(`Д)۶lpl冲鸭"))