FROM python:3.8-slim as base

COPY . /app/
WORKDIR /app


# ===========================
# Image to run scraper script
# ===========================
FROM base as scraper

RUN \
  apt-get update -qq && \
  apt-get install -qq gcc postgresql python3-psycopg2 libpq-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN python /app/setup.py install

ENTRYPOINT ["/bin/sh"]


# ================
# Image to run API
# ================
FROM base as webapp

RUN pip install -r /app/requirements-app.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
