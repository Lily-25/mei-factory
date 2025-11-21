import matplotlib.pyplot as plt

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