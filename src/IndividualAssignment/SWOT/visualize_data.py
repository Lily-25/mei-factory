import matplotlib.pyplot as plt
import numpy as np

# Set font parameters
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

import matplotlib.pyplot as plt
def create_swot_bubble_chart(swot_metrics,
                             title = 'SWOT Analysis: Autonomous Driving Technology in Park'):
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))

    # Set background color
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')

    # Color settings for each quadrant (keeping for bubbles only)
    colors = {
        'Strengths': '#2ecc71',  # Green
        'Weaknesses': '#e74c3c',  # Red
        'Opportunities': '#3498db',  # Blue
        'Threats': '#f39c12'  # Orange
    }

    # Add dashed lines to separate quadrants
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.7, linewidth=1)
    ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.7, linewidth=1)

    # Draw bubbles for each metric
    for category, metrics in swot_metrics.items():
        color = colors[category]
        for metric in metrics:
            # Calculate bubble size based on score
            bubble_size = metric['score'] / 25

            # Draw bubble
            bubble = plt.Circle((metric['x'], metric['y']),
                                bubble_size,
                                color=color,
                                alpha=0.7,
                                edgecolor='white',
                                linewidth=2)
            ax.add_patch(bubble)

            # Scale text size with score
            fontsize = 8 + metric['score'] * 5

            # Add text inside bubble (scaled font)
            ax.text(metric['x'], metric['y'], metric['text'],
                    ha='center', va='center',
                    fontsize=fontsize, fontweight='bold',
                    color='white', wrap=True)

    # Add quadrant Label (using a neutral color)
    ax.text(0.25, 0.95, 'STRENGTHS', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#2c3e50')
    ax.text(0.25, 0.05, 'WEAKNESSES', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#2c3e50')
    ax.text(0.75, 0.95, 'OPPORTUNITIES', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#2c3e50')
    ax.text(0.75, 0.05, 'THREATS', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#2c3e50')

    # Add quadrant descriptions (using a neutral color)
    ax.text(0.25, 0.9, 'Internal Positive Factors', ha='center', va='center',
            fontsize=10, style='italic', color='#2c3e50')
    ax.text(0.25, 0.1, 'Internal Negative Factors', ha='center', va='center',
            fontsize=10, style='italic', color='#2c3e50')
    ax.text(0.75, 0.9, 'External Positive Factors', ha='center', va='center',
            fontsize=10, style='italic', color='#2c3e50')
    ax.text(0.75, 0.1, 'External Negative Factors', ha='center', va='center',
            fontsize=10, style='italic', color='#2c3e50')

    # Add main title
    ax.text(0.5, 1.02, title + '\n(Bubble Size Represents Impact Level)',
            ha='center', va='bottom', fontsize=18, fontweight='bold',
            color='#2c3e50')

    # Set axis limits and remove ticks
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    return fig, ax
def create_swot_bubble_chart_1(swot_metrics):
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))

    # Set background color
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')

    # Color settings for each quadrant
    colors = {
        'Strengths': '#2ecc71',  # Green
        'Weaknesses': '#e74c3c',  # Red
        'Opportunities': '#3498db',  # Blue
        'Threats': '#f39c12'  # Orange
    }

    # Draw quadrant background
    ax.add_patch(plt.Rectangle((0, 0.5), 0.5, 0.5, color=colors['Strengths'], alpha=0.2))
    ax.add_patch(plt.Rectangle((0, 0), 0.5, 0.5, color=colors['Weaknesses'], alpha=0.2))
    ax.add_patch(plt.Rectangle((0.5, 0.5), 0.5, 0.5, color=colors['Opportunities'], alpha=0.2))
    ax.add_patch(plt.Rectangle((0.5, 0), 0.5, 0.5, color=colors['Threats'], alpha=0.2))

    # Draw bubbles for each metric
    for category, metrics in swot_metrics.items():
        color = colors[category]
        for metric in metrics:
            # Calculate bubble size based on score
            bubble_size = metric['score'] / 25

            # Draw bubble
            bubble = plt.Circle((metric['x'], metric['y']),
                                bubble_size,
                                color=color,
                                alpha=0.7,
                                edgecolor='white',
                                linewidth=2)
            ax.add_patch(bubble)

            # Scale text size with score
            fontsize = 8 + metric['score'] * 3

            # Add text inside bubble (scaled font)
            ax.text(metric['x'], metric['y'], metric['text'],
                    ha='center', va='center',
                    fontsize=fontsize, fontweight='bold',
                    color='white', wrap=True)

    # Add quadrant Label
    ax.text(0.25, 0.95, 'STRENGTHS', ha='center', va='center',
            fontsize=16, fontweight='bold', color=colors['Strengths'])
    ax.text(0.25, 0.05, 'WEAKNESSES', ha='center', va='center',
            fontsize=16, fontweight='bold', color=colors['Weaknesses'])
    ax.text(0.75, 0.95, 'OPPORTUNITIES', ha='center', va='center',
            fontsize=16, fontweight='bold', color=colors['Opportunities'])
    ax.text(0.75, 0.05, 'THREATS', ha='center', va='center',
            fontsize=16, fontweight='bold', color=colors['Threats'])

    # Add quadrant descriptions
    ax.text(0.25, 0.9, 'Internal Positive Factors', ha='center', va='center',
            fontsize=10, style='italic', color=colors['Strengths'])
    ax.text(0.25, 0.1, 'Internal Negative Factors', ha='center', va='center',
            fontsize=10, style='italic', color=colors['Weaknesses'])
    ax.text(0.75, 0.9, 'External Positive Factors', ha='center', va='center',
            fontsize=10, style='italic', color=colors['Opportunities'])
    ax.text(0.75, 0.1, 'External Negative Factors', ha='center', va='center',
            fontsize=10, style='italic', color=colors['Threats'])

    # Add main title
    ax.text(0.5, 1.02, 'SWOT Analysis: Autonomous Driving Technology in Park\n(Bubble Size Represents Impact Level)',
            ha='center', va='bottom', fontsize=18, fontweight='bold',
            color='#2c3e50')

    plt.tight_layout()
    return fig, ax


# Generate charts
if __name__ == "__main__":
    print("Generating SWOT Bubble Charts...")

    # SWOT data with scores (for bubble sizes) and positions
    swot_metrics_549 = {
        'Strengths': [
            {'text': 'Media coverage from\nauthoritative sources', 'score': 3, 'x': 0.15, 'y': 0.75},
            {'text': 'First-mover advantage\nin Central China', 'score': 2, 'x': 0.35, 'y': 0.65},
        ],
        'Weaknesses': [
            {'text': 'High technical\ntransformation costs', 'score': 2, 'x': 0.2, 'y': 0.25},
            {'text': 'Insufficient\noperational maintenance\ncapabilities', 'score': 2, 'x': 0.4, 'y': 0.2}
        ],
        'Opportunities': [
            {'text': 'Friendly laws and\nregulations', 'score': 3, 'x': 0.85, 'y': 0.75},
            {'text': 'Higher acceptance\namong younger\ntourists', 'score': 2, 'x': 0.7, 'y': 0.6}
        ],
        'Threats': [
            {'text': 'Emergence of\nsimilar competitive\nprojects', 'score': 2, 'x': 0.9, 'y': 0.25},
            {'text': 'Declining long-term\nattention', 'score': 2, 'x': 0.7, 'y': 0.3},
            {'text': 'Not considered\n core tourist\n attraction', 'score': 1, 'x': 0.6, 'y': 0.2}
        ]
    }

    swot_metrics_5001_Jackson = {
        'Strengths': [
            {'text': 'High Market Share\n in North America', 'score': 3, 'x': 0.15, 'y': 0.75},
            {'text': 'Partnership with \n the Red Cross', 'score': 2, 'x': 0.35, 'y': 0.65},
            {'text': 'FDA application\ncycle', 'score': 2, 'x': 0.35, 'y': 0.85},
        ],
        'Weaknesses': [
            {'text': 'Low Initial Payment', 'score': 2, 'x': 0.2, 'y': 0.25},
            {'text': 'Exclusive License\nfor North America', 'score': 2, 'x': 0.4, 'y': 0.2}
        ],
        'Opportunities': [
            {'text': 'Establish the\nindustry standard.', 'score': 3, 'x': 0.85, 'y': 0.75}
        ],
        'Threats': [
            {'text': 'Distribution\nmarket uncertainty', 'score': 2, 'x': 0.9, 'y': 0.25},
            {'text': 'Creating a\nFuture Competitor', 'score': 2, 'x': 0.7, 'y': 0.3},
        ]
    }

    swot_metrics_5001_hemaglobal = {
        'Strengths': [
            {'text': 'Large Market Share\nin Europe', 'score': 3, 'x': 0.15, 'y': 0.75},
            {'text': 'Actively Embraces\nInnovation', 'score': 1, 'x': 0.35, 'y': 0.65},
        ],
        'Weaknesses': [
            {'text': 'Exclusive Ownership of\nDerivative Technologies', 'score': 3, 'x': 0.2, 'y': 0.25},
            {'text': 'No Foundation\nin North American\nor Asian Markets', 'score': 2, 'x': 0.4, 'y': 0.2},
            {'text': 'Requests\na Shared License\nfor North America', 'score': 1, 'x': 0.4, 'y': 0.4},
        ],
        'Opportunities': [
            {'text': 'Jointly Develop\nthe Animal Blood\nSegment', 'score': 3, 'x': 0.85, 'y': 0.75}
        ],
        'Threats': [
            {'text': 'Disrupting\nNorth American\npartnership', 'score': 2, 'x': 0.8, 'y': 0.4},
            {'text': 'Creating a\nFuture Competitor', 'score': 1, 'x': 0.7, 'y': 0.3},
            {'text': 'Distribution\nmarket uncertainty', 'score': 3, 'x': 0.8, 'y': 0.15},
        ]
    }
    title_5001 = 'SWOT Analysis: Agreement with Hemaglobal'

    # Generate detailed bubble chart
    fig1, ax1 = create_swot_bubble_chart(swot_metrics_5001_hemaglobal, title=title_5001)
    plt.figure(fig1.number)
    print("Detailed SWOT bubble chart saved as 'swot_bubble_detailed.png'")

    # Display charts
    plt.savefig('data/output/swot.png')