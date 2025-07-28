import pandas as pd

from src.StockAgent.common.candlestick_pattern_tools import BullishReversal, BearishReversal, ContinuationTrend
from src.StockAgent.common.statistics_indicator_tools import StatisticsIndicator
from src.StockAgent.utils.operate_files import create_directory, walk_directory


class IndicatorMonitor(StatisticsIndicator, BullishReversal, BearishReversal, ContinuationTrend):

    def __init__(self, indicator_list:list):
        super().__init__()

        if len(indicator_list):
            self.refresh_active_indicator(indicator_list)
        else:
            self.refresh_active_indicator(list(self.indicator_signal_dict.keys()))

        self.indicator_signal_dir = self.dir + 'etf_analysis/indicator_signal/'
        self.recommend_etf_dir = self.dir + 'etf_recommendation/'

    def evaluate_statistics_indicator(self):

        create_directory(self.indicator_signal_dir)

        walk_directory(self.schema_config['etf']['price_and_fund_merger_dir'], self.evaluate_single_project)

        self.indicator_signal_df.to_csv(self.indicator_signal_dir + 'overview.csv', index=False)

    def recommend_etfs(self, reference_dict, filename):
        etf_df = pd.read_csv(self.indicator_signal_dir + 'overview.csv', dtype={'symbol': 'string'})

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

        create_directory(self.recommend_etf_dir)
        recommend_etf_df.to_csv(self.recommend_etf_dir + f'{filename}.csv',
                                               index=False)


if __name__ == '__main__':

    active_indicator_list = ['evaluate_support_resistance_lines',
                             'evaluate_fund_flow_ma_fork',
                             'evaluate_price_kdj']

    obj = IndicatorMonitor(active_indicator_list)

    obj.evaluate_statistics_indicator()
