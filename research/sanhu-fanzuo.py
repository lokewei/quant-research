"""
邢不行-散户卖出占比统计
作者：邢不行
作者微信：xbx297
"""

import os
import pandas as pd

def load_file(path, file):
    path += file
    df = pd.read_csv(path, encoding='gbk', parse_dates=['交易日期'], skiprows=1)
    return df

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 后续计算N日后涨跌幅所需参数
day_list = [1, 5, 10, 20]
# 测试时间段，可根据数据时间更改
start_time = '20070101'
end_time = '20220331'

# ======= 此处需修改
# 这里填写文件夹的绝对路径。
file_path = r'/Users/xbx/Desktop/xbx_stock_day_data_pro/stock/'
# 获取文件夹下的所有csv文件
file_list = os.listdir(file_path)
file_list = [f for f in file_list if '.csv' in f]

# 测试可使用下方代码
# file_list = ['sh600000.csv', 'sh600519.csv','sz300750.csv']

dfs = []
for f in file_list:
    print(f)
    # 加载数据
    df = load_file(file_path, f)
    df['factor'] = df['散户资金卖出额'] * 10000 / df['成交额'] * 100
    for i in [1, 3, 5]:
        df['未来%d日涨跌幅' % i] = df['收盘价'].shift(-i) / df['前收盘价'].shift(-1) - 1
    df.dropna(subset=['散户资金卖出额', '成交额'], how='any', inplace=True, axis=0)

    dfs.append(df)
all_df = pd.concat(dfs, ignore_index=True)

# ===计算未来N天涨跌幅
all_df = all_df[all_df['交易日期'] >= pd.to_datetime(start_time)]
all_df = all_df[all_df['交易日期'] <= pd.to_datetime(end_time)]

# ===计算最终表格
result = pd.DataFrame()  # 创建一个空的表格
for flow in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
    # 筛选出净买入大于flow的情况
    t_df = all_df[all_df['factor'] > flow]
    # 计算出现次数
    result.loc[flow, '出现次数'] = t_df.shape[0]
    # 计算未来N天数据
    for i in [1, 3, 5]:
        result.loc[flow, '未来%d日上涨次数' % i] = t_df[t_df['未来%d日涨跌幅' % i] > 0].shape[0]
        result['未来%d日上涨概率' % i] = result['未来%d日上涨次数' % i] / result['出现次数']
        result.loc[flow, '未来%d日上涨平均涨幅' % i] = t_df['未来%d日涨跌幅' % i].mean()
# ===输出统计结果
print(result)
result.to_csv('result.csv', encoding='gbk')













