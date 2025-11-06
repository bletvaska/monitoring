import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pendulum
from pendulum.tz.exceptions import InvalidTimezone
import logging_loki
from starlette_prometheus import metrics, PrometheusMiddleware


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-8s %(levelname)-8s: %(message)s'
)

# rename level tag to level
logging_loki.emitter.LokiEmitter.level_tag = 'level'

# create loki handler
handler = logging_loki.LokiHandler(
    url = 'http://loki:3100/loki/api/v1/push',
    version = '1'
)

# create logger
logger = logging.getLogger(__name__)
# add loki handler to logger
logger.addHandler(handler)

logger.info('Starting WorldTime application.')
app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', metrics)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    # process request
    start_time = pendulum.now()
    response = await call_next(request)

    # process response
    process_time = pendulum.now() - start_time
    response.headers['X-Process-Time'] = f'{process_time.microseconds}'

    # pass to next middleware function (return the response to the user)
    return response


@app.get('/api/timezones')
def list_of_timezones(request: Request, user):
    logger.debug('Request for timezones.')
    logger.info('New request', extra={
        "tags": {
            "client": request.client.host,
            "port": request.client.port,
            "path": request.url.path
        }
    })
    return pendulum.timezones()


@app.get('/api/timezone/{area}/{location}')
def get_timezone_info(request: Request, area: str, location: str):
    logger.info(f'Request for timezone {area}/{location}.')

    try:
        # retrieve the timezone info abou given area and location
        user = {
            'who': request.client.host,
            'what': request.url.path,
            'with': f'{area}/{location}'
        }
        logger.info(user)

        now = pendulum.now(f'{area}/{location}')
        return now.isoformat()

    except InvalidTimezone as ex:
        logger.info(f"Unknown timezone '{area}/{location}'")
        logger.exception(ex)

        return JSONResponse(
            status_code=404,
            content={
                "error": f"Unknown timezone '{area}/{location}'"
            }
        )


logger.info('Waiting for connections.')
