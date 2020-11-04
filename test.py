from datetime import datetime
from datetime import timedelta
def getHourlyChime(dt, step=0):
    """
    计算整小时的时间
    :param step: 往前或往后跳跃取整值，默认为0，即当前所在的时间，正数为往后，负数往前。
                例如：
                step = 0 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:21
                step = 1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:22
                step = -1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:20
    :return: 整理后的时间戳
    """
    # 整小时
    td = timedelta(days=0, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0, minutes=dt.minute, hours=-step, weeks=0)
    print(td)
    new_dt = dt - td
    return new_dt
    '''
    print(new_dt)
    new_dt = dt
    timestamp = new_dt.timestamp()  # 对于 python 3 可以直接使用 timestamp 获取时间戳
    return timestamp
    '''
a = "20140317055456"
time = datetime.strptime(a, '%Y%m%d%H%M%S')
print(getHourlyChime(time))
ONEHOUREND = datetime.strptime("2020010101000", '%Y%m%d%H%M%S')

ONEHOURBEGIN = datetime.strptime("2020010100000", '%Y%m%d%H%M%S')
print(ONEHOURBEGIN)
print(ONEHOUREND)
ONEHOURTIME = ONEHOUREND-ONEHOURBEGIN
print(ONEHOURTIME)