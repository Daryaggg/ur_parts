import os
from typing import List, Union

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
UrPartDataPoint = List[Union[str, int, None]]

# Scrapping
URPARTS_URL = "https://www.urparts.com/"
CATALOGUE_DIR = "index.cfm/page/catalogue"

BS_PARSER = "html.parser"
SUBDIRECTORY_REGEXP = "/(\w|\d|-)*"
PART_REGEXP = "\?part=\d*"
NAME_CAT_SPLIT_SIGN = " - "

# Database
DB_NAME = "UrParts.db"
