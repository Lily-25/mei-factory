from datetime import datetime
import os,time

import akshare as ak
import pandas as pd

from src.StockAgent.common.abstract_schema_define import SchemaManager
from src.StockAgent.utils.customize_timer import last_day_of_last_season, absolute_timer
from src.StockAgent.utils.operate_files import create_directory, walk_directory, check_whether_files_created_today
from src.StockAgent.stock.crawl_data_from_em import DataSourceEM as stock_etl_dataSourceEM


class DataSourceEM(SchemaManager):

    def __init__(self):
        super().__init__()
        self.etf_name_dir = self.dir + 'etf_org_data/etf_name_em/'
        self.stock_hold_detail_dir = self.dir + 'etf_org_data/stock_hold_detail/'
        self.hist_price_dir = self.dir + 'etf_org_data/hist_price_em/'
        self.hist_price_spot_dir = self.dir + 'etf_org_data/fund_etf_spot_em/'
        self.hist_fund_flow_dir = self.dir + 'etf_org_data/hist_fund_flow_em/'

        self.stock = stock_etl_dataSourceEM()

        self.refresh_config()

    def refresh_config(self):
        self.schema_config_mgt.insert('etf.etf_name_dir',os.path.abspath(self.etf_name_dir) + '/')
        self.schema_config_mgt.insert('etf.stock_hold_detail_dir',
                                  os.path.abspath(self.stock_hold_detail_dir) + '/')
        self.schema_config_mgt.insert('etf.hist_price_dir',
                                  os.path.abspath(self.hist_price_dir) + '/')
        self.schema_config_mgt.insert('etf.hist_fund_flow_dir',
                                  os.path.abspath(self.hist_fund_flow_dir) + '/')
        self.schema_config_mgt.insert('etf.hist_price_spot_dir',
                                  os.path.abspath(self.hist_price_spot_dir) + '/')

    def etf_basic_info(self):
        """
        获取etf清单
        :return:
        """
        create_directory(self.etf_name_dir)

        try:
            fund_name_em_df = ak.fund_name_em()
            fund_name_em_df.to_csv(self.etf_name_dir + "overview.csv", index=False)
        except Exception as e:
            print(f'Crawl etf overview Error:{e}')
            pass

    def refresh_etf_observation_pool_by_popularity(self, max_etfs=50):
        # get the top ETF sorted by volume periodically
        etf_spot_em_df = ak.fund_etf_spot_em().sort_values(by='成交量', ascending=False).head(max_etfs)
        self.etf_observation_pool_dict = (self.etf_focus_dict
                                          | dict(zip(etf_spot_em_df['代码'], etf_spot_em_df['名称'])))


    def refresh_etf_observation_pool_by_sector(self, max_etfs=50):
        """
        the method to query this information will trigger frequent visit to the finance platform
        , bringing about that the platform rejects requires from this tool.
        """

        # get the top ETF sorted by volume periodically
        etf_spot_em_df = ak.fund_etf_spot_em().sort_values(by='成交量', ascending=False).head(max_etfs)

        # get the stocks related to low-cost sectors
        target_sector_df = pd.read_csv(self.schema_config['stock']['stock_low_cost_observation_pool_file'])

        # set the time to get holding information
        date = last_day_of_last_season(backward=1)

        def get_sector_by_stock(stock_id):
            if stock_id in target_sector_df['代码'].values:
                return target_sector_df[stock_id]['sector']
            else:
                return 'Unknown'

        etf_observation_pool_df = pd.DataFrame([])
        for _, row in etf_spot_em_df.iterrows():
            etf_code = row['代码']
            etf_name = row['名称']

            try:
                holdings = ak.stock_report_fund_hold_detail(symbol=etf_code, date=date)
                time.sleep(1)  # Be gentle to avoid blocking

                # Step 2: Map stocks to sectors
                holdings['sector'] = holdings['股票代码'].apply(get_sector_by_stock)
                holdings['etf_code'] = etf_code
                holdings['etf_name'] = etf_name

                if etf_observation_pool_df.empty:
                    etf_observation_pool_df = holdings
                else:
                    etf_observation_pool_df = pd.concat([etf_observation_pool_df, holdings])

            except Exception as e:
                print(e)
                pass

        etf_observation_pool_df = etf_observation_pool_df[etf_observation_pool_df['sector'] != 'Unknown']
        if not etf_observation_pool_df.empty:
            self.etf_observation_pool_dict = (self.etf_focus_dict
                                          | dict(zip(etf_observation_pool_df['etf_code'], etf_observation_pool_df['etf_name'])))
        else:
            self.etf_observation_pool_dict = self.etf_focus_dict

        print(self.etf_observation_pool_dict)

    def crawl_etf_history_price(self, period="daily", start_date="20250101", adjust="hfq"):
        """
        根据ETF索引获取etf价格历史记录
        """
        create_directory(self.hist_price_dir)

        end_date = datetime.now().strftime('%Y%m%d')

        for symbol_index in self.etf_observation_pool_dict.keys():
            try:
                file_name = self.hist_price_dir + f'{symbol_index}.csv'

                # this action just do onetime per day
                if check_whether_files_created_today(file_name):
                    continue

                exist_df = pd.DataFrame()
                if os.path.exists(file_name):
                    exist_df = pd.read_csv(file_name, index_col=0)
                    start_date = datetime.strptime(exist_df.index[-1], '%Y-%m-%d').strftime('%Y%m%d')

                fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol=symbol_index,
                                                          period=period,
                                                          start_date=start_date,
                                                          end_date=end_date,
                                                          adjust=adjust).set_index('日期')
                fund_etf_hist_em_df = fund_etf_hist_em_df.loc[:,
                                                 ~fund_etf_hist_em_df.columns.str.contains('^Unnamed')]

                if not exist_df.empty:
                    # unique the type of index
                    fund_etf_hist_em_df = exist_df.iloc[:-1].combine_first(fund_etf_hist_em_df)

                fund_etf_hist_em_df.to_csv(file_name)

            except Exception as e:
                print(f'Crawl {symbol_index} history data Error:{e}')
                pass

    def crawl_history_fund_flow(self):
        """
        根据etf获取etf主力资金流入情况
        :return:
        """

        create_directory(self.hist_fund_flow_dir)

        for symbol_index in self.etf_observation_pool_dict.keys():
            try:
                file_name = self.hist_fund_flow_dir + f'{symbol_index}.csv'

                # this action just do onetime per day
                if check_whether_files_created_today(file_name):
                    print(f'crawl_history_fund_flow {file_name} has been updated today')
                    continue

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

    def crawl_etf_stock_hold_detail(self):
        """
        抓去etf关联的股票信息
        :return:
        """
        create_directory(self.stock_hold_detail_dir)

        date = last_day_of_last_season(backward=1)
        for symbol_index in self.etf_focus_dict.keys():
            try:
                file_name = self.stock_hold_detail_dir + f'{symbol_index}.csv'

                # this action just do onetime per day
                if check_whether_files_created_today(file_name):
                    print(f'crawl_etf_stock_hold_detail {file_name} has been updated today')
                    continue

                stock_report_fund_hold_df = ak.stock_report_fund_hold_detail(symbol=symbol_index,
                                                                            date=date)
                stock_report_fund_hold_df.to_csv(file_name, index=False)
            except Exception as e:
                print(f'Crawl {symbol_index} stock detail Error:{e}')
                pass

    def craw_relative_stock_history_data(self, file):
        """
        抓去ETF关联的股票的历史几个变化
        :param file:
        :return:
        """
        df = pd.read_csv(file)
        end_date = datetime.now().strftime('%Y%m%d')
        for symbol in df['股票代码']:
            flag = self.get_stock_market_abbreviation(str(symbol))
            self.stock.crawl_history_price_by_daily(symbol_index=f'{flag}{symbol}',
                                                    start_date='20250101',
                                                    end_date=end_date)

    def crawl_realtime_data(self):
        """
        获取实时的ETF价格数据
        :return:
        """

        print(f"enter crawl_realtime_data at {datetime.now().strftime('%y%m%d %h%m')}")

        path_dir = (self.hist_price_spot_dir
                    + datetime.now().strftime('%y%m%d')) + '/'
        create_directory(path_dir)

        try:
            fund_etf_spot_em_df = ak.fund_etf_spot_em()
            fund_etf_spot_em_df.to_csv(path_dir
                                       + datetime.now().strftime('%H%M')
                                       + '.csv')
        except Exception as e:
            print(f'Crawl etf realtime data Error:{e}')
            pass

    def refresh_hist_data(self):

        # 刷新观测的etf范围
        self.refresh_etf_observation_pool_by_popularity()

        # 获取目标etf历史价格数据
        self.crawl_etf_history_price()

        # 获取目标etf历史资金流入情况
        self.crawl_history_fund_flow()

    def refresh_related_stock_etl_data(self):

        # 获取关联股票信息
        self.crawl_etf_stock_hold_detail()
        walk_directory(self.stock_hold_detail_dir, self.craw_relative_stock_history_data)


if __name__ == '__main__':

    obj_etf = DataSourceEM()

    # 抓取实时数据
    absolute_timer(5, obj_etf.crawl_realtime_data)

    # 新浪获取etf数据
    # ak.stock_zh_index_spot_sina() # 实时接口
    # ak.fund_etf_hist_sina('sh512480') # 单指数历史数据
    # ak.fund_etf_category_sina(symbol='ETF基金') # 全部指数的数据


