#
# cli_handler.py
# Brief: Simple cli implementation to read config data
#

import app_logger
import time
import sys
import uselect
import config_handler as cfg

CLI_EVT_NEW_CFG = 0
CLI_EVT_RETRY_CONN = 1

CONNECTION_RETRY_CNT = 12

CMD_WIFI = 'w'
CMD_UTC = 'o'

__spoll = uselect.poll()
__log = app_logger.get_logger(__name__)

def __read_one():
    return(sys.stdin.read(1) if __spoll.poll(0) else None)

def run():
    __spoll.register(sys.stdin, uselect.POLLIN)
    recovery_cnt = 0
    while True:
        print(f"[RECOVERY] Select operation:\n - (w) input wifi paramenters\n - (o) input utc offset")
        rx_cmd = __read_one()
        if rx_cmd != None:
            if rx_cmd == CMD_WIFI:
                __spoll.unregister(sys.stdin)
                print(f"Wifi update command")
                print(f"Enter new SSID")
                ssid = sys.stdin.readline()
                ssid = ssid.rstrip()
                cfg.set_ssid(ssid)
                print(f"Enter new PSSW")
                pssw = sys.stdin.readline()
                pssw = pssw.rstrip()
                cfg.set_pssw(pssw)
                return CLI_EVT_NEW_CFG
            elif rx_cmd == CMD_UTC:
                __spoll.unregister(sys.stdin)
                print(f"Utc Offset command")
                print(f"Enter new utc offset:")
                utc_offset_str = sys.stdin.readline()
                try:
                    utc_offset = int(utc_offset_str)
                    print(f"New utc setup:")
                    print(f"- UTC_OFFSET: {utc_offset}")
                    cfg.set_utc_offset(utc_offset)
                    return CLI_EVT_NEW_CFG
                except:
                    __spoll.register(sys.stdin, uselect.POLLIN)
            else:
                print(f"Unknown cmd: {rx_cmd}")
        else:
            time.sleep(5)
            recovery_cnt += 1

        if recovery_cnt == CONNECTION_RETRY_CNT:
            __spoll.unregister(sys.stdin)
            print(f"Retry connection...")
            return CLI_EVT_RETRY_CONN

# EOF
