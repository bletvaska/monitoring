from functools import wraps
import logging

import logging_loki


# rename level tag to level
logging_loki.emitter.LokiEmitter.level_tag = 'level'


def get_logger(name):
    # create loki handler
    handler = logging_loki.LokiHandler(
        url="http://loki:3100/loki/api/v1/push",
        version='1'
    )

    # configure logging
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s:%(lineno)d %(levelname)-8s: %(message)s")

    # create logger
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    
    return logger
