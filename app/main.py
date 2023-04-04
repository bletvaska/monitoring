import sys
from functools import wraps
from time import sleep

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

def log_client_ip(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        logger.info(f'Connection from {request.client.host}',
            extra={
                'tags': {
                    'client': request.client.host,
                    'port': request.client.port
                }
            })
        return await func(*args, **kwargs)
        
    return wrapper
    
    
@log_client_ip
@app.get('/api/timezones')
async def get_timezones(request: Request):
    return pendulum.timezones


@log_client_ip
@app.head('/api/timezones/{area}/{location}')
@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(request: Request, area, location):
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
        

@app.get('/api/deadlock')
def endless_loop():
    logger.info('>> in deadlock   ') 
    while True:
        logger.info('work in progress...')
        # sleep(1)


@app.get('/api/healthz')
@app.head('/api/healthz')
def healthcheck():
    return {
        'status': 'up',
        'filesystem': 'ok',
        'database': 'ok'
        }


def main():
    uvicorn.run('main:app', host='0.0.0.0', reload=True, port=8000)
    

if __name__ == '__main__':
    main()
    