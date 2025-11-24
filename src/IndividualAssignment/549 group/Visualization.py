import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# 设置中文字体
plt.rcParams['font.family'] = 'Songti SC'
plt.rcParams['axes.unicode_minus'] = False

def draw_porter_5_forces_fan():
    # 数据整理
    data = {
        "Existing Rivalry": {
            "Number & Balance of Competitors": 5,
            "Market Growth Rate": 4,
            "Product Differentiation Level": 4,
            "Switching Costs": 4,
            "Exit Barriers": 3,
            "Price Competition Intensity": 5,
            "Total": 4.16
        },
        "Threat of New Entrants": {
            "Capital Requirements": 1,
            "Economies of Scale": 2,
            "Brand Loyalty / Switching Costs": 2,
            "Access to Distribution Channels": 2,
            "Technology & Product Differentiation": 2,
            "Regulatory Barriers": 2,
            "Expected Retaliation by Incumbents": 1,
            "Network Effects / Ecosystem Lock-In": 2,
            "Total": 1.75
        },
        "Supplier Power": {
            "Number & Concentration of Suppliers": 3,
            "Uniqueness of Inputs / Switching Costs": 3,
            "Supplier Forward Integration Threat": 2,
            "Importance of Samsung to Supplier": 2,
            "Price Sensitivity & Supplier Margins": 3,
            "Total": 2.5
        },
        "Buyer Power": {
            "Number & Concentration of Buyers": 1,
            "Buyer Price Sensitivity": 3,
            "Buyer Ability to Backward Integrate": 1,
            "Importance of Product to Buyer": 3,
            "Availability of Alternatives": 2,
            "Total": 2.0
        },
        "Threat of Substitutes": {
            "Availability of Substitutes": 2,
            "Performance / Functionality of Substitutes": 3,
            "Price of Substitutes": 3,
            "Buyer Willingness to Substitute": 3,
            "Switching Costs": 2,
            "Potential Substitutes": 4,
            "Total": 2.8
        }
    }

    # 创建从绿到红的渐变色
    def create_gradient_cmap():
        colors = ['#2E8B57', '#7CFC00', '#ADFF2F', '#FFFF00', '#FFA500', '#FF4500', '#FF0000']
        cmap = mcolors.LinearSegmentedColormap.from_list('green_red', colors, N=100)
        return cmap

    cmap = create_gradient_cmap()

    # 创建图形 - 上下布局，总分在上，细分项在下
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 16), gridspec_kw={'height_ratios': [1, 3]})
    plt.subplots_adjust(hspace=0.6)  # 调整上下子图之间的间距

    # 第一部分：五力总分横向条形图（放在上面）
    forces = list(data.keys())
    force_totals = [data[force]["Total"] for force in forces]

    # 为总分创建颜色 - 使用渐变色
    norm = plt.Normalize(1, 5)
    force_colors = [cmap(norm(score)) for score in force_totals]

    # 创建横向条形图 - 修改边框颜色为灰色
    y_pos = np.arange(len(forces))
    bars1 = ax1.barh(y_pos, force_totals, color=force_colors, alpha=0.6, edgecolor='gray', linewidth=1, height=0.6)

    # 添加总分标签
    for i, (bar, total) in enumerate(zip(bars1, force_totals)):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height() / 2,
                 f'{total:.2f}', ha='left', va='center', fontweight='bold', fontsize=11)

    ax1.set_xlabel('Total Score (1-5)', fontsize=12, fontweight='bold')
    ax1.set_title("Porter's Five Forces Analysis - Samsung Smart Phone\nTotal Scores",
                  fontsize=16, fontweight='bold', pad=20)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(forces, fontsize=11)
    ax1.set_xlim(0, 5.5)
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()  # 反转y轴使最高分在最上面

    # 将注释文本移到右上角
    fig.text(0.78, 0.76,
             'Interpretation:\n• Scores range from 1 (Low/Weak) to 5 (High/Strong)\n• Green indicates weaker competitive forces\n  (better for Samsung)\n• Red indicates stronger competitive forces\n  (worse for Samsung)\n• Existing Rivalry is the strongest\n  competitive force (4.16)\n• Threat of New Entrants is the weakest\n  competitive force (1.75)',
             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor='none', edgecolor='black', linestyle='--'),
             transform=fig.transFigure, ha='left')

    # 第二部分：各力细分项得分的横向条形图（放在下面）- 扩大条形
    # 准备数据 - 按竞争力分组
    all_categories = []
    all_subcategories = []
    all_scores = []

    for force in forces:
        for subcategory, score in data[force].items():
            if subcategory != "Total":
                all_categories.append(force)
                all_subcategories.append(subcategory)
                all_scores.append(score)

    # 为细分项创建颜色 - 使用渐变色
    subcategory_colors = [cmap(norm(score)) for score in all_scores]

    # 创建横向条形图 - 扩大条形高度
    y_pos2 = np.arange(len(all_subcategories))
    bars2 = ax2.barh(y_pos2, all_scores, color=subcategory_colors, alpha=0.8, edgecolor='gray', linewidth=1, height=0.8)

    # 添加细分项得分标签
    for i, (bar, score) in enumerate(zip(bars2, all_scores)):
        width = bar.get_width()
        ax2.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                 f'{score}', ha='left', va='center', fontsize=10, fontweight='bold')

    # 设置y轴标签
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(all_subcategories, fontsize=10)
    ax2.set_xlabel('Score (1-5)', fontsize=12, fontweight='bold')
    ax2.set_title("Detailed Subcategory Scores", fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlim(0, 5.5)
    ax2.grid(axis='x', alpha=0.3)

    # 添加竞争力分组标签 - 移到右上角
    current_category = all_categories[0]
    start_idx = 0
    for i, category in enumerate(all_categories + [None]):  # 添加None作为结束标记
        if i == len(all_categories) or category != current_category:
            end_idx = i
            # 添加竞争力标签到右上角
            mid_point = start_idx + (end_idx - start_idx) / 2 - 0.5

            # 将标签放在右上角 (x=5.5, y=mid_point)
            ax2.text(5.3, mid_point, current_category, ha='left', va='center',
                     fontweight='bold', fontsize=11)

            # 添加分隔线
            if i < len(all_categories):
                ax2.axhline(y=end_idx - 0.5, color='gray', linestyle='--', alpha=0.5)

            if i < len(all_categories):
                current_category = category
                start_idx = i

    # 调整x轴限制以容纳右侧标签
    ax2.set_xlim(0, 6.5)


    plt.tight_layout()
    #plt.subplots_adjust(bottom=0.1)  # 调整底部空间
    plt.savefig('data/output/porter_detail.png')

def draw_porter_bar():
    # 数据
    forces = [
        "The Degree of Existing Rivalry",
        "Threat of Potential Entrants",
        "Bargaining Power of Suppliers",
        "Bargaining Power of Buyers",
        "Threat of Substitutes"
    ]
    scores = [4.16, 1.75, 2.5, 2.0, 2.8]

    # 自定义颜色（按您的表格）
    colors = ['#FF0000', '#00CC00', '#D3D3D3', '#D3D3D3', '#FFA500']  # 红、绿、黄、橙、橙

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 横向条形图
    bars = plt.barh(forces, scores, color=colors, edgecolor='black', linewidth=1)

    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.2f}',
                 va='center', ha='left', fontsize=10, fontweight='bold')

    # 标题与标签
    plt.title("Porter's Five Forces Analysis", fontsize=14, fontweight='bold')
    plt.xlabel("Score (Higher = Greater Threat)", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # 调整布局避免文字重叠
    plt.tight_layout()

    # 显示图表
    plt.savefig('data/output/porter')

if __name__ == '__main__':
    draw_porter_5_forces_fan()