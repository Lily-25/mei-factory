from src.StockAgent.sector.crawl_data_from_em import DataSourceEM as Sector_DataSourceEM
from src.StockAgent.sector.prepare_data import DataFactory as Sector_DataFactory
from src.StockAgent.sector.model_data import IndicatorMonitor as Sector_IndicatorMonitor

from src.StockAgent.etf.crawl_data_from_em import DataSourceEM as ETF_DataSourceEM
from src.StockAgent.etf.prepare_data import DataFactory as ETF_DataFactory
from src.StockAgent.etf.model_data import IndicatorMonitor as ETF_IndicatorMonitor

from src.StockAgent.stock.crawl_data_from_em import DataSourceEM as Stock_DataSourceEM
from src.StockAgent.stock.prepare_data import DataFactory as Stock_DataFactory
from src.StockAgent.stock.model_data import IndicatorMonitor as Stock_IndicatorMonitor

gStock_active_indicator_list = ['evaluate_support_resistance_lines',
                               'evaluate_price_ma_fork',
                               'evaluate_fund_flow_ma_fork',
                               'evaluate_volume_ma_fork',
                               'evaluate_price_macd',
                               'evaluate_price_kdj',
                               'evaluate_price_rsi',
                               'evaluate_volume_vr',
                               'evaluate_uptrend_signal_bullish_engulfing',
                               'evaluate_uptrend_signal_hammer',
                               'evaluate_uptrend_signal_inverted_hammer',
                               'evaluate_uptrend_signal_morning_doji_star',
                               'evaluate_uptrend_signal_morning_star',
                               'evaluate_uptrend_signal_piercing_line',
                               'evaluate_uptrend_signal_three_white_soldiers',
                               'evaluate_uptrend_signal_tweezer_bottom',
                               'evaluate_downtrend_signal_bearish_engulfing',
                               'evaluate_downtrend_signal_dark_cloud_cover',
                               'evaluate_downtrend_signal_evening_star',
                               'evaluate_downtrend_signal_gravestone_doji',
                               'evaluate_downtrend_signal_shooting_star',
                               'evaluate_downtrend_signal_three_black_crows',
                               'evaluate_downtrend_signal_tweezer_top',
                               'evaluate_continue_signal_falling_three_methods',
                               'evaluate_continue_signal_rectangle',
                               'evaluate_continue_signal_rising_three_methods',
                               ]

def discover_low_cost_sector():

    # refresh sector history information
    df_sector = Sector_DataSourceEM()
    df_sector.refresh_hist_data()

    obj = Sector_DataFactory()
    obj.batch_align_price_and_fund_flow()

    obj = Sector_IndicatorMonitor([])
    obj.evaluate_statistics_indicator()
    obj.recommend_potential_boards()

def discover_low_cost_stocks():

    # refresh stock history information
    obj_stock = Stock_DataSourceEM()
    obj_stock.refresh_stock_observation_pool()

    obj_stock = Stock_DataFactory()
    obj_stock.batch_align_price_and_fund_flow()

    obj_stock = Stock_IndicatorMonitor(gStock_active_indicator_list)
    obj_stock.evaluate_statistics_indicator()
    obj_stock.recommend_stocks(obj_stock.stock_observation_pool_dict,
                               'low_cost')

def discover_hot_pot_etfs():
    # refresh etf history information
    obj_etf = ETF_DataSourceEM()
    # 刷新观测的etf范围
    obj_etf.refresh_etf_observation_pool_by_popularity()
    # 获取目标etf历史价格数据
    obj_etf.crawl_etf_history_price()
    # 获取目标etf历史资金流入情况
    obj_etf.crawl_history_fund_flow()

    obj_etf = ETF_DataFactory()
    obj_etf.batch_align_price_and_fund_flow()

    active_indicator_list = ['evaluate_support_resistance_lines',
                               'evaluate_price_ma_fork',
                               'evaluate_fund_flow_ma_fork',
                               'evaluate_volume_ma_fork',
                               'evaluate_price_macd',
                               'evaluate_price_kdj',
                               'evaluate_price_rsi',
                               'evaluate_volume_vr']

    obj_etf = ETF_IndicatorMonitor(active_indicator_list)
    obj_etf.evaluate_statistics_indicator()
    obj_etf.recommend_etfs(obj_etf.etf_focus_dict, 'hot_spot')

if __name__ == '__main__':
    discover_low_cost_sector()
    discover_low_cost_stocks()
    discover_hot_pot_etfs()