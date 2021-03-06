import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging_loki
from starlette_prometheus import metrics, PrometheusMiddleware

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

username = 'john'
password = 'hello.world'

handler = logging_loki.LokiHandler(
        url="http://loki:3100/loki/api/v1/push",
    tags={
            "application": "dummy-service",
            "author": "mirek"
        },
    # auth=("username", "password"),
    version="1",
)

logger = logging.getLogger(__name__)  # 'dummy')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
)
logger.addHandler(handler)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    response.headers['X-Process-Time'] = str(process_time)

    return response


@app.get('/api/slow')
def slow_response():
    print('sleeping for 3 seconds...')
    time.sleep(3)
    print('waking up...')

    return "waking up"



@app.head('/api/hello')
@app.get("/api/hello")
def hello_world():
    logger.debug('inside of hello_world()')
    logger.debug(f'username is {username} and password {password}')

    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')

    return {"Hello": "World"}

@app.get('/api/exception')
def exception_example():
    try:
        print('>> start')

        file = open('/root/doesnt.exist', 'r')

        10 / 0

        print('>> end')

    except ZeroDivisionError as ex:
        logger.error('>> it is not possible to divide by zero')
        logger.exception(ex)

    except FileNotFoundError as ex:
        logger.error('Error: File was not found')
        logger.exception(ex)

    except PermissionError as ex:
        logger.error('Error: You dont have permissions to access this file')
        logger.exception(ex)

    except Exception as ex:
        # never happens
        pass


def check_db_status():
    return True

def check_storage_status():
    return True

@app.get('/health')
def health():
    is_healthy = check_db_status() and check_storage_status()
    status_code = 200
    if is_healthy is False:
        status_code = 500

    payload = {
        'healthy': is_healthy,
        'db': check_db_status(),
        'storage': check_storage_status()
    }

    return JSONResponse(
            status_code = status_code,
            content=payload
            )



