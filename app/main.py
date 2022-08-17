from time import time
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_time():
    now = datetime.now()

    return {
        'day': now.day,
        'month': now.month,
        'year': now.year,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'isoformat': now.isoformat(),
        'unixtime': int(time())
    }

