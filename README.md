## Setting up package

    python3 setup.py sdist bdist_wheel

## Pushing to PYPI

    pip install twine
    python -m twine upload dist/*

# How to use:

## Install

pip install primary-data-analysis

## Import

from primary import get_all_data_analysis

## Call function

get_all_data_analysis(dataframe, target="target_class_label", path="./desired_folder_name")

## Prerequisites

    1. Install all requirements
    2. better to label encode ordinal categorical variables
