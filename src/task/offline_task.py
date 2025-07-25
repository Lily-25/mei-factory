from src.sector.crawl_data_from_em import DataSourceEM as Sector_DataSourceEM
from src.sector.prepare_data import DataFactory as Sector_ataFactory
from src.sector.model_data import IndicatorMonitor as Sector_IndicatorMonitor

from src.etf.crawl_data_from_em import DataSourceEM as ETF_DataSourceEM
from src.etf.prepare_data import DataFactory as ETF_DataFactory
from src.etf.model_data import IndicatorMonitor as ETF_IndicatorMonitor

from src.stock.crawl_data_from_em import DataSourceEM as Stock_DataSourceEM
from src.stock.prepare_data import DataFactory as Stock_DataFactory
from src.stock.model_data import IndicatorMonitor as Stock_IndicatorMonitor

def discover_low_cost_products():

    # refresh sector history information
    df_sector = Sector_DataSourceEM()
    df_sector.refresh_hist_data()

    obj = Sector_ataFactory()
    obj.batch_align_price_and_fund_flow()

    obj = Sector_IndicatorMonitor([])
    obj.evaluate_statistics_indicator()
    obj.recommend_potential_boards()

    # refresh etf history information
    obj_etf = ETF_DataSourceEM()
    obj_etf.refresh_hist_data()

    obj_etf = ETF_DataFactory()
    obj_etf.batch_align_price_and_fund_flow()

    active_indicator_list = ['evaluate_support_resistance_lines',
                             'evaluate_fund_flow_ma_fork',
                             'evaluate_price_kdj']
    obj_etf = ETF_IndicatorMonitor(active_indicator_list)
    obj_etf.evaluate_statistics_indicator()

    # refresh stock history information
    obj_stock = Stock_DataSourceEM()
    obj_stock.refresh_stock_observation_pool()

    obj_stock = Stock_DataFactory()
    obj_stock.batch_align_price_and_fund_flow()

    obj_stock = Stock_IndicatorMonitor([])
    obj_stock.evaluate_statistics_indicator()
    obj_stock.discover_high_value_indicator()

def recommend_sectors_and_stocks():
    obj_stock = Stock_IndicatorMonitor([])
    obj_stock.recommend_potential_stocks()

if __name__ == '__main__':
    recommend_sectors_and_stocks()