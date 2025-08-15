import pandas as pd
import os

from src.StockAgent.common.candlestick_pattern_tools import BullishReversal, BearishReversal, ContinuationTrend
from src.StockAgent.common.statistics_indicator_tools import StatisticsIndicator
from src.StockAgent.utils.customize_timer import get_date_tag
from src.StockAgent.utils.operate_files import create_directory, walk_directory, backup_file


class IndicatorMonitor(BullishReversal, BearishReversal, ContinuationTrend,StatisticsIndicator):

    def __init__(self, indicator_list:list):
        super().__init__()

        if len(indicator_list):
            self.refresh_active_indicator(indicator_list)
        else:
            self.refresh_active_indicator(list(self.indicator_signal_dict.keys()))

        self.indicator_signal_dir = self.dir + 'stock_analysis/indicator_signal/'
        self.schema_config_mgt.insert('stock.indicator_signal_dir',
                                      os.path.abspath(self.indicator_signal_dir) + '/')

        self.recommend_stock_dir = self.dir + 'stock_recommendation/'
        self.schema_config_mgt.insert('stock.recommend_stock_dir',
                                      os.path.abspath(self.recommend_stock_dir) + '/')

        self.stock_current_observation_pool_dict = self.schema_tmp_config['stock']['stock_current_observation_pool_dict']


    def evaluate_statistics_indicator(self, filename):

        create_directory(self.indicator_signal_dir)

        walk_directory(self.schema_config['stock']['price_and_fund_merger_dir'], self.evaluate_single_project)

        file_path = self.indicator_signal_dir + filename
        if not self.indicator_signal_df.empty:
            self.indicator_signal_df.to_csv(file_path, index=False)
        else:
            if os.path.exists(file_path):
                os.remove(file_path)

    def discover_high_value_indicator(self):

        if not os.path.exists(self.indicator_signal_dir + 'hot_spot.csv'):
            return

        df = pd.read_csv(self.indicator_signal_dir + 'hot_spot.csv')
        record_num = df.shape[0]

        column_list = []
        for column in df.columns:
            if column.startswith('Validated_'):
                thread = (df[column] > df['PriceCRS']).sum() / record_num
                if thread > 0.4:
                    column_list.append(column)

        print(column_list)

    def recommend_stocks(self, reference_dict, filename):

        if not os.path.exists(self.indicator_signal_dir + filename):
            return pd.DataFrame([])

        stock_df = pd.read_csv(self.indicator_signal_dir + filename, dtype={'symbol': 'string'})

        # rule1
        stock_df['rule_1'] = ((stock_df['PriceL1_Risk_exponent'] < 30)
                                      & ((stock_df['PriceL1_Fluctuation_window'] > 5)
                                         | ((stock_df['PriceL2_Risk_exponent'] < 30)
                                            & stock_df['PriceL2_Fluctuation_window'] > 5)))

        recommend_sectors_and_stocks_df = stock_df[stock_df['rule_1']
                                                   & stock_df['VolumePW30D']]

        name_list = []
        for symbol in list(recommend_sectors_and_stocks_df['symbol'].dropna()):
            if symbol in reference_dict.keys():
                print(f'{symbol} : {reference_dict[symbol]}')
                name_list.append(reference_dict[symbol])
            else:
                name_list.append('unknown')

        recommend_sectors_and_stocks_df.insert(0, 'name', name_list)
        recommend_sectors_and_stocks_df = recommend_sectors_and_stocks_df[recommend_sectors_and_stocks_df['name']
                                                                          != 'unknown']
        if recommend_sectors_and_stocks_df.empty:
            return recommend_sectors_and_stocks_df

        recommend_sectors_and_stocks_df['date'] = get_date_tag()

        create_directory(self.recommend_stock_dir)
        file_path = self.recommend_stock_dir + filename
        if os.path.exists(file_path):
            exist_df = pd.read_csv(file_path)

            # just keep the latest analytical data per day
            exist_df = exist_df[exist_df['date'] != get_date_tag()]

            if not exist_df.empty:
                recommend_sectors_and_stocks_df = recommend_sectors_and_stocks_df.combine_first(exist_df)

        cols = ['date'] + [col for col in recommend_sectors_and_stocks_df.columns if col != 'date']
        recommend_sectors_and_stocks_df = recommend_sectors_and_stocks_df[cols]

        recommend_sectors_and_stocks_df.to_csv(file_path, index=False)

        return recommend_sectors_and_stocks_df


if __name__ == '__main__':

    obj = IndicatorMonitor([])

    obj.evaluate_statistics_indicator()

    obj.discover_high_value_indicator()
