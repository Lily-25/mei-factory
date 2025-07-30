
from src.StockAgent.etf.crawl_data_from_em import DataSourceEM as ETF_DataSource
from src.StockAgent.utils.customize_timer import absolute_timer


def crawl_online_data():
    obj_etf = ETF_DataSource()

    # 抓取实时数据
    # absolute_timer(5, obj_etf.crawl_realtime_data)
    obj_etf.crawl_realtime_data()


if __name__ == '__main__':
    crawl_online_data()