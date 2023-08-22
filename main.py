import fsm_nixie
import app_logger


def test_nixie():
    import nixie_driver
    import ps_driver
    import time

    PIN_SER_DATA=5
    PIN_SER_CLOCK=7
    PIN_REG_CLOCK=6
    PIN_EN_PS=10
    SLEEP_PERIOD=0.1

    TEST_NUM_DIGITS=6
    TEST_NUM_DP=2
    TEST_MAX_VALUE=10

    nix=nixie_driver.NixieDisplay(pin_ser_data=PIN_SER_DATA, pin_ser_clock=PIN_SER_CLOCK, pin_reg_clock=PIN_REG_CLOCK)
    ps = ps_driver.PoweSupply(PIN_EN_PS)
    ps.enable()

    while True:
        for digit in range(0,TEST_NUM_DIGITS):
            for value in range(0,TEST_MAX_VALUE):
                nix.set_digit(digit, value)
                nix.update()
                time.sleep(SLEEP_PERIOD)
        for dp in range(0,TEST_NUM_DP):
            nix.set_dp(dp, True)
            nix.update()
            time.sleep(SLEEP_PERIOD)
            nix.set_dp(dp, False)
            nix.update()
            time.sleep(SLEEP_PERIOD)

def main(arguments):
    log = app_logger.get_logger(__name__)
    log.info("Nixie Clock Application")
    fsm_nixie.run()
    # test_nixie()

if __name__ == '__main__':
    main(None)

# EOF
