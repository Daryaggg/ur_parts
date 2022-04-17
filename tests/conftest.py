import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def catalogue_content() -> bytes:
    with open("tests/catalogue_content.bin", "rb") as file:
        cat_content = file.read()
    return cat_content


@pytest.fixture
def model_content() -> bytes:
    with open("tests/model_content.bin", "rb") as file:
        m_content = file.read()
    return m_content


@pytest.fixture
def catalogue_bs_obj(catalogue_content) -> BeautifulSoup:
    bs_obj = BeautifulSoup(catalogue_content, "html.parser")
    return bs_obj
