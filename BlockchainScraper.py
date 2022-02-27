from bs4 import BeautifulSoup as bs
import pandas as pandas
import requests

url = r"https://www.blockchain.com/btc/unconfirmed-transactions"
request = requests.get(url)
soup = bs(request.text)
print(soup.prettify)