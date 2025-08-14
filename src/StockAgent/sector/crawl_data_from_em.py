import os.path
from datetime import datetime

import akshare as ak
import pandas as pd

from src.StockAgent.common.abstract_schema_define import SchemaManager
from src.StockAgent.utils.customize_timer import get_date_tag
from src.StockAgent.utils.operate_files import create_directory, check_whether_files_created_today


class DataSourceEM(SchemaManager):
    def __init__(self):
        super().__init__()
        self.sector_board_info_dir = self.dir + 'sector_org_data/sector_board_info/'
        self.history_price_dir = self.dir + 'sector_org_data/hist_price_em/'
        self.history_fund_flow_dir = self.dir + 'sector_org_data/hist_fund_flow_em/'
        self.refresh_config()

    def refresh_config(self):
        self.schema_config_mgt.insert('sector.sector_board_info_dir',os.path.abspath(self.sector_board_info_dir) + '/')
        self.schema_config_mgt.insert('sector.hist_price_dir',
                                  os.path.abspath(self.history_price_dir) + '/')
        self.schema_config_mgt.insert('sector.history_fund_flow_dir',
                                  os.path.abspath(self.history_fund_flow_dir) + '/')
        return

    def crawl_sector_infor(self):
        """
        :return:
        """
        create_directory(self.sector_board_info_dir)
        stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
        stock_board_industry_name_em_df.to_csv(self.sector_board_info_dir
                                               + datetime.now().strftime('%y%m%d')
                                               + '.csv',
                                               index=False)

    def crawl_sector_history_fund_flow(self):
        """
        :return:
        """
        stock_board_industry_name_em_df = pd.read_csv(self.sector_board_info_dir
                                                      + datetime.now().strftime('%y%m%d')
                                                      + '.csv')
        create_directory(self.history_fund_flow_dir)

        for symbol in stock_board_industry_name_em_df['板块名称']:

            try:
                file_name = self.history_fund_flow_dir + symbol + '.csv'

                # this action just do onetime per day
                if check_whether_files_created_today(file_name):
                    print(f'crawl_sector_history_fund_flow {file_name} has been updated today')
                    continue

                sector_fund_flow_hist_df = ak.stock_sector_fund_flow_hist(symbol=symbol).set_index('日期')
                sector_fund_flow_hist_df = sector_fund_flow_hist_df.loc[:,
                                                 ~sector_fund_flow_hist_df.columns.str.contains('^Unnamed')]

                if os.path.exists(file_name):
                    exist_df = pd.read_csv(file_name,index_col=0)

                    # unique the type of index
                    exist_df.index = pd.to_datetime(exist_df.index)
                    sector_fund_flow_hist_df.index = pd.to_datetime(sector_fund_flow_hist_df.index)

                    sector_fund_flow_hist_df = pd.concat([
                        exist_df.iloc[:-1],
                        sector_fund_flow_hist_df
                    ]).groupby(level=0).last()

                sector_fund_flow_hist_df.to_csv(file_name)

            except Exception as e:
                print(e)
                pass

    def crawl_sector_history_fluctuation(self):
        """
        :return:
        """
        stock_board_industry_name_em_df = pd.read_csv(self.sector_board_info_dir
                                                      + datetime.now().strftime('%y%m%d')
                                                      + '.csv')
        create_directory(self.history_price_dir)
        for symbol in stock_board_industry_name_em_df['板块名称']:
            try:
                start_date = "20250101",
                end_date = datetime.now().strftime('%Y%m%d')

                file_name = self.history_price_dir + symbol + '.csv'

                # this action just do onetime per day
                if check_whether_files_created_today(file_name):
                    print(f'crawl_sector_history_fluctuation {file_name} has been updated today')
                    continue

                exist_df = pd.DataFrame()
                if os.path.exists(file_name):
                    exist_df = pd.read_csv(file_name,index_col=0)
                    start_date = datetime.strptime(exist_df.index[-1], '%Y-%m-%d').strftime('%Y%m%d')

                stock_board_industry_hist_em_df = ak.stock_board_industry_hist_em(symbol = symbol,
                                     start_date = start_date,
                                     end_date = end_date).set_index('日期')

                stock_board_industry_hist_em_df = stock_board_industry_hist_em_df.loc[:,
                                                 ~stock_board_industry_hist_em_df.columns.str.contains('^Unnamed')]

                if not exist_df.empty:
                    stock_board_industry_hist_em_df = exist_df.iloc[:-1].combine_first(stock_board_industry_hist_em_df)

                stock_board_industry_hist_em_df.to_csv(file_name)
            except Exception as e:
                print(e)
                pass

    def refresh_hist_data(self):

        self.crawl_sector_infor()
        self.crawl_sector_history_fund_flow()
        self.crawl_sector_history_fluctuation()

        self.schema_tmp_config_mgt.insert('sector.refresh_time', get_date_tag())

if __name__ == '__main__':
    df_sector = DataSourceEM()
    df_sector.refresh_hist_data()