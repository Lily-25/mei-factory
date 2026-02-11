import pandas as pd
import numpy as np

# 模拟 BYD 和 Nissan 全球销量数据（2024年）
data = {
    'country': ['China', 'United States', 'Japan', 'Germany', 'Brazil', 'Thailand',
                'Australia', 'United Kingdom', 'France', 'India', 'Mexico', 'South Korea',
                'Canada', 'Spain', 'Italy', 'Netherlands', 'Norway', 'Sweden'],
    'iso_code': ['CHN', 'USA', 'JPN', 'DEU', 'BRA', 'THA', 'AUS', 'GBR', 'FRA', 'IND',
                 'MEX', 'KOR', 'CAN', 'ESP', 'ITA', 'NLD', 'NOR', 'SWE'],
    'byd_sales': [2100000, 350000, 0, 80000, 85000, 68000, 45000, 40000, 35000, 30000,
                  28000, 25000, 22000, 18000, 15000, 12000, 10000, 8000],
    'nissan_sales': [50000, 600000, 450000, 120000, 180000, 40000, 80000, 70000, 65000, 150000,
                     140000, 200000, 90000, 55000, 50000, 30000, 25000, 45000]
}

df = pd.DataFrame(data)
print(df.head())

import plotly.express as px

# 将数据转换为长格式（适合叠加）
df_long = pd.melt(
    df,
    id_vars=['country', 'iso_code'],
    value_vars=['byd_sales', 'nissan_sales'],
    var_name='brand',
    value_name='sales'
)

# 替换列名便于显示
df_long['brand'] = df_long['brand'].replace({
    'byd_sales': 'BYD',
    'nissan_sales': 'Nissan'
})

# 创建气泡地图
fig = px.scatter_geo(
    df_long,
    locations='iso_code',
    size='sales',
    color='brand',
    hover_name='country',
    hover_data={'sales': ':,', 'brand': True},
    projection='natural earth',
    size_max=60,
    color_discrete_map={'BYD': '#2E86AB', 'Nissan': '#A23B72'},
    title='BYD vs Nissan: Global Sales Bubble Map 2024'
)

fig.update_layout(
    title_x=0.5,
    title_font_size=22,
    legend_title_text='Brand',
    margin=dict(l=0, r=0, t=60, b=0),
    geo=dict(showcoastlines=True, coastlinecolor='gray')
)

fig.show()
fig.write_html('byd_vs_nissan_bubble.html')