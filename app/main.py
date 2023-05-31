import pendulum
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello():
    return 'hello world!'

@app.get('/api/timezones')
def get_timezones():
    return pendulum.timezones

@app.get('/api/timezones/{area}/{location}')
def get_timezone_info(area, location):
    now = pendulum.now(f'{area}/{location}')
    return {
        'datetime': now.isoformat(),
        'unixtime': int(now.timestamp())
    }
    