import pandas as pd

from src.StockAgent.common.abstract_indicator_tools import IndicatorTools


class BullishReversal(IndicatorTools):

    """
    identify bullish signals that there may be a reversal from bearish market to bullish market
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def identify_hammer(df:pd.DataFrame, target):

        """
        Hammer Pattern Characteristics:
        1. Small body near the top of the candle.
        2. Long lower shadow, at least twice the size of the body.
        3. Little or no upper shadow.
        A Hammer often signals a potential bullish reversal after a downtrend,
        suggesting that sellers were in control for most of the session,
        but buyers pushed the price up before the close.
        """

        df[target] = 0
        for i in range(1, len(df)):
            open_price = df['Open'].iloc[i]
            close_price = df['Close'].iloc[i]
            high_price = df['High'].iloc[i]
            low_price = df['Low'].iloc[i]

            # Small body condition: body size is <= 30% of the total candle height
            body_size = abs(close_price - open_price)
            candle_height = high_price - low_price

            # Check if the body size is <= 30% of candle height
            if body_size / candle_height <= 0.3:
                # Long lower shadow condition: lower shadow is at least twice the body size
                lower_shadow = min(open_price, close_price) - low_price
                if lower_shadow >= 2 * body_size:
                    # Small or no upper shadow
                    upper_shadow = high_price - max(open_price, close_price)
                    if upper_shadow <= body_size:
                        df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_bullish_engulfing(df:pd.DataFrame, target):

        """
        Bullish Engulfing Pattern Characteristics:
        First candle: A small bearish (down) candle, where the close is lower than the open.
        Second candle: A larger bullish (up) candle that completely engulfs the body of the previous bearish candle.
        In other words, the open of the second candle is lower than the close of the first,
        and the close of the second candle is higher than the open of the first candle.
        :return:
        """
        df[target] = 0
        for i in range(1, len(df)):
            # First candle (previous day)
            open1 = df['Open'].iloc[i - 1]
            close1 = df['Close'].iloc[i - 1]

            # Second candle (current day)
            open2 = df['Open'].iloc[i]
            close2 = df['Close'].iloc[i]

            # Conditions for Bullish Engulfing:
            if close1 < open1 and close2 > open2:  # Second candle is bullish, first is bearish
                if open2 < close1 and close2 > open1:  # Second candle engulfs first candle's body
                    df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_morning_star(df:pd.DataFrame, target):

        """
        Morning Star Characteristics:
        First candle: A large bearish (down) candle, typically showing strong selling pressure.
        Second candle: A small-bodied candle, either bullish or bearish, indicating indecision or a pause in the downward momentum. The candle could be a Doji or a small bearish/bullish candle.
        Third candle: A large bullish (up) candle that closes well above the midpoint of the first candle. This suggests that the buyers have gained control and a reversal is likely.
        Conditions for the Morning Star:
        The third candle must be bullish and close above the midpoint of the first candle.
        The first candle is bearish, and the second candle is a small-bodied candle.
        It should appear after a downtrend.
        :return:
        """
        df[target] = 0
        for i in range(2, len(df)):
            # First candle (previous to previous)
            open1 = df['Open'].iloc[i - 2]
            close1 = df['Close'].iloc[i - 2]

            # Second candle (previous)
            open2 = df['Open'].iloc[i - 1]
            close2 = df['Close'].iloc[i - 1]

            # Third candle (current)
            open3 = df['Open'].iloc[i]
            close3 = df['Close'].iloc[i]

            # Condition for Morning Star:
            if close1 < open1 and close2 < open2:  # First and second candles must be bearish
                # Second candle is small-bodied
                body2_size = abs(close2 - open2)
                candle2_height = df['High'].iloc[i - 1] - df['Low'].iloc[i - 1]
                if body2_size <= 0.2 * candle2_height:
                    # Third candle is bullish and closes above the midpoint of the first candle
                    if close3 > open3 and close3 > (open1 + close1) / 2:
                        df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_piercing_line(df:pd.DataFrame, target):

        """
        Piercing Line Pattern Characteristics:
        First candle: A long bearish candle (Close1 < Open1), continuing the current downtrend.
        Second candle:
        Opens below the low of the first candle (gap down).
        Closes above the midpoint of the first candle’s body (but not above the open).
        This pattern suggests that buyers are stepping in strongly, potentially reversing the trend.
        :return:
        """
        df[target] = 0
        for i in range(1, len(df)):
            open1, close1 = df['Open'].iloc[i - 1], df['Close'].iloc[i - 1]
            open2, close2 = df['Open'].iloc[i], df['Close'].iloc[i]

            # First candle bearish, second bullish
            if close1 < open1 and close2 > open2:
                midpoint = (open1 + close1) / 2
                if (open2 < close1
                        and midpoint < close2 < open1):
                    df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_inverted_hammer(df:pd.DataFrame, target):

        """
        Inverted Hammer Characteristics:
        Appears after a downtrend.
        Has a small real body near the low of the day.
        Has a long upper shadow (at least 2× the body size).
        Has little or no lower shadow.
        Can be either green (bullish) or red (bearish), though green is stronger.

        We’ll define these rules in code:

        Small body: abs(Close - Open) <= 0.3 * (High - Low)
        Long upper shadow: High - max(Open, Close) > 2 * abs(Open - Close)
        Small lower shadow: min(Open, Close) - Low <= 0.1 * (High - Low)
        (Optional) Ensure recent candles are in a downtrend.
        """

        df[target] = 0
        for i in range(1, len(df)):
            o = df['Open'].iloc[i]
            c = df['Close'].iloc[i]
            h = df['High'].iloc[i]
            l = df['Low'].iloc[i]
            body = abs(c - o)
            candle_range = h - l
            upper_shadow = h - max(o, c)
            lower_shadow = min(o, c) - l

            # Conditions for Inverted Hammer
            if body <= 0.3 * candle_range and \
                    upper_shadow >= 2 * body and \
                    lower_shadow <= 0.1 * candle_range:
                # (Optional) Check previous candle is bearish
                prev_close = df['Close'].iloc[i - 1]
                prev_open = df['Open'].iloc[i - 1]
                if prev_close < prev_open:  # Downtrend support
                    df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_three_white_soldiers(df:pd.DataFrame, target):

        """
        Pattern Characteristics:
        Three consecutive bullish candles (Close > Open).
        Each candle closes higher than the previous candle’s close.
        Each candle opens within the real body of the previous candle.
        Candles ideally have small wicks — indicating strong buying with little selling resistance.

        For candles at positions i-2, i-1, and i:

        All 3 are bullish: Close > Open
        Candle[i] opens within body of Candle[i-1]
        Candle[i-1] opens within body of Candle[i-2]
        Close[i] > Close[i-1] > Close[i-2]
        (Optional) Avoid very long wicks or overbought gaps

        """
        df[target] = 0
        for i in range(2, len(df)):
            o1, c1 = df['Open'].iloc[i - 2], df['Close'].iloc[i - 2]
            o2, c2 = df['Open'].iloc[i - 1], df['Close'].iloc[i - 1]
            o3, c3 = df['Open'].iloc[i], df['Close'].iloc[i]

            # All 3 are bullish
            if c1 > o1 and c2 > o2 and c3 > o3:
                # Opens within body of previous candle
                if o2 >= o1 and o2 <= c1 and o3 >= o2 and o3 <= c2:
                    # Closes successively higher
                    if c2 > c1 and c3 > c2:
                        df.at[df.index[i], target] = 1

        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def is_doji(open_price, close_price, high, low, threshold=0.1):
        body = abs(close_price - open_price)
        range_ = high - low
        return body <= threshold * range_

    @staticmethod
    def identify_morning_doji_star(df:pd.DataFrame, target):

        """
        Morning Doji Star Pattern Components:
        Candle 1: Long bearish candle continuing the downtrend.
        Candle 2 (Doji):
        Small real body (Open ≈ Close)
        Gaps down from the first candle.
        Candle 3: Strong bullish candle that closes well into the body of the first candle (ideally above its midpoint).

        Pattern Requirements in Code Terms:
        For candles at i-2, i-1, and i:

        i-2: Large red candle → Close2 < Open2 and large body.
        i-1: Doji → abs(Close1 - Open1) < small_threshold
        i: Large green candle → Close0 > Open0, and Close0 > (Open2 + Close2)/2
        You can define body size and "doji-ness" relative to candle range.
        """

        df[target] = 0
        for i in range(2, len(df)):
            o2, c2, h2, l2 = df.iloc[i - 2][['Open', 'Close', 'High', 'Low']]
            o1, c1, h1, l1 = df.iloc[i - 1][['Open', 'Close', 'High', 'Low']]
            o0, c0, h0, l0 = df.iloc[i][['Open', 'Close', 'High', 'Low']]

            body2 = abs(c2 - o2)

            # Candle 1: large bearish
            if c2 < o2 and body2 > 0.6 * (h2 - l2):
                # Candle 2: doji
                if BullishReversal.is_doji(o1, c1, h1, l1, threshold=0.1):
                    # Candle 3: bullish engulfing candle
                    midpoint = (o2 + c2) / 2
                    if c0 > o0 and c0 > midpoint:
                        df.at[df.index[i], target] = 1

        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_tweezer_bottom(df:pd.DataFrame, target, tolerance):

        """
        Tweezer Bottom Characteristics:
        Occurs after a downtrend.
        Two consecutive candles:
        Candle 1: bearish (Close < Open)
        Candle 2: bullish (Close > Open)
        Both candles have similar lows (within a small tolerance).
        Second candle opens below or near the first candle's close and then closes higher (bullish confirmation).
        """

        df[target] = 0
        for i in range(1, len(df)):
            o1, c1, l1, h1 = df.iloc[i - 1][['Open', 'Close', 'Low', 'High']]
            o2, c2, l2, h2 = df.iloc[i][['Open', 'Close', 'Low', 'High']]

            range1 = h1 - l1
            range2 = h2 - l2
            avg_range = (range1 + range2) / 2

            # First candle bearish, second bullish
            if c1 < o1 and c2 > o2:
                # Lows nearly equal
                if abs(l1 - l2) <= tolerance * avg_range:
                    df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}


class BearishReversal(IndicatorTools):

    """
    identify Bearish signals that there may be a reversal from bullish market to bearish market
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def identify_shooting_star(df:pd.DataFrame, target):

        """
        Shooting Star Characteristics:
        Appears after an uptrend.
        Small real body near the low of the day.
        Long upper shadow, typically at least 2× the size of the real body.
        Little or no lower shadow.
        The candle can be either red or green, but red is more bearish.
        """
        df[target] = 0
        for i in range(1, len(df)):
            o, c, h, l = df.iloc[i][['Open', 'Close', 'High', 'Low']]
            body = abs(c - o)
            candle_range = h - l
            upper_shadow = h - max(o, c)
            lower_shadow = min(o, c) - l

            # Shooting star criteria
            if body <= 0.3 * candle_range and \
                    upper_shadow >= 2 * body and \
                    lower_shadow <= 0.1 * candle_range:
                # Optional: previous candle was bullish (uptrend continuation)
                prev_close = df['Close'].iloc[i - 1]
                prev_open = df['Open'].iloc[i - 1]
                if prev_close > prev_open:  # prior bullish candle
                    df.at[df.index[i], target] = 1

        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_bearish_engulfing(df:pd.DataFrame, target):

        """
        Bearish Engulfing Pattern Characteristics:
        Candle 1 (bullish):
        Small body: Close1 > Open1
        Candle 2 (bearish):
        Large body: Close2 < Open2
        Fully engulfs the body of Candle 1 (i.e., Open2 > Close1 and Close2 < Open1)
        Appears after an uptrend or rally.
        """

        df[target] = 0
        for i in range(1, len(df)):
            o1, c1 = df.iloc[i - 1]['Open'], df.iloc[i - 1]['Close']
            o2, c2 = df.iloc[i]['Open'], df.iloc[i]['Close']

            # First candle bullish, second bearish
            if c1 > o1 and c2 < o2:
                # Second body engulfs first body
                if o2 > c1 and c2 < o1:
                    df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_evening_star(df:pd.DataFrame, target):

        """
        Evening Star Pattern Characteristics:
        Candle 1: Large bullish candle (Close > Open)
        Candle 2: Small body (bullish, bearish, or doji) — shows indecision
        Candle 3: Large bearish candle (Close < Open), which closes well into Candle 1's body
        Appears after an uptrend
        """

        df[target] = 0
        for i in range(2, len(df)):
            o1, c1, h1, l1 = df.iloc[i - 2][['Open', 'Close', 'High', 'Low']]
            o2, c2, h2, l2 = df.iloc[i - 1][['Open', 'Close', 'High', 'Low']]
            o3, c3, h3, l3 = df.iloc[i][['Open', 'Close', 'High', 'Low']]

            body1 = abs(c1 - o1)
            body2 = abs(c2 - o2)
            body3 = abs(c3 - o3)
            range2 = h2 - l2

            # Candle 1: large bullish
            if c1 > o1 and body1 > 0.6 * (h1 - l1):
                # Candle 2: small real body
                if body2 < 0.3 * range2:
                    # Candle 3: bearish candle closing below midpoint of Candle 1
                    midpoint1 = (o1 + c1) / 2
                    if c3 < o3 and c3 < midpoint1:
                        df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_dark_cloud_cover(df:pd.DataFrame, target):

        """
        Dark Cloud Cover Pattern Characteristics:
        Candle 1: Strong bullish candle (Close1 > Open1)
        Candle 2:
            Opens above the high or close of Candle 1 (gap up)
            Closes well into Candle 1’s body, ideally below its midpoint
            Is a bearish candle (Close2 < Open2)
        Appears after an uptrend
        """

        df[target] = 0
        for i in range(1, len(df)):
            o1, c1 = df.iloc[i - 1]['Open'], df.iloc[i - 1]['Close']
            o2, c2 = df.iloc[i]['Open'], df.iloc[i]['Close']

            if c1 > o1 and c2 < o2:  # bullish first, bearish second
                if o2 > c1 and c2 < ((o1 + c1) / 2):  # gap up and closes below midpoint
                    df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_gravestone_doji(df:pd.DataFrame, target, tolerance):

        """
        Gravestone Doji Characteristics:
        The open, low, and close prices are nearly the same.
        The high is significantly higher — forming a long upper shadow.
        Appears after an uptrend (ideally).
        Indicates potential trend reversal due to bullish exhaustion.
        """

        df[target] = 0
        for i in range(len(df)):
            o, c, h, l = df.iloc[i][['Open', 'Close', 'High', 'Low']]
            body = abs(c - o)
            candle_range = h - l

            if candle_range == 0:
                continue

            body_ratio = body / candle_range
            upper_shadow = h - max(o, c)
            lower_shadow = min(o, c) - l

            if (body_ratio <= tolerance
                    and upper_shadow >= 2 * body
                    and lower_shadow <= tolerance * candle_range):

                df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_three_black_crows(df:pd.DataFrame, target):

        """
        Three Black Crows Pattern Characteristics:
        Three consecutive bearish candles:
        Each opens within or near the previous candle's body.
        Each closes lower than the previous.
        Ideally, each candle has a long real body with little or no lower shadow.
        Appears after an uptrend (but can appear in other contexts with lower strength).
        """

        df['Three_Black_Crows'] = 0
        for i in range(2, len(df)):
            o1, c1 = df.iloc[i - 2]['Open'], df.iloc[i - 2]['Close']
            o2, c2 = df.iloc[i - 1]['Open'], df.iloc[i - 1]['Close']
            o3, c3 = df.iloc[i]['Open'], df.iloc[i]['Close']

            # Three bearish candles
            if c1 < o1 and c2 < o2 and c3 < o3:
                # All open within or near previous body
                if o2 <= o1 and o2 >= c1 and o3 <= o2 and o3 >= c2:
                    # Each close lower than previous
                    if c2 < c1 and c3 < c2:
                        df.at[df.index[i], 'Three_Black_Crows'] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_tweezer_top(df:pd.DataFrame, target, tolerance):

        """
        Tweezer Top Characteristics:
        Appears after an uptrend
        Two consecutive candles:
        Candle 1: Bullish (Close > Open)
        Candle 2: Bearish (Close < Open)
        Highs of both candles are nearly equal (within a small tolerance)
        Suggests buyers were rejected at the same high level on both days
        """

        df[target] = 0
        for i in range(1, len(df)):
            o1, c1, h1 = df.iloc[i - 1][['Open', 'Close', 'High']]
            o2, c2, h2 = df.iloc[i][['Open', 'Close', 'High']]

            if c1 > o1 and c2 < o2:  # bullish then bearish
                if abs(h1 - h2) <= tolerance * (c2 - o2):  # similar highs
                    df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}


