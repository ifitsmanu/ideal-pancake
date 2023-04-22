

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(
        'C:/Paste Path Here/chromedriver.exe')

driver.get('https://www.nike.com/ca/w/sale-3yaep')


last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height


soup = BeautifulSoup(driver.page_source, 'lxml')

#Grabs the HTML of each product
product_card = soup.find_all('div', class_ = 'product-card__body')

#Creates an empty dataframe where the product information will go
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Subtitle':[''], 'Price':[''], 'Sale Price':['']})

#This loop will then go through the HTML of each posting and find the link, name, subtitle, full price, and sale price for each product
for product in product_card:
    try:
        link = product.find('a', class_ = 'product-card__link-overlay').get('href')
        name = product.find('div', class_ = 'product-card__title').text
        subtitle = product.find('div', class_ = 'product-card__subtitle').text
        full_price = product.find('div', class_ = 'product-price css-1h0t5hy').text
        sale_price = product.find('div', class_ = 'product-price is--current-price css-s56yt7').text
        #The link, name, subtitle, full price, and sale price for each product is added to our dataframe 
        df = df.append({'Link':link, 'Name':name, 'Subtitle':subtitle, 'Price':full_price, 'Sale Price':sale_price},
                    ignore_index = True)
    except:
        pass



df = df.iloc[1:,:]
def dollar_sign(x):
    try:
        x = x[1:]
        return float(x)
    except:
        pass
df['Price'] = df['Price'].apply(dollar_sign)
df['Sale Price'] = df['Sale Price'].apply(dollar_sign)
df['Discount Percentage'] = (((df['Price'] - df['Sale Price'])/df['Price'])*100).round(2)


print(df)

df.to_csv('Nike.csv', index = False)




