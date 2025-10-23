import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 定义事件数据
events = [
    {
        'time': datetime(2025, 9, 18, 0, 30),
        'title': 'Took Technological Operation',
        'description': 'Firewall upgrade initiated'
    },
    {
        'time': datetime(2025, 9, 18, 0, 35),
        'title': 'Triggered Outage',
        'description': 'Failure period start'
    },
    {
        'time': datetime(2025, 9, 18, 9, 0),
        'title': 'Initial Issue Reports',
        'description': 'Customers discovered this issue'
    },
    {
        'time': datetime(2025, 9, 18, 13, 30),
        'title': 'Realized by Optus',
        'description': 'Optus officially realized the outage'
    },
    {
        'time': datetime(2025, 9, 18, 13, 50),
        'title': 'Took measure to fix the outage',
        'description': 'Optus stopped the upgrade and reverted the firewall changes'
    },
    {
        'time': datetime(2025, 9, 18, 18, 0),
        'title': ' Investigated impacts',
        'description': ''
    }
]

# 标记中断期间
outage_start = datetime(2025, 9, 18, 00, 35)
outage_end = datetime(2025, 9, 18, 13, 50)

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(14, 6))

# 设置时间范围
start_time = datetime(2025, 9, 17, 23, 0)
end_time = datetime(2025, 9, 18, 19, 30)

# 绘制时间线
ax.axhline(y=0, color='black', linewidth=2, alpha=0.7)

# 绘制事件点
y_positions = [0.6, -0.3, 0.3, -0.6, 0.6, -0.3]  # 垂直位置，避免重叠

for i, event in enumerate(events):
    # 绘制时间点
    ax.plot(event['time'], 0, 'o', color='red', markersize=8, alpha=0.7)

    # 绘制垂直线
    ax.vlines(x=event['time'], ymin=0, ymax=y_positions[i], color='gray', linestyle='--', alpha=0.7)

    # 添加事件文本
    ax.text(event['time'], y_positions[i],
            f"{event['title']}\n{event['description']}\n{event['time'].strftime('%H:%M %d %b')}",
            fontsize=10, ha='center', va='bottom' if y_positions[i] > 0 else 'top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='none', alpha=0.7),
            fontweight='bold')

#
ax.axvspan(outage_start, outage_end, alpha=0.2, color='red', label='The period of interruption ')

# 设置坐标轴
ax.set_xlim(start_time, end_time)
ax.set_ylim(-1.5, 1.5)
ax.set_yticks([])
ax.set_xlabel('Time', fontsize=12, fontweight='bold')
ax.set_title('Optus Outage Time Line', fontsize=16, fontweight='bold', pad=20)

# 格式化x轴
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%d %b'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
plt.xticks(rotation=45)

# 添加网格
ax.grid(True, alpha=0.3)

# 添加图例
ax.legend(loc='upper right')

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()

# 可选：保存图片
# plt.savefig('optus_outage_timeline.png', dpi=300, bbox_inches='tight')