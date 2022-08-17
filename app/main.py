from time import time
from datetime import datetime
import logging

from fastapi import FastAPI, Request
import logging_loki


# configuration of logging
logging_loki.emitter.LokiEmitter.level_tag = 'level'

handler = logging_loki.LokiHandler(
    url='http://loki:3100/loki/api/v1/push',
    version='1'
)
logger = logging.getLogger('uservice')
logger.addHandler(handler)
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# print("something important just occured")
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warning message')
# logger.error('error message')
# logger.critical('critical message')


logger.info('Starting FastAPI application.')
app = FastAPI()
logger.info('Waiting for connections.')


@app.get("/")
def get_time(request: Request):
    logger.info(f'Connection from {request.client.host}.')
    now = datetime.now()

    return {
        'client_ip': request.client.host,
        'day_of_week': now.weekday(),
        'day': now.day,
        'month': now.month,
        'year': now.year,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'isoformat': now.isoformat(),
        'unixtime': int(time())
    }

