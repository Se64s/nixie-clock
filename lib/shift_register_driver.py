#
# shift_register_driver.py
# Brief: Driver to handle shift register.
#
from machine import Pin

class ShiftRegister:
    def __init__(self, ser_data, ser_clk, reg_clk, invert=False):
        if invert:
            self.on = 0
            self.off = 1
        else:
            self.on = 1
            self.off = 0
        # Create pin
        self.pin_ser_data = Pin(ser_data, Pin.OUT)
        self.pin_ser_clk = Pin(ser_clk, Pin.OUT)
        self.pin_reg_clk = Pin(reg_clk, Pin.OUT)
        # Init pin state
        self.pin_ser_data(self.off)
        self.pin_ser_clk(self.off)
        self.pin_reg_clk(self.off)
    
    def enable_output(self):
        # Generate rise flank
        self.pin_reg_clk(self.off)
        self.pin_reg_clk(self.on)
        self.pin_reg_clk(self.off)

    def send_bytes(self, data_array):
        # Transfer data bytes
        for byte in data_array:
            # Send send bits for each byte
            for bit in range(8):
                self.pin_ser_clk(self.off)
                if ((byte >> bit) & 0x01):
                    self.pin_ser_data(self.on)
                else:
                    self.pin_ser_data(self.off)
                self.pin_ser_clk(self.on)
        # Reset lines
        self.pin_ser_data(self.off)
        self.pin_ser_clk(self.off)

# EOF
