#
# fsm_nixie.py
# Brief: Implementation of finite state machine for nixie clock
#

import fsm
import app_logger
import time
import config_handler as cfg
import wifi_handler
import sync_handler
import cli_handler
import nixie_driver

import nixie_handler
import ps_driver

# System states
STATE_CONNECTING = 0
STATE_SYNC = 1
STATE_ONLINE = 2
STATE_RECOVERY = 3
STATE_NONE = -1

__state_to_name = {
    STATE_CONNECTING: "CONNECTING",
    STATE_SYNC: "SYNC",
    STATE_ONLINE: "ONLINE",
    STATE_RECOVERY: "RECOVERY",
    STATE_NONE: "NONE",
}

# System events
EVT_WIFI_CONN_ERR = 0
EVT_WIFI_CONN_OK = 1
EVT_NTP_CONN_ERR = 2
EVT_NTP_CONN_OK = 3
EVT_MIDNIGHT = 4
EVT_NEW_CFG = 5
EVT_SYSTEM_RECOVERY = 6
EVT_NONE = -1

__event_to_name = {
    EVT_WIFI_CONN_ERR: "WIFI_CONN_ERR",
    EVT_WIFI_CONN_OK: "WIFI_CONN_OK",
    EVT_NTP_CONN_ERR: "NTP_CONN_ERR",
    EVT_NTP_CONN_OK: "NTP_CONN_OK",
    EVT_MIDNIGHT: "MIDNIGHT",
    EVT_NEW_CFG: "NEW_CFG",
    EVT_SYSTEM_RECOVERY: "SYSTEM_RECOVERY",
    EVT_NONE: "NONE",
}

# Internal methods ------------------------------------------------------------

# Internal vars ---------------------------------------------------------------

DATE_SECOND = 40
DATE_SHOW_TIME = 5

SYNC_HOUR = 3
SYNC_MIN = 0
SYNC_SEC = 0

CONNECT_MAX_CNT = 1

PIN_SER_DATA=5
PIN_SER_CLOCK=7
PIN_REG_CLOCK=6
PIN_EN_PS=10

dp_state = False

log = app_logger.get_logger(__name__)

nix = nixie_driver.NixieDisplay(pin_ser_data=PIN_SER_DATA, 
                                pin_ser_clock=PIN_SER_CLOCK, 
                                pin_reg_clock=PIN_REG_CLOCK)

ps = ps_driver.PoweSupply(PIN_EN_PS)

# Private functions -----------------------------------------------------------

def set_value_nixie(a, b, c, scroll=False, toggle_dp=False):
    if scroll:
        nixie_handler.scroll_to_value(nix, a, b, c)
    else:
        nixie_handler.set_value(nix, a, b, c)
    if toggle_dp:
        toggle_dp_value()

def toggle_dp_value():
    global dp_state
    global nix
    dp_state = not dp_state
    nixie_handler.set_dp(nix, dp_state)

def init_hardware():
    global dp_state
    global nix
    global ps
    dp_state = False
    # enable power supply
    ps.enable()
    # Setup init value on nixie
    nixie_handler.set_value(nix, 0, 0, 0)
    # Update dp
    nixie_handler.set_dp(nix, False)

# Handlers for defined states -------------------------------------------------

def __connecting_state_handler():
    log.debug(f"State: {__state_to_name[STATE_CONNECTING]}")
    log.debug(f"Read config data")
    wifi_handler.update_ssid(cfg.get_ssid())
    wifi_handler.update_pssw(cfg.get_pssw())
    sync_handler.update_offset(cfg.get_utc_offset())
    connect_cnt = 0
    while connect_cnt < CONNECT_MAX_CNT:
        if wifi_handler.connect():
            return EVT_WIFI_CONN_OK
        connect_cnt += 1
        toggle_dp_value()
        log.debug(f"Connetion attemp {connect_cnt}")
    return EVT_WIFI_CONN_ERR


def __sync_state_handler():
    log.debug(f"State: {__state_to_name[STATE_SYNC]}")
    if sync_handler.update_time():
        return EVT_NTP_CONN_OK
    else:
        return EVT_NTP_CONN_ERR

def __online_state_handler():
    log.debug(f"State: {__state_to_name[STATE_ONLINE]}")
    year, month, mday, hour, minute, second, weekday, yearday = sync_handler.get_time()
    if (hour == SYNC_HOUR) and (minute == SYNC_MIN) and (second == SYNC_SEC):
        return EVT_MIDNIGHT
    # Print date every minute
    if second == DATE_SECOND:
        set_value_nixie(mday, month, int(year % 100), scroll=True)
        for second in range(DATE_SHOW_TIME):
            toggle_dp_value()
            time.sleep(1)
        year, month, mday, hour, minute, second, weekday, yearday = sync_handler.get_time()
        set_value_nixie(hour, minute, second, scroll=True, toggle_dp=False)
    # Print time
    else:
        set_value_nixie(hour, minute, second, toggle_dp=True)
        time.sleep(1)
    return EVT_NONE

def __recovery_state_handler():
    log.debug(f"State: {__state_to_name[STATE_RECOVERY]}")
    cli_evt = cli_handler.run()
    if cli_evt == cli_handler.CLI_EVT_NEW_CFG:
        return EVT_NEW_CFG
    elif cli_evt == cli_handler.CLI_EVT_RETRY_CONN:
        return EVT_SYSTEM_RECOVERY
    else:
        return EVT_NONE

# Event handler ---------------------------------------------------------------

def __event_handler(current_state, input_evet):
    next_state = STATE_NONE

    log.debug(f"Manage event: {__event_to_name[input_evet]}")

    # State transition for state connecting
    if current_state is STATE_CONNECTING:
        if input_evet == EVT_WIFI_CONN_ERR:
            next_state = STATE_RECOVERY
        elif input_evet == EVT_WIFI_CONN_OK:
            next_state = STATE_SYNC
        else:
            next_state = STATE_CONNECTING
    
    # State transition for state sync
    elif current_state is STATE_SYNC:
        if input_evet == EVT_NTP_CONN_ERR:
            next_state = STATE_RECOVERY
        elif input_evet == EVT_NTP_CONN_OK:
            next_state = STATE_ONLINE
        else:
            next_state = STATE_SYNC
    
    # State transition for state online
    elif current_state is STATE_ONLINE:
        if input_evet == EVT_MIDNIGHT:
            next_state = STATE_SYNC
        else:
            next_state = STATE_ONLINE
    
    # State transition for state recovery
    elif current_state is STATE_RECOVERY:
        if input_evet == EVT_NEW_CFG:
            next_state = STATE_CONNECTING
        elif input_evet == EVT_SYSTEM_RECOVERY:
            next_state = STATE_ONLINE
        else:
            next_state = STATE_RECOVERY

    if next_state != current_state:
        log.debug(f"State update: {__state_to_name[current_state]} -> {__state_to_name[next_state]}")

    return next_state

# Collector of handlers -------------------------------------------------------

__state_handler_list = [
    __connecting_state_handler,
    __sync_state_handler,
    __online_state_handler,
    __recovery_state_handler,
]

# External execution point ----------------------------------------------------

def run():
    log.info(f"Start nixie app FSM")
    init_hardware()
    app_fsm = fsm.Fsm(STATE_CONNECTING, __state_handler_list, __event_handler)

    while True:
        new_event = app_fsm.execute_state()
        log.info(f"Processing event: {__event_to_name[new_event]}")
        if new_event != EVT_NONE:
            new_state = app_fsm.rise_event(new_event)

# EOF
