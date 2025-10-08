import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

def draw_rate():
    # Sample data - replace with your actual data
    # Assuming multiple user rating data
    df = pd.read_csv('data/output/rate_result.csv')
    data = {
        'service_experience': list(df['service_experience']),
        'moment_of_surprise': list(df['moment_of_surprise']),
        'product_experience': list(df['product_experience']),
        'goal_achievement': list(df['goal_achievement']),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate average scores for each metric
    means = df.replace(0, np.nan).mean()
    print("Average Scores for Each Metric:")
    for key, value in means.items():
        print(f"{key}: {value:.2f}")
    
    # Calculate comprehensive score (average of four metrics)
    comprehensive_score = means.mean()
    print(f"\nComprehensive Score: {comprehensive_score:.2f}")
    
    # Create visualization charts
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Set colors
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    # Subplot 1: Radar Chart
    categories = ['Service Experience', 'Moment of Surprise', 'Product Experience', 'Goal Achievement', 'Comprehensive Score']
    values = list(means.values) + [comprehensive_score]
    
    # To close the radar chart, repeat the first value
    values_radar = values + [values[0]]
    categories_radar = categories + [categories[0]]
    
    # Calculate angles
    angles = np.linspace(0, 2*np.pi, len(categories_radar), endpoint=True).tolist()
    
    ax1 = plt.subplot(2, 1, 1, polar=True)
    ax1.plot(angles, values_radar, 'o-', linewidth=2, label='Scores', color=colors[0])
    ax1.fill(angles, values_radar, alpha=0.25, color=colors[0])
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories_radar[:-1])
    ax1.set_ylim(0, 5)
    ax1.set_yticks([1, 2, 3, 4, 5])
    ax1.grid(True)
    ax1.set_title('User Experience Quality Radar Chart Analysis', size=14, fontweight='bold', pad=20)
    
    # Add value labels on radar chart
    for angle, value, category in zip(angles[:-1], values, categories):
        ax1.text(angle, value + 0.3, f'{value:.1f}', ha='center', va='center', fontweight='bold')
    
    # Subplot 2: Bar Chart + Line Chart
    ax2 = plt.subplot(2, 1, 2)
    
    # Bar chart
    bars = ax2.bar(categories, values, color=colors[:5], alpha=0.7, edgecolor='black')
    
    # Display values on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Set y-axis range
    ax2.set_ylim(0, 5.5)
    ax2.set_ylabel('Score (0-5 points)', fontweight='bold')
    ax2.set_xlabel('Evaluation Dimensions', fontweight='bold')
    ax2.set_title('Detailed Scores by Dimension', size=14, fontweight='bold', pad=20)
    ax2.grid(True, axis='y', alpha=0.3)
    
    # Add horizontal reference lines
    for y in [1, 2, 3, 4, 5]:
        ax2.axhline(y=y, color='gray', linestyle='--', alpha=0.3)
    
    # Add data table
    table_data = []
    for i, category in enumerate(categories):
        table_data.append([category, f'{values[i]:.2f}'])
    
    # Add table below the chart
    plt.figtext(0.03, 0.03,
               f"Data Source: DianPing\n",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="None", edgecolor='None', alpha=0.5), # 设置 edgecolor='None'
               fontsize=13)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # Make space for table
    # plt.show()
    plt.savefig('data/output/User Experience Quality Chart Analysis')
    
    # Additional detailed statistical information
    print("\n" + "="*50)
    print("Detailed Statistical Analysis")
    print("="*50)
    print(f"Number of data samples: {len(df)}")
    print(f"Score range for each dimension: 1-5 points")
    print(f"Highest scoring dimension: {categories[np.argmax(values)]} ({max(values):.2f} points)")
    print(f"Lowest scoring dimension: {categories[np.argmin(values)]} ({min(values):.2f} points)")
    print(f"Standard deviation: {df.std().mean():.2f}")
    
    # Create optional trend chart
    plt.figure(figsize=(10, 6))
    plt.plot(categories, values, marker='o', linewidth=2, markersize=8, color='#FF6B6B')
    plt.fill_between(categories, values, alpha=0.3, color='#FF6B6B')
    plt.axhline(y=comprehensive_score, color='red', linestyle='--', label=f'Comprehensive Score Line ({comprehensive_score:.2f})')
    plt.ylabel('Score')
    plt.title('User Experience Dimension Score Trend')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Add value labels
    for i, v in enumerate(values):
        plt.text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    # plt.show()
    plt.savefig('data/output/User Experience Dimension Score Trend')
    
