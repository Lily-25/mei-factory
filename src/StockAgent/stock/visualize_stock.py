import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader.data as web
import datetime
import pandas as pd


def visualize_relation_between_interest_and_index():
    # 1. Create Date Range
    # Set date range
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=5*365)
    full_index = pd.date_range(start=start_date, end=end_date, freq='D')

    # Download data for major US indices

    df_Dow_Jones = yf.download('^DJI', start=start_date, end=end_date).reindex(full_index).ffill().reset_index()

    # Download Federal Funds Rate from FRED (use FRED's "FEDFUNDS")
    rate_US = web.DataReader('FEDFUNDS', 'fred', start_date, end_date)
    rate_US = rate_US.resample('D').ffill().dropna()
    rate_US = rate_US.reindex(full_index).ffill().reset_index()


    # 4. Create DataFrames
    us_data = pd.DataFrame({
        'Date': df_Dow_Jones['index'],
        'US Interest Rate (%)': rate_US.FEDFUNDS,
        'Dow Jones Index': df_Dow_Jones.Close['^DJI']
    })

    # Download data for major US indices

    df_CSI_300 = yf.download('000300.SS', start=start_date, end=end_date).reindex(full_index).ffill().reset_index()

    # Download Federal Funds Rate from FRED (use FRED's "FEDFUNDS")
    rate_China = web.DataReader('IRSTCI01CNM156N', 'fred', start_date, end_date)
    rate_China = rate_China.resample('D').ffill().dropna()
    rate_China = rate_China.reindex(full_index).ffill().reset_index()

    china_data = pd.DataFrame({
        'Date': df_CSI_300['index'],
        'China Interest Rate (LPR, %)': rate_China.IRSTCI01CNM156N,
        'CSI 300 Index': df_CSI_300.Close['000300.SS']
    })

    # 5. Plot Combined Chart
    fig, ax1 = plt.subplots(figsize=(14, 7))
    ax1.set_title("Interest Rates and Stock Indices: USA vs China (2020–2025)", fontsize=15)

    # Interest Rates (left y-axis)
    ax1.plot(us_data['Date'], us_data['US Interest Rate (%)'], color='red', linestyle='--', label='US Interest Rate (%)')
    ax1.plot(china_data['Date'], china_data['China Interest Rate (LPR, %)'], color='green', linestyle='--', label='China LPR (%)')
    ax1.set_ylabel('Interest Rate (%)')
    ax1.tick_params(axis='y')

    # Stock Indices (right y-axis)
    ax2 = ax1.twinx()
    ax2.plot(us_data['Date'], us_data['Dow Jones Index'], color='blue', label='Dow Jones Index (US)')
    ax2.plot(china_data['Date'], china_data['CSI 300 Index'], color='purple', label='CSI 300 Index (China)')
    ax2.set_ylabel('Stock Index Level')
    ax2.tick_params(axis='y')

    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    # Grid and layout
    ax1.grid(True)
    fig.tight_layout()
    plt.show()

    return plt