import os
from datetime import datetime

import akshare as ak
import pandas as pd

from src.StockAgent.utils.operate_files import create_directory
from src.StockAgent.common.abstract_define import BasicManager


class DataSourceEM(BasicManager):

    def __init__(self):
        super().__init__()
        self.hist_price_dir = self.dir + 'stock_org_data/hist_price_em/'
        self.hist_fund_flow_dir = self.dir + 'stock_org_data/hist_fund_flow_em/'

        self.refresh_config()

    def refresh_config(self):
        self.basic_config_mgt.insert('stock.hist_price_dir',os.path.abspath(self.hist_price_dir) + '/')
        self.basic_config_mgt.insert('stock.hist_fund_flow_dir',
                                  os.path.abspath(self.hist_fund_flow_dir) + '/')


    def crawl_history_price_by_daily(self, symbol_index):
        """
        from 新浪财经
        "stock_zh_a_daily"  # A 股历史行情数据(日频)
        "stock_zh_a_minute"  # A 股分时历史行情数据(分钟)
        :return:
        """

        create_directory(self.hist_price_dir)
        try:
            start_date = "20250101"
            end_date = datetime.now().strftime('%Y%m%d')

            file_name = self.hist_price_dir + symbol_index + '.csv'

            exist_df = pd.DataFrame()
            if os.path.exists(file_name):
                exist_df = pd.read_csv(file_name, index_col=0)
                start_date = datetime.strptime(exist_df.index[-1], '%Y-%m-%d').strftime('%Y%m%d')

            stock_zh_a_daily_df = ak.stock_zh_a_daily(
                symbol=self.get_stock_market_abbreviation(symbol_index) + symbol_index,
                start_date=start_date,
                end_date=end_date,
                adjust="qfq").set_index('date')
            stock_zh_a_daily_df = stock_zh_a_daily_df.loc[:,
                                              ~stock_zh_a_daily_df.columns.str.contains('^Unnamed')]

            # 此接口中没有PriceCA
            stock_zh_a_daily_df['PriceCA'] = stock_zh_a_daily_df['close'] - stock_zh_a_daily_df['open']

            if not exist_df.empty:
                stock_zh_a_daily_df = exist_df.iloc[:-1].combine_first(stock_zh_a_daily_df)

            stock_zh_a_daily_df.to_csv(file_name)

        except Exception as e:
            print(e)
            pass

    def batch_crawl_history_price_by_daily(self):

        for symbol_index in self.stock_observation_dict.keys():
            print(f'{symbol_index} : {self.stock_observation_dict[symbol_index]}')
            self.crawl_history_price_by_daily(symbol_index)


    def crawl_history_data_by_min(self, symbol_index, period='1'):
        """
        新浪数据
        """
        try:
            stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol=symbol_index,
                                                            period=period,

                                                            adjust="qfq")
            stock_zh_a_minute_df.to_csv(self.dir +
                                            f'stock_zh_a_minute_{datetime.now()}.csv')

        except:
            pass

    def crawl_history_fund_flow(self):

        create_directory(self.hist_fund_flow_dir)

        for symbol_index in self.stock_observation_dict.keys():
            try:
                file_name = self.hist_fund_flow_dir + f'{symbol_index}.csv'
                market = self.get_stock_market_abbreviation(symbol_index)
                stock_individual_fund_flow_df = ak.stock_individual_fund_flow(stock=symbol_index,
                                                                              market=market).set_index('日期')
                stock_individual_fund_flow_df = stock_individual_fund_flow_df.loc[:,
                                      ~stock_individual_fund_flow_df.columns.str.contains('^Unnamed')]

                if os.path.exists(file_name):
                    exist_df = pd.read_csv(file_name, index_col=0)
                    exist_df.index = pd.to_datetime(exist_df.index)
                    stock_individual_fund_flow_df.index = pd.to_datetime(stock_individual_fund_flow_df.index)

                    stock_individual_fund_flow_df = pd.concat([
                        exist_df.iloc[:-1],
                        stock_individual_fund_flow_df
                    ]).groupby(level=0).last()

                stock_individual_fund_flow_df.to_csv(file_name)

            except Exception as e:
                print(e)
                pass


    def crawl_realtime_data(self):
        try:
            stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
            stock_zh_a_spot_em_df.to_csv(self.dir + f'stock_zh_a_spot_em_'
                                       + datetime.now().strftime('%y-%m-%d-%H-%M')
                                       + '.csv')
        except:
            pass

    def refresh_stock_raw_data(self):

        """
        According to the stock list that I hold to refresh the raw data
        :return:
        """

        self.batch_crawl_history_price_by_daily()
        self.crawl_history_fund_flow()


    def refresh_stock_observation_pool(self):

        """
        According to the strategies such as low-cost boards to search high-value stocks, combining the stocks I hold and
        the potential stocks recommended by these strategies to refresh the raw data
        :return:
        """

        df = pd.DataFrame([])
        for symbol in self.basic_config['sector']['low_cost_board_list']:
            if df.empty:
                df = ak.stock_board_industry_cons_em(symbol=symbol)
            else:
                df = pd.concat([df, ak.stock_board_industry_cons_em(symbol=symbol)])

        create_directory(self.dir + 'stock_org_data/')
        df.to_csv(self.dir + 'stock_org_data/stock_pool.csv', index=False)

        self.stock_observation_dict = self.stock_observation_dict | dict(zip(df['代码'], df['名称']))

        self.basic_config_mgt.insert("stock.stock_observation_dict", self.stock_observation_dict)

        self.batch_crawl_history_price_by_daily()

        self.crawl_history_fund_flow()

if __name__ == '__main__':
    obj_stock = DataSourceEM()
    # absolute_timer(1, obj_etf.crawl_realtime_data)

    obj_stock.refresh_stock_observation_pool()
