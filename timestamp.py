import datetime as dt
import time

def get_tte(date):
    #input date '%Y-%m-%d'
    #return time to expiration in years, expiration timestamp string, month of expiration(?)

    #-14440 because timestamps are off by exactly four hours for some reason
    exp_stamp = float(time.mktime(dt.datetime.strptime(date, '%Y-%m-%d').timetuple())-14400)
    exp_string = str(int(exp_stamp))
    #print('exp string : ', exp_string)
    now_stamp = float(convert_date(dt.datetime.now()))

    time_left = (exp_stamp - now_stamp)/(3600.0 * 24.0 * 365.0)


    return time_left, exp_string


print(dt.datetime.today().date())


#'%Y-%m-%d' (datetime object), returns str
def convert_date(day):
    day = dt.datetime.strftime(day, "%Y-%m-%d")
    return str(int(time.mktime(dt.datetime.strptime(day, "%Y-%m-%d").timetuple())))


