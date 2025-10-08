import streamlit as st
import pandas as pd
import time
import numpy as np

from sympy.physics.control.control_plots import matplotlib

from offline_task import discover_holding_stocks
from src.StockAgent.sector.visualize_sector import DashBoard as sector_DashBoard

from src.StockAgent.task.offline_task import (discover_low_cost_sector,
                                              discover_low_cost_stocks,
                                              discover_hot_spot_stocks,
                                              discover_hot_spot_etfs)

from src.StockAgent.stock.visualize_stock import visualize_relation_between_interest_and_index

from src.StockAgent.utils.manage_config import ConfigManager

g_schema_config = ConfigManager('../config/schema_config.yaml').config

st.set_page_config(page_title='📊 Financial Tool Demo', layout='wide')
st.title('📊 Financial Tool Dashboard')

"""
Section 1: Display recommend products
"""

def load_sector_overview_data():
    sector_df = None
    try:
        sector_df = pd.read_csv(g_schema_config['sector']['indicator_signal_dir']
                       + 'overview.csv')
        sector_df = sector_df.loc[:,
                              ~sector_df.columns.str.contains('^Unnamed')]
    except Exception as e:
        print(f'load_sector_overview_data failed {e}')

    return sector_df

def load_sector_focus_data():
    name_list = ['hot_spot'] * len(g_schema_config['sector']['sector_focus_list']['hot_spot'])
    value_list = g_schema_config['sector']['sector_focus_list']['hot_spot']

    name_list = name_list + ['low_cost'] * len(g_schema_config['sector']['sector_focus_list']['low_cost'])
    value_list = value_list + g_schema_config['sector']['sector_focus_list']['low_cost']

    sector_df = pd.DataFrame({ 'type': name_list,
                               'sector name':value_list})

    return sector_df

def load_stock_overview_data():
    stock_df = None
    try:
        stock_df = pd.read_csv(g_schema_config['stock']['indicator_signal_dir']
                       + 'hot_spot.csv')
        stock_df = stock_df.loc[:,
                    ~stock_df.columns.str.contains('^Unnamed')]
    except Exception as e:
        print(f'load_stock_overview_data failed {e}')

    return stock_df

def load_hot_spot_stock_recommendation_data():
    stock_df = None
    try:
        stock_df = pd.read_csv(g_schema_config['stock']['recommend_stock_dir']
                       + 'hot_spot.csv')
        stock_df = stock_df.loc[:,
                    ~stock_df.columns.str.contains('^Unnamed')]
    except Exception as e:
        print(f'load_hot_spot_stock_recommendation_data failed {e}')

    return stock_df

def load_low_cost_stock_recommendation_data():
    stock_df = None
    try:
        stock_df = pd.read_csv(g_schema_config['stock']['recommend_stock_dir']
                       + 'low_cost.csv')
        stock_df = stock_df.loc[:,
                    ~stock_df.columns.str.contains('^Unnamed')]
    except Exception as e:
        print(f'load_low_cost_stock_recommendation_data failed {e}')

    return stock_df

def load_holding_stock_recommendation_data():
    stock_df = None
    try:
        stock_df = pd.read_csv(g_schema_config['stock']['recommend_stock_dir']
                       + 'holding.csv')
        stock_df = stock_df.loc[:,
                    ~stock_df.columns.str.contains('^Unnamed')]
    except Exception as e:
        print(f'load_holding_stock_recommendation_data failed {e}')

    return stock_df

def load_etf_overview_data():
    etf_df = None
    try:
        etf_df = pd.read_csv(g_schema_config['etf']['indicator_signal_dir']
                       + 'overview.csv')
        etf_df = etf_df.loc[:,
                    ~etf_df.columns.str.contains('^Unnamed')]
    except Exception as e:
        print(f'load_stock_overview_data failed {e}')

    return etf_df

def load_etf_recommendation_data():
    etf_df = None
    try:
        etf_df = pd.read_csv(g_schema_config['etf']['recommend_etf_dir']
                       + 'hot_spot.csv')
        etf_df = etf_df.loc[:,
                    ~etf_df.columns.str.contains('^Unnamed')]
    except Exception as e:
        print(f'load_etf_recommendation_data failed {e}')

    return etf_df

DATA_SOURCES = {

    'sector focus': load_sector_focus_data,
    'hot_spot_stock_recommendation': load_hot_spot_stock_recommendation_data,
    'low_cost_stock_recommendation': load_low_cost_stock_recommendation_data,
    'etf recommendation': load_etf_recommendation_data,
    'holding_stock_recommendation': load_holding_stock_recommendation_data,
    'etf overview': load_etf_overview_data,
    'stock overview': load_stock_overview_data,
    'sector overview': load_sector_overview_data,
}

# Sidebar - dataset selection
st.sidebar.header('Data Source')
selected_table = st.sidebar.selectbox('Choose a dataset', list(DATA_SOURCES.keys()))

# Load dataset
df = DATA_SOURCES[selected_table]()

