import logging

import pendulum
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)

logging.info('Starting WorldTime Application.')
app = FastAPI()
logging.info('Waiting for connections.')

logging.warning('This is warning.')
logging.error('This is error.')
logging.critical('This is critical.')




@app.get('/')
def hello():
    return 'hello world!'

@app.get('/api/timezones')
def get_timezones():
    return pendulum.timezones

@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(area, location):
    now = pendulum.now(f'{area}/{location}')
    return {
        'datetime': now.isoformat(),
        'unixtime': int(now.timestamp())
    }
    