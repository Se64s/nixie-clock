#
# ps_driver.py
# Brief: Driver to handle Power supply
#
from machine import Pin

class PoweSupply:
    def __init__(self, enable_pin):
        # Create pin
        self.pin_enable = Pin(enable_pin, Pin.OUT)
        # Init pin state
        self.pin_enable(0)
    
    def enable(self):
        self.pin_enable(1)

    def disable(self):
        self.pin_enable(0)

# EOF
