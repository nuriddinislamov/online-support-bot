import pandas as pd
import datetime


def generate_date_slots():
    today = datetime.datetime.today()
    dates = []
    for i in range(1, 9):
        date = today + datetime.timedelta(days=i)
        if date.isoweekday() == 7:
            continue
        dates.append(date.strftime('%d-%m-%Y'))
    return dates


def generate_time_slots():
    return (pd.DataFrame(columns=['NULL'],
                         index=pd.date_range('2022-07-18T13:00:00Z', '2022-07-18T20:00:00Z',
                                             freq='30T'))
            .between_time('13:00', '20:00')
            .index.strftime('%H:%M')
            .tolist()
            )
