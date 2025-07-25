import pandas as pd
import numpy as np
import os
import bisect

from pandas.core.interchange.dataframe_protocol import DataFrame

from src.common.abstract_define import BasicManager
from src.common.abstract_indicator_tools import IndicatorTools
from src.utils.operate_files import create_directory, walk_directory, extract_filename

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import mplcursors


class StatisticsIndicator(IndicatorTools):

    def __init__(self):
        super().__init__()

    @staticmethod
    def calculate_support_resistance_lines(df:pd.DataFrame, observation_item, indicator_prefix, period_list):
        """
            Evaluate support and resistance levels and calculate risk exposure based on the current closing price position.

            This function identifies potential support (price floors) and resistance (price ceilings) levels from the historical price data,
            and then assesses the relative position of the current closing price within that range to estimate market risk or opportunity.

            Parameters:
            ----------
            df : pd.DataFrame
                Input DataFrame that must include a 'close' column, and optionally others like 'high' and 'low' if used for analysis.

            Returns:
            -------
            pd.DataFrame
                The input DataFrame with additional columns representing:
                - Identified support and resistance levels
                - Price position indicator (e.g. normalized score between support and resistance)
                - Risk exponent or signal reflecting proximity to support/resistance
            """

        range_line = {
            observation_item: df[observation_item].iloc[-1],
            f'{indicator_prefix}L1_Risk_exponent':100,
            f'{indicator_prefix}L1_Fluctuation_window': 0,
            f'{indicator_prefix}L2_Risk_exponent':100,
            f'{indicator_prefix}L2_Fluctuation_window': 0,
        }

        # Identify support line and pressure line according to MA
        avg_line_list = []
        for period in period_list:
            ref = list(df[observation_item].rolling(window=period).mean())
            avg_line_list.append(ref[-1])

        avg_line_list.sort()

        last_close = df[observation_item].iloc[-1]

        index = bisect.bisect_left(avg_line_list, last_close)

        if index >= len(avg_line_list):
            range_line[f'{indicator_prefix}Top_ma'] = np.inf
            range_line[f'{indicator_prefix}Bottom_ma'] = avg_line_list[-1]
        elif avg_line_list[index] == last_close:
            if index == 0:
                range_line[f'{indicator_prefix}Top_ma'] = avg_line_list[index + 1]
                range_line[f'{indicator_prefix}Bottom_ma'] = -np.inf
            elif index == len(avg_line_list) - 1:
                range_line[f'{indicator_prefix}Top_ma'] = np.inf
                range_line[f'{indicator_prefix}Bottom_ma'] = avg_line_list[index]
            else:
                range_line[f'{indicator_prefix}Top_ma'] = avg_line_list[index + 1]
                range_line[f'{indicator_prefix}Bottom_ma'] = avg_line_list[index - 1]
        else:
            if index == 0:
                range_line[f'{indicator_prefix}Top_ma'] = avg_line_list[index]
                range_line[f'{indicator_prefix}Bottom_ma'] = -np.inf
            else:
                range_line[f'{indicator_prefix}Top_ma'] = avg_line_list[index]
                range_line[f'{indicator_prefix}Bottom_ma'] = avg_line_list[index - 1]

        # Identify support line and pressure line according to extreme points
        thread = min(period_list[-1], len(df)-1)
        _,_,ep_df = BasicManager.discover_extreme_points(df[-thread:][observation_item].to_numpy())
        range_line[f'{indicator_prefix}Top_ep'] = max(ep_df['top'])
        range_line[f'{indicator_prefix}Bottom_ep'] = min(ep_df['bottom'])

        # locating the position of Close Price
        range_line[f'{indicator_prefix}L1_top'] = min(range_line[f'{indicator_prefix}Top_ma'],
                                                    range_line[f'{indicator_prefix}Top_ep'])
        range_line[f'{indicator_prefix}L1_bottom'] = (
            max(range_line[f'{indicator_prefix}Bottom_ma'], range_line[f'{indicator_prefix}Bottom_ep']))

        range_line[f'{indicator_prefix}L2_top'] = (
            max(range_line[f'{indicator_prefix}Top_ma'], range_line[f'{indicator_prefix}Top_ep']))
        range_line[f'{indicator_prefix}L2_top'] = (
            range_line)[f'{indicator_prefix}L2_top'] \
            if range_line[f'{indicator_prefix}L2_top'] != np.inf else range_line[f'{indicator_prefix}L1_top']
        range_line[f'{indicator_prefix}L2_bottom'] = (
            min(range_line[f'{indicator_prefix}Bottom_ma'], range_line[f'{indicator_prefix}Bottom_ep']))
        range_line[f'{indicator_prefix}L2_bottom'] = (
            range_line)[f'{indicator_prefix}L2_bottom'] \
            if range_line[f'{indicator_prefix}L2_bottom'] != -np.inf else range_line[f'{indicator_prefix}L1_bottom']

        # Computing the risk exponents
        if range_line[f'{indicator_prefix}L1_top'] > last_close :
            range_line[f'{indicator_prefix}L1_Risk_exponent'] = (
                    ((last_close - range_line[f'{indicator_prefix}L1_bottom'])
                     / (range_line[f'{indicator_prefix}L1_top'] - range_line[f'{indicator_prefix}L1_bottom'])) * 100)
        else:
            range_line[f'{indicator_prefix}L1_Risk_exponent'] = 100 # approaching the top

        range_line[f'{indicator_prefix}L1_Fluctuation_window'] = (
                ((range_line[f'{indicator_prefix}L1_top'] - range_line[f'{indicator_prefix}L1_bottom'])
                 / range_line[f'{indicator_prefix}L1_bottom']) * 100)

        if range_line[f'{indicator_prefix}L2_top'] > last_close :
            range_line[f'{indicator_prefix}L2_Risk_exponent'] = (
                    ((last_close - range_line[f'{indicator_prefix}L2_bottom'])
                     / (range_line[f'{indicator_prefix}L2_top'] - range_line[f'{indicator_prefix}L2_bottom'])) * 100)
        else:
            range_line[f'{indicator_prefix}L2_Risk_exponent'] = 100 # approaching the top

        range_line[f'{indicator_prefix}L2_Fluctuation_window'] = (
                ((range_line[f'{indicator_prefix}L2_top'] - range_line[f'{indicator_prefix}L2_bottom'])
                 / range_line[f'{indicator_prefix}L2_bottom']) * 100)

        return df, range_line

    @staticmethod
    def calculate_ma_fork(df:DataFrame,
                         observation_item,
                         indicator_prefix,
                         period_list):
        """
        Calculate moving averages and identify golden forks and death forks

        Parameters:
        ----------
        df : DataFrame
            A DataFrame containing a column specified by `observation_item`.
        observation_item : str
            The name of the column used to compute moving averages.
        indicator_prefix : str
            A prefix for the output moving average column names.
        period_list : list of int, default [5, 10, 30, 60]
            The periods over which to compute moving averages.
        evaluate_win : int, default 5
            The number of days after a golden fork over which to evaluate returns.

        Returns:
        -------
        dict
            A dictionary containing:
            - The ratio of positive evaluation windows
            - The cumulative return of golden forks across different MA periods
        """

        if not len(df) or not (observation_item in df.columns):
            return

        overview_dict = {}

        for period, evaluate_win in reversed(period_list):

            ref_mean = df[observation_item].rolling(window=period).mean()

            # PW : positive window
            df.insert(0, f'{indicator_prefix}PW{period}D', ((ref_mean < df[observation_item])
                                                         & (df[observation_item] > 0)))

            # PWGF: positive window start point as a golden fork
            mid_tag = list((df[f'{indicator_prefix}PW{period}D'] == True)
                           & (df[f'{indicator_prefix}PW{period}D'].shift(1) == False))

            for index in range(evaluate_win,len(mid_tag)):
                if not mid_tag[index] or (sum(mid_tag[index-evaluate_win:index]) != 0.0):
                    mid_tag[index] = False

            df.insert(1, f'{indicator_prefix}PW{period}DGF', mid_tag)

            # NW : negative window, it's a signal to sell stock
            df.insert(2, f'{indicator_prefix}NW{period}D', ((ref_mean > df[observation_item])
                                                         & (df[observation_item] < 0)))
            # NWIF: negative window start point as a death fork
            df.insert(3, f'{indicator_prefix}NW{period}DDF', ((ref_mean > df[observation_item])
                                                           & (df[observation_item] < 0)
                                                           & (df[observation_item].shift(1) > 0)))

            overview_dict[observation_item] = df[observation_item].iloc[-1]
            overview_dict[f'{indicator_prefix}PW{period}D'] = df[f'{indicator_prefix}PW{period}D'].iloc[-1]

        return df, overview_dict

    @staticmethod
    def validate_ma_fork(df:DataFrame,
                         observation_item,
                         indicator_prefix,
                         period_list,
                         target):

        if not len(df) or not (observation_item in df.columns):
            return

        validated_df = pd.DataFrame([])

        validated_df[observation_item] = df[observation_item]
        validated_df[target] = df[target]

        summary_dict = {}

        for period, evaluate_win in reversed(period_list):

            # PWGFR: the revenue in the next week
            validated_df[f'{indicator_prefix}PW{period}DGFRS'] = (df[f'{indicator_prefix}PW{period}DGF']
                                                             * (df[target].shift(0 - evaluate_win).rolling(
                        window=evaluate_win).sum()))

            summary_dict[f'Validated_{indicator_prefix}PW{period}DGFRS'] = (
                validated_df[f'{indicator_prefix}PW{period}DGFRS'].sum())

        return validated_df, summary_dict

    @staticmethod
    def calculate_ma_cd(df:pd.DataFrame, observation_item, period_n, period_m, period_s):
        """
        The Moving Average Convergence Divergence (MACD) is a widely used technical analysis indicator that helps
        traders identify trends in stock prices, commodities, or other financial assets. It's calculated by taking
        the difference between two exponential moving averages (EMAs) of a security’s price:

        DIF Line = 12-day EMA - 26-day EMA
        DEP line = 9-day EMA of the MACD Line
        MACD Histogram = DIF Line - DEP Line

        对比长短两个周期的移动平均数变化，如果短周期的上穿长周期，表示看涨；相反，看跌
        :return:
        """
        # Calculate the Raw Stochastic Value (RSV)
        # Calculate 12-day EMA
        df.insert(0, 'EMA12', (df[observation_item].ewm(span=period_n, adjust=False).mean()))

        # Calculate 26-day EMA
        df.insert(1, 'EMA26', df[observation_item].ewm(span=period_m, adjust=False).mean())

        # Calculate MACD line
        df.insert(2, 'DIF', df['EMA12'] - df['EMA26'])

        # Calculate Signal line (9-day EMA of MACD)
        df.insert(3, 'DEF', df['DIF'].ewm(span=period_s, adjust=False).mean())

        # Calculate Histogram (MACD - Signal)
        df.insert(4, 'MACD Histogram', df['DIF'] - df['DEF'])

        # sign golden fork and death fork
        df.insert(0, 'MACDDF', (df['MACD Histogram'] <= 0) & (df['MACD Histogram'].shift(1) > 0 ))
        df.insert(0, 'MACDGF', (df['MACD Histogram'] >= 0) & (df['MACD Histogram'].shift(1) < 0))

        overview_dict = {
            'DIF': df['DIF'].iloc[-1],
            'DEF': df['DEF'].iloc[-1],
            'MACDGF': df['MACDGF'].iloc[-1],
            'MACDDF': df['MACDDF'].iloc[-1],
        }

        return df, overview_dict

    @staticmethod
    def calculate_kdj(df: pd.DataFrame,
                      observation_item,
                      observation_item_l,
                      observation_item_h,
                      period_n,
                      period_m):
        """
        Calculate the KDJ (Stochastic Oscillator) indicators: K, D, and J.

        This function evaluates market momentum by comparing the current closing price
        to the high-low range over the past N days (stochastic oscillator).

        Parameters:
        ----------
        df : pd.DataFrame
            Input DataFrame that must include columns: 'Close', 'High', and 'Low'.
        period_n : int, default 20
            Lookback period for calculating the raw stochastic value (RSV).
        period_m : int, default 10
            Smoothing period for the D-line, which is the moving average of the K-line.

        Returns:
        -------
        pd.DataFrame
            The input DataFrame with three new columns added: 'K', 'D', and 'J'.

        中文说明：
        ----------
        随机振荡器（KDJ）通过对比当前收盘价与最近N天区间，评估市场动能。
        - K线：表示当前收盘价在N日最低和最高之间所处的位置，数值范围为 [0, 100]。
        - D线：为M日K值的移动平均，数值范围同样为 [0, 100]。
        - J线：由公式 J = 3D - 2K 得出，对价格波动更敏感。

        解释：
        - 若 J > 100：说明收盘价接近高点，但平均值趋缓，可能处于超买区域。
        - 若 J < 0：说明收盘价接近低点，但均值上升，可能处于超卖区域。
        """

        # Calculate the Raw Stochastic Value (RSV)
        df['Lowest'] = df[observation_item_l].rolling(window=period_n).min()
        df['Highest'] = df[observation_item_h].rolling(window=period_n).max()

        df.insert(0, 'RSV', (df[observation_item] - df['Lowest'])
                  / (df['Highest'] - df['Lowest']) * 100)

        # Calculate the K line (n-day EMA of RSV)
        df.insert(1, 'K', df['RSV'].ewm(alpha=1 / period_m, adjust=False).mean())

        # Calculate the D line (m-day EMA of K line)
        df.insert(2, 'D', df['K'].ewm(alpha=1 / period_m, adjust=False).mean())

        # Calculate the J line
        df.insert(3, 'J', 3 * df['K'] - 2 * df['D'])

        df.insert(4, 'KDJGF', df['J'] <= 0)
        df.insert(5, 'KDJIF', df['J'] >= 100)

        overview_dict = {
            'K': df['K'].iloc[-1],
            'D': df['D'].iloc[-1],
            'J': df['J'].iloc[-1],
            'KDJGF': df['KDJGF'].iloc[-1],
            'KDJIF': df['KDJIF'].iloc[-1],
            'Lowest': df['Lowest'].iloc[-1],
            'Highest': df['Highest'].iloc[-1],
        }

        return df, overview_dict

    @staticmethod
    def validate_kdj(df: pd.DataFrame,
                     observation_item,
                     observation_item_l,
                     observation_item_h,
                     period_n,
                     period_m,
                     target,
                     validated_period):

        validated_df = pd.DataFrame([])

        validated_df[observation_item] = df[observation_item]
        validated_df['J'] = df['J']
        validated_df['KDJGF'] = df['KDJGF']
        validated_df[target] = df[target]

        summary_dict = {}

        # PWGFR: the revenue in the next week
        validated_df['KDJGFRS'] = (df['KDJGF'] * (df[target].shift(0 - validated_period).rolling(
                    window=validated_period).sum()))

        summary_dict['Validated_KDJGFRS'] = validated_df['KDJGFRS'].sum()

        return validated_df, summary_dict

    @staticmethod
    def calculate_rsi(df:pd.DataFrame, observation_item, period_list=[]):
        """
        The Relative Strength Index (RSI) is a popular momentum oscillator used in technical analysis
        to measure the speed and change of price movements. It is typically used to identify overbought
        or oversold conditions in a market.

        Extension: This method also can be extended to measure the relative change of other indicators,
        such as Volume.

        通过一定时期内股价的变动情况来计算对比市场的买卖力量，进行判断股市的供需关系，推测股价走势
        RSI： 大于 80% 强市，主卖
             等于 50% 疲软
              小于 20% 极弱， 主买
        :return:
        """
        # Separate the gains and losses
        df['Gain'] = df[observation_item].where(df[observation_item] > 0, 0)
        df['Loss'] = -df[observation_item].where(df[observation_item] < 0, 0)


        # Calculate the average gain and average loss over a 14-day period
        overview_dict = {}

        for period in reversed(period_list):

            # Calculate the RSI
            df.insert(0, f'RSI{period}D', df['Gain'].rolling(window=period).mean() * 100
                      / (df['Gain'].rolling(window=period).mean() + df['Loss'].rolling(window=period).mean()))

            overview_dict[f'RSI{period}D'] = df[f'RSI{period}D'].iloc[-1]

        return df, overview_dict

    @staticmethod
    def calculate_vr(df:pd.DataFrame, observation_item, indicator_prefix, period_list):
        """
        VR (Volume Ratio) is a technical indicator used to measure the relative strength of an asset’s
        price movements, taking into account the volume of trades. It is mainly used in stock trading
        and aims to assess whether an asset's price movement is supported by strong or weak volume.

        Extension: This method also can be extended to measure the absolute change amplitude of other indicators,
        such as fund flow

        """
        vr_dict = {}
        for period in reversed(period_list):
            df[f'{indicator_prefix}BasicVolume{period}D'] = (
                df[observation_item].ewm(span=period, adjust=False).mean())

            df.insert(0, f'{indicator_prefix}SR{period}D',
                      np.where(df[f'{indicator_prefix}BasicVolume{period}D'] == 0,
                               np.nan, df['Volume'] / df[f'{indicator_prefix}BasicVolume{period}D']))

            df.insert(1, f'{indicator_prefix}CR{period}D',
                      np.where(df[observation_item].shift(1) == 0,
                               np.nan,
                               (df[observation_item] - df[observation_item].shift(1)) / df[observation_item].shift(1)))

            vr_dict = vr_dict | {
                f'{indicator_prefix}BasicVolume{period}D': df[f'{indicator_prefix}BasicVolume{period}D'].iloc[-1],
                f'{indicator_prefix}SR{period}D': df[f'{indicator_prefix}SR{period}D'].iloc[-1],
                f'{indicator_prefix}CR{period}D': df[f'{indicator_prefix}CR{period}D'].iloc[-1]}

        return df, vr_dict

    @staticmethod
    def find_tp_relationship_between_price_and_fund(df:pd.DataFrame):
        """
        discover the turning points of price and funds flow
        :return:
        """

        intern = 20

        max1, min1, _ = df.discover_extreme_points(df.tail(intern)['FundFlowMNI5DMA'].to_numpy())
        max2, min2, _ = df.discover_extreme_points(df.tail(intern)['FundFlowMNI'].to_numpy())
        max3, min3, _= df.discover_extreme_points(df.tail(intern)['PriceCR'].to_numpy())

        x = mdates.date2num(df.tail(intern)['Date'])
        y1 = df.tail(intern)['FundFlowMNI5DMA'].to_numpy()
        y2 = df.tail(intern)['FundFlowMNI'].to_numpy()
        y3 = df.tail(intern)['PriceCR'].to_numpy()
        # Plot group lines
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()

        # --- Group 1 & 2 on left Y-axis ---
        line1, = ax1.plot(x, y1, label='Mean-Funds', color='blue')
        line2, = ax1.plot(x, y2, label='Spot-Fund', color='orange')
        s1_max = ax1.scatter(x[max1], y1[max1], color='Red', marker='^', label='Mean-Funds Max')
        s1_min = ax1.scatter(x[min1], y1[min1], color='Green', marker='v', label='Mean-Funds Min')
        s2_max = ax1.scatter(x[max2], y2[max2], color='Red', marker='^', label='Spot-Fund Max')
        s2_min = ax1.scatter(x[min2], y2[min2], color='Green', marker='v', label='Spot-Fund Min')

        # --- Group 3 on right Y-axis ---
        line3, = ax2.plot(x, y3, label='Stock-Price', color='black')
        s3_max = ax2.scatter(x[max3], y3[max3], color='Red', marker='^', label='Stock-Price Max')
        s3_min = ax2.scatter(x[min3], y3[min3], color='Green', marker='v', label='Stock-Price Min')

        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

        # Combine all into one legend
        handles = [line1, line2, line3]
        labels = [h.get_label() for h in handles]
        legend = ax2.legend(handles, labels, loc='upper right')

        # Axis labels
        ax1.set_ylabel("Fund flow")
        ax2.set_ylabel("Price")
        ax1.set_title("Two Y-Axis Plot with Extrema")

        # Make legend items interactive
        lined = {legline: origline for legline, origline in zip(legend.get_lines(), handles)}
        for legline in legend.get_lines():
            legline.set_picker(True)
            legline.set_pickradius(5)

        # Pick event: toggle line visibility (ignore picks on text annotations)
        def on_pick(event):
            legline = event.artist
            if not isinstance(legline, Line2D):
                return  # Ignore picks that are not legend lines

            origline = lined.get(legline)
            if origline is None:
                return

            visible = not origline.get_visible()
            origline.set_visible(visible)
            legline.set_alpha(1.0 if visible else 0.2)
            fig.canvas.draw()

        fig.canvas.mpl_connect('pick_event', on_pick)

        # Add interactive cursor tooltips
        cursor = mplcursors.cursor(handles, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            x, y = sel.target
            date_str = mdates.num2date(x).strftime('%Y-%m-%d')
            sel.annotation.set_text(f"Date: {date_str}\nValue: {y:.2f}")

        # Grid and layout
        ax1.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def fibonacci_retrace_level(filename):

        df = pd.read_csv(filename)
        # Identify swing high and low (manual or programmatic)
        swing_low = df['Close'].min()
        swing_high = df['Close'].max()

        # Calculate Fibonacci levels
        diff = swing_high - swing_low
        fib_levels = {
            '0.0%': swing_high,
            '23.6%': swing_high - 0.236 * diff,
            '38.2%': swing_high - 0.382 * diff,
            '50.0%': swing_high - 0.500 * diff,
            '61.8%': swing_high - 0.618 * diff,
            '78.6%': swing_high - 0.786 * diff,
            '100.0%': swing_low
        }

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(df['Close'], label='Close Price', color='blue')
        for level, price in fib_levels.items():
            plt.axhline(price, label=f'Fibo {level} = {price:.2f}', linestyle='--')

        plt.title(f'Fibonacci Retracement Levels')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    obj = StatisticsIndicator()

    create_directory(obj.indicator_signal_dir)
    """
    active_indicator_list = list(obj.indicator_signal_dict.keys())

    obj.refresh_active_indicator(active_indicator_list)

    walk_directory(obj.basic_config['sector']['price_and_fund_merger_dir'], obj.evaluate_single_project)

    obj.indicator_signal_df.to_csv(obj.indicator_signal_dir + 'overview.csv')
    """


