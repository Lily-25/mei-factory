import os

import pandas as pd

from src.StockAgent.common.abstract_define import BasicManager
from src.StockAgent.utils.operate_files import walk_directory, create_directory


class DataFactory(BasicManager):
    def __init__(self):
        super().__init__()
        self.price_and_fund_merger_dir = self.dir + 'stock_etl_data/price_and_fund_merger/'
        self.refresh_config()

    def refresh_config(self):
        self.basic_config_mgt.insert('stock.price_and_fund_merger_dir',
                                     os.path.abspath(self.price_and_fund_merger_dir) + '/')

    def align_price_and_fund_flow(self, history_price_file):
        if not os.path.exists(history_price_file):
            return

        filename = os.path.basename(history_price_file)
        history_fund_flow_file = (self.basic_config['stock']['hist_fund_flow_dir']
                                         + filename)

        if not os.path.exists(history_fund_flow_file):
            return

        price_df = pd.read_csv(history_price_file, index_col=0)
        price_df.columns = self.column_translation(price_df.columns)

        fund_df = pd.read_csv(history_fund_flow_file, index_col=0)
        fund_df.columns = self.column_translation(fund_df.columns)

        merged_df = pd.merge(price_df, fund_df, left_index=True, right_index=True, suffixes=('', '_df1'))

        if (('Close_df1' in merged_df.columns) and
                (merged_df[merged_df['Close'] != merged_df['Close_df1']].shape[0])):
            print(f'{filename} Close price conflict, keep the price from hist_price_em')
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

        merged_df.to_csv(self.price_and_fund_merger_dir + filename)

    def batch_align_price_and_fund_flow(self):
        create_directory(self.price_and_fund_merger_dir)

        walk_directory(self.basic_config['stock']['hist_price_dir'], self.align_price_and_fund_flow)


if __name__ == '__main__':
    stock_obj = DataFactory()
    stock_obj.batch_align_price_and_fund_flow()