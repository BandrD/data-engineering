import pandas as pd
import matplotlib
import numpy as np
import os

pd.set_option('display.max_rows', 20, 'display.max_columns', 60)
file_size = os.path.getsize('[1]game_logs.csv')
file_name = '[1]game_logs.csv'
def read_file(file_name):
    return pd.read_csv(file_name)
    # df = pd.read_csv(dataserts[year], chunksize=chunksize, compression='gzip')



def get_memory_stat_by_column(df):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usages = memory_usage_stat.sum()
    print(f"file in memory size = {total_memory_usages//1024:10} КБ")
    column_stat = list()
    for key in df.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": int(memory_usage_stat[key] // 1024),
            "memory_per": round(memory_usage_stat[key] / total_memory_usages * 100, 4),
            "dtype": df.dtypes[key]
        })
    column_stat.sort(key=lambda x: x["memory_abs"], reverse=True)
    for column in column_stat:
        print(
            f"{column['column_name']:30}: {column['memory_abs']:10} КБ: {column['memory_per']:10}% : {column['dtype']}")


    print(f'file size                 = {file_size // 1024:10} КБ')

# dataset = read_file('[1]game_logs.csv')

# get_memory_stat_by_column(dataset)

print("\n\nС днем рождения, Санек!\n")