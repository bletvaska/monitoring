import logging
from functools import wraps

import pendulum
from pendulum.tz.zoneinfo.exceptions import InvalidTimezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging_loki

# rename level tag to level
logging_loki.emitter.LokiEmitter.level_tag = 'level'

# create loki handler
handler = logging_loki.LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    version='1'
)

# configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s:%(lineno)d %(levelname)-8s: %(message)s")

# create logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)

logger.info('Starting WorldTime Application.')
app = FastAPI()
logger.info('Waiting for connections.')


def log_client_ip(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        logger.info(f'Connection from {request.client.host}',
                    extra={'tags': {
                        'client': request.client.host,
                        'action': 'audit'
                    }})
        return await func(*args, **kwargs)
    return wrapper
    
    
@app.get('/')
def hello():
    return 'hello world!'


@log_client_ip
@app.get('/api/timezones')
def get_timezones(request: Request):
    return pendulum.timezones 


@log_client_ip
@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(request: Request, area, location):
    try:
        now = pendulum.now(f'{area}/{location}')
        return {
            'datetime': now.isoformat(),
            'unixtime': int(now.timestamp())
        }
    except InvalidTimezone as ex:
        logger.error(f'Unknown timezone {area}/{location}')
        logger.exception(ex)
        
        return JSONResponse(status_code=404, content={
            'error': f'Uknown timezone {area}/{location}'
        })
    
