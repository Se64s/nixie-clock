# Nixie Clock

# FSM design

## FSM States

### CONNECTING

Initial state, device use the network config to try to stablish a internet connection.
If connection stablishment fails several times, a event to indicate an connection error should be generated.

Events:

 - evt_wifi_conn_error: Generated after several failrues at connecting to wifi ap.
 - evt_conn_success: Generated after connect to wifi ap.

### SYNC

State to get datetime from internet.

Events:

 - evt_ntp_conn_error: Generated after several failrues at retrieving datetime from ntp server.
 - evt_sync_success: Generated after connect to wifi ap.

### ONLINE

Device has a valid datetime. It can keep the hour until midnight.

Events:

- evt_midnight: Generate every day at 00:00:00. Device should sync.

### RECOVERY

Fallback state. The device had communication errors and config parameters should be check. In this state a minimal CLI is implemented to provide again config parameters:

- wifi_ssid
- wifi_pssw
- ntp_addr

Every 5 minutes, the system should valuate wifi cfg and ntp data to see if the system has recovered the normal state.

Events:

 - evt_new_config: Generated if the user provide a new configuration via CLI.
 - evt_system_recovered: Generated if the wifi connection is restablished and ntp server is online.

## FSM Event table summary

| Name | Current state | Next state | Cause |
| --- | --- | --- | --- |
| evt_wifi_conn_error | CONNECTING | RECOVERY |Generated after several failrues at connecting to wifi ap. |
| evt_conn_success | CONNECTING | SYNC | Generated after connect to wifi ap. |
| evt_ntp_conn_error | SYNC | RECOVERY | Generated after several failrues at retrieving datetime from ntp server. |
| evt_sync_success | SYNC | ONLINE | Generated after connect to wifi ap. |
| evt_midnight | ONLINE | SYNC | Generate every day at 00:00:00. Device should sync. |
| evt_new_config | RECOVERY | CONNECTING | Generated if the user provide a new configuration via CLI. |
| evt_system_recovered | RECOVERY | ONLINE | Generated if the wifi connection is restablished and ntp server is online. |
