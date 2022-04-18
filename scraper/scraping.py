import logging
import re
from typing import List
from urllib.parse import parse_qs, urlparse

import requests
import scraper.config as cfg
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag


def parse_name_from_obj(bs_object: Tag) -> str:
    """Parse name from BeautifulSoup object's text"""
    return bs_object.text.strip()


def get_bs_from_url(url: str, session: requests.Session) -> BeautifulSoup:
    """Get parsed BeautifulSoup object from given url and requests session."""
    url_data = session.get(url).content
    bs_object = BeautifulSoup(url_data, cfg.BS_PARSER)
    return bs_object


def get_subobjects(bs_object: BeautifulSoup, directory: str, regexp: str = "") -> ResultSet:
    """Get all subobjects/subdirectories for specified directory."""
    if directory.endswith("/"):
        directory = directory[:-1]

    subobjects = bs_object.find_all("a", attrs={"href": re.compile(f"{directory}{regexp}")})
    return subobjects


def get_catalogue_sub_dir_objects(sub_dir: str, session: requests.Session):
    """Get objects from given catalogue subdirectory."""
    sub_content = get_bs_from_url(cfg.URPARTS_URL + sub_dir, session)
    subobjects = get_subobjects(sub_content, sub_dir, cfg.SUBDIRECTORY_REGEXP)
    return subobjects


def parse_part_id(url: str) -> str:
    """Parse part id from href url."""
    url_query = urlparse(url).query
    part_id = int(parse_qs(url_query)["part"][0])
    return part_id


def get_part_data(part_obj: Tag, vehicle_info: List[str]) -> cfg.UrPartDataPoint:
    """Parse part object and return all part data as list."""
    part_id = parse_part_id(part_obj.attrs["href"])

    part_info = parse_name_from_obj(part_obj)
    part_info_splitted = part_info.split(cfg.NAME_CAT_SPLIT_SIGN)
    part_name = part_info_splitted[0].strip()

    if len(part_info_splitted) < 2:
        part_category = None
        logging.warning(f"Part '{part_info}' id={part_id} of vehicle {'/'.join(vehicle_info)} doesn't have category")
    else:
        part_category = part_info_splitted[1].strip().lower()

    return vehicle_info + [part_name, part_category, part_id]


def scrape_urparts(session: requests.Session) -> List[cfg.UrPartDataPoint]:
    """
    Scrape urparts website and return parts information.
    Columns: vehicle_brand, vehicle_category, vehicle_model, part_name, part_category, part_site_id
    """
    urparts_data = []

    brand_objects = get_catalogue_sub_dir_objects(cfg.CATALOGUE_DIR, session)
    for brand_obj in brand_objects:
        brand_name = parse_name_from_obj(brand_obj)
        logging.info(f"Start to parse brand {brand_name}")

        brand_dir = f"{cfg.CATALOGUE_DIR}/{brand_name}"
        cat_objects = get_catalogue_sub_dir_objects(brand_dir, session)

        for cat_obj in cat_objects:
            cat_name = parse_name_from_obj(cat_obj)
            cat_dir = f"{cfg.CATALOGUE_DIR}/{brand_name}/{cat_name}"
            model_objects = get_catalogue_sub_dir_objects(cat_dir, session)

            for model_obj in model_objects:
                model_name = parse_name_from_obj(model_obj)
                model_dir = f"{cfg.CATALOGUE_DIR}/{brand_name}/{cat_name}/{model_name}"

                model_content = get_bs_from_url(cfg.URPARTS_URL + model_dir, session)
                part_objects = get_subobjects(model_content, cfg.CATALOGUE_DIR, cfg.PART_REGEXP)

                for part_obj in part_objects:
                    part_data = get_part_data(part_obj, vehicle_info=[brand_name, cat_name, model_name])
                    urparts_data.append(part_data)
        break

    return urparts_data
