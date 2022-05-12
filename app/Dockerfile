FROM bletvaska/python

WORKDIR /app
COPY main.py .
COPY requirements.txt .

USER root

RUN pip install -r requirements.txt \
    && rm requirements.txt \
    && apt update \
    && apt install -y curl

HEALTHCHECK \
    --interval=10s \
    --timeout=3s \
    CMD curl -f http://localhost/api/health || exit 1

USER pythonista

EXPOSE 80

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload" ]

