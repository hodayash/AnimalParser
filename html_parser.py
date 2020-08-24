import requests
import pandas as pd
from bs4 import BeautifulSoup

def parse_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return [parse_html_table(table) \
            for table in soup.find_all('table')]  

def parse_html_table(table):
    """
    finds the relevant tags for a table.
    :param table: an html 'table' object of BeautifulSoup
    :return: a DataFrame object representing the table.
    """
    parsed_table = []
    column_names = []
   
    for br in table.find_all("br"):
        br.replace_with("\n")

    #did not use list comprehension so the code will be readable
    for row in table.find_all('tr'):
        #grabs the table headers, only the first row containing it
        th_tags = row.find_all('th')
        if th_tags and not column_names:
            #would let us create titles for the DataFrame
            column_names = [th.get_text().strip() for th in th_tags]
        else: 
            td_tags = row.find_all('td')
            row = [td.get_text().strip() for td in td_tags]
            if row:
                parsed_table.append(row)

    #we assume the row width is consistent
    table_width = len(column_names) if column_names else len(parsed_table[0])
    table_height = len(parsed_table)

    titles = column_names if column_names else range(0, table_width)

    df = pd.DataFrame(parsed_table, columns=titles,
                          index=range(0, table_height))
 
    return df
