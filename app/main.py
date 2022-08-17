from time import time
from datetime import datetime

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def get_time(request: Request):
    now = datetime.now()

    return {
        'client_ip': request.client.host,
        'day_of_week': now.weekday(),
        'day': now.day,
        'month': now.month,
        'year': now.year,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'isoformat': now.isoformat(),
        'unixtime': int(time())
    }

