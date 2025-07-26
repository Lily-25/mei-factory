import os
import pandas as pd
import mplfinance as mpf

from src.StockAgent.common.abstract_define import BasicManager


class DashboardManager(BasicManager):
    def __init__(self):
        super().__init__()
        self.dashboard_dir = self.dir + 'dashboard/'

        self.refresh_config()

    def refresh_config(self):
        self.basic_config_mgt.insert('etf.dashboard_dir',
                                     os.path.abspath(self.dashboard_dir) + '/')

    def draw_candle_chart(self,symbol_index):

        file_name = self.basic_config['etf']['hist_price_dir'] + f'{symbol_index}.csv'
        df = pd.read_csv(file_name, index_col=0, parse_dates=True)
        df.columns = ['Open', 'Close', 'High', 'Low', 'Volume','Amount','Amplitude','outstanding_rate','outstanding_share','turnover']
        mpf.plot(df, type='candle', style='charles', volume=True, title=f'ETF {symbol_index} Price', mav=(5, 10))

if __name__ == '__main__':
    obj = DashboardManager()
    obj.draw_candle_chart('562500')