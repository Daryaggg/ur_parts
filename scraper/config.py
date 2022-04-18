import os
from typing import List, Union

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
UrPartDataPoint = List[Union[str, int, None]]

# Scrapping
URPARTS_URL = "https://www.urparts.com/"
CATALOGUE_DIR = "index.cfm/page/catalogue"

BS_PARSER = "html.parser"
SUBDIRECTORY_REGEXP = "/(\w|\d|-)*"
PART_REGEXP = "\?part=\d*"
NAME_CAT_SPLIT_SIGN = " - "

# Database
PG_DB_NAME = os.environ.get("POSTGRES_DB", "ur_parts")
PG_USER = os.environ.get("POSTGRES_USER")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
PG_HOST = os.environ.get("POSTGRES_HOST")
PG_PORT = int(os.environ.get("POSTGRES_PORT"))
