import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def draw_inventory_rating():
    # 你的数据（已从表格提取）
    data = {
        'No': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        'Organization': [
            'Intranet', 'Intranet', 'Intranet',
            'Roland Berger China', 'Roland Berger China', 'Roland Berger China',
            'Intranet', 'Intranet', 'Intranet',
            'Roland Berger Global',
            'Intranet',
            'Roland Berger China', 'Roland Berger China'
        ],
        'Knowledge Assets': [
            'Requirement Specification',
            'Internal Case Analysis Report',
            'AI generated insight Report',
            'Application Specification',
            'Special Topic Insight Report',
            'Industrial Report',
            'Topic Experience in interview',
            'Topic insights in brainstorming',
            'Clarification Report',
            'Consulting Topic Insight Reports From RBG',
            'Contracts',
            'Specific Topic Insight Report',
            'External Expert List'
        ],
        'Rating': [5, 2, 1, 4, 4, 4, 1, 1, 1, 4, 5, 3, 3]
    }

    df = pd.DataFrame(data)

    # 1. 计算各 Organization 的平均 Rating
    org_avg = df.groupby('Organization')['Rating'].mean().reset_index()

    # 2. 准备下半部分数据：按 Organization 分组排列
    org_order = org_avg['Organization'].tolist()
    df['Org_Index'] = df['Organization'].map({org: i for i, org in enumerate(org_order)})
    df_sorted = df.sort_values(['Org_Index', 'No']).reset_index(drop=True)

    # 3. 定义评分颜色映射（反转版：高分=绿，低分=红）
    def get_color(rating):
        colors = {
            1: '#FF4500',  # 红色 → 最差
            2: '#FFA500',  # 橙色
            3: '#FFD700',  # 黄色
            4: '#9ACD32',  # 浅绿
            5: '#2E8B57'   # 深绿 → 最好
        }
        return colors.get(rating, 'gray')

    # 4. 绘图设置
    fig, axes = plt.subplots(2, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [1, 3]})
    plt.subplots_adjust(hspace=0.4)

    # --- 上半部分：Organization 平均 Rating ---
    ax1 = axes[0]
    bars1 = ax1.barh(org_avg['Organization'], org_avg['Rating'],
                     color=[get_color(round(x)) for x in org_avg['Rating']],
                     edgecolor='black', linewidth=1.2)
    ax1.set_title('Average Rating by Organization', fontsize=16, fontweight='bold', pad=10)
    ax1.set_xlabel('Average Rating (1-5) — Higher is Better', fontsize=12)
    ax1.grid(axis='x', linestyle='--', alpha=0.6)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # 添加数值标签
    for i, bar in enumerate(bars1):
        width = bar.get_width()
        ax1.text(width + 0.05, bar.get_y() + bar.get_height() / 2, f'{width:.2f}',
                 ha='left', va='center', fontsize=11, fontweight='bold')

    # --- 下半部分：Knowledge Assets Rating ---
    ax2 = axes[1]

    y_positions = np.arange(len(df_sorted))
    colors = [get_color(r) for r in df_sorted['Rating']]
    bars2 = ax2.barh(y_positions, df_sorted['Rating'], color=colors, edgecolor='black', linewidth=1)

    # 设置 y 轴标签
    ax2.set_yticks(y_positions)
    ax2.set_ytickLabel(df_sorted['Knowledge Assets'], fontsize=10, fontfamily='monospace')
    ax2.set_xlabel('Rating (1-5) — Higher is Better', fontsize=12)
    ax2.set_title('Detailed Knowledge Asset Ratings (Grouped by Organization)', fontsize=16, fontweight='bold', pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.6)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # 添加水平虚线分隔不同 Organization 区块，并在右侧标注组织名
    current_y = 0
    max_rating = max(df_sorted['Rating'])  # 用于定位标注位置

    for org in org_order:
        group_data = df_sorted[df_sorted['Organization'] == org]
        if len(group_data) == 0:
            continue
        start_idx = current_y
        end_idx = current_y + len(group_data) - 1
        mid_y = (start_idx + end_idx) / 2

        # 添加虚线分隔（除了第一个区块顶部）
        if start_idx > 0:
            ax2.axhline(y=end_idx + 0.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

        # ✅ 微调1：让虚线右侧与标注文字右侧对齐 → 使用 text 的 ha='right'
        # ✅ 微调2：取消边框和底色 → 移除 bbox 参数，只保留纯文本
        ax2.text(max_rating + 0.3, mid_y, org,
                 fontsize=12, fontweight='bold', color='darkblue',
                 ha='right', va='center')  # ← 关键：ha='right' 对齐右侧

        current_y += len(group_data)

    # 添加数值标签到每个条形末端
    for i, bar in enumerate(bars2):
        width = bar.get_width()
        ax2.text(width + 0.05, bar.get_y() + bar.get_height() / 2, str(int(width)),
                 ha='left', va='center', fontsize=10, fontweight='bold', color='black')

    # 添加图例说明颜色含义（右上角注释框）
    legend_text = (
        "Interpretation:\n"
        "Scores range from 1 (Low) to 5 (High Quality)\n"
        "Green: high-quality knowledge assets\n"
        "Red: low-quality or tacit assets\n"
        "Higher score: More accurate and valuable"
    )
    fig.text(0.78, 0.76,
             legend_text,
             fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor='none', edgecolor='black', linestyle='--'),
             transform=fig.transFigure, ha='left')

    # 调整布局并保存
    plt.tight_layout()
    plt.savefig('data/output/inventory_rating.png', dpi=300, bbox_inches='tight')
    plt.show()  # 可选：显示图形

if __name__ == '__main__':
    draw_inventory_rating()