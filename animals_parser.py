"""
This script allows the user to print all the collateral adjectives
and the animals which belong to each one.

It dBoes so by scraping a web page and extracting relevant data.

Requirments: Python 3.6 +
Packages: Pandas, requests, bs4 (BeautifulSoup)

This file can also be imported as a module in order to use the animal grabber.
"""
import pandas as pd
from html_parser import HTMLTableParser
import consts

def merge_animals_tables(tables):
    """
    gets list of tables as DFs.
    merges the animals tables to one table of animal + collateral adjectives.
    :return: pd.DataFrame representing all animals' data
    """
    relevant = [table for table in tables if ANIMAL_COL in table.columns.to_list()]
    if len(relevant) > 1:
        animals = pd.concat(relevant)
        return animals
    return relevant[0]

def grab_relevant_data(df):
    """
    gets an animal DF and strips all of the irrelevant characters
    from the 'Animal' (animal name) column.
    :return: pd.DataFrame, containing 'Animals' and 'Collateral adjectives'
    """
    filters = [f"({filter})" for filter in consts.FILTERS]
    all_filters = "|".join(filters)
    filtered = df[consts.ANIMAL_COL].replace(all_filters, "", regex=True)
    df[consts.ANIMAL_COL] = filtered

    return df[[consts.ANIMAL_COL, consts.COLLATERAL_ADJECTIVE_COL]]

def pretty_print(data):
    """
    For each collateral adjective, prints all animals.
    :return: None
    """
    pass

def main():
    hp = HTMLTableParser()
    tables = hp.parse_url(consts.ANIMALS_WIKI_PAGE)
    df = merge_animals_tables(tables)
    relevant_data = grab_relevant_data(df)
    pretty_print(relevant_data)

if __name__ == '__main__':
    main()