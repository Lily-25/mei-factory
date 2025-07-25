import pandas as pd

from src.common.candlestick_pattern_tools import BullishReversal, BearishReversal, ContinuationTrend
from src.common.statistics_indicator_tools import StatisticsIndicator
from src.utils.operate_files import create_directory, walk_directory


class IndicatorMonitor(BullishReversal, BearishReversal, ContinuationTrend,StatisticsIndicator):

    def __init__(self, indicator_list:list):
        super().__init__()

        if len(indicator_list):
            self.refresh_active_indicator(indicator_list)
        else:
            self.refresh_active_indicator(list(self.indicator_signal_dict.keys()))

        self.indicator_signal_dir = self.dir + 'stock_analysis/indicator_signal/'


    def evaluate_statistics_indicator(self):

        create_directory(self.indicator_signal_dir)

        walk_directory(self.basic_config['stock']['price_and_fund_merger_dir'], self.evaluate_single_project)

        self.indicator_signal_df.to_csv(self.indicator_signal_dir + 'overview.csv', index=False)

    def discover_high_value_indicator(self):

        df = pd.read_csv(self.indicator_signal_dir + 'overview.csv')
        record_num = df.shape[0]

        column_list = []
        for column in df.columns:
            if column.startswith('Validated_'):
                thread = (df[column] > df['PriceCRS']).sum() / record_num
                if thread > 0.4:
                    column_list.append(column)

        print(column_list)

    def recommend_potential_stocks(self):
        stock_df = pd.read_csv(self.indicator_signal_dir + 'overview.csv', dtype={'symbol': str})

        # rule1
        stock_df.insert(0, 'rule_1', ((stock_df['PriceL1_Risk_exponent'] < 30)
                                      & ((stock_df['PriceL1_Fluctuation_window'] > 5)
                                         | ((stock_df['PriceL2_Risk_exponent'] < 30)
                                            & stock_df['PriceL2_Fluctuation_window'] > 5))))

        stock_observation_dict = self.basic_config['stock']['stock_observation_dict']

        # print(list(stock_df['symbol'].where(stock_df['rule_1'] & stock_df['VolumePW30D']).dropna()))
        for symbol in list(stock_df['symbol'].where(stock_df['rule_1'] & stock_df['VolumePW30D']).dropna()):
            if symbol in stock_observation_dict.keys():
                print(f'{symbol} : {stock_observation_dict[symbol]}')


if __name__ == '__main__':

    obj = IndicatorMonitor([])

    obj.evaluate_statistics_indicator()

    obj.discover_high_value_indicator()
