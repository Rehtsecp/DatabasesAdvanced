from bs4 import BeautifulSoup as bs
import pymongo as mongo
import requests, json, time, redis, subprocess

# Runs setup.sh
#rc = subprocess.call('./setup.sh', shell=True)

# Connect to MongoDB
client = mongo.MongoClient ('mongodb://127.0.0.1:27017')
# Creating a new database
transaction_db = client['Blockchain']
# Creating a collection
collection_name = transaction_db['unconfirmed_transactions']

# Connect to Redis
r = redis.Redis()

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

    # Writing to a transaction log
    #with open('transaction.log', 'a') as file:
    #    file.write(json.dumps(transaction_dict))
    #    file.write('\n')
    #print('Added to transaction.log')

    # This will set the keys
    r.mset(transaction_dict)

    # This will insert the current highest transaction into MongoDB
    collection_name.insert_one(transaction_dict)

# This will allow the program to only run when in use, and will scrape the website every minute
if __name__ == '__main__':
    while True:
        scrape_blockchain()
        print(f'Inserted in MongoDB: "{transaction_db.name}"')
        wait_time = 60
        print(f'Waiting {wait_time} seconds...')
        time.sleep(wait_time)