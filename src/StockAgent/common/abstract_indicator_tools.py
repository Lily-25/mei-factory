import pandas as pd

import os

from src.StockAgent.common.abstract_define import BasicManager
from src.StockAgent.utils.manage_config import ConfigManager
from src.StockAgent.utils.operate_files import create_directory


class IndicatorTools(BasicManager):

    def __init__(self):

        super().__init__()

        self.indicator_config_mgt =ConfigManager('../config/indicator_config.yaml')
        self.indicator_config = self.indicator_config_mgt.config

        self.indicator_signal_dict = self.indicator_config['global']['indicator_signal_dict']

        # Store analytical result
        self.indicator_signal_dir = self.dir + 'analysis/indicator_signal/'

        self.refresh_config()

        # Store the indicators which will be analyzed through this instance.
        # it should be initiated by refresh_active_indicator
        self.active_indicator_dict = {}
        self.indicator_signal_df = pd.DataFrame([])

    def refresh_config(self):

        self.indicator_config_mgt.insert('global.indicator_signal_dict',
                                     self.indicator_signal_dict)
        self.basic_config_mgt.insert('global.indicator_signal_dir',
                                     self.indicator_signal_dir)

    def get_indicator_dict(self, class_name):
        var_name = f'{class_name}_signal_dict'
        return getattr(self, var_name)

    def get_indicator_dir(self, class_name):
        var_name = f'{class_name}_signal_dir'
        return getattr(self, var_name)

    def refresh_active_indicator(self, indicator_list:list):

        active_indicator_dict = {}
        for key in indicator_list:
            if key not in self.indicator_signal_dict.keys():
                print(f'refresh_active_indicator {key} is invalid')
                break

            active_indicator_dict[key] = self.indicator_signal_dict[key]
        self.active_indicator_dict = active_indicator_dict

    @staticmethod
    def validate_trend(df:pd.DataFrame, signal_column, period_list:list):

        validated_df = pd.DataFrame([])
        validated_df['Open'] = df['Open']
        validated_df['Close'] = df['Close']
        validated_df['PriceCR'] = df['PriceCR']
        validated_df[signal_column] = df[signal_column]

        summary_dict = {}
        for period in period_list:
            validated_df[f'{signal_column}_{period}D_RS'] = \
                (df[signal_column] * (df['PriceCR'].shift(0 - period).rolling(window=period).sum()))

            summary_dict[f'Validated_{signal_column}_{period}D_RS'] = validated_df[f'{signal_column}_{period}D_RS'].sum()

        return validated_df, summary_dict

    def evaluate_single_project(self, filename):

        df = pd.read_csv(filename, index_col=0)

        overview_dict = {
            'Open': df['Open'].iloc[-1],
            'Close': df['Close'].iloc[-1],
            'PriceCR': df['PriceCR'].iloc[-1],
            'PriceCRS': df['PriceCR'].sum()
        }

        for item in self.active_indicator_dict.keys():
            try:
                df, single_dict = \
                        (getattr(self, self.active_indicator_dict[item]['function_name'])(df,
                                                **self.active_indicator_dict[item]['parameter_set']))

                if 'validated_function' in self.active_indicator_dict[item]:
                    validated_df, summary_dict = (getattr(self, self.active_indicator_dict[item]['validated_function'])(df,
                                                **self.active_indicator_dict[item]['validated_parameter_set']))

                    create_directory(self.indicator_signal_dir + f'/{item}/')

                    validated_df.to_csv(self.indicator_signal_dir + f'/{item}/' + os.path.basename(filename))

                    overview_dict = overview_dict | single_dict | summary_dict
                else:
                    overview_dict = overview_dict | single_dict
            except Exception as e:
                print(e)

        df.to_csv(self.indicator_signal_dir + os.path.basename(filename))

        if self.indicator_signal_df.empty:
            self.indicator_signal_df = pd.DataFrame([], columns=['symbol'] + list(overview_dict.keys()))

        self.indicator_signal_df.loc[len(self.indicator_signal_df)] = ([os.path.splitext(os.path.basename(filename))[0]]
                                                       + list(overview_dict.values()))

if __name__ == '__main__':
    obj = IndicatorTools()