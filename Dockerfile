FROM python:3.8-slim as builder

RUN \
  apt-get update -qq && \
  apt-get install -qq gcc postgresql python3-psycopg2 libpq-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

COPY . /app/
RUN python /app/setup.py install
RUN pip install -r /app/requirements-app.txt
WORKDIR /app
ENTRYPOINT ["/bin/sh"]
