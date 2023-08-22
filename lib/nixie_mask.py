#
# nixie_mask.py
# Brief: Bitmask to encode digit position into shift register.
#
import app_logger

class SrMask:
    def __init__(self, byte, bitmask):
        self.byte=byte
        self.bitmask=bitmask

__TOTAL_BYTES=8
__log = app_logger.get_logger(__name__)

__digit_0 = [
    SrMask(1, 0x20),
    SrMask(1, 0x10),
    SrMask(1, 0x08),
    SrMask(1, 0x04),
    SrMask(1, 0x02),
    SrMask(1, 0x01),
    SrMask(0, 0x80),
    SrMask(0, 0x40),
    SrMask(0, 0x20),
    SrMask(0, 0x10),
]

__digit_1 = [
    SrMask(2, 0x80),
    SrMask(2, 0x40),
    SrMask(2, 0x20),
    SrMask(2, 0x10),
    SrMask(2, 0x08),
    SrMask(2, 0x04),
    SrMask(2, 0x02),
    SrMask(2, 0x01),
    SrMask(1, 0x80),
    SrMask(1, 0x40),
]

__digit_2 = [
    SrMask(4, 0x02),
    SrMask(4, 0x01),
    SrMask(3, 0x80),
    SrMask(3, 0x40),
    SrMask(3, 0x20),
    SrMask(3, 0x10),
    SrMask(3, 0x08),
    SrMask(3, 0x04),
    SrMask(3, 0x02),
    SrMask(3, 0x01),
]

__digit_3 = [
    SrMask(5, 0x08),
    SrMask(5, 0x04),
    SrMask(5, 0x02),
    SrMask(5, 0x01),
    SrMask(4, 0x80),
    SrMask(4, 0x40),
    SrMask(4, 0x20),
    SrMask(4, 0x10),
    SrMask(4, 0x08),
    SrMask(4, 0x04),
]

__digit_4 = [
    SrMask(6, 0x20),
    SrMask(6, 0x10),
    SrMask(6, 0x08),
    SrMask(6, 0x04),
    SrMask(6, 0x02),
    SrMask(6, 0x01),
    SrMask(5, 0x80),
    SrMask(5, 0x40),
    SrMask(5, 0x20),
    SrMask(5, 0x10),
]

__digit_5 = [
    SrMask(7, 0x80),
    SrMask(7, 0x40),
    SrMask(7, 0x20),
    SrMask(7, 0x10),
    SrMask(7, 0x08),
    SrMask(7, 0x04),
    SrMask(7, 0x02),
    SrMask(7, 0x01),
    SrMask(6, 0x80),
    SrMask(6, 0x40),
]

__digit_list = [
    __digit_0,
    __digit_1,
    __digit_2,
    __digit_3,
    __digit_4,
    __digit_5,
]

__dp_list = [
    SrMask(0, 0x04),
    SrMask(0, 0x08),
]

def get_total_bytes():
    return __TOTAL_BYTES

def get_total_digits():
    return len(__digit_list)

def get_total_dp():
    return len(__dp_list)

def get_digit_mask(pos, digit):
    if pos > len(__digit_list):
        raise ValueError(f"Position not valid, {pos} > {len(__digit_list)}")
    if digit > len(__digit_list[pos]):
        raise ValueError(f"Digit not valid, {digit} > {len(__digit_list[pos])}")
    return (__digit_list[pos])[digit].bitmask

def get_digit_byte(pos, digit):
    if pos > len(__digit_list):
        raise ValueError(f"Position not valid, {pos} > {len(__digit_list)}")
    if digit > len(__digit_list[pos]):
        raise ValueError(f"Digit not valid, {digit} > {len(__digit_list[pos])}")
    return (__digit_list[pos])[digit].byte

def get_dp_mask(dp_pos):
    if dp_pos > len(__dp_list):
        raise ValueError(f"Position not valid, {dp_pos} > {len(__dp_list)}")
    return __dp_list[dp_pos].bitmask

def get_dp_byte(dp_pos):
    if dp_pos > len(__dp_list):
        raise ValueError(f"Position not valid, {dp_pos} > {len(__dp_list)}")
    return __dp_list[dp_pos].byte

# EOF
