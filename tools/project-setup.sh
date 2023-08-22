#!/bin/bash
# Get tool parameters
pyint=$1
pytoolpath=$2
pyport=$3
pybaudrate=$4
# Define project folders
pfolders=(
    "config"
    "lib"
)
# Define project sources
psources=(
    "config/sys_cfg.json"

    "lib/logging.py"
    "lib/app_logger.py"
    "lib/fsm.py"
    "lib/nixie_driver.py"
    "lib/nixie_handler.py"
    "lib/nixie_mask.py"
    "lib/ps_driver.py"
    "lib/shift_register_driver.py"
    "lib/cli_handler.py"
    "lib/config_handler.py"
    "lib/sync_handler.py"
    "lib/wifi_handler.py"
    
    "fsm_nixie.py"
    "main.py"
)
# Create folders
echo " - Setup project folders:"
for val1 in ${pfolders[*]}; do
    $pyint $pytoolpath "-d" $pyport "-b" $pybaudrate "-f" "mkdir" $val1
done
# Create sources
echo " - Copy sources into device:"
for val1 in ${psources[*]}; do
    $pyint $pytoolpath "-d" $pyport "-b" $pybaudrate "-f" "cp" $val1 :$val1
done

# EOF
