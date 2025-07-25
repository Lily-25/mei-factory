import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np


def ploting_multi_pics_linechart(df):
    category_group = df['Category'].unique()
    fig, axes = plt.subplots(len(category_group), 1, figsize=(12, 12), sharex=True)

    for i, category in enumerate(category_group):
        category_df = df[df['Category'] == category]
        sns.lineplot(
            x='Date',
            y='Value',
            data=category_df,
            ax=axes[i],
            linewidth=2
        )
        axes[i].set_title(f'Category {category} Trend', fontsize=14)
        axes[i].set_ylabel('Value')

    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()


def ploting_multi_lines_linechart(df):
    """
    the format of dataframe is as follow:
    Date | Value | Category
    2025-06-18 | 1441.0 | A
    2025-06-18 | 1432 | B

    the example to struct the dataframe is as follow:
    # 创建类别A的数据
    df_a = pd.DataFrame({
        'Date': data.index,
        'Value': data.Open,
        'Category': 'Open'
    })

    # 创建类别B的数据
    df_b = pd.DataFrame({
        'Date': data.index,
        'Value': data.Close,
        'Category': 'Close'
    })

    # 合并所有数据
    df = pd.concat([df_a, df_b], ignore_index=True)
    """

    plt.figure(figsize=(18, 9))

    category_group = df.Category.unique()
    category_dict = {}
    for item in category_group:
        if item.find('MA'):
            category_dict[item] = ""
        else:
            category_dict[item] = (4, 2)
    print(category_dict)

    # 创建带置信区间的趋势图
    sns.lineplot(
        x='Date',
        y='Value',
        hue='Category',
        style='Category',
        dashes=category_dict,
        data=df,
        err_style='band',  # 置信区间显示为带状
        estimator='mean',  # 显示均值趋势
        errorbar=('ci', 95),  # 95% 置信区间
    )

    # 添加标题和标签
    plt.title('Value Trend with 95% Confidence Interval', fontsize=16, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)

    # 添加垂直线标记重要日期
    start_date = min(df.Date)
    plt.axvline(start_date, color='red', linestyle='--', alpha=0.7)
    plt.text(start_date, df['Value'].min(), 'Event', rotation=90, verticalalignment='bottom')
    # plt.axvline(pd.Timestamp('2025-05-15'), color='red', linestyle='--', alpha=0.7)
    # plt.text(pd.Timestamp('2025-05-15'), df['Value'].min(), 'Event', rotation=90, verticalalignment='bottom')

    ax = plt.gca()

    # 设置主刻度为每1天
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    # 添加水平参考线
    plt.axhline(y=min(df.Value) - 1, color='gray', linestyle='-', alpha=0.4)

    # 优化日期格式
    plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    df = pd.DataFrame({"Date": pd.date_range(start='2025-01-01', end='2025-01-10', freq='D'),
                       "A": np.linspace(-5, 5, 10),
                       "B": np.linspace(5, -5, 10), })
    df['MA5'] = df['A'].rolling(window=5).mean()
    df = df.melt(id_vars=['Date'], value_vars=['A', 'B', 'MA5'], var_name='Category', value_name='Value',
                 ignore_index=True)

    ploting_multi_lines_linechart(df)