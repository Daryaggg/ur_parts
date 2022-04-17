FROM python:3.8-slim as builder

COPY . /app/
RUN python /app/setup.py install
RUN pip install -r /app/requirements-app.txt
WORKDIR /app
ENTRYPOINT ["/bin/sh"]
