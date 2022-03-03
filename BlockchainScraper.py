from bs4 import BeautifulSoup as bs
import requests
import json
import time

def scrape_blockchain():
    html_text = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions').text
    soup = bs(html_text, 'lxml')
    tables = soup.find_all('div', class_ = 'sc-1g6z4xm-0 hXyplo')

    hash_list = []
    time_list = []
    btc_amount_list = []
    usd_amount_list = []

    # Get highest transaction data and index
    def highest_transaction():
        # Get transaction amount in USD
        for table in tables:
            usd_amount = table.find_all('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
            usd_amount_list.append(usd_amount[2].text)
    # Formatting the USD amount
        new_usd_amount_list = []
        for x in usd_amount_list:
            no_dollar = x.replace('$', '')
            no_comma = no_dollar.replace(',', '')
            new_usd_amount_list.append(no_comma)

        # Converting list of string to list of float
        results = [float(i) for i in new_usd_amount_list]
        # Look for the highest transaction
        find_highest_value = max(results)

        # Find the index of the highest transaction
        find_highest_value_index = results.index(find_highest_value)
        return find_highest_value_index 

    x = highest_transaction()

    # Get transaction hash data
    def hash_data(x):
        for table in tables:
                hash = table.find_all('a', class_ = 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK')
                hash_list.append(hash[0].text)
        max_hash = hash_list[x]
        return max_hash

    # Get transaction time data
    def time_data(x):
        for table in tables:
            time = table.find_all('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
            time_list.append(time[0].text)
        max_time = time_list[x]
        return max_time

    #Get transaction amount in BTC
    def btc_amount_data(x):
        for table in tables:
            btc_amount = table.find_all('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
            btc_amount_list.append(btc_amount[1].text)
        max_btc_amount = btc_amount_list[x]
        return max_btc_amount

    # Get highest transaction amount in USD
    def max_usd_amount_data(x):
        for table in tables:
            usd_amount = table.find_all('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
            usd_amount_list.append(usd_amount[2].text)
        max_usd_amount = usd_amount_list[x]
        return max_usd_amount


    # Storing the highest transaction in an dictionary
    transaction_dict = {
    'Hash': hash_data(x),
    'Time': time_data(x),
    'Amount (BTC)': btc_amount_data(x),
    'Amount (USD)': max_usd_amount_data(x)
    }

    with open('transaction.log', 'w') as file:
        file.write(json.dumps(transaction_dict))
    print('Added to transaction.log')

if __name__ == '__main__':
    while True:
        scrape_blockchain()
        wait_time = 60
        print(f'Waiting {wait_time} seconds...')
        time.sleep(wait_time)