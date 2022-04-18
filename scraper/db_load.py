import logging
from typing import List

import psycopg2
import scraper.config as cfg


class DBLoader:
    def __init__(self, con: psycopg2.extensions.connection, urparts_data: List[cfg.UrPartDataPoint]):
        self.con = con
        self.cur = con.cursor()

        self.urparts_data = urparts_data

    def _load_vehicle_brands(self):
        vehicle_unique_brands = {row[0] for row in self.urparts_data}
        self.vehicle_brands_table_data = {brand: i for i, brand in enumerate(vehicle_unique_brands)}
        self.cur.executemany(
            "INSERT INTO vehicle_brands (vehicle_brand, vehicle_brand_id) VALUES (%s, %s)",
            list(self.vehicle_brands_table_data.items()),
        )

    def _load_vehicle_categories(self):
        vehicle_unique_categories = {row[1] for row in self.urparts_data}
        self.vehicle_categories_table_data = {cat: i for i, cat in enumerate(vehicle_unique_categories)}
        self.cur.executemany(
            "INSERT INTO vehicle_categories (vehicle_category, vehicle_category_id) VALUES (%s, %s)",
            list(self.vehicle_categories_table_data.items()),
        )

    def _load_vehicle_models(self):
        vehicle_unique_models = {(row[0], row[1], row[2]) for row in self.urparts_data}
        vehicle_models_table_data = [
            (i, self.vehicle_brands_table_data[model[0]], self.vehicle_categories_table_data[model[1]], model[2])
            for i, model in enumerate(vehicle_unique_models)
        ]
        self.vehicle_models_dict = {model[3]: model[0] for model in vehicle_models_table_data}
        self.cur.executemany(
            """
            INSERT INTO vehicles (vehicle_id, vehicle_brand_id, vehicle_category_id, vehicle_model)
            VALUES (%s, %s, %s, %s)
            """,
            vehicle_models_table_data,
        )

    def _load_part_categories(self):
        part_unique_categories = {row[4] for row in self.urparts_data}
        self.part_categories_table_data = {cat: i for i, cat in enumerate(part_unique_categories)}
        self.cur.executemany(
            "INSERT INTO part_categories (part_category, part_category_id) VALUES (%s, %s)",
            list(self.part_categories_table_data.items()),
        )

    def _load_part_items(self):
        parts_table_data = [
            (i, part[5], part[3], self.part_categories_table_data[part[4]], self.vehicle_models_dict[part[2]])
            for i, part in enumerate(self.urparts_data)
        ]
        self.cur.executemany(
            """
            INSERT INTO parts (part_id, part_site_id, part_name, part_category_id, vehicle_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            parts_table_data,
        )

    def check_data(self):
        parts_v_count = self.cur.execute("select count(*) from parts_v").fetchone()[0]
        scraped_count = len(self.urparts_data)
        if parts_v_count == scraped_count:
            logging.info(f"Data check passed. Number of data in DB is the same as scraped ({parts_v_count}).")
        else:
            logging.warning(f"Number of data in DB ({parts_v_count}) mismatches the number scraped ({scraped_count}).")

    def load_data(self):
        _ = self._load_vehicle_brands()
        _ = self._load_vehicle_categories()
        _ = self._load_vehicle_models()

        _ = self._load_part_categories()
        _ = self._load_part_items()

        self.con.commit()
