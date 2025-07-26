from abc import abstractmethod

import pandas as pd

from src.StockAgent.utils.manage_config import ConfigManager
import numpy as np
from scipy.signal import argrelextrema


class BasicManager():
    def __init__(self):

        self.dir = 'dataset/'

        self.etf_observation_dict = {
            '515790':'光伏ETF',
            '513090':'香港证券ETF',
            '560090':'证券ETF龙头',
            '515700':'新能车ETF',
            '512680':'军工ETF龙头',
            '512480':'半导体ETF',
            '515070':'人工智能AIETF',
            '516910':'物流ETF',
            '562500':'机器人ETF',
        }

        self.stock_observation_dict = {
            '002557' : '恰恰食品',
            '603605' : '珀莱雅', }

        self.basic_config_mgt =ConfigManager('../config/basic_config.yaml')
        self.basic_config = self.basic_config_mgt.config

        self.column_maps = (
            ConfigManager('../config/indicator_config.yaml').config)['global']['indicator_translation_dict']

        # 过滤数据太多被平台限制，先控制下载范围
        self.etf_observation_pool_prefix = list(self.etf_observation_dict.keys())
        self.etf_observation_pool_dict = {}
        if not len(self.etf_observation_pool_prefix):
            if self.basic_config.get('global') and self.basic_config['global'].get('etf_observation_pool_dict'):
                self.etf_observation_pool_dict = self.basic_config['global']['etf_observation_pool_dict']
        self.etf_observation_pool_list = list(self.etf_observation_pool_dict.keys())

    @staticmethod
    def get_stock_market_abbreviation(symbol_index):
        if symbol_index.startswith(('60', '68', '51', '56', '58')):
            return 'sh'
        elif symbol_index.startswith(('000','001','002','15','16','300','301','399')):
            return 'sz'
        elif symbol_index.startswith(('83','87','88','899')):
            return 'bj'
        else:
            return ''

    @staticmethod
    def discover_extreme_points(data, fix_type='avg'):
        if type(data) != np.ndarray:
            return None, None, None

        d_len = len(data)
        if fix_type=='zero':
            empty_data = [[0.0,0.0] for i in range(d_len)]
        else:
            avg = sum(data) / d_len
            empty_data = [[avg, avg] for i in range(d_len)]

        ep_df = pd.DataFrame(empty_data, columns=['top','bottom'])
        max_idx = argrelextrema(data, np.greater)[0]
        ep_df.loc[max_idx, 'top'] = data[max_idx]
        min_idx = argrelextrema(data, np.less)[0]
        ep_df.loc[min_idx, 'bottom'] = data[min_idx]
        return max_idx, min_idx, ep_df

    @abstractmethod
    def refresh_config(self):
        pass

    def column_translation(self, column_list, mode = 'z2e'):
        new_column = []
        for item in column_list:
            if item in self.column_maps[mode]:
                new_column.append(self.column_maps[mode][item])
            else:
                if item in self.column_maps[mode+'_extend']:
                    new_column.append(self.column_maps[mode+'_extend'][item])
                else:
                    new_column.append(item)
                    print(f'translate column name {item} failed')

        return new_column

    def refresh_observation_etf(self, new_dict):
        self.etf_observation_pool_dict = new_dict

        self.etf_observation_pool_list = list(self.etf_observation_pool_dict.keys())

        # reset existed config
        if self.basic_config.get('global') and self.basic_config['global'].get('etf_observation_pool_dict'):
            self.basic_config_mgt.delete('global.etf_observation_pool_dict')

        # add new config
        self.basic_config_mgt.insert('global.etf_observation_pool_dict', self.etf_observation_pool_dict)

if __name__ == '__main__':
    column_maps = {
        "z2e": {'日期': 'Date',
                '开盘': 'Open',
                '收盘': 'Close',
                '收盘价': 'Close',
                '最高': 'High',
                '最低': 'Low',
                '成交量': 'Volume',
                '成交额': 'Amount',
                '振幅': 'PriceAmplitude',
                '涨跌幅': 'PriceCR',
                '涨跌额': 'PriceCA',
                '换手率': 'TurnoverR',
                '主力净流入-净额': 'FundFlowMNI',
                '主力净流入-净占比': 'FundFlowMNIR',
                '超大单净流入-净额': 'FundFlowHNI',
                '超大单净流入-净占比': 'FundFlowHNIR',
                '大单净流入-净额': 'FundFlowLNI',
                '大单净流入-净占比': 'FundFlowLNIR',
                '中单净流入-净额': 'FundFlowMMNI',
                '中单净流入-净占比': 'FundFlowMMNIR',
                '小单净流入-净额': 'FundFlowSNI',
                '小单净流入-净占比': 'FundFlowSNIR'},
        "z2e_extend": {'date': 'Date',
                       'open': 'Open',
                       'high': 'High',
                       'low': 'Low',
                       'close': 'Close',
                       'volume': 'Volume',
                       'amount': 'Amount',
                       'outstanding_share': 'Outstanding_share',
                       'turnover': 'Turnover'},
        "e2z": {'Date': '日期',
                'Open': '开盘价格',
                'Close': '收盘价格',
                'High': '一天中最高价格',
                'Low': '一天中最低价格',
                'Volume': '成交量',
                'Amount': '成交金额',
                'PriceAmplitude': '价格振幅 = (High - Low) / Open',
                'PriceCR': '涨跌幅P',
                'PriceCA': '价格变化 = Close - Open',
                'TurnoverR': '换手率 Turnover Ratio',
                'FundFlowMNI': '主力净流入-净额 Main Net inflow-Amount',
                'FundFlowMNIR': '主力净流入-比例 Main Net inflow-Ratio',
                'FundFlowHNI': '超大单净流入-净额 Huge Order Net inflow-Amount',
                'FundFlowHNIR': '超大单净流入-比例 Huge Order Net inflow-Ratio',
                'FundFlowLNI': '大单净流入-净额',
                'FundFlowLNIR': '大单净流入-净占比',
                'FundFlowMMNI': '中单净流入-净额',
                'FundFlowMMNIR': '中单净流入-净占比',
                'FundFlowSNI': '小单净流入-净额',
                'FundFlowSNIR': ' 小单净流入-净占比'},
    }
    config = ConfigManager('../config/indicator_config.yaml')
    config.insert('global.indicator_translation_dict', column_maps)
