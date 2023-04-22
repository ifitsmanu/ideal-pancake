
import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.nfl.com/standings/league/2020/reg/'
#Asks the server we can copy the HTML
page = requests.get(url)
#Parses the HTML of the webpage and copies it into Python
soup = BeautifulSoup(page.text, 'lxml')


table_data = soup.find('table', class_ = "d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-standings--detailed d3-o-table--sortable {sortlist: [[4,1]], sortinitialorder: 'desc'}")


headers = []
for i in table_data.find_all('th'):
    title = i.text.strip()
    headers.append(title)
df = pd.DataFrame(columns = headers)

for j in table_data.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [tr.text.strip() for tr in row_data]
        length = len(df)
        df.loc[length] = row





