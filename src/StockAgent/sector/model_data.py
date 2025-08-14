import pandas as pd
import os

from src.StockAgent.common.candlestick_pattern_tools import BullishReversal, BearishReversal, ContinuationTrend
from src.StockAgent.common.statistics_indicator_tools import StatisticsIndicator
from src.StockAgent.utils.operate_files import walk_directory


class IndicatorMonitor(BullishReversal, BearishReversal, ContinuationTrend,StatisticsIndicator):

    def __init__(self, indicator_list:list):
        super().__init__()

        if len(indicator_list):
            self.refresh_active_indicator(indicator_list)
        else:
            self.refresh_active_indicator(list(self.indicator_signal_dict.keys()))

        self.indicator_signal_dir = self.dir + 'sector_analysis/indicator_signal/'
        self.schema_config_mgt.insert('sector.indicator_signal_dir',
                                      os.path.abspath(self.indicator_signal_dir) + '/')

    def evaluate_statistics_indicator(self):

        walk_directory(self.schema_config['sector']['price_and_fund_merger_dir'], self.evaluate_single_project)

        self.indicator_signal_df.to_csv(self.indicator_signal_dir + 'overview.csv')

    def recommend_potential_boards(self):
        """
        Recommend high-potential boards based on the following criteria:

        1. The board's current closing price is below 80% of its fluctuation range
           over a specified period, where the fluctuation range exceeds 5%.
           
        2. The volume is greater than its 20-period moving average (MA20)

        3. News sentiment related to the board is favorable — ideally positive,
           or at the very least, not negative.

        :return: A list of recommended boards that meet the above conditions.
        """
        board_df = pd.read_csv(self.indicator_signal_dir + 'overview.csv')

        # rule1
        board_df.insert(0, 'rule_1', ((board_df['PriceL1_Risk_exponent'] < 30 )
                              & ((board_df['PriceL1_Fluctuation_window'] > 5 )
                                 | ((board_df['PriceL2_Risk_exponent'] < 30)
                                 & board_df['PriceL2_Fluctuation_window'] > 5))))

        board_df = board_df[board_df['rule_1'] & board_df['VolumePW30D']]

        self.schema_config_mgt.insert('sector.sector_focus_list.low_cost', list(board_df['symbol'].dropna()))

        return board_df

if __name__ == '__main__':

    obj = IndicatorMonitor([])
    obj.evaluate_statistics_indicator()
    obj.recommend_potential_boards()