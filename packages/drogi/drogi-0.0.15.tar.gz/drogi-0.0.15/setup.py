# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drogi",
    version="0.0.15",
    author="Maciej Kluczyński",
    author_email="maciej.lukasz.kluczynski@gmail.com",
    description="Tool for analysing urban moveability.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mklucz/drogi",
    packages=setuptools.find_packages(),
    # install_requires=[
    #     "matplotlib",
    #     "pypng",
    #     "overpass >= 0.6.0",
    #     "psycopg2",
    #     "shapely",
    #     "networkx",
    #     "osmium",
    #     "pathfinding"
    # ]
)