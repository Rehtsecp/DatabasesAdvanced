# DatabasesAdvanced 
## Blockchainscraper

### Introduction
This is a scraper, that will output the most valuable Hash for BTC per minute of unconfirmed transactions of: https://www.blockchain.com/btc/unconfirmed-transactions.

### Requirements
A couple of packages should be installed before running this program.
<ul>
    <li>BeautifulSoup</li>
    <li>requests</li>
    <li>json</li>
    <li>time</li>
</ul>

### Usage
Download **BlockchainScraper.py** </br>
Open a terminal on your device and and go to the directory where the python program is located </br>
Type **python BlockchainScraper.py** </br>

It should now be running and will be writing to **transaction.log** (located in the same directory as the program) every minute.
