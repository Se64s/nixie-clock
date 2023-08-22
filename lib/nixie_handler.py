#
# nixie_handler.py
# Brief: Library to manage nixie display with effects.
#

import app_logger
import nixie_driver
import time

# Module variables ------------------------------------------------------------

__log = app_logger.get_logger(__name__)
__frame_rate = 0.05
__data_value=[0,0,0,0,0,0]

# Private methods -------------------------------------------------------------

def __update_display(nix_driver:nixie_driver.NixieDisplay, data_array:list):
    
    for data_index in range(0, len(__data_value)):
        nix_driver.set_digit(data_index, data_array[data_index])
    nix_driver.update()

# Public methods --------------------------------------------------------------

def set_dp(nix_driver:nixie_driver.NixieDisplay, dp_value=False):
    nix_driver.set_dp(0, dp_value)
    nix_driver.set_dp(1, dp_value)
    nix_driver.update()


def set_value(nix_driver:nixie_driver.NixieDisplay, a=0, b=0, c=0):
    
    global __data_value
    if (a > 100) or (b > 100) or (c > 100):
        raise ValueError(f"Any input value should exceed 100: {a}, {b}, {c}")
    
    __data_value=[
        int(c % 10), int(c / 10),
        int(b % 10), int(b / 10),
        int(a % 10), int(a / 10),
    ]
    
    __update_display(nix_driver, __data_value)


def scroll_to_value(nix_driver:nixie_driver.NixieDisplay, new_a=0, new_b=0, new_c=0):
    
    global __data_value
    if (new_a > 100) or (new_b > 100) or (new_c > 100):
        raise ValueError(f"Any input value should exceed 100: {new_a}, {new_b}, {new_c}")
    
    # Scroll out old values
    __update_display(nix_driver, __data_value)

    for scroll_pos in range(len(__data_value)):        
        time.sleep(__frame_rate)
        __data_value.pop(0)
        __data_value.append(nixie_driver.DIGIT_VALUE_OFF)
        __update_display(nix_driver, __data_value)

    # Scroll in new values
    new_data_value=[
        int(new_c % 10), int(new_c / 10),
        int(new_b % 10), int(new_b / 10),
        int(new_a % 10), int(new_a / 10),
    ]

    for scroll_pos in range(len(__data_value)):
        time.sleep(__frame_rate)
        __data_value.pop(0)
        __data_value.append(new_data_value[scroll_pos])
        __update_display(nix_driver, __data_value)
        

def set_frame_rate(frame_rate: int):
    global __frame_rate
    if frame_rate == 0:
        raise ValueError(f"Frame rate value not valid: {frame_rate}")
    __frame_rate = frame_rate / 1000


# EOF
