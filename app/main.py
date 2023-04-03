import sys

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import pendulum
import logging
import logging_loki

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s: %(message)s'
)
logger = logging.getLogger('worldtime')

logging_loki.emitter.LokiEmitter.level_tag = 'level'

# create a loki handler
handler = logging_loki.LokiHandler(
    url='http://loki:3100/loki/api/v1/push',
    version='1'
)

# add handler to logger
logger.addHandler(handler)

logger.info('Starting WorldTime Aplication...')
app = FastAPI()
logger.info('Waiting for connections... ')


@app.get('/api/timezones')
def get_timezones(request: Request):
    logger.info(f'Connection from {request.client.host}',
                extra={
                    'tags': {
                        'client': request.client.host,
                        'port': request.client.port
                    }
                })
    return pendulum.timezones


@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(request: Request, area, location):
    logger.info(f'Connection from {request.client.host}',
                extra={
                    'tags': {
                        'client': request.client.host,
                        'port': request.client.port
                    }
                })
    try:
        now = pendulum.now(f'{area}/{location}')   # raised exception
        return {
            'hour': now.hour,
            'minute': now.minute,
            'second': now.second,
            'month': now.month,
            'day': now.day,
            'year': now.year,
            'datetime': now.isoformat(),
            'timezone': f'{area}/{location}',
            'day_of_week': now.weekday(),
        }
    except Exception as ex:
        logger.error(f'Invalid location {area}/{location}.')  # handled exception
        logger.exception(ex,
                extra={
                    'tags': {
                        'client': request.client.host,
                        'port': request.client.port
                    }
                })
        return JSONResponse(
            status_code=404,
            content={
                'error': f'Unknown timezone {area}/{location}.'
            }
        )


def main():
    uvicorn.run('main:app', host='0.0.0.0', reload=True, port=8000)
    

if __name__ == '__main__':
    main()
    