#
# sync_handler.py
# Brief: Class to manage ntp time sync
#

import app_logger
import ntptime
import utime

__log = app_logger.get_logger(__name__)
__utc_offset = 0

def update_offset(utc_offset):
    global __utc_offset
    __utc_offset = utc_offset
    __log.debug(f"UTC offset {__utc_offset}")

def update_time():
    try:
        ntptime.settime()
        __log.debug(f"Update local time")
        return True
    except:
        return False

def get_time():
    global __utc_offset
    dst = 0
    cur_year = utime.localtime()[0]
    start_dst = [cur_year,3,24,2,0,0,0,0]
    end_dst = [cur_year,10,24,3,0,0,0,0]
    start_dst[2] += 6 - utime.localtime(utime.mktime(start_dst))[6]
    end_dst[2] += 6 - utime.localtime(utime.mktime(end_dst))[6]
    start_dst = utime.mktime(start_dst)
    end_dst = utime.mktime(end_dst)
    if start_dst < (utime.time() + __utc_offset * 3600) < end_dst:
        dst = 1
    else:
        dst = 0
    localtime = utime.localtime(utime.time() + __utc_offset * 3600 + dst * 3600)
    __log.debug(f"localtime {localtime[0]}/{localtime[1]:02d}/{localtime[2]:02d} {localtime[3]:02d}:{localtime[4]:02d}:{localtime[5]:02d}")
    return localtime

# EOF