def draw_visitor():
    
    # Data preparation
    years = ['2019', '2023']

    # Visitor data (unit: 10,000 visitors)
    visitors_data = {
        'Longlinshan Park': [3, 2.8],
        'Zhongshan Park': [4, 12]
    }

    # Calculate growth rates
    growth_rates = {
        'Longlinshan Park': [0, ((visitors_data['Longlinshan Park'][1] - visitors_data['Longlinshan Park'][0])
                                 / visitors_data['Longlinshan Park'][0])],  # Growth rate: (new-old)/old * 100%
        'Zhongshan Park': [0, ((visitors_data['Zhongshan Park'][1] - visitors_data['Zhongshan Park'][0])
                                 / visitors_data['Zhongshan Park'][0])]
    }

    # Create figure and axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Set bar chart positions
    x = np.arange(len(years))  # [0, 1]
    width = 0.35  # Bar width

    # Draw bar chart (left Y-axis)
    bars1 = ax1.bar(x - width / 2, visitors_data['Longlinshan Park'], width,
                    label='Longlinshan Park Visitors', color='#F8BBD0', alpha=0.8)
    bars2 = ax1.bar(x + width / 2, visitors_data['Zhongshan Park'], width,
                    label='Zhongshan Park Visitors', color='#D3D3D3', alpha=0.8)

    # Set left Y-axis (visitors)
    #ax1.set_xlabel('Year')
    ax1.set_ylabel('Visitors (10,000 persons)', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.legend(loc='upper left')

    # Create right Y-axis (growth rate)
    ax2 = ax1.twinx()

    # Draw line chart (right Y-axis)
    line1 = ax2.plot(x, growth_rates['Longlinshan Park'], marker='o', linestyle='-',
                     color='blue', linewidth=2, markersize=8, label='Longlinshan Park Growth Rate')
    line2 = ax2.plot(x, growth_rates['Zhongshan Park'], marker='s', linestyle='--',
                     color='red', linewidth=2, markersize=8, label='Zhongshan Park Growth Rate')

    # Set right Y-axis (growth rate)
    ax2.set_ylabel('Growth Rate (%)', fontsize=12)
    ax2.legend(loc='upper right')

    # Add data labels
    def add_labels(bars, ax):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.0f}',
                    ha='center', va='bottom', fontsize=10)

    def add_line_labels(lines, ax):
        for line in lines:
            for x_val, y_val in zip(line.get_xdata(), line.get_ydata()):
                if y_val > 0:  # Only add labels for non-zero values
                    ax.text(x_val, y_val, f'{y_val:.1f}%',
                            ha='center', va='bottom', fontsize=10)

    add_labels(bars1, ax1)
    add_labels(bars2, ax1)
    add_line_labels(line1, ax2)
    add_line_labels(line2, ax2)

    # Set title and grid
    plt.title('Park Visitors Comparison: 2019 vs 2023 with Growth Rate Analysis', fontsize=14, pad=20)
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Adjust layout
    plt.tight_layout()

    # Display chart
    plt.savefig('data/output/traffic')

def draw_park_review_chart():
    # Get data
    review_types = ['Self-driving', 'Total']
    review_counts = [20, 401]  # 851 divided into two part  450/401

    # Lower section: Annual review trends (2019-2025)
    years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025']
    annual_reviews = [4, 0, 12, 2, 0, 1, 1]  # Example data

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Add overall title
    fig.suptitle('Park Review Analysis - Dianping Platform',
                 fontsize=16, fontweight='bold', y=0.99)

    # Upper section: Self-driving vs Total reviews (Bar chart)
    colors = ['#F8BBD0', '#D3D3D3']

    # Create bar chart
    bars = ax1.bar(review_types, review_counts, color=colors, alpha=0.8, width=0.6)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 20,
                 f'{height}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Calculate percentage of self-driving reviews
    self_driving_pct = (review_counts[0] / review_counts[1]) * 100

    # Add percentage annotation
    ax1.text(0.5, 0.95, f'Self-driving reviews: {self_driving_pct:.1f}% of total',
             transform=ax1.transAxes, ha='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    # Configure upper chart
    ax1.set_ylabel('Number of Reviews', fontsize=12, fontweight='bold')
    ax1.set_title('Self-driving Reviews vs Total Reviews',
                  fontsize=14, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_axisbelow(True)

    # Lower section: Annual review trends (Line chart)
    x_positions = np.arange(len(years))

    # Create line plot
    line = ax2.plot(x_positions, annual_reviews, marker='o', linestyle='-',
                    color='#F18F01', linewidth=3, markersize=8,
                    markerfacecolor='#C73E1D', markeredgecolor='black',
                    markeredgewidth=1, label='Annual Reviews')

    # Add data point labels
    for i, (x, y) in enumerate(zip(x_positions, annual_reviews)):
        ax2.annotate(f'{y}', (x, y),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center',
                     fontsize=10,
                     fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

    # Configure lower chart
    ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Reviews', fontsize=12, fontweight='bold')
    ax2.set_title('Annual Review Trends (2019-2025)',
                  fontsize=14, fontweight='bold', pad=20)
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(years)
    ax2.grid(True, alpha=0.3)
    ax2.set_axisbelow(True)

    # Add projection note for future years
    ax2.text(0.02, 0.98, 'Note: 2024-2025 data are projections',
             transform=ax2.transAxes, fontsize=10, color='blue',
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    # Adjust layout
    plt.tight_layout()

    # Display chart
    plt.savefig('data/output/reviews')

if __name__ == '__main__':
    draw_visitor()