from abc import abstractmethod

from src.StockAgent.utils.manage_config import ConfigManager


class SchemaManager():
    def __init__(self):
        self.dir = 'dataset/'

        self.schema_config_mgt =ConfigManager('../config/schema_config.yaml')
        self.schema_config = self.schema_config_mgt.config
        
        self.schema_tmp_config_mgt =ConfigManager('../config/schema_tmp_config.yaml')
        self.schema_tmp_config = self.schema_tmp_config_mgt.config

        # format column names
        self.column_maps = self.schema_config['global']['indicator_translation_dict']

        # sector data schema
        self.sector_field_dict = {}
        self.sector_observation_pool_dict = {}
        self.sector_low_cost_focus_dict = self.schema_config['sector']['sector_focus_list']['low_cost']
        self.sector_hot_spot_focus_dict = self.schema_config['sector']['sector_focus_list']['hot_spot']
        self.sector_focus_dict = self.sector_low_cost_focus_dict + self.sector_hot_spot_focus_dict

        # stock data schema
        self.stock_field_dict = {}
        self.stock_low_cost_focus_dict = self.schema_config['stock']['stock_focus_dict']['low_cost']
        self.stock_hot_spot_focus_dict = self.schema_config['stock']['stock_focus_dict']['hot_spot']
        self.stock_focus_dict = self.stock_low_cost_focus_dict | self.stock_hot_spot_focus_dict
        self.stock_current_observation_pool_dict = self.schema_tmp_config['stock']['stock_current_observation_pool_dict']

        # etf data schema
        self.etf_field_dict = {}
        self.etf_low_cost_focus_dict = self.schema_config['etf']['etf_focus_dict']['low_cost']
        self.etf_hot_spot_focus_dict = self.schema_config['etf']['etf_focus_dict']['hot_spot']
        self.etf_focus_dict = self.etf_low_cost_focus_dict | self.etf_hot_spot_focus_dict
        self.etf_current_observation_pool_dict = self.schema_tmp_config['etf']['etf_current_observation_pool_dict']


    @abstractmethod
    def refresh_config(self):
        pass

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
    def check_board_category(symbol_index):
        if symbol_index.startswith(('300','301')):
            return 'Venture Boards'
        elif symbol_index.startswith(('688')):
            return 'Sci-Tech Boards'
        else:
            return 'Main Boards'

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


if __name__ == '__main__':
    etf_observation_dict = {
        '510300': '沪深300ETF',
        '510500': '中证500ETF',
        '512100': '中证1000ETF',
        '515790': '光伏ETF',
        '513090': '香港证券ETF',
        '560090': '证券ETF龙头',
        '515700': '新能车ETF',
        '512680': '军工ETF龙头',
        '512480': '半导体ETF',
        '515070': '人工智能AIETF',
        '516910': '物流ETF',
        '562500': '机器人ETF',
    }

    stock_observation_low_cost_dict = {
            '603619' : '中曼石油',
            '002557' : '恰恰食品'}

    stock_observation_hot_dict = {
        '002065' : '东华软件',
        '002405' : '四维图新',
        '000034' : '神州数码',
        '600100' : '同方股份',
        '000733' : '振华科技',
    }

    config = ConfigManager('../config/schema_config.yaml')
    sector_focus_list = ['消费电子',
                         '电子元件',
                         '软件开发',
                         '计算机设备',
                         '半导体',
                         '电池']

    config.insert('sector.sector_focus_list.hot_spot', sector_focus_list)
    config.insert('sector.sector_focus_list.low_cost', [])

    config.insert('etf.etf_focus_dict.hot_spot', etf_observation_dict)
    config.insert('etf.etf_focus_dict.low_cost', {})

    config.insert('stock.stock_focus_dict.low_cost', stock_observation_low_cost_dict)
    config.insert('stock.stock_focus_dict.hot_spot', stock_observation_hot_dict)

    tmp_config = ConfigManager('../config/schema_tmp_config.yaml')
    tmp_config.insert('etf.etf_current_observation_pool_dict', {})
    tmp_config.insert('stock.stock_current_observation_pool_dict', {})