import os
import time
from datetime import datetime

import akshare as ak
import pandas as pd

from src.StockAgent.common.abstract_schema_define import SchemaManager
from src.StockAgent.utils.customize_timer import get_date_tag
from src.StockAgent.utils.operate_files import create_directory, check_whether_files_created_today


class DataSourceEM(SchemaManager):

    def __init__(self):
        super().__init__()
        self.hist_price_dir = self.dir + 'stock_org_data/hist_price_em/'
        self.hist_fund_flow_dir = self.dir + 'stock_org_data/hist_fund_flow_em/'

        self.refresh_config()

    def refresh_config(self):
        self.schema_config_mgt.insert('stock.hist_price_dir',os.path.abspath(self.hist_price_dir) + '/')
        self.schema_config_mgt.insert('stock.hist_fund_flow_dir',
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

            # this action just do onetime per day
            if check_whether_files_created_today(file_name):
                print(f'crawl_history_price_by_daily {file_name} has been updated today')
                return

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

            print(f'crawl_history_price_by_daily report an Exception: {e}')

            pass

    def batch_crawl_history_price_by_daily(self):

        print('enter batch_crawl_history_price_by_daily')

        batch_count = 0
        for symbol_index in self.stock_current_observation_pool_dict.keys():
            print(f'batch_crawl_history_price_by_daily - {symbol_index} : {self.stock_current_observation_pool_dict[symbol_index]}')
            self.crawl_history_price_by_daily(symbol_index)

            batch_count = batch_count + 1
            if batch_count >= self.schema_config['global']['batch_crawl']['size']:
                time.sleep(self.schema_config['global']['batch_crawl']['break_time'])
                batch_count = 0


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

        except Exception as e:
            print(f'crawl_history_data_by_min report an Exception: {e}')
            pass

    def crawl_history_fund_flow(self, symbol_index):

        try:
            file_name = self.hist_fund_flow_dir + f'{symbol_index}.csv'

            # this action just do onetime per day
            if check_whether_files_created_today(file_name):
                print(f'crawl_history_fund_flow {file_name} has been updated today')
                return

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
            print(f'crawl_history_fund_flow report an Exception: {e}')
            pass

    def batch_crawl_history_fund_flow(self):

        create_directory(self.hist_fund_flow_dir)

        for symbol_index in self.stock_current_observation_pool_dict.keys():
            print(f'batch_crawl_history_fund_flow - {symbol_index} : {self.stock_current_observation_pool_dict[symbol_index]}')
            self.crawl_history_fund_flow(symbol_index)


    def crawl_realtime_data(self):
        try:
            stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
            stock_zh_a_spot_em_df.to_csv(self.dir + f'stock_zh_a_spot_em_'
                                       + datetime.now().strftime('%y-%m-%d-%H-%M')
                                       + '.csv')
        except Exception as e:
            print(f'crawl_realtime_data report an Exception: {e}')
            pass

    def refresh_stock_holding_data(self):

        """
        According to the stock list that I hold to refresh the raw data
        :return:
        """
        self.stock_current_observation_pool_dict = self.stock_focus_dict

        self.schema_tmp_config_mgt.insert("stock.stock_current_observation_pool_dict", self.stock_current_observation_pool_dict)

        self.batch_crawl_history_price_by_daily()
        self.batch_crawl_history_fund_flow()

    def refresh_stock_observation_pool(self, sector_list, file_name):

        """
        According to the strategies such as low-cost boards to search high-value stocks, combining the stocks I hold and
        the potential stocks recommended by these strategies to refresh the raw data
        市净率（Price-to-Book Ratio, P/B）
        定义：市净率是股票市价与每股净资产（市净值）的比值，反映市场对净资产的溢价程度。
        市净率 = 股票市价 / 每股净资产
        意义：
        P/B < 1：股价低于净资产，可能被低估（但需警惕资产质量差或盈利能力弱的企业）。
        P/B > 1：股价高于净资产，市场对公司增长有更高预期（如科技、消费行业）。
        P/B 过高（如>5）：可能存在泡沫，需结合盈利能力和行业特点分析。
        """

        df = pd.DataFrame([])
        for symbol in sector_list:
            if df.empty:
                df = ak.stock_board_industry_cons_em(symbol=symbol)
                df['sector'] = symbol
            else:
                df_extend = ak.stock_board_industry_cons_em(symbol=symbol)
                df_extend['sector'] = symbol
                df = pd.concat([df, df_extend])

        self.stock_current_observation_pool_dict = {}
        if not df.empty:
            df = df[df['市净率'] <= 3]
            df = df[df['代码'].apply(self.check_board_category) == 'Main Boards']

            dir_path = self.dir + 'stock_org_data/'
            create_directory(dir_path)
            df.to_csv(dir_path + file_name, index=False)

            self.stock_current_observation_pool_dict = dict(zip(df['代码'], df['名称']))

            self.schema_tmp_config_mgt.insert("stock.stock_current_observation_pool_dict",
                                              self.stock_current_observation_pool_dict)

            self.batch_crawl_history_price_by_daily()

            self.batch_crawl_history_fund_flow()

            self.schema_tmp_config_mgt.insert('stock.refresh_time', get_date_tag())

        self.schema_tmp_config_mgt.insert("stock.stock_current_observation_pool_dict",
                                          self.stock_current_observation_pool_dict)


if __name__ == '__main__':
    obj_stock = DataSourceEM()
    # absolute_timer(1, obj_etf.crawl_realtime_data)

    obj_stock.refresh_stock_observation_pool()
