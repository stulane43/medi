from datetimerange import DateTimeRange
from datetime import date

morning_start_time = "05:00"
morning_end_time = "16:00"
night_start_time = "16:01"
night_end_time = "23:59"

def splitDate_getTime(date_time):
    split_time = str(date_time).split(' ')
    _time = split_time[-1]
    return _time

def time_in_range(time_given):
    if time_given in DateTimeRange(morning_start_time, morning_end_time):
        return "Received Morning Medication Medication  :sunny:"
    elif time_given in DateTimeRange(night_start_time, night_end_time):
        return "Received Night Medication  :new_moon:"
    else:
        return "Received Night Medication :moon:"
    
def get_todays_date():
    today = date.today()
    str_today = f"{today.year}-{today.month}-{today.day}"
    return str_today

def splitDateTime_getHoursMinutes(_time):
    split_time = str(_time).split(':')
    split_time_again = split_time[0].split(' ')
    return {"hour": split_time_again[-1], "minute": split_time[1]}

def splitTime_getHoursMinutes(_time):
    split_time = str(_time).split(':')
    return {"hour": split_time[0], "minute": split_time[1]}