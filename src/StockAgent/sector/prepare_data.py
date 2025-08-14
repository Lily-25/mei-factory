import os

import pandas as pd

from src.StockAgent.common.abstract_schema_define import SchemaManager
from src.StockAgent.utils.operate_files import create_directory, walk_directory, check_whether_files_created_today


class DataFactory(SchemaManager):
    def __init__(self):
        super().__init__()
        self.price_and_fund_merger_dir = self.dir + 'sector_etl_data/price_and_fund_merger/'
        self.refresh_config()

    def refresh_config(self):
        self.schema_config_mgt.insert('sector.price_and_fund_merger_dir',
                                  os.path.abspath(self.price_and_fund_merger_dir) + '/')
        return

    def combine_price_and_fund_flow(self, sector_history_fluctuation_file):
        if (not os.path.exists(sector_history_fluctuation_file)
                or not check_whether_files_created_today(sector_history_fluctuation_file,
                                                     self.schema_tmp_config['sector']['refresh_time'])):
            return

        file_name = os.path.basename(sector_history_fluctuation_file)
        sector_history_fund_flow_file = (self.schema_config['sector']['history_fund_flow_dir']
                                         + file_name)

        if not os.path.exists(sector_history_fund_flow_file):
            return

        price_df = pd.read_csv(sector_history_fluctuation_file, index_col=0)
        price_df.columns = self.column_translation(price_df.columns)
        fund_df = pd.read_csv(sector_history_fund_flow_file, index_col=0)
        fund_df.columns = self.column_translation(fund_df.columns)

        merged_df = pd.merge(price_df, fund_df, left_index=True, right_index=True, suffixes=('_df1', ''))

        merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('_df1')]

        merged_df['Close5DMA'] = merged_df['Close'].rolling(5).mean()
        merged_df['Close10DMA'] = merged_df['Close'].rolling(10).mean()
        merged_df['Close30DMA'] = merged_df['Close'].rolling(30).mean()
        merged_df['Close60DMA'] = merged_df['Close'].rolling(60).mean()

        merged_df['FundFlowMNI5DMA'] = merged_df['FundFlowMNI'].rolling(5).mean()
        merged_df['FundFlowMNI10DMA'] = merged_df['FundFlowMNI'].rolling(10).mean()
        merged_df['FundFlowMNI30DMA'] = merged_df['FundFlowMNI'].rolling(30).mean()
        merged_df['FundFlowMNI60DMA'] = merged_df['FundFlowMNI'].rolling(60).mean()

        merged_df.rename_axis('Date', inplace=True)

        merged_df.to_csv(self.price_and_fund_merger_dir + file_name)


    def batch_align_price_and_fund_flow(self):
        sector_history_fluctuation_dir = self.schema_config['sector']['hist_price_dir']

        create_directory(self.price_and_fund_merger_dir, is_empty=True)

        walk_directory(sector_history_fluctuation_dir, self.combine_price_and_fund_flow)

    @staticmethod
    def prepare_history_data():
        obj = DataFactory()
        obj.batch_align_price_and_fund_flow()

if __name__ == '__main__':

    DataFactory.prepare_history_data()