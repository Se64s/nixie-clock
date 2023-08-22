import fsm_nixie
import app_logger


def main(arguments):
    log = app_logger.get_logger(__name__)
    log.info("Nixie Clock Application")
    fsm_nixie.run()


if __name__ == '__main__':
    main(None)

# EOF