st.sidebar.header('Filters')
with st.sidebar.expander('Show Filters', expanded=False):
    filtered_df = df.copy()
    for col in df.columns:
        col_data = df[col].replace([np.inf, -np.inf], np.nan).dropna()

        # Numeric columns
        if pd.api.types.is_numeric_dtype(col_data):
            if not col_data.empty:
                min_val = float(col_data.min())
                max_val = float(col_data.max())
                if min_val == max_val:
                    continue
                selected_range = st.slider(
                    f'{col} range',
                    min_val,
                    max_val,
                    (min_val, max_val),
                    key=f'filter_{col}'
                )
                filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[1])]
            else:
                st.write(f'{col}: No numeric data available')

        # Datetime columns
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            if not col_data.empty:
                min_date = col_data.min()
                max_date = col_data.max()
                if min_date == max_date:
                    continue
                selected_date = st.date_input(
                    f'{col} range',
                    [min_date, max_date],
                    key=f'filter_{col}'
                )
                if len(selected_date) == 2:
                    filtered_df = filtered_df[
                        (df[col] >= pd.to_datetime(selected_date[0])) &
                        (df[col] <= pd.to_datetime(selected_date[1]))
                    ]
            else:
                st.write(f'{col}: No date data available')

        # Categorical/Text columns
        else:
            unique_vals = sorted(col_data.unique().tolist())
            if unique_vals:
                selected_vals = st.multiselect(
                    f'Select {col}',
                    unique_vals,
                    default=unique_vals,
                    key=f'filter_{col}'
                )
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
            else:
                st.write(f'{col}: No categorical data available')

# Show filtered table
st.subheader(f'📄 {selected_table} (Filtered)')
st.dataframe(filtered_df)

"""
Section 2: visualize key indicators
"""

def visualize_fund_flow_by_sector():
    # Set font to a Chinese-supported one (e.g., PingFang SC)
    matplotlib.rcParams['font.family'] = 'Songti SC'

    # Fix potential minus sign rendering issue
    matplotlib.rcParams['axes.unicode_minus'] = False

    obj_sector = sector_DashBoard()

    # This assumes visualize_sector_spot() plots on the current matplotlib figure
    return obj_sector.visualize_sector_spot()

def visualize_sector_fund_flow_relationship(symbol):
    obj_sector = sector_DashBoard()
    return  obj_sector.visualize_sector_fund_flow(obj_sector.schema_config['sector']['price_and_fund_merger_dir']
                                                  + f'{symbol}.csv')

# Sidebar - analysis selection
st.sidebar.header('Main Index Chart')
selected_main_index = st.sidebar.selectbox(
    'Choose an index',
    ['None', 'Overview'])

# 分析输出区域
st.subheader(f'📄 The relationship between interest and index  (Index Name : {selected_main_index})')

if selected_main_index != 'None':
    log_area = st.empty()  # placeholder for logs
    if selected_main_index == 'Overview':
        fig = visualize_relation_between_interest_and_index()
        st.pyplot(fig)


# ----------------- Streamlit App -----------------
# Sidebar - analysis selection
st.sidebar.header('Main Board Chart')
selected_task = st.sidebar.selectbox(
    'Choose an task',
    ['None', 'Overview',] + list(DATA_SOURCES['sector focus']()['sector name'])
)

# 分析输出区域
st.subheader(f'📄 The relationship between Fund Flow and Price  (Board Name : {selected_task})')

if selected_task != 'None':
    log_area = st.empty()  # placeholder for logs
    if selected_task == 'Overview':
        fig = visualize_fund_flow_by_sector()
    else:
        fig = visualize_sector_fund_flow_relationship(selected_task)
    st.pyplot(fig)

# -----------------------------
# 3. Analytical Tasks
# -----------------------------
# Sidebar - analysis selection
st.sidebar.header('Analytical Tasks')
selected_analysis = st.sidebar.selectbox(
    'Choose an analysis',
    ['None', 'Do the whole offline task', 'Do stock recommendation task']
)

if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []

def run_analysis(task):
    """Simulate analytical tasks and log steps."""

    st.session_state.log_messages.append(f'▶ Starting task: **{task}**')
    log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
    time.sleep(0.5)

    result = None
    if task == 'Do the whole offline task':

        st.session_state.log_messages.append('📊 Start discover_low_cost_sector...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        discover_low_cost_sector()

        st.session_state.log_messages.append('📊 Complete discover_low_cost_sector...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        st.session_state.log_messages.append('📊 Start discover_low_cost_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        discover_low_cost_stocks(refresh_data_flag=True)

        st.session_state.log_messages.append('📊 Complete discover_low_cost_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        st.session_state.log_messages.append('📊 Start discover_hot_spot_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        discover_hot_spot_stocks(refresh_data_flag=True)

        st.session_state.log_messages.append('📊 Complete discover_hot_spot_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        st.session_state.log_messages.append('📊 Start discover_hot_spot_etfs...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        discover_hot_spot_etfs(refresh_data_flag=True)

        st.session_state.log_messages.append('📊 Complete discover_hot_spot_etfs...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        st.session_state.log_messages.append('✅ Task completed.')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
    elif task == 'Do stock recommendation task':
        st.session_state.log_messages.append('📊 Start discover_holding_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        discover_holding_stocks()

        st.session_state.log_messages.append('📊 Complete discover_holding_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        st.session_state.log_messages.append('📊 Start discover_low_cost_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        discover_low_cost_stocks()

        st.session_state.log_messages.append('📊 Complete discover_low_cost_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        st.session_state.log_messages.append('📊 Start discover_hot_spot_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        discover_hot_spot_stocks()

        st.session_state.log_messages.append('📊 Complete discover_hot_spot_stocks...')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
        time.sleep(0.5)

        st.session_state.log_messages.append('✅ Task completed.')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)
    else:
        st.session_state.log_messages.append(f'⚠ Warning: unknown task **{task}** selected.')
        log_area.text_area("Log Output", "\n".join(st.session_state.log_messages), height=300)

    return result

# 添加执行按钮
run_button = st.sidebar.button('Run Analysis')

# 分析输出区域
st.subheader('🛠 Analytical Task Output')

if run_button and selected_analysis != 'None':
    log_area = st.empty()
    run_analysis(selected_analysis)
    # 自动重置选择
    selected_analysis = 'None'
    st.rerun()  # 触发页面重新渲染
elif selected_analysis == 'None':
    st.info('Select a task from the menu to run analysis.')


