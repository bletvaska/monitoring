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



@app.get('/api/exception')
def exception_example():
    try:
        print('>> start')

        file = open('/root/doesnt.exist', 'r')

        10 / 0

        print('>> end')

    except ZeroDivisionError as ex:
        logger.error('>> it is not possible to divide by zero')
        logger.exception(ex)

    except FileNotFoundError as ex:
        logger.error('Error: File was not found')
        logger.exception(ex)

    except PermissionError as ex:
        logger.error('Error: You dont have permissions to access this file')
        logger.exception(ex)

    except Exception as ex:
        # never happens
        pass

