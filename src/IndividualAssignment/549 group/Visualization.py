import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import pandas as pd


# 设置中文字体
plt.rcParams['font.family'] = 'Songti SC'
plt.rcParams['axes.unicode_minus'] = False

def draw_porter_detail():
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
            "Availability of Alternatives": 4,
            "Total": 2.4
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
    ax1.set_ytickLabel(forces, fontsize=11)
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
    ax2.set_ytickLabel(all_subcategories, fontsize=10)
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
    scores = [4.16, 1.75, 2.5, 2.4, 2.8]

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


def draw_competitive_advantage_stack_chart(figsize=(14, 8), subplot_figsize=(16, 6)):
    """
    Create stacked bar charts showing competitive advantage distribution across value chain activities.

    Parameters:
    -----------
    dataframe : pd.DataFrame
        DataFrame containing the resource and capability data
    figsize : tuple, default=(14, 8)
        Size of the main chart
    subplot_figsize : tuple, default=(16, 6)
        Size of the subplot chart

    Returns:
    --------
    None (displays the charts)
    """
    data = {
        'Activity Type': ['Primary', 'Primary', 'Primary', 'Primary', 'Primary', 'Primary',
                          'Primary', 'Primary', 'Primary', 'Primary', 'Primary', 'Support',
                          'Support', 'Support', 'Support', 'Support', 'Support'],
        'Value Chain Activity': ['Inbound Logistics', 'Inbound Logistics', 'Operations',
                                 'Operations', 'Operations', 'Outbound Logistics',
                                 'Marketing & Sales', 'Marketing & Sales', 'Marketing & Sales',
                                 'Service', 'Service', 'Firm Infrastructure',
                                 'Human Resource Management', 'Technology Development',
                                 'Technology Development', 'Technology Development',
                                 'Procurement'],
        'Resource / Capability': ['Global supply chain', 'Strategic supplier partnerships',
                                  'Manufacturing plants', 'Advanced operational capabilities',
                                  'AMOLED / Foldable Display Patents', 'Global distribution channels',
                                  'Brand reputation', 'Marketing capabilities',
                                  'Galaxy ecosystem', 'Customer service / after-sales support',
                                  'Innovation culture', 'Financial resources',
                                  'Skilled, cross-domain workforce', 'Patents & IP portfolio',
                                  'R&D budget', 'On-device AI integration capability',
                                  'Strategic sourcing & vertical self-supply capability'],
        'Competitive Implication': ['Competitive Parity', 'Sustainable Advantage',
                                    'Competitive Parity', 'Sustainable Advantage',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Sustainable Advantage',
                                    'Competitive Parity', 'Sustainable Advantage',
                                    'Competitive Advantage']
    }

    dataframe = pd.DataFrame(data)

    # Group by value chain activity and competitive implication, then count
    activity_counts = dataframe.groupby(['Value Chain Activity', 'Competitive Implication']).size().unstack(
        fill_value=0)

    # Define activity order for better visualization
    primary_activities = ['Inbound Logistics', 'Operations', 'Outbound Logistics', 'Marketing & Sales', 'Service']
    support_activities = ['Firm Infrastructure', 'Human Resource Management', 'Technology Development', 'Procurement']

    # Ensure all activities are in the list and in correct order
    all_activities = primary_activities + support_activities
    activity_counts = activity_counts.reindex(all_activities)

    # Define colors for competitive implications
    colors = {
        'Competitive Parity': '#FF6B6B',
        'Sustainable Advantage': '#4ECDC4',
        'Competitive Advantage': '#45B7D1'
    }

    # Create main stacked bar chart
    plt.figure(figsize=figsize)
    bars = activity_counts.plot(kind='bar',
                                stacked=True,
                                color=[colors[col] for col in activity_counts.columns],
                                figsize=figsize)

    # Customize main chart
    plt.title('Competitive Advantage Distribution Across Value Chain Activities',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Value Chain Activities', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Resources/Capabilities', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Competitive Implication', title_fontsize=10)

    # Add value Label on bars
    for container in bars.containers:
        bars.bar_label(container, label_type='center', fontsize=9, color='white', fontweight='bold')

    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

    # Print summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total Resources/Capabilities: {len(dataframe)}")
    print(
        f"Sustainable Advantage Resources: {len(dataframe[dataframe['Competitive Implication'] == 'Sustainable Advantage'])}")
    print(
        f"Competitive Parity Resources: {len(dataframe[dataframe['Competitive Implication'] == 'Competitive Parity'])}")
    print(
        f"Competitive Advantage Resources: {len(dataframe[dataframe['Competitive Implication'] == 'Competitive Advantage'])}")

    print("\n=== Distribution by Activity Type ===")
    activity_type_summary = dataframe.groupby('Activity Type')['Competitive Implication'].value_counts().unstack()
    print(activity_type_summary)

    # Create subplots by activity type
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=subplot_figsize)

    # Primary activities
    primary_df = dataframe[dataframe['Activity Type'] == 'Primary']
    primary_counts = primary_df.groupby(['Value Chain Activity', 'Competitive Implication']).size().unstack(
        fill_value=0)
    primary_counts = primary_counts.reindex(primary_activities)
    primary_counts.plot(kind='bar', stacked=True,
                        color=[colors[col] for col in primary_counts.columns],
                        ax=ax1, title='Primary Activities')
    ax1.set_ylabel('Number of Resources/Capabilities')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(title='Competitive Implication')

    # Support activities
    support_df = dataframe[dataframe['Activity Type'] == 'Support']
    support_counts = support_df.groupby(['Value Chain Activity', 'Competitive Implication']).size().unstack(
        fill_value=0)
    support_counts = support_counts.reindex(support_activities)
    support_counts.plot(kind='bar', stacked=True,
                        color=[colors[col] for col in support_counts.columns],
                        ax=ax2, title='Support Activities')
    ax2.set_ylabel('Number of Resources/Capabilities')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(title='Competitive Implication')

    plt.tight_layout()
    plt.savefig('data/output/internal_env_stack_chart.png')


