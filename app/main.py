import pendulum
from fastapi import FastAPI, Request
from starlette_prometheus import metrics, PrometheusMiddleware

from helpers import get_logger
import api


logger = get_logger('worldtime')

logger.info('Starting WorldTime Application.')
app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', metrics)
app.include_router(api.router)
logger.info('Waiting for connections.')


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = pendulum.now()
    response = await call_next(request)
    process_time = pendulum.now() - start_time
    response.headers['X-Process-Time'] = f'{process_time.microseconds}'
    return response



