import pandas as pd
import os

from src.StockAgent.common.candlestick_pattern_tools import BullishReversal, BearishReversal, ContinuationTrend
from src.StockAgent.common.statistics_indicator_tools import StatisticsIndicator
from src.StockAgent.utils.customize_timer import get_date_tag
from src.StockAgent.utils.operate_files import create_directory, walk_directory


class IndicatorMonitor(StatisticsIndicator, BullishReversal, BearishReversal, ContinuationTrend):

    def __init__(self, indicator_list:list):
        super().__init__()

        if len(indicator_list):
            self.refresh_active_indicator(indicator_list)
        else:
            self.refresh_active_indicator(list(self.indicator_signal_dict.keys()))

        self.indicator_signal_dir = self.dir + 'etf_analysis/indicator_signal/'
        self.schema_config_mgt.insert('etf.indicator_signal_dir',
                                      os.path.abspath(self.indicator_signal_dir) + '/')

        self.recommend_etf_dir = self.dir + 'etf_recommendation/'
        self.schema_config_mgt.insert('etf.recommend_etf_dir',
                                      os.path.abspath(self.recommend_etf_dir) + '/')

        self.etf_current_observation_pool_dict = self.schema_tmp_config['etf']['etf_current_observation_pool_dict']

    def evaluate_statistics_indicator(self, filename):

        create_directory(self.indicator_signal_dir)

        walk_directory(self.schema_config['etf']['price_and_fund_merger_dir'], self.evaluate_single_project)

        file_path = self.indicator_signal_dir + filename
        if not self.indicator_signal_df.empty:
            self.indicator_signal_df.to_csv(file_path, index=False)
        else:
            if os.path.exists(file_path):
                os.remove(file_path)

    def recommend_etfs(self, reference_dict, filename):

        if not os.path.exists(self.indicator_signal_dir + filename):
            return pd.DataFrame([])

        etf_df = pd.read_csv(self.indicator_signal_dir + filename, dtype={'symbol': 'string'})

        # rule1
        etf_df['rule_1'] = ((etf_df['PriceL1_Risk_exponent'] < 30)
                                      & ((etf_df['PriceL1_Fluctuation_window'] > 5)
                                         | ((etf_df['PriceL2_Risk_exponent'] < 30)
                                            & etf_df['PriceL2_Fluctuation_window'] > 5)))

        recommend_etf_df = etf_df[etf_df['rule_1'] & etf_df['VolumePW30D']]

        name_list = []
        for symbol in list(recommend_etf_df['symbol'].dropna()):
            if symbol in reference_dict.keys():
                print(f'{symbol} : {reference_dict[symbol]}')
                name_list.append(reference_dict[symbol])
            else:
                name_list.append('unknown')

        recommend_etf_df.insert(0, 'name', name_list)
        recommend_etf_df = recommend_etf_df[recommend_etf_df['name'] != 'unknown']
        if recommend_etf_df.empty:
            return recommend_etf_df

        recommend_etf_df['date'] = get_date_tag()

        create_directory(self.recommend_etf_dir)
        file_path = self.recommend_etf_dir + filename
        if os.path.exists(file_path):
            exist_df = pd.read_csv(file_path)

            # just keep the latest analytical data per day
            exist_df = exist_df[exist_df['date'] != get_date_tag()]

            if not exist_df.empty:
                recommend_etf_df = recommend_etf_df.combine_first(exist_df)

        recommend_etf_df.to_csv(self.recommend_etf_dir + f'{filename}.csv',
                                               index=False)

        return recommend_etf_df


if __name__ == '__main__':

    active_indicator_list = ['evaluate_support_resistance_lines',
                             'evaluate_fund_flow_ma_fork',
                             'evaluate_price_kdj']

    obj = IndicatorMonitor(active_indicator_list)

    obj.evaluate_statistics_indicator()
