"""
This script allows the user to print all the collateral adjectives
and the animals which belong to each one.

It dBoes so by scraping a web page and extracting relevant data.

Requirements: Python 3.6+
Packages: Pandas, requests, bs4 (BeautifulSoup)

This file can also be imported as a module in order to use the animal grabber.
"""

import pandas as pd
from html_parser import HTMLTableParser
import consts

def merge_animals_tables(tables):
    """
    merges the animals tables to one table of animal + collateral adjectives.
    :param tables: list of DataFrames.
    :return: pd.DataFrame representing all animals' data
    """
    relevant = [table for table in tables if consts.ANIMAL_COL in table.columns.to_list()]
    if len(relevant) > 1:
        animals = pd.concat(relevant)
        return animals
    return relevant[0]

def prepare_filters(filters):
    """
    :param filters:  list of regular expressions
    :return: string representing all matching groups
    """
    filters = [f"({filter})" for filter in filters]
    all_filters = "|".join(filters)
    return all_filters

def grab_relevant_data(df):
    """
    gets an animal DF and strips all of the irrelevant characters
    from the 'Animal' (animal name) column.
    :param df: dataframe of animals
    :return: pd.DataFrame, containing 'Animals' and 'Collateral adjectives'
    """
    # removes values which point to another value
    df = df[~df[consts.ANIMAL_COL].str.contains("See ")]

    # changes all blank or unknown values to string 'unknown'
    df[consts.COLLATERAL_ADJECTIVE_COL] = df[consts.COLLATERAL_ADJECTIVE_COL].str.strip(" \n?")
    df[consts.COLLATERAL_ADJECTIVE_COL].replace(r'^$', 'Unknown', regex=True, inplace=True)

    # remove irrelevant data from relevant names such as "see also"
    all_filters = prepare_filters(consts.FILTERS)
    df[consts.ANIMAL_COL].replace(all_filters, "", regex=True, inplace=True)


    return df[[consts.ANIMAL_COL, consts.COLLATERAL_ADJECTIVE_COL]]

def pretty_print(data):
    """
    For each collateral adjective, prints all animals.
    :param data: DataFrame of relevant animals data
    :return: None
    """
    by_adjective = data.groupby(consts.COLLATERAL_ADJECTIVE_COL)
    for adjective, animals in by_adjective:
        all_animals = ', '.join(animals[consts.ANIMAL_COL].tolist())
        print(f"{adjective}: {all_animals}")


def main():
    hp = HTMLTableParser()
    tables = hp.parse_url(consts.ANIMALS_WIKI_PAGE)
    df = merge_animals_tables(tables)
    relevant_data = grab_relevant_data(df)
    pretty_print(relevant_data)

if __name__ == '__main__':
    main()