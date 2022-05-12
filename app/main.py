import logging

from fastapi import FastAPI
import logging_loki

app = FastAPI()

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


