import logging
import sqlite3

import requests
import scraper.config as cfg
from scraper.db_load import DBLoader
from scraper.scraping import scrape_urparts


def main():
    logger = logging.getLogger()
    logger.setLevel(cfg.LOGLEVEL)

    # website scraping
    session = requests.Session()
    urparts_data = scrape_urparts(session)

    n_parts_scraped = len(urparts_data)
    logging.info(f"Scraping done! {n_parts_scraped} partes scraped")

    # loading to database
    con = sqlite3.connect(cfg.DB_NAME)
    db_loader = DBLoader(con, urparts_data)
    _ = db_loader.load_data()

    _ = db_loader.create_view()
    logging.info("Data loading done!")

    _ = db_loader.check_data()


if __name__ == "__main__":
    main()