class ContinuationTrend(IndicatorTools):

    def __init__(self):
        super().__init__()

    @staticmethod
    def identify_rising_three_methods(df:pd.DataFrame, target):

        """
        Rising Three Methods Characteristics:
        Candle 1: Long bullish candle
        Candles 2–4: Small-bodied candles (bullish or bearish) that stay within the range of Candle 1
        Candle 5: Strong bullish candle that closes above Candle 1’s high
        """
        df[target] = 0
        for i in range(4, len(df)):
            o1, c1, h1, l1 = df.iloc[i - 4][['Open', 'Close', 'High', 'Low']]
            o2, c2, h2, l2 = df.iloc[i - 3][['Open', 'Close', 'High', 'Low']]
            o3, c3, h3, l3 = df.iloc[i - 2][['Open', 'Close', 'High', 'Low']]
            o4, c4, h4, l4 = df.iloc[i - 1][['Open', 'Close', 'High', 'Low']]
            o5, c5 = df.iloc[i][['Open', 'Close']]

            # Candle 1: bullish and large
            if c1 > o1 and (c1 - o1) > (h1 - l1) * 0.5:
                # Candles 2-4: all within Candle 1's range
                if all(l1 <= l <= h <= h1 for l, h in [(l2, h2), (l3, h3), (l4, h4)]):
                    # Candle 5: bullish close above Candle 1 high
                    if c5 > o5 and c5 > h1:
                        df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_falling_three_methods(df:pd.DataFrame, target):

        """
        Falling Three Methods Pattern Characteristics:
        Candle 1: Large bearish candle (strong down move).
        Candles 2–4: Small-bodied candles (bullish or bearish) that stay within the range of Candle 1.
        Candle 5: Strong bearish candle that closes below Candle 1’s low.
        This shows a pause in a downtrend where bulls attempt to rally but fail, and bears regain control.
        """

        df[target] = 0
        for i in range(4, len(df)):
            o1, c1, h1, l1 = df.iloc[i - 4][['Open', 'Close', 'High', 'Low']]
            o2, c2, h2, l2 = df.iloc[i - 3][['Open', 'Close', 'High', 'Low']]
            o3, c3, h3, l3 = df.iloc[i - 2][['Open', 'Close', 'High', 'Low']]
            o4, c4, h4, l4 = df.iloc[i - 1][['Open', 'Close', 'High', 'Low']]
            o5, c5 = df.iloc[i][['Open', 'Close']]
            l5 = df.iloc[i]['Low']

            # Candle 1: large bearish
            if c1 < o1 and (o1 - c1) > (h1 - l1) * 0.5:
                # Candles 2–4: within Candle 1's high-low range
                if all(l1 <= l <= h <= h1 for l, h in [(l2, h2), (l3, h3), (l4, h4)]):
                    # Candle 5: bearish and closes below Candle 1's low
                    if c5 < o5 and c5 < l1:
                        df.at[df.index[i], target] = 1
        return df, {target: df[target].iloc[-1]}

    @staticmethod
    def identify_rectangle(df:pd.DataFrame, target, tolerance, window, min_touches):

        """
        The Rectangle pattern in technical sector_analysis is a continuation or reversal pattern formed
        when price moves sideways between parallel support and resistance levels,
        creating a “box” or “rectangle” shape on the chart. It reflects a period of consolidation
        where bulls and bears are in balance before price eventually breaks out or breaks down.

        Rectangle Pattern Characteristics:
        Price oscillates between horizontal resistance (ceiling) and horizontal support (floor).
        Typically consists of at least two touches on each support and resistance levels.
        Volume usually decreases during the consolidation.
        Breakout direction (up or down) signals continuation or reversal.

        Rectangle Pattern Detection Concept:
        Identify support and resistance price levels where price repeatedly bounces.
        Confirm at least 2-3 touches on support and resistance.
        Duration: usually lasts for several bars/candles.
        """

        df[target] = 0  # initialize all zeros

        for start in range(len(df) - window):
            segment = df.iloc[start:start + window]
            highs = segment['High']
            lows = segment['Low']

            # Use mode of highs and lows as resistance and support candidates
            if not highs.mode().empty and not lows.mode().empty:
                res_level = round(highs.mode()[0], 2)
                sup_level = round(lows.mode()[0], 2)
            else:
                continue

            res_touches = sum(abs(highs - res_level) <= tolerance * res_level)
            sup_touches = sum(abs(lows - sup_level) <= tolerance * sup_level)

            if res_touches >= min_touches and sup_touches >= min_touches:

                # Mark rectangle rows in DataFrame as 1
                df.iloc[start:start + window, df.columns.get_loc('Rectangle')] = 1

        return df, {target: df[target].iloc[-1]}

class CandleStickManager(BullishReversal, BearishReversal, ContinuationTrend):

    def __init__(self):
        super().__init__()

if __name__ == '__main__':


    obj = CandleStickManager()
    """
    active_indicator_list = list(obj.indicator_signal_dict.keys())

    obj.refresh_active_indicator(active_indicator_list)

    walk_directory(obj.basic_config['etf']['price_and_fund_merger_dir'], obj.evaluate_single_project)

    obj.indicator_signal_df.to_csv(obj.indicator_signal_dir + 'overview.csv')
    """