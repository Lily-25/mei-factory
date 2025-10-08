import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
import warnings

warnings.filterwarnings('ignore')

# Load your CSV file
# Replace 'your_file.csv' with the actual path to your file
df = pd.read_csv('data/output/diffusion_rate_by_dimension', sep='\t')

# Display basic info about the data
print("Dataset Info:")
print(df.head())
print(f"\nDataset shape: {df.shape}")
print(f"\nColumn names: {df.columns.tolist()}")

# Check if required columns exist
required_columns = ['Speed Score', 'Breadth Score', 'Depth Score']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Warning: Missing columns: {missing_columns}")
    # You might need to adjust column names based on your actual data


# 1. RADAR CHART FOR DIFFUSION ANALYSIS
def create_radar_chart(df, title="Technical Innovation Diffusion Analysis"):
    """
    Create a radar chart showing Speed, Breadth, and Depth scores
    """
    # Get the scores (assuming single row or taking mean if multiple rows)
    if len(df) == 1:
        scores = df[['Speed Score', 'Breadth Score', 'Depth Score']].iloc[0].values
    else:
        # If multiple rows, you might want to aggregate (mean, sum, etc.)
        scores = df[['Speed Score', 'Breadth Score', 'Depth Score']].sum().values

    scores = [
        df['Speed Score'].sum() / df['Speed'].sum(),
        df['Breadth Score'].sum() / df['Breadth'].sum(),
        df['Depth Score'].sum() / df['Depth'].sum(),
        ]

    # Number of variables
    categories = ['Speed', 'Breadth', 'Depth']
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Complete the loop

    # Add scores to complete the loop
    scores_complete = np.concatenate((scores, [scores[0]]))

    # Initialize the spider plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=12)

    # Draw ylabels
    ax.set_rlabel_position(30)
    plt.yticks([0.2, 0.4, 0.6], ["0.2", "0.4", "0.6"], color="grey", size=10)
    plt.ylim(0, 1)  # Adjust based on your score range

    # Plot data
    ax.plot(angles, scores_complete, linewidth=2, linestyle='solid', color='red',label='Diffusion Score')

    # Fill area
    ax.fill(angles, scores_complete, 'r', alpha=0.25)

    # Add title and legend
    plt.title(title, size=16, pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    plt.tight_layout()
    return fig

def analyze_diffusion_factors(df):
    """
    Framework to analyze factors impacting diffusion dimensions
    """
    print("\n" + "=" * 60)
    print("DIFFUSION ANALYSIS INSIGHTS")
    print("=" * 60)

    # Basic statistics
    if len(df) > 1:
        print("\n1. DESCRIPTIVE STATISTICS:")
        stats = df[['Speed Score', 'Breadth Score', 'Depth Score']].describe()
        print(stats)

        print("\n2. CORRELATION BETWEEN DIMENSIONS:")
        correlation_matrix = df[['Speed Score', 'Breadth Score', 'Depth Score']].corr()
        print(correlation_matrix)

        # Create correlation heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Between Diffusion Dimensions')
        plt.tight_layout()
        plt.show()

    # Individual dimension analysis
    print("\n3. INDIVIDUAL DIMENSION ANALYSIS:")

    # Assuming scores are on a scale (adjust range as needed)
    score_columns = ['Speed Score', 'Breadth Score', 'Depth Score']

    for col in score_columns:
        if col in df.columns:
            if len(df) == 1:
                score = df[col].iloc[0]
                print(f"\n{col.replace(' Score', '')}: {score:.2f}")
                if score >= 8:
                    print(f"   → Strong performance: High {col.replace(' Score', '').lower()} indicates...")
                elif score >= 6:
                    print(f"   → Moderate performance: Room for improvement in {col.replace(' Score', '').lower()}")
                else:
                    print(f"   → Weak performance: {col.replace(' Score', '').lower()} is a bottleneck")
            else:
                mean_score = df[col].mean()
                std_score = df[col].std()
                print(f"\n{col.replace(' Score', '')}: Mean = {mean_score:.2f}, Std = {std_score:.2f}")

    # 4. IDENTIFYING KEY IMPACT FACTORS
    print("\n4. POTENTIAL KEY IMPACT FACTORS TO INVESTIGATE:")
    print("\nSPEED FACTORS (Rate of adoption):")
    print("   • Technology readiness and reliability")
    print("   • Regulatory approval and policy support")
    print("   • Market demand and urgency")
    print("   • Competitive pressure")
    print("   • Infrastructure readiness")

    print("\nBREADTH FACTORS (Geographic/Market reach):")
    print("   • Scalability of the technology")
    print("   • Geographic adaptability")
    print("   • Distribution channels and partnerships")
    print("   • Cultural and regional acceptance")
    print("   • Cost-effectiveness for mass adoption")

    print("\nDEPTH FACTORS (Integration and usage intensity):")
    print("   • User experience and interface design")
    print("   • Integration with existing systems/processes")
    print("   • Training and support availability")
    print("   • Customization and flexibility")
    print("   • Long-term value realization")

    # 5. RECOMMENDATIONS BASED ON SCORES
    if len(df) == 1:
        scores_dict = {col.replace(' Score', ''): df[col].iloc[0] for col in score_columns if col in df.columns}
        min_dimension = min(scores_dict, key=scores_dict.get)
        max_dimension = max(scores_dict, key=scores_dict.get)

        print(f"\n5. STRATEGIC RECOMMENDATIONS:")
        print(f"   • Primary focus area: {min_dimension} (lowest score)")
        print(f"   • Leverage strength: {max_dimension} (highest score)")
        print(f"   • Balance approach: Address {min_dimension} while maintaining {max_dimension}")

# Additional visualization: Bar chart comparison
def create_bar_chart(df):
    """
    Create a simple bar chart comparing the three dimensions
    """
    if len(df) == 1:
        scores = df[['Speed Score', 'Breadth Score', 'Depth Score']].iloc[0]
    else:
        scores = df[['Speed Score', 'Breadth Score', 'Depth Score']].mean()

    plt.figure(figsize=(10, 6))
    bars = plt.bar(['Speed', 'Breadth', 'Depth'], scores,
                   color=['#FFB6C1', '#ADD8E6', '#D3D3D3'])

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                 f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

    plt.title('Technical Innovation Diffusion - Dimension Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Score')
    plt.ylim(0, max(scores) * 1.2)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/output/bar.png')


def uncover_key_points(score_c_name, weight_c_name, file_name):
    import pandas as pd
    import matplotlib.pyplot as plt

    # 读取你的实际数据（替换文件路径）
    # df = pd.read_csv('your_file.csv')

    # 找出正向影响最大的2个指标（Speed Score 最高）
    top2_positive = df.nlargest(2, score_c_name)[
        ['Ref. Dimension', score_c_name, 'Arbitration Score', weight_c_name]
    ]

    # 找出负向影响最大的2个指标（Speed Score 最低）
    top2_negative = df.nsmallest(2, score_c_name)[
        ['Ref. Dimension', score_c_name, 'Arbitration Score', weight_c_name]
    ]

    print("=== 正向影响最大的2个指标 ===")
    print(top2_positive)
    print("\n=== 负向影响最大的2个指标 ===")
    print(top2_negative)

    # 3. 可视化结果
    plt.figure(figsize=(8, 8))

    # 创建子图：左侧显示指标名称，右侧显示详细信息
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 3), width_ratios=[1, 1.5])

    # 左图：Speed Score 条形图
    all_top = pd.concat([top2_positive, top2_negative], ignore_index=True)
    all_top['Type'] = ['Positive', 'Positive', 'Negative', 'Negative']
    colors = ['#2E8B57', '#3CB371', '#DC143C', '#FF6347']  # 绿色系正向，红色系负向

    bars = ax1.barh(range(len(all_top)), all_top[score_c_name], color=colors, height=0.5,  edgecolor='black')
    ax1.set_yticks(range(len(all_top)))
    ax1.set_yticklabels(all_top['Ref. Dimension'])
    ax1.set_xlabel(score_c_name)
    ax1.set_title('The indicator with the greatest impact on the dimension')

    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, all_top[score_c_name])):
        ax1.text(score + 0.01, i, f'{score:.3f}', va='center', fontweight='bold')

    # 右图：详细信息表格
    ax2.axis('tight')
    ax2.axis('off')
    table_data = all_top[['Ref. Dimension', score_c_name, 'Arbitration Score', weight_c_name]].round(3)
    table = ax2.table(cellText=table_data.values,
                      colLabels=['Ref. Dimension', score_c_name, 'Arbitration Score', weight_c_name],
                      cellLoc='center',
                      loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)

    # 设置表格颜色
    for i in range(len(all_top)):
        if i < 2:  # 正向
            table[(i + 1, 0)].set_facecolor('#E8F5E8')
            table[(i + 1, 1)].set_facecolor('#E8F5E8')
        else:  # 负向
            table[(i + 1, 0)].set_facecolor('#FFE8E8')
            table[(i + 1, 1)].set_facecolor('#FFE8E8')

    ax2.set_title('Detailed indicator information', pad=20)

    plt.tight_layout()
    plt.savefig(file_name)

if __name__ == '__main__':
    file_name = 'data/output/Depth'
    uncover_key_points('Depth Score', 'Depth Weight', file_name)
    # Create radar chart
    # radar_fig = create_radar_chart(df)
    # radar_fig.savefig('data/output/radar.png')

    # create_bar_chart(df)