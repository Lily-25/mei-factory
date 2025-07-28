from sympy.physics.control.control_plots import matplotlib

from src.StockAgent.sector.visualize_sector import DashBoard as sector_DashBoard


def visualize_fund_flow_by_sector():
    # Set font to a Chinese-supported one (e.g., PingFang SC)
    matplotlib.rcParams['font.family'] = 'Songti SC'

    # Fix potential minus sign rendering issue
    matplotlib.rcParams['axes.unicode_minus'] = False

    obj_sector = sector_DashBoard()
    obj_sector.visualize_sector_spot()

if __name__ == '__main__':
    visualize_fund_flow_by_sector()