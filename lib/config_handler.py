#
# config_handler.py
# Brief: Module to handle config file
#

import app_logger
import json

__CONFIG_FILE_PATH = "/config/sys_cfg.json"
__log = app_logger.get_logger(__name__)

def get_ssid():
    f = open(__CONFIG_FILE_PATH, 'r')
    json_data = json.loads(f.read())
    __log.debug(f"Read ssid from json: {json_data["ssid"]}")
    return json_data["ssid"]

def get_pssw():
    f = open(__CONFIG_FILE_PATH, 'r')
    json_data = json.loads(f.read())
    __log.debug(f"Read pssw from json: {json_data["pssw"]}")
    return json_data["pssw"]

def get_utc_offset():
    f = open(__CONFIG_FILE_PATH, 'r')
    json_data = json.loads(f.read())
    __log.debug(f"Read utc_offset from json: {json_data["utc_offset"]}")
    return json_data["utc_offset"]

def set_ssid(new_ssid):
    f = open(__CONFIG_FILE_PATH, 'r')
    json_data = json.loads(f.read())
    f.close()
    json_data["ssid"] = new_ssid
    f = open(__CONFIG_FILE_PATH, 'w')
    f.write(json.dumps(json_data))
    f.close()
    __log.debug(f"Read set ssid in json data: {new_ssid}")

def set_pssw(new_pssw):
    f = open(__CONFIG_FILE_PATH, 'r')
    json_data = json.loads(f.read())
    f.close()
    json_data["pssw"] = new_pssw
    f = open(__CONFIG_FILE_PATH, 'w')
    f.write(json.dumps(json_data))
    f.close()
    __log.debug(f"Set pssw in json data: {new_pssw}")

def set_utc_offset(new_utc_offset):
    f = open(__CONFIG_FILE_PATH, 'r')
    json_data = json.loads(f.read())
    f.close()
    json_data["utc_offset"] = new_utc_offset
    f = open(__CONFIG_FILE_PATH, 'w')
    f.write(json.dumps(json_data))
    f.close()
    __log.debug(f"Set utc_offset in json data: {new_utc_offset}")

# EOF
