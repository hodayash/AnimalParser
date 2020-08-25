"""
This module allows the user to print all the collateral adjectives
and the animals which belong to each one.
It does so by scraping a web page and extracting relevant data.
Requirements: Python 3.6+
Packages: Pandas, requests, bs4 (BeautifulSoup)
This file is imported as a module in order to use the animal grabber.
"""

import pandas as pd
from html_parser import parse_url
import consts
import html_templates


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


def grab_relevant_data(table):
    """
    gets an animal DF and strips all of the irrelevant characters
    from the 'Animal' (animal name) column.
    :param table: DataFrame of animals
    :return: pd.DataFrame, containing 'Animals' and 'Collateral adjectives'
    """
    # removes values which point to another value
    table.loc[:, :] = table[~table[consts.ANIMAL_COL].str.contains("See ")]

    # changes all blank or unknown values to string 'unknown'
    table.loc[:, consts.COLLATERAL_ADJECTIVE_COL] = table[consts.COLLATERAL_ADJECTIVE_COL].apply(lambda x: x.strip(" \n?") if isinstance(x, str) else x)
    table[consts.COLLATERAL_ADJECTIVE_COL].replace(consts.ADJ_FILTER, '', regex=True, inplace=True)
    table[consts.COLLATERAL_ADJECTIVE_COL].replace(consts.BLANK, 'Unknown', regex=True, inplace=True)

    # remove irrelevant data from relevant names such as "see also"
    all_filters = prepare_filters(consts.NAMES_FILTERS)
    table[consts.ANIMAL_COL].replace(all_filters, "", regex=True, inplace=True)
    table.loc[:, consts.ANIMAL_COL] = table[consts.ANIMAL_COL].apply(lambda x: x.strip(" \n?") if isinstance(x, str) else x)

    return table[[consts.ANIMAL_COL, consts.COLLATERAL_ADJECTIVE_COL]]


def duplicate_rows(table):
    """
    duplicates the rows where the Collateral adjective is more than one,
    so the animal will count for each one of them.
    :param table: DataFrame of animals
    :return: pd.DataFrame, containing 'Animals' and 'Collateral adjectives'
    """
    table[consts.COLLATERAL_ADJECTIVE_COL] = table[consts.COLLATERAL_ADJECTIVE_COL].apply(lambda x: x.split("\n") if isinstance(x, str) else [x])
    table = table.explode(consts.COLLATERAL_ADJECTIVE_COL) 
    table[consts.COLLATERAL_ADJECTIVE_COL] = table[consts.COLLATERAL_ADJECTIVE_COL].str.strip()
    return table  


def animal_relations(data):
    """
    For each collateral adjective, saves all animals in dictionary.
    :param data: DataFrame of relevant animals data
    :return: None
    """
    by_adjective = data.groupby(consts.COLLATERAL_ADJECTIVE_COL)
    results = {}

    for adjective, animals in by_adjective:
        all_animals = ', '.join(animals[consts.ANIMAL_COL].tolist())
        results[adjective] = all_animals

    return results 


def dict_html_cache(to_html, path):
    """
    gets a dictionary and saves it to a nice-looking html page.
    :param to_html: dictioanry
    :param path: output path
    :return: None
    """
    body = ""
    for key, value in to_html.items():
        header = html_templates.HEADER.format(key=key)
        list_items = "\n".join([html_templates.LIST_ITEM.format(item=item) \
            for item in value.split(", ")])

        html_list = html_templates.LIST_WRAPPER.format(list_items=list_items)

        body += f"{header}\n{html_list}"
    
    full_html = html_templates.HTML_TEMPLATE.format(body=body)
    with open(path, 'w', encoding="utf8") as out:
        out.write(full_html)


def pretty_print(dictionary):
    for key, value in dictionary.items():
        print(f"{key}: {value}")