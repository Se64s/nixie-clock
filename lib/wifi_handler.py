#
# wifi_handler.py
# Brief: Class to manage interaction with wifi interface.
#

import app_logger
import network
import time

__log = app_logger.get_logger(__name__)
__wlan = network.WLAN(network.STA_IF)
__ssid = ""
__pssw = ""
__n_conn = 5

def update_ssid(ssid):
    global __ssid
    __ssid = ssid
    __log.debug(f"Set ssid {__ssid}")

def update_pssw(pssw):
    global __pssw
    __pssw = pssw
    __log.debug(f"Set pssw {__pssw}")

def update_n_connect(n_conn):
    global __n_conn
    __n_conn = n_conn
    __log.debug(f"Set n_conn {__n_conn}")

def connect():
    global __wlan
    __log.debug(f"Connect to {__ssid} : {__pssw}")
    __wlan.active(True)
    __wlan.config(reconnects=__n_conn)
    if not __wlan.isconnected():
        __wlan.connect(__ssid, __pssw)
        nw_status = __wlan.status()
        while nw_status == network.STAT_CONNECTING:
            time.sleep(1)
            nw_status = __wlan.status()
            __log.debug(f"wlan status: {__wlan.status()}")
    return __wlan.isconnected()

def is_connected():
    return __wlan.isconnected()

# EOF
