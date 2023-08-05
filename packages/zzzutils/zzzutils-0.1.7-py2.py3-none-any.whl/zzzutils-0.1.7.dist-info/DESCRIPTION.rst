Requests: Python utils - Time
=========================

Get demand time from all kinds of original time format after delay without specified type.

Usage
---------------

def get_time(ts=None, delay=0, fmt=19)

Arguments: [original_time] [delay] [output_fmt:{0,6,8,10,16,17,19}]

output_fmt:
    19: '%Y-%m-%d %H:%M:%S',
    8: '%Y%m%d',
    6: '%Y%m',
    10: '%Y-%m-%d',
    16: '%Y-%m-%d %H:%M',
    17: '%Y%m%d-%H:%M:%S'


Input format(Any one of them)
------------

#   201809
#   20180910
#   2018-09-10
#   2018-09-10 18:00
#   20180910-18:00:00
#   2018-09-10 18:00:00
#   1536573600(int)
#   1536573600.00(float)

Return format(Any one of them)
-------------

#   201809
#   20180910
#   2018-09-10
#   2018-09-10 18:00
#   20180910-18:00:00
#   2018-09-10 18:00:00
#   1536573600(int)


