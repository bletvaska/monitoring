from functools import wraps
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pendulum
import logging
import logging_loki
from starlette_prometheus import metrics, PrometheusMiddleware

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

# app initialization
app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', metrics)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    response.headers['X-Lecturer-Name'] = 'mirek'
    return response


def log_client_ip(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = kwargs["request"]
        logger.info(f"Incomming connection from {request.client.host}",
                    extra={
                        'tags': {
                            'client': request.client.host,
                            'port': request.client.port,
                            'path': request.url.path
                        }
                })
        return func(*args, **kwargs)

    return wrapper
    
    
@app.get('/api/timezones')
@log_client_ip
def get_timezones(request: Request):
    return pendulum.timezones


@app.head('/api/timezones/{area}/{location}')
@app.get('/api/timezones/{area}/{location}')
@log_client_ip
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
        

@app.get('/deadlock')
def deadlock():
    while True:
        logger.info('>> work in progress...')
        time.sleep(1)
        


@app.get('/api/healthz')
@app.head('/api/healthz')
def healthcheck():
    # sleep(30)
    
    return {
        'status': 'up',
        'filesystem': 'ok',
        'database': 'ok'
        }
