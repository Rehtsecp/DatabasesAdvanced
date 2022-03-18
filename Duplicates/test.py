from bs4 import BeautifulSoup as bs
import pymongo as mongo
import requests, json, time, redis, subprocess


html_text = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions').text
soup = bs(html_text, 'lxml')
tables = soup.find_all('div', class_ = 'sc-1g6z4xm-0 hXyplo')

hash_list = []
time_list = []
btc_amount_list = []
usd_amount_list = []

print(tables)