import logging
from functools import wraps
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pendulum
from pendulum.tz.zoneinfo.exceptions import InvalidTimezone
import logging_loki
from starlette_prometheus import metrics, PrometheusMiddleware

# logging configuration
logging.basicConfig(level = logging.INFO, format='%(asctime)s %(name)-8s %(levelname)-8s: %(message)s')

# rename level tag to level
logging_loki.emitter.LokiEmitter.level_tag = 'level'

# create loki handler
handler = logging_loki.LokiHandler(
    url = 'http://loki:3100/loki/api/v1/push',
    version='1'
)

# create logger 
logger = logging.getLogger(__name__)
logger.addHandler(handler)    

logger.info('Starting WorldTime Application')
app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', metrics)

logger.info('Waiting for Connections')


def log_client_ip(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        logger.info(f'Connection from {request.client.host}.',
                    extra={'tags': {
                     'client': request.client.host,
                     'action': 'audit',
                     'path': '/api/timezones'   
                    }})
        return await func(*args, **kwargs)
    return wrapper


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    logger.info('counting processing time')
    start = pendulum.now()
    
    # invoke
    response = await call_next(request)
    
    duration = pendulum.now() - start
    response.headers['X-Process-Time'] = f'{duration.microseconds}'
    return response
    

@log_client_ip
@app.get('/api/timezones')
def get_list_of_timezones(request: Request):
    return pendulum.timezones


@log_client_ip
@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(request: Request, area, location):
    try:
        now = pendulum.now(f'{area}/{location}')
        return {
            'datetime': now.isoformat()
        }
    except InvalidTimezone as ex:
        message = f"Unknown timezone '{area}/{location}'"
        logger.warning(message)
        logger.exception(ex)
        
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "title": "Not Found",
                "detail": message,
                "instance": f"/api/timezones/{area}/{location}",
                "type": "/errors/timezones/unknown",
            }
        )


@app.get('/deadlock')
def deadlock():
    while True:
        logger.info('work in progress...')
        time.sleep(1)
    
    
@app.get('/healthz')
def health_check():
    return {
        'status': 'up'
    }
    