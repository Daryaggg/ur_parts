# UrParts scraper
<img src="UrParts-company.jpeg" alt="UrPartsLogo" width="150"/>

Service for scraping www.urparts.com website and build API for fetching data.

### Quick start
Use docker-compose to start the service.
```
docker-compose up
```

### Stages
1. [Postgres](https://www.postgresql.org/) database start up
2. Run pytest on scraper
3. Starting the scraper if there is no data in the database yet
4. Run webapp [FastAPI](https://fastapi.tiangolo.com/) on http://127.0.0.1:8000/ur_parts/

### Run tests
```
bash tests/run_tests.sh
```

### Tech
- Python 3.8
- requests
- BeautifulSoup4
- psycopg2
- Encode Databases
