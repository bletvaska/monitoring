from time import time
from datetime import datetime
import logging

from fastapi import FastAPI, Request


logging.basicConfig(level=logging.DEBUG)
print("something important just occured")
logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')


app = FastAPI()


@app.get("/")
def get_time(request: Request):
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

