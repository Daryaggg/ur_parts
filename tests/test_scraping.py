from unittest.mock import MagicMock

import pytest
from scraper.scraping import (
    get_bs_from_url,
    get_catalogue_sub_dir_objects,
    get_part_data,
    get_subobjects,
    parse_name_from_obj,
    parse_part_id,
)


def test_get_bs_from_url(catalogue_content, catalogue_bs_obj):
    url_content_mock = MagicMock()
    url_content_mock.content = catalogue_content

    session = MagicMock()
    session.get.return_value = url_content_mock

    bs_obj = get_bs_from_url("https://www.urparts.com/index.cfm/page/catalogue", session)
    assert bs_obj == catalogue_bs_obj


def test_get_catalogue_sub_dir_objects(catalogue_content):
    url_content_mock = MagicMock()
    url_content_mock.content = catalogue_content

    session = MagicMock()
    session.get.return_value = url_content_mock

    bs_tags = get_catalogue_sub_dir_objects("index.cfm/page/catalogue", session)
    assert len(bs_tags) == 16


def test_parse_name_from_obj(catalogue_content):
    url_content_mock = MagicMock()
    url_content_mock.content = catalogue_content

    session = MagicMock()
    session.get.return_value = url_content_mock

    bs_tags = get_catalogue_sub_dir_objects("index.cfm/page/catalogue", session)
    assert parse_name_from_obj(bs_tags[0]) == "Ammann"


def test_get_part_data(model_content):
    url_content_mock = MagicMock()
    url_content_mock.content = model_content

    session = MagicMock()
    session.get.return_value = url_content_mock
    model_content = get_bs_from_url(
        "https://www.urparts.com/index.cfm/page/catalogue/Volvo/Roller Parts/SD77DA", session
    )
    part_objs = get_subobjects(model_content, "index.cfm/page/catalogue", "\\?part=\\d*")
    part_data = get_part_data(part_objs[0], ["Volvo", "Roller Parts", "SD77DA"])
    assert part_data == ["Volvo", "Roller Parts", "SD77DA", "RM13062518", "trim moulding", 4231569]


def test_parse_part_id():
    part_id = parse_part_id("index.cfm/page/catalogue?part=4231891")
    assert part_id == 4231891
