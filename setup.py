import os.path

from setuptools import find_packages, setup


def find_requires():
    """Take requirements from file."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "requirements/requirements-scraper.txt"), "r") as reqs:
        requirements = reqs.readlines()
    return requirements


setup(
    name="scraper",
    version="0.0.1",
    author="Darya Pronina",
    description="Scraper of static website https://www.urparts.com/",
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=find_requires(),
)
