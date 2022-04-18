import logging

import psycopg2
import requests
import scraper.config as cfg
from scraper.db_load import DBLoader
from scraper.scraping import scrape_urparts


def main():
    logger = logging.getLogger()
    logger.setLevel(cfg.LOG_LEVEL)

    # website scraping
    session = requests.Session()
    urparts_data = scrape_urparts(session)

    n_parts_scraped = len(urparts_data)
    logging.info(f"Scraping done! {n_parts_scraped} partes scraped")

    # loading to database
    con = psycopg2.connect(
        dbname=cfg.PG_DB_NAME,
        host=cfg.PG_HOST,
        user=cfg.PG_USER,
        password=cfg.PG_PASSWORD,
        port=cfg.PG_PORT,
    )

    db_loader = DBLoader(con, urparts_data)
    _ = db_loader.load_data()
    logging.info("Data loading done!")

    _ = db_loader.check_data()
    con.close()


if __name__ == "__main__":
    main()
