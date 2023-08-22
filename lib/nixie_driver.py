#
# nixie_driver.py
# Brief: Driver to handle nixie digits.
#
import shift_register_driver as sr_driver
import app_logger
import nixie_mask

DIGIT_VALUE_OFF=255
__MAX_DIGIT_VALUE=9
__log = app_logger.get_logger(__name__)

class NixieDisplay:
    def __init__(self, pin_ser_data=5, pin_ser_clock=7, pin_reg_clock=6) -> None:
        self.sr_handler = sr_driver.ShiftRegister(pin_ser_data, pin_ser_clock, pin_reg_clock, invert=True)
        self.num_digits = nixie_mask.get_total_digits()
        self.num_dp = nixie_mask.get_total_dp()
        self.digit_values = [0] * self.num_digits
        self.dp_values = [False] * self.num_dp

    def set_digit(self, pos: int, value: int):
        if pos > self.num_digits:
            raise ValueError(f"Position not valid, {pos} > {self.num_digits}")
        if (value > __MAX_DIGIT_VALUE) and (value != DIGIT_VALUE_OFF):
            raise ValueError(f"Value not valid, {value} > {__MAX_DIGIT_VALUE}")
        self.digit_values[pos] = value
        __log.debug(self.digit_values)
    
    def set_dp(self, pos: int, value: bool):
        if pos > self.num_dp:
            raise ValueError(f"Position not valid, {pos} > {self.num_dp}")
        self.dp_values[pos] = value
        __log.debug(self.dp_values)

    def update(self):
        # Create empty frame
        sr_data = bytearray(nixie_mask.get_total_bytes())
        for digit_pos in range(0, self.num_digits):
            byte_mask = 0
            byte_pos = 0
            if self.digit_values[digit_pos] != DIGIT_VALUE_OFF:
                byte_mask = nixie_mask.get_digit_mask(digit_pos, self.digit_values[digit_pos])
                byte_pos = nixie_mask.get_digit_byte(digit_pos, self.digit_values[digit_pos])
            sr_data[byte_pos] |= byte_mask
            __log.debug(f"digit: {digit_pos}({self.digit_values[digit_pos]}), byte {byte_pos}, mask x{byte_mask:02x}")
        for dp_pos in range(0, self.num_dp):
            if self.dp_values[dp_pos] == True:
                byte_mask = nixie_mask.get_dp_mask(dp_pos)
                byte_pos = nixie_mask.get_dp_byte(dp_pos)
                sr_data[byte_pos] |= byte_mask
                __log.debug(f"dp: {dp_pos}({self.dp_values[dp_pos]}), byte {byte_pos}, mask x{byte_mask:02x}")
        # Send data into shift register
        __log.debug(sr_data)
        self.sr_handler.send_bytes(sr_data)
        self.sr_handler.enable_output()

# EOF
