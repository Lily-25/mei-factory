import streamlit as st
import pandas as pd
import time
import numpy as np

from sympy.physics.control.control_plots import matplotlib

from src.StockAgent.sector.visualize_sector import DashBoard as sector_DashBoard

from src.StockAgent.task.offline_task import (discover_low_cost_sector,
                                              discover_low_cost_stocks,
                                              discover_hot_spot_stocks)

from src.StockAgent.utils.manage_config import ConfigManager

g_schema_config = ConfigManager('../config/schema_config.yaml').config

st.set_page_config(page_title='📊 Financial Tool Demo', layout='wide')
st.title('📊 Financial Tool Dashboard')

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

def visualize_fund_flow_by_sector():
    # Set font to a Chinese-supported one (e.g., PingFang SC)
    matplotlib.rcParams['font.family'] = 'Songti SC'

    # Fix potential minus sign rendering issue
    matplotlib.rcParams['axes.unicode_minus'] = False

    obj_sector = sector_DashBoard()

    # This assumes visualize_sector_spot() plots on the current matplotlib figure
    fig = obj_sector.visualize_sector_spot()

    return fig

def visualize_sector_fund_flow_relationship(symbol):
    obj_sector = sector_DashBoard()
    return  obj_sector.visualize_sector_fund_flow(obj_sector.schema_config['sector']['price_and_fund_merger_dir']
                                                  + f'{symbol}.csv')

# ----------------- Streamlit App -----------------
# Sidebar - analysis selection
st.sidebar.header('Main Boards Comparison')
selected_task = st.sidebar.selectbox(
    'Choose an task',
    ['None'] + list(DATA_SOURCES['sector focus']()['sector name'])
)

st.subheader(f'📄 {selected_task} (main board chart)')

if selected_task != 'None':
    log_area = st.empty()  # placeholder for logs
    fig = visualize_sector_fund_flow_relationship(selected_task)
    st.pyplot(fig)


# -----------------------------
# 2. Analytical Tasks
# -----------------------------
def run_analysis(task):
    """Simulate analytical tasks and log steps."""
    log_area.write(f'▶ Starting task: **{task}**')
    time.sleep(0.5)

    result = None
    if task == 'Discover low-cost sectors':
        log_area.write('📊 Start discovering low-cost sectors...')
        time.sleep(0.5)
        df = discover_low_cost_sector()
        log_area.write('📊 Complete discovering low-cost sectors...')
        result = df
    elif task == 'Discover low-cost stocks':
        log_area.write('📊 Start discovering low-cost stocks...')
        time.sleep(0.5)
        df = discover_low_cost_stocks()
        log_area.write('📊 Start Complete low-cost stocks...')
        result = df
    elif task == 'Discover hot-spot stocks':
        log_area.write('📊 Start discovering hot-spot stocks...')
        time.sleep(0.5)
        df = discover_hot_spot_stocks()
        log_area.write('📊 Start Complete hot-spot stocks...')
        result = df
    else:
        log_area.write('⚠ Unknown task selected.')

    log_area.write('✅ Task completed.')
    return result


# Sidebar - analysis selection
st.sidebar.header('Analytical Tasks')
selected_analysis = st.sidebar.selectbox(
    'Choose an analysis',
    ['None', 'Discover low-cost sectors', 'Discover low-cost stocks', 'Discover hot-spot stocks']
)

# Analysis Output + Log
st.subheader('🛠 Analytical Task Output')

col1, col2 = st.columns([2, 1])
with col1:
    if selected_analysis != 'None':
        log_area = st.empty()  # placeholder for logs
        result = run_analysis(selected_analysis)
        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        elif result is not None:
            st.write(result)
    else:
        st.info('Select a task from the menu to run analysis.')

with col2:
    st.markdown('### 📜 Log Window')
    st.info('Logs will appear here as tasks run.')
