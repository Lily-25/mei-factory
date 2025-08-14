import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import mplcursors
from sympy.physics.control.control_plots import matplotlib

from src.StockAgent.sector.model_data import IndicatorMonitor


class DashBoard(IndicatorMonitor):
    def __init__(self):
        super().__init__([])

    def visualize_sector_spot(self):

        sector_df = (pd.read_csv(self.indicator_signal_dir + 'overview.csv').
                     sort_values(by='FundFlowMNI',ascending=False))

        sector_df = pd.concat([sector_df.head(30),sector_df.tail(30)])

        sectors = sector_df['symbol']
        price_fluctuations = sector_df['PriceCR'] # in percentage
        mni_amount = sector_df['FundFlowMNI']

        x = np.arange(len(sectors))
        # Create figure and primary axis
        fig, ax1 = plt.subplots(figsize=(16, 6))

        # Plot price fluctuations on primary Y-axis
        bar1 = ax1.bar(x - 0.2, mni_amount, width=0.4, label='Main Net Fund inFlow', color='orange')
        ax1.set_xticks(x)
        ax1.set_xticklabels(sectors, rotation=45, ha='right')  # rotate for readability
        ax1.set_xlabel('头尾部板块')

        # Create secondary Y-axis
        ax2 = ax1.twinx()
        bar2 = ax2.bar(x + 0.2, price_fluctuations, width=0.4, label='Price Change Ratio (%)', color='skyblue')
        ax2.set_ylabel('Price Change Ratio', color='skyblue')
        ax2.tick_params(axis='y', labelcolor='orange')

        # Add legends
        fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

        # Add title
        plt.title('The relationship between the MNI and PriceCR')

        # Show plot
        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_sector_fund_flow(filename):

        sector_df = pd.read_csv(filename)

        # Make sure your sector_df['日期'] is datetime type:
        # sector_df = sector_df.copy()
        sector_df['Date_num'] = mdates.date2num(sector_df['Date'])

        fig, ax1 = plt.subplots(figsize=(14, 7))
        ax1.set_title("Analysis the relationship between main funds flow and stock price", fontsize=15)

        # Plot main funds data (left y-axis)
        line1, = ax1.plot(sector_df['Date_num'], sector_df['FundFlowMNI'] / 100000000,
                          color='green', linestyle='--', label='main funds flow')

        valid_mask = sector_df['FundFlowMNI5DMA'].notna()
        line2, = ax1.plot(sector_df.loc[valid_mask, 'Date_num'],
                 sector_df.loc[valid_mask, 'FundFlowMNI5DMA'] / 100000000,
                          color='blue', linestyle='--', label='Mean-Funds-5 Days')

        valid_mask = sector_df['FundFlowMNI10DMA'].notna()
        line3, = ax1.plot(sector_df.loc[valid_mask, 'Date_num'],
                 sector_df.loc[valid_mask, 'FundFlowMNI10DMA'] / 100000000,
                          color='red', linestyle='--', label='Mean-Funds-10 Days')
        """
        line2, = ax1.plot(sector_df['日期_num'], sector_df['Mean-Funds-5 Days-Main'] / 100000000,
                          color='blue', linestyle='--', label='Mean-Funds-5 Days')

        line3, = ax1.plot(sector_df['日期_num'], sector_df['Total-Funds-5 Days-Main'] / 100000000,
                          color='red', linestyle='--', label='Total-Funds-5 Days')
        
        """

        ax1.set_ylabel('main funds flow')
        ax1.tick_params(axis='y')

        # Plot stock income data (right y-axis)
        ax2 = ax1.twinx()
        line4, = ax2.plot(sector_df['Date_num'], sector_df['Close'],
                          color='purple', label='stock price')
        ax2.set_ylabel('stock income')
        ax2.tick_params(axis='y')

        # Set x-axis format
        # ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

        # Combine all lines and labels manually
        all_lines = [line1, line2, line3, line4]
        all_labels = [line.get_label() for line in all_lines]

        # Use ax1 to draw the legend, even for lines from ax2
        legend = ax2.legend(all_lines, all_labels, loc='upper right')

        # Make legend items interactive
        lined = {legline: origline for legline, origline in zip(legend.get_lines(), all_lines)}
        for legline in legend.get_lines():
            legline.set_picker(True)
            legline.set_pickradius(5)

        # Pick event: toggle line visibility (ignore picks on text annotations)
        def on_pick(event):
            legline = event.artist
            if not isinstance(legline, Line2D):
                return  # Ignore picks that are not legend lines

            origline = lined.get(legline)
            if origline is None:
                return

            visible = not origline.get_visible()
            origline.set_visible(visible)
            legline.set_alpha(1.0 if visible else 0.2)
            fig.canvas.draw()

        fig.canvas.mpl_connect('pick_event', on_pick)

        # Add interactive cursor tooltips
        cursor = mplcursors.cursor(all_lines, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            x, y = sel.target
            date_str = mdates.num2date(x).strftime('%Y-%m-%d')
            sel.annotation.set_text(f"Date: {date_str}\nValue: {y:.2f}")

        # Final layout
        ax1.grid(True)
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

        return plt

        # create_directory(self.dashboard)
        # plt.savefig(self.dashboard + 'Analysis the relationship between main funds flow and stock price')


if __name__ == '__main__':
    # Set font to a Chinese-supported one (e.g., PingFang SC)
    matplotlib.rcParams['font.family'] = 'Songti SC'

    # Fix potential minus sign rendering issue
    matplotlib.rcParams['axes.unicode_minus'] = False

    obj_sector = DashBoard()
    # obj_sector.visualize_sector_spot()
    obj_sector.visualize_sector_fund_flow(obj_sector.schema_config['sector']['price_and_fund_merger_dir'] + '半导体.csv')