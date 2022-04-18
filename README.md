# UrParts scraper
<img src="UrParts-company.jpeg" alt="UrPartsLogo" width="50"/>

Service for scraping www.urparts.com website and build API for fetching data.

### Quick start
Use ```docker-compose up``` to start the service.

### Stages
1. [Postgres](https://www.postgresql.org/) database start up
2. Run pytest on scraper
3. Starting the scraper if there is no data in the database yet
4. Run webapp [FastAPI](https://fastapi.tiangolo.com/) on http://127.0.0.1:8000/ur_parts/
