import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.family'] = 'Songti SC'
plt.rcParams['axes.unicode_minus'] = False

# 这里需要您将完整的数据替换到下面的数据框中
# 创建示例数据（请用您的实际数据替换）


df = pd.read_csv('data/mid/statics_classified.csv', sep='\t')
df['标准化日期'] = pd.to_datetime(df['标准化日期'])

def plot_problem_type_pie(df):
    plt.figure(figsize=(6, 3))
    problem_counts = df['问题分类'].value_counts()

    # 设置颜色：浅红色，浅黄色，浅蓝色（填充色）
    colors = ['#FFB6C1', '#FFFACD', '#ADD8E6']  # 浅红色, 浅黄色, 浅蓝色

    # 设置边框颜色：比填充颜色深一点的不同颜色
    edgecolors = ['#FF1493', '#FFA500', '#0000FF']  # 深粉色, 橙色, 蓝色

    # 设置爆炸距离，让每个部分有微小空隙
    explode = [0.02, 0.02, 0.02]  # 每个部分向外爆炸2%的距离

    wedges, texts, autotexts = plt.pie(problem_counts.values,
                                      labels=problem_counts.index,
                                      autopct='%1.1f%%',
                                      colors=colors,
                                      explode=explode,  # 添加爆炸效果
                                      startangle=90,
                                      textprops={'fontsize': 12})

    # 为每个扇形单独设置不同颜色的边框
    for i, wedge in enumerate(wedges):
        wedge.set_edgecolor(edgecolors[i % len(edgecolors)])
        wedge.set_linewidth(2)  # 边框宽度

    # 美化百分比文字
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')

    plt.title('问题类型分布', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('data/output/overall_ratio.png')


# 处理方式1：根据时间按月度呈现投诉数量变化（折线图+半年均线）
def plot_monthly_complaints_line_with_ma(df, title_suffix=""):
    """绘制月度投诉数量变化折线图（含半年均线）"""
    # 按月份分组统计
    monthly_complaints = df.groupby(df['标准化日期'].dt.to_period('M')).size().sort_index()
    monthly_complaints.index = monthly_complaints.index.astype(str)

    # 计算半年移动平均（6个月）
    monthly_series = pd.Series(monthly_complaints.values, index=pd.to_datetime(monthly_complaints.index))
    half_year_ma = monthly_series.rolling(window=6, min_periods=1).mean()

    plt.figure(figsize=(6, 3))

    # 绘制原始数据折线图
    line_original = plt.plot(monthly_complaints.index, monthly_complaints.values,
                             marker='o', linewidth=2, markersize=6, color='#2E86AB',
                             markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=1,
                             label='月度投诉量')

    # 绘制半年均线
    line_ma = plt.plot(monthly_complaints.index, half_year_ma.values,
                       linewidth=3, color='#FF6B6B', linestyle='--',
                       alpha=0.8, label='半年均线 (6个月)')

    # 在原始数据点上显示数值
    for i, value in enumerate(monthly_complaints.values):
        plt.annotate(str(value),
                     (monthly_complaints.index[i], value),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center',
                     fontsize=9,
                     fontweight='bold')

    # 在半年均线上显示数值（只显示有完整6个月数据的点）
    for i, value in enumerate(half_year_ma.values):
        if i >= 5:  # 从第6个月开始显示均线数值
            plt.annotate(f'{value:.1f}',
                         (monthly_complaints.index[i], value),
                         textcoords="offset points",
                         xytext=(0, -15),
                         ha='center',
                         fontsize=8,
                         color='#FF6B6B',
                         fontweight='bold')

    plt.title(f'月度投诉数量变化趋势{title_suffix}（含半年均线）', fontsize=16, fontweight='bold')
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('投诉数量', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'data/output/月度投诉数量变化趋势{title_suffix}（含半年均线）')

    return monthly_complaints, half_year_ma


# 处理方式3：过滤指定问题类型，根据时间按月度呈现投诉数量变化（折线图+半年均线）
def plot_filtered_monthly_complaints_line_with_ma(df, problem_type):
    """绘制指定问题类型的月度投诉数量变化折线图（含半年均线）"""
    filtered_df = df[df['问题分类'] == problem_type]

    if len(filtered_df) == 0:
        print(f"没有找到问题类型为 '{problem_type}' 的投诉数据")
        return None, None

    print(f"\n{problem_type}的投诉统计:")
    print(f"总数量: {len(filtered_df)}")
    print(f"占比: {len(filtered_df) / len(df) * 100:.1f}%")

    # 调用带均线的月度统计函数
    monthly_data, ma_data = plot_monthly_complaints_line_with_ma(filtered_df, f' - {problem_type}')

    return monthly_data, ma_data



# 执行可视化分析
print("=" * 50)
print("开始数据可视化分析（含半年均线）")
print("=" * 50)

# 1. 总体月度投诉趋势（折线图+半年均线）
print("\n1. 总体月度投诉趋势分析（含半年均线）")
monthly_overall, ma_overall = plot_monthly_complaints_line_with_ma(df, " - 总体")

# 2. 问题类型分布
print("\n2. 问题类型分布分析")
problem_distribution = plot_problem_type_pie(df)

# 3. 按问题类型分别分析月度趋势（折线图+半年均线）
print("\n3. 按问题类型分析月度趋势（含半年均线）")
problem_types = df['问题分类'].unique()

for problem_type in problem_types:
    print(f"\n分析问题类型: {problem_type}")
    filtered_monthly, filtered_ma = plot_filtered_monthly_complaints_line_with_ma(df, problem_type)

