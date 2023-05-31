import logging

import pendulum
from fastapi import FastAPI, Request
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

# logger.warning('this is warning')
# logger.error('this is error')
# logger.critical('this is critical',
#                 extra={"tags": {
#                     "service": "worldtime",
#                     'customer': 'tsystems',
#                     'location': 'kosice',
#                     'training': 'monitoring'
#                     }})

@app.get('/')
def hello():
    return 'hello world!'

@app.get('/api/timezones')
def get_timezones(request: Request):
    logger.info(f'get_timezones() from {request.client.host}',
                extra={'tags': {
                    'client': request.client.host
                }})
    return pendulum.timezones 

@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(area, location):
    now = pendulum.now(f'{area}/{location}')
    return {
        'datetime': now.isoformat(),
        'unixtime': int(now.timestamp())
    }
    