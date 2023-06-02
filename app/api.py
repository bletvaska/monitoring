from functools import wraps
from time import sleep

from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
import pendulum
from pendulum.tz.zoneinfo.exceptions import InvalidTimezone

from helpers import get_logger


router = APIRouter()
logger = get_logger('worldtime.api')

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


@router.get('/deadlock')
def deadlock():
    while True:
        logger.info('>> work in progress')
        sleep(1)


@router.get('/api/healthz')
def check_health():
    return {
        'status': 'up'
    }
    
    
@router.get('/')
def hello():
    return 'hello world!'


@log_client_ip
@router.get('/api/timezones')
def get_timezones(request: Request):
    return pendulum.timezones 


@log_client_ip
@router.get('/api/timezones/{area}/{location}')
def get_timezone_info(request: Request, area, location):
    try:
        now = pendulum.now(f'{area}/{location}')
        return {
            'datetime': now.isoformat(),
            'unixtime': int(now.timestamp())
        }
    except InvalidTimezone as ex:
        logger.error(f'Unknown timezone {area}/{location}')
        logger.exception(ex, extra={'tags': {'exception': 'InvalidTimezone'}})
        
        return JSONResponse(status_code=404, content={
            'error': f'Uknown timezone {area}/{location}'
        })
