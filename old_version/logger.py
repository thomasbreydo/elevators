import logging

LOGFILE = 'elevators.log'

NUM_PANELS = 2
LOG_MESSAGE = '%d panels parsed,%s'

LOG_FORMAT = '%(levelname)s:%(asctime)s:%(message)s'

logging.basicConfig(filename=LOGFILE,
                    level=logging.INFO, format=LOG_FORMAT)


def log(parsed):
    num_parsed = len(parsed)
    parsed_string = ' '.join(parsed)
    if num_parsed == NUM_PANELS:  # location of both elevators found
        logging.info(LOG_MESSAGE, num_parsed, parsed_string)
    else:
        logging.warning(LOG_MESSAGE, num_parsed, parsed_string)
