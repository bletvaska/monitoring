import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pendulum
from pendulum.tz.exceptions import InvalidTimezone
import logging_loki

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


@app.get('/api/timezones')
def list_of_timezones(request: Request):
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
    logger.debug(f'Request for timezone {area}/{location}.')

    try:
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
