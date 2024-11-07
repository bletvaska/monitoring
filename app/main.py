import logging
from functools import wraps

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pendulum
from pendulum.tz.exceptions import InvalidTimezone
from logging_loki import LokiHandler
import logging_loki

# rename level tag to level
logging_loki.emitter.LokiEmitter.level_tag = 'level'

# create handler for loki
handler = LokiHandler(
    url = 'http://loki:3100/loki/api/v1/push',
    tags={"app": "worldtime"},
    version = '1'
)

# create logger and add loki handler to it
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-5s %(levelname)-8s: %(message)s'
    )

logger.info('WorldTime app is starting.', extra={"tags": {"hello": "world"}})
app = FastAPI()
logger.info('Waiting for connections.')
logger.warning('warning')
logger.error('error')
logger.critical('critical')


def log_client_ip(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs['request']
        logger.info(f'Connection from {request.client.host}.',
                    extra={'tags': {
                     'client': request.client.host,
                     'action': 'audit',
                     'path': request.url.path
                    }})
        return await func(*args, **kwargs)
    return wrapper


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start = pendulum.now()
    response = await call_next(request)
    duration = pendulum.now() - start
    response.headers['X-Process-Time'] = f'{duration.microseconds}'
    return response


@app.get('/api/timezones')
@log_client_ip
async def get_list_of_timezones(request: Request):
    return pendulum.timezones()


@app.get('/api/timezones/{area}/{location}')
@log_client_ip
async def get_time_from_timezone(request: Request, area, location):
    try:
        now = pendulum.now(f'{area}/{location}')
        return now.isoformat()
    except InvalidTimezone as ex:
        logger.warning(f'Unknown timezone "{area}/{location}"')
        logger.exception(ex, extra={'tags': {
            'exception': str(ex.__class__)
        }})

        return JSONResponse(
            status_code=404,
            content={
                "error": f"Unknow timezone '{area}/{location}'"
            }
        )