def draw_vrio_scatter_plot(figsize=(14, 10)):
    """
    Create a color-coded scatter plot showing the relationship between Rarity and Imitability
    of resources/capabilities, with color indicating Competitive Implication.

    Parameters:
    -----------
    dataframe : pd.DataFrame
        DataFrame containing the resource and capability data
    figsize : tuple, default=(14, 10)
        Size of the chart

    Returns:
    --------
    None (displays the chart)
    """

    # Create a copy of the dataframe to avoid modifying the original
    data = {
        'Activity Type': ['Primary', 'Primary', 'Primary', 'Primary', 'Primary', 'Primary',
                          'Primary', 'Primary', 'Primary', 'Primary', 'Primary', 'Support',
                          'Support', 'Support', 'Support', 'Support', 'Support'],
        'Value Chain Activity': ['Inbound Logistics', 'Inbound Logistics', 'Operations',
                                 'Operations', 'Operations', 'Outbound Logistics',
                                 'Marketing & Sales', 'Marketing & Sales', 'Marketing & Sales',
                                 'Service', 'Service', 'Firm Infrastructure',
                                 'Human Resource Management', 'Technology Development',
                                 'Technology Development', 'Technology Development',
                                 'Procurement'],
        'Resource / Capability': ['Global supply chain', 'Strategic supplier partnerships',
                                  'Manufacturing plants', 'Advanced operational capabilities',
                                  'AMOLED / Foldable Display Patents', 'Global distribution channels',
                                  'Brand reputation', 'Marketing capabilities',
                                  'Galaxy ecosystem', 'Customer service / after-sales support',
                                  'Innovation culture', 'Financial resources',
                                  'Skilled, cross-domain workforce', 'Patents & IP portfolio',
                                  'R&D budget', 'On-device AI integration capability',
                                  'Strategic sourcing & vertical self-supply capability'],
        'Type': ['Tangible / Capability', 'Capability', 'Tangible', 'Capability',
                 'Tangible / Intangible', 'Tangible / Capability', 'Intangible',
                 'Capability', 'Intangible / Capability', 'Capability', 'Intangible',
                 'Tangible', 'Intangible / Capability', 'Intangible',
                 'Tangible / Capability', 'Capability', 'Capability'],
        'Value': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes',
                  'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'Rarity': ['No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes',
                   'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes'],
        'Imitability': ['Medium', 'High', 'High', 'High', 'Very High', 'Medium',
                        'High', 'Medium', 'High', 'Medium', 'Moderate', 'Low',
                        'High', 'Very High', 'Medium', 'High', 'Medium-High'],
        'Organization': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes',
                         'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'Competitive Implication': ['Competitive Parity', 'Sustainable Advantage',
                                    'Competitive Parity', 'Sustainable Advantage',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Competitive Parity',
                                    'Sustainable Advantage', 'Sustainable Advantage',
                                    'Competitive Parity', 'Sustainable Advantage',
                                    'Competitive Advantage']
    }
    df = pd.DataFrame(data)

    # Convert categorical data to numerical values for plotting
    df['Rarity_Num'] = df['Rarity'].map({'Yes': 1, 'No': 0})

    imitability_mapping = {'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4, 'Moderate': 2.5, 'Medium-High': 3.5}
    df['Imitability_Num'] = df['Imitability'].map(imitability_mapping)

    # Define colors for competitive implications
    colors = {
        'Competitive Parity': '#FF6B6B',
        'Sustainable Advantage': '#4ECDC4',
        'Competitive Advantage': '#45B7D1'
    }

    # Apply jitter to separate overlapping points
    np.random.seed(42)  # For reproducible jitter
    jitter_strength_x = 0.08
    jitter_strength_y = 0.15

    # Group points by their original position to apply different jitter strategies
    position_groups = df.groupby(['Rarity_Num', 'Imitability_Num'])

    # Apply jitter within each group
    for (rarity, imitability), group in position_groups:
        if len(group) > 1:
            n_points = len(group)
            grid_size = int(np.ceil(np.sqrt(n_points)))

            x_offsets = np.linspace(-jitter_strength_x, jitter_strength_x, grid_size)
            y_offsets = np.linspace(-jitter_strength_y, jitter_strength_y, grid_size)

            for i, (idx, row) in enumerate(group.iterrows()):
                x_offset = x_offsets[i % grid_size]
                y_offset = y_offsets[i // grid_size]
                df.loc[idx, 'Rarity_Jitter'] = rarity + x_offset
                df.loc[idx, 'Imitability_Jitter'] = imitability + y_offset
        else:
            df.loc[group.index[0], 'Rarity_Jitter'] = rarity + np.random.normal(0, jitter_strength_x / 3)
            df.loc[group.index[0], 'Imitability_Jitter'] = imitability + np.random.normal(0, jitter_strength_y / 3)

    # For points that weren't processed above
    df['Rarity_Jitter'] = df['Rarity_Jitter'].fillna(df['Rarity_Num'])
    df['Imitability_Jitter'] = df['Imitability_Jitter'].fillna(df['Imitability_Num'])

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, gridspec_kw={'width_ratios': [3, 1]})

    # Plot the scatter plot with SMALLER numbered bubbles on the left subplot
    for i, row in df.iterrows():
        ax1.scatter(
            x=row['Rarity_Jitter'],
            y=row['Imitability_Jitter'],
            s=250,  # SMALLER bubbles (reduced from 400)
            c=colors[row['Competitive Implication']],
            alpha=0.7,
            edgecolors='black',
            linewidth=1.5
        )
        # Add number to the center of the bubble
        ax1.text(row['Rarity_Jitter'], row['Imitability_Jitter'], str(i + 1),
                 ha='center', va='center', fontsize=9, fontweight='bold', color='black')

    # Customize the scatter plot
    ax1.set_title('VRIO Analysis: Resource/Capability Rarity vs. Imitability',
                  fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Rarity (No=0, Yes=1)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Imitability (Low=1, Medium=2, High=3, Very High=4)', fontsize=11, fontweight='bold')
    ax1.set_xticks([0, 1])
    ax1.set_xtickLabel(['Not Rare (0)', 'Rare (1)'])
    ax1.set_yticks([1, 2, 3, 4])
    ax1.set_ytickLabel(['Low (1)', 'Medium (2)', 'High (3)', 'Very High (4)'])
    ax1.grid(alpha=0.3, linestyle='--')

    # Add quadrant Label
    ax1.text(0.1, 3.5, 'Competitive Disadvantage\n(Low Rarity, High Imitability)',
             fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
    ax1.text(0.1, 1.5, 'Temporary Advantage\n(Low Rarity, Low Imitability)',
             fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
    ax1.text(0.6, 3.5, 'Sustainable Advantage\n(High Rarity, High Imitability)',
             fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
    ax1.text(0.6, 1.5, 'Competitive Parity\n(High Rarity, Low Imitability)',
             fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))

    # Create a custom legend for competitive implications
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[imp],
               markersize=8, label=imp)
        for imp in colors.keys()
    ]
    ax1.legend(handles=legend_elements, title='Competitive Implication', loc='upper left')

    # Create a neat list of resources on the right side with TWO-LINE FORMAT
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, len(df) + 1)
    ax2.axis('off')
    ax2.set_title('Resource/Capability Legend', fontsize=12, fontweight='bold', pad=20)

    # Add resource names with numbers on the right side - NOW WITH TWO LINES
    for i, row in df.iterrows():
        y_pos = len(df) - i  # Position from top to bottom

        # Add colored circle matching the competitive implication
        ax2.scatter(0.1, y_pos, s=80, c=colors[row['Competitive Implication']],
                    alpha=0.7, edgecolors='black')

        # Add number (larger font)
        ax2.text(0.15, y_pos, f"{i + 1}.", fontsize=10, va='center', fontweight='bold')

        # Add resource name (FIRST LINE - larger font)
        resource_name = row['Resource / Capability']
        # Shorten if too long
        if len(resource_name) > 30:
            resource_name = resource_name[:27] + "..."
        ax2.text(0.25, y_pos + 0.15, resource_name, fontsize=9, va='center', fontweight='bold')

        # Add activity type and value chain activity (SECOND LINE - larger font)
        activity_info = f"{row['Value Chain Activity']} ({row['Activity Type']})"
        # Shorten if too long
        if len(activity_info) > 30:
            activity_info = activity_info[:27] + "..."
        ax2.text(0.25, y_pos - 0.15, activity_info, fontsize=8, va='center', style='italic', color='gray')

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()

    # Print a detailed numbered list
    print("\n" + "=" * 80)
    print("DETAILED RESOURCE/CAPABILITY ANALYSIS")
    print("=" * 80)

    # Group by competitive implication for better organization
    for implication in df['Competitive Implication'].unique():
        print(f"\n--- {implication.upper()} ---")
        subset = df[df['Competitive Implication'] == implication]
        for i, row in subset.iterrows():
            print(f"\n{str(i + 1).zfill(2)}. {row['Resource / Capability']}")
            print(f"    Value Chain: {row['Value Chain Activity']} ({row['Activity Type']})")
            print(f"    Type: {row['Type']}")
            print(f"    Rarity: {row['Rarity']}, Imitability: {row['Imitability']}")
            print(f"    Strategic Position: {get_strategic_position(row['Rarity_Num'], row['Imitability_Num'])}")


def get_strategic_position(rarity, imitability):
    """Helper function to determine strategic position based on rarity and imitability"""
    if rarity == 0 and imitability >= 3:
        return "Competitive Disadvantage (Low Rarity, High Imitability)"
    elif rarity == 0 and imitability <= 2:
        return "Temporary Advantage (Low Rarity, Low Imitability)"
    elif rarity == 1 and imitability <= 2:
        return "Competitive Parity (High Rarity, Low Imitability)"
    elif rarity == 1 and imitability >= 3:
        return "Sustainable Advantage (High Rarity, High Imitability)"
    else:
        return "Intermediate Position"


if __name__ == '__main__':


    # Use the function to create charts
    draw_porter_detail()