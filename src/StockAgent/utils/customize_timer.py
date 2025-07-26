import time
from datetime import datetime, timedelta, date

def generate_validated_intern():
    refer_intern_dict = {"sgement"}

def last_day_of_last_season(backward = 0):
    today = date.today()
    year = today.year
    month = today.month

    total_month = year * 12 + month
    backward_month = total_month - backward * 3
    year = int((backward_month - 1) / 12)
    month = (backward_month - 1) % 12 + 1

    # Determine current season
    if month in [1, 2, 3]:  # Current: Q1, last season is Q4 of previous year
        last_season_end = date(year -1, 12, 31)
    elif month in [4, 5, 6]:  # Current: Q2, last season Q1
        last_season_end = date(year, 3, 31)
    elif month in [7, 8, 9]:  # Current: Q3, last season Q2
        last_season_end = date(year, 6, 30)
    else:  # Current: Q4, last season Q3
        last_season_end = date(year, 9, 30)

    return last_season_end.strftime('%Y%m%d')

def absolute_timer(minutes, callback, validated_intern={}):

    while True:
        end_time = datetime.now() + timedelta(minutes=minutes)
        while datetime.now() < end_time:
            remaining = end_time - datetime.now()
            mins, secs = divmod(remaining.seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end='\r')
            time.sleep(1)
        callback()

def my_callback():
    print(f'Callback function triggered at {datetime.now()}')

if __name__ == '__main__':
    # absolute_timer(1, my_callback)
    last_day_of_last_season(backward=1)

