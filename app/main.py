import logging

from fastapi import FastAPI
import pendulum
# import logging_loki

# logging configuration
logging.basicConfig(level = logging.INFO, format='%(asctime)s %(name)-8s %(levelname)-8s: %(message)s')

# rename level tag to level
# logging_loki.emitter.LokiEmitter.level_tag = 'level'

# # create loki handler
# handler = logging_loki.LokiHandler(
#     url = 'http://loki:3100/loki/api/v1/push',
#     version='1'
# )

# create logger 
logger = logging.getLogger(__name__)
# logger.addHandler(handler)

logger.warning('Starting WorldTime Application')
app = FastAPI()
logger.info('Waiting for Connections')
logger.error('Error')
logger.critical('Critical')


@app.get('/api/timezones')
def get_list_of_timezones():
    return pendulum.timezones


@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(area, location):
    now = pendulum.now(f'{area}/{location}')
    return {
        'datetime': now.isoformat()
    }
