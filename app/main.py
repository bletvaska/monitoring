import logging

from fastapi import FastAPI

app = FastAPI()

username = 'john'
password = 'hello.world'

logger = logging.getLogger('dummy')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
)

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

