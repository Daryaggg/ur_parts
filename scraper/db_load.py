import logging
import sqlite3
from typing import List

import scraper.config as cfg


class DBLoader:
    def __init__(self, con: sqlite3.Connection, urparts_data: List[cfg.UrPartDataPoint]):
        self.con = con
        self.cur = con.cursor()

        self.urparts_data = urparts_data

    def _load_vehicle_brands(self):
        vehicle_unique_brands = {row[0] for row in self.urparts_data}
        self.vehicle_brands_table_data = {brand: i for i, brand in enumerate(vehicle_unique_brands)}
        self.cur.execute("CREATE TABLE vehicle_brands (vehicle_brand char, vehicle_brand_id int)")
        self.cur.executemany("INSERT INTO vehicle_brands VALUES (?, ?)", list(self.vehicle_brands_table_data.items()))

    def _load_vehicle_categories(self):
        vehicle_unique_categories = {row[1] for row in self.urparts_data}
        self.vehicle_categories_table_data = {cat: i for i, cat in enumerate(vehicle_unique_categories)}
        self.cur.execute("CREATE TABLE vehicle_categories (vehicle_category char, vehicle_category_id int)")
        self.cur.executemany(
            "INSERT INTO vehicle_categories VALUES (?, ?)", list(self.vehicle_categories_table_data.items())
        )

    def _load_vehicle_models(self):
        vehicle_unique_models = {(row[0], row[1], row[2]) for row in self.urparts_data}
        vehicle_models_table_data = [
            (i, self.vehicle_brands_table_data[model[0]], self.vehicle_categories_table_data[model[1]], model[2])
            for i, model in enumerate(vehicle_unique_models)
        ]
        self.vehicle_models_dict = {model[3]: model[0] for model in vehicle_models_table_data}
        self.cur.execute(
            "CREATE TABLE vehicles (vehicle_id int, vehicle_brand_id int, vehicle_category_id int, vehicle_model char)"
        )
        self.cur.executemany("INSERT INTO vehicles VALUES (?, ?, ?, ?)", vehicle_models_table_data)

    def _load_part_categories(self):
        part_unique_categories = {row[4] for row in self.urparts_data}
        self.part_categories_table_data = {cat: i for i, cat in enumerate(part_unique_categories)}
        self.cur.execute("CREATE TABLE part_categories (part_category char, part_category_id int)")
        self.cur.executemany("INSERT INTO part_categories VALUES (?, ?)", list(self.part_categories_table_data.items()))

    def _load_part_items(self):
        parts_table_data = [
            (i, part[5], part[3], self.part_categories_table_data[part[4]], self.vehicle_models_dict[part[2]])
            for i, part in enumerate(self.urparts_data)
        ]
        self.cur.execute(
            "CREATE TABLE parts (part_id int, part_site_id int, part_name char, part_category_id int, vehicle_id int)"
        )
        self.cur.executemany("INSERT INTO parts VALUES (?, ?, ?, ?, ?)", parts_table_data)

    def create_view(self):
        self.cur.execute(
            """
            CREATE VIEW parts_v
            AS
            SELECT
                vehicle_brand,
                vehicle_category,
                vehicle_model,
                part_name,
                part_category,
                part_site_id,
                part_id
            FROM
                parts
            LEFT JOIN part_categories ON part_categories.part_category_id = parts.part_category_id
            LEFT JOIN vehicles ON vehicles.vehicle_id = parts.vehicle_id
            LEFT JOIN vehicle_categories ON vehicle_categories.vehicle_category_id = vehicles.vehicle_category_id
            LEFT JOIN vehicle_brands ON vehicle_brands.vehicle_brand_id = vehicles.vehicle_brand_id
        """
        )
        self.con.commit()

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
