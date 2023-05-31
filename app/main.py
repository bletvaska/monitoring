import logging

import pendulum
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s:%(lineno)d %(levelname)-8s: %(message)s")
logger = logging.getLogger(__name__)

logger.info('Starting WorldTime Application.')
app = FastAPI()
logger.info('Waiting for connections.')


@app.get('/')
def hello():
    return 'hello world!'

@app.get('/api/timezones')
def get_timezones():
    logger.info('get_timezones()')
    return pendulum.timezones

@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(area, location):
    now = pendulum.now(f'{area}/{location}')
    return {
        'datetime': now.isoformat(),
        'unixtime': int(now.timestamp())
    }
    