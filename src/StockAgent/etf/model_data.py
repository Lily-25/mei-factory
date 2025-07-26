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


    def evaluate_statistics_indicator(self):

        create_directory(self.indicator_signal_dir)

        walk_directory(self.basic_config['etf']['price_and_fund_merger_dir'], self.evaluate_single_project)

        self.indicator_signal_df.to_csv(self.indicator_signal_dir + 'overview.csv', index=False)


if __name__ == '__main__':

    active_indicator_list = ['evaluate_support_resistance_lines',
                             'evaluate_fund_flow_ma_fork',
                             'evaluate_price_kdj']

    obj = IndicatorMonitor(active_indicator_list)

    obj.evaluate_statistics_indicator()
