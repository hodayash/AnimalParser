import requests
import pandas as pd
from bs4 import BeautifulSoup

class HTMLTableParser:
       
        def parse_url(self, url):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            return [self.parse_html_table(table)\
                    for table in soup.find_all('table')]  
    
        def parse_html_table(self, table):
            parsed = [(row.find_all('th'), len(row.find_all('td'))) for row in table.find_all('tr')]

            # checks if have exactly one row name
            if len([{} for i in parsed if len(i[0]) != 1]) != 0:
                raise Exception("must contain row title")


            columns = [parsed[0][0] for i in parsed]

            df = pd.DataFrame(columns = columns,
                              index= range(0, len(parsed)))

            for row_index, row in enumerate(table.find_all('tr')):
                columns = row.find_all('td')

                for col_inedx, column in enumerate(columns):
                    df.iat[row_index, col_inedx] = column.get_text()
    
                    
            # Convert to float if possible
            for col in df:
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass
            
            return df