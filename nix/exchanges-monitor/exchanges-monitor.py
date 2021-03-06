from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import start_http_server
import requests
import json
import random
import time
import urllib.request
import sys

#Create a metric to track time spent and requests made.
EXPORTER_PORT = 8000
SLEEP_TIME = 300 # 5 minutes
BINANCE_REQUEST_TIME = Summary('binance_process_time', 'Time spent processing binance assets')
BINANCE_MAINTENANCE_REQUEST_TIME = Summary('binance_maintenance_process_time', 'Time spent processing binance maintenance check')
BITTREX_REQUEST_TIME = Summary('bittrex_process_time', 'Time spent processing bittrex assets')
BITHUMB_REQUEST_TIME = Summary('bithumb_process_time', 'Time spent processing bithumb assets')
HITBTC_REQUEST_TIME = Summary('hitbtc_process_time', 'Time spent processing hitbtc assets')
COINEX_REQUEST_TIME = Summary('coinex_process_time', 'Time spent processing coinex assets')
BITMAX_REQUEST_TIME = Summary('bitmax_process_time', 'Time spent processing bitmax assets')
BITRUE_REQUEST_TIME = Summary('bitrue_process_time', 'Time spent processing bitrue assets')
HUOBI_REQUEST_TIME = Summary('huobi_process_time', 'Time spent processing huobi assets')
KUCOIN_REQUEST_TIME = Summary('kucoin_process_time', 'Time spent processing kucoin assets')
EXX_REQUEST_TIME = Summary('exx_process_time', 'Time spent processing exx assets')
BKEX_REQUEST_TIME = Summary('bkex_process_time', 'Time spent processing bkex assets')
MXC_REQUEST_TIME = Summary('mxc_process_time', 'Time spent processing mxc assets')
binance_active = Gauge('binance_active', 'Binance Wallet enabled')
bittrex_active = Gauge('bittrex_active', 'Bittrex Wallet enabled')
bittrex_withdraw_queue_depth = Gauge('bittrex_withdraw_queue_depth', 'Bittrex Withdraw Queue Depth')
huobi_deposits = Gauge('huobi_deposits', 'Huobi deposits enabled')
huobi_withdraws = Gauge('huobi_withdraw', 'Huobi withdraws enabled')
kucoin_deposits = Gauge('kucoin_deposits', 'Kucoin deposits enabled')
kucoin_withdraws = Gauge('kucoin_withdraw', 'Kucoin withdraws enabled')
bithumb_active = Gauge('bithumb_active', 'Bithumb Wallet enabled')
hitbtc_deposits = Gauge('hitbtc_deposits', 'Hitbtc Deposits enabled')
hitbtc_withdraws = Gauge('hitbtc_withdraws', 'Hitbtc Withdraws enabled')
coinex_deposits = Gauge('coinex_deposits', 'Coinex Deposits enabled')
coinex_withdraws = Gauge('coinex_withdraws', 'Coinex Withdraws enabled')
bitmax_active = Gauge('bitmax_active', 'Bitmax Wallet enabled')
bkex_deposits = Gauge('bkex_deposits', 'Bkex Deposits enabled')
bkex_withdraws = Gauge('bkex_withdraws', 'Bkex Withdraws enabled')
bitrue_active = Gauge('bitrue_active', 'Bitrue Wallet enabled')
exx_active = Gauge('exx_active', 'EXX Wallet enabled')
mxc_active = Gauge('mxc_active', 'MXC Wallet enabled')

# Decorate function with metric.
@BINANCE_REQUEST_TIME.time()
def process_binance_assets():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    json_obj = urllib.request.urlopen(url)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print("processing binance assets")
    access_content = crypto_assets['symbols']
    counter = 0
    for crypto_asset in access_content:
        if crypto_asset['baseAsset'] == 'ADA' and crypto_asset['status'] == 'TRADING':
            counter +=1
        elif crypto_asset['baseAsset'] == 'ADA' and crypto_asset['status'] != 'TRADING':
            counter -=1
    if counter > 3:
        binance_active.set(True)
    else:
        process_binance_maintenance()
    sys.stdout.flush()

# Decorate function with metric.
@BINANCE_MAINTENANCE_REQUEST_TIME.time()
def process_binance_maintenance():
    url = "https://api.binance.com/wapi/v3/systemStatus.html"
    json_obj = urllib.request.urlopen(url)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print("processing binance maintenance check")
    print(crypto_assets)
    if crypto_assets['status'] == 1:
        binance_active.set(True)
    elif crypto_assets['status'] == 0:
        print("failed to process Binance maintenance check")
        binance_active.set(False)

# Decorate function with metric.
@BITTREX_REQUEST_TIME.time()
def process_bittrex_assets():
    url = "https://bittrex.com/api/v2.0/pub/currencies/GetWalletHealth"
    json_obj = urllib.request.urlopen(url)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))["result"]
    print("processing bittrex assets")
    for crypto_asset in crypto_assets:
        if crypto_asset['Health']['Currency'] == "ADA":
            bittrex_active.set(crypto_asset['Health']['IsActive'])
            bittrex_withdraw_queue_depth.set(crypto_asset['Health']['WithdrawQueueDepth'])
    sys.stdout.flush()

# Decorate function with metric.
@HUOBI_REQUEST_TIME.time()
def process_huobi_assets():
    url = "https://api.huobi.pro/v2/reference/currencies"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    access_content = crypto_assets['data']
    print("processing huobi assets")
    for crypto_asset in access_content:
        if crypto_asset['currency'] == 'ada':
            confirm = crypto_asset['chains']
            for ada_live in confirm:
                if ada_live['withdrawStatus'] == 'allowed':
                    huobi_withdraws.set(True)
                if ada_live['depositStatus'] == 'allowed':
                    huobi_deposits.set(True)
                sys.stdout.flush()

def process_kucoin_assets():
    url = "https://api.kucoin.com/api/v1/currencies"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    access_content = crypto_assets['data']
    print("processing kucoin assets")
    for crypto_asset in access_content:
        if crypto_asset['currency'] == 'ADA':
            kucoin_withdraws.set(crypto_asset['isWithdrawEnabled'])
            kucoin_deposits.set(crypto_asset['isDepositEnabled'])
    sys.stdout.flush()

# Decorate function with metric.
@BITHUMB_REQUEST_TIME.time()
def process_bithumb_assets():
    url = "https://api.bithumb.com/public/ticker/ADA"
    json_obj = urllib.request.urlopen(url)
    crypto_asset = json.loads(json_obj.read().decode('utf-8'))
    print("processing bithumb assets")
    if crypto_asset['status'] == '0000':
        bithumb_active.set(True)
    sys.stdout.flush()

    # Decorate function with metric.
@HITBTC_REQUEST_TIME.time()
def process_hitbtc_assets():
    url = "https://api.hitbtc.com/api/2/public/currency/ADA"
    json_obj = urllib.request.urlopen(url)
    crypto_asset = json.loads(json_obj.read().decode('utf-8'))
    print("Processing HITbtc assets")
    if crypto_asset['id'] == 'ADA':
        hitbtc_deposits.set(crypto_asset['payinEnabled'])
        hitbtc_withdraws.set(crypto_asset['payoutEnabled'])
    sys.stdout.flush()

# Decorate function with metric.
@COINEX_REQUEST_TIME.time()
def process_coinex_assets():
    url = "https://api.coinex.com/v1/common/asset/config?coin_type=ADA"
    json_obj = urllib.request.urlopen(url)
    crypto_asset = json.loads(json_obj.read().decode('utf-8'))
    print ("Processing Coinex assets")
    if crypto_asset['code'] == 0:
        coinex_deposits.set(crypto_asset['data']['ADA']['can_deposit'])
        coinex_withdraws.set(crypto_asset['data']['ADA']['can_withdraw'])
    sys.stdout.flush()

# Decorate function with metric.
@BITMAX_REQUEST_TIME.time()
def process_bitmax_assets():
    url  = "https://bitmax.io/api/v1/assets"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print("processing bitmax assets")
    for crypto_asset in crypto_assets:
        if crypto_asset['assetCode'] == 'ADA' and crypto_asset['status'] == 'Normal':
            bitmax_active.set(True)
    sys.stdout.flush()

# Decorate function with metric.
@BKEX_REQUEST_TIME.time()
def process_bkex_assets():
    url = "https://api.bkex.com/v1/exchangeInfo"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print ("Processing bkex assets")
    access_content = crypto_assets['data']['coinTypes']
    for crypto_asset in access_content:
        if crypto_asset['coinType'] == 'ADA':
            bkex_deposits.set(crypto_asset['supportDeposit'])
            bkex_withdraws.set(crypto_asset['supportTrade'])
    sys.stdout.flush()

# Decorate function with metric.
@BITRUE_REQUEST_TIME.time()
def process_bitrue_assets():
    url = "https://www.bitrue.com/api/v1/exchangeInfo"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print ("Processing Bitrue assets")
    access_content = crypto_assets['symbols']
    for crypto_asset in access_content:
        if crypto_asset['symbol'] == 'ADABTC' and crypto_asset['status'] == 'TRADING':
            bitrue_active.set(True)
    sys.stdout.flush()

    # Decorate function with metric.
@EXX_REQUEST_TIME.time()
def process_exx_assets():
    url = "https://api.exx.com/data/v1/markets"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print ("Processing EXX assets")
    access_content = crypto_assets['ada_usdt']['isOpen']
    if access_content == True:
        exx_active.set(True)
    sys.stdout.flush()

    # Decorate function with metric.
@MXC_REQUEST_TIME.time()
def process_mxc_assets():
    url = "https://www.mxc.com/open/api/v1/data/markets"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print ("Processing MXC assets")
    access_content = crypto_assets['data']
    for crypto_asset in access_content:
     if crypto_asset == 'ada_usdt':
        mxc_active.set(True)
    sys.stdout.flush()

def process_get_height():
    url  = "http://localhost/api/blocks/pages"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_obj = urllib.request.urlopen(req)
    crypto_assets = json.loads(json_obj.read().decode('utf-8'))
    print(crypto_assets)
    blockheight = crypto_assets['Right'][0]['cbeBlkHeight']
    print(blockheight)
    sys.stdout.flush()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(EXPORTER_PORT)
    # Main Loop: Process all API's and sleep for a certain amount of time
    while True:
        try:
            process_binance_assets()
        except:
            print("failed to process Binance assets")
            binance_active.set(False)
        try:
            process_huobi_assets()
        except:
            print("failed to process huobi assets")
            huobi_deposits.set(False)
            huobi_withdraws.set(False)
        try:
            process_kucoin_assets()
        except:
            print("failed to process kucoin assets")
            kucoin_deposits.set(False)
            kucoin_withdraws.set(False)
        try:
            process_bittrex_assets()
        except:
            print("failed to process bittrex assets")
            bittrex_active.set(False)
            bittrex_withdraw_queue_depth.set(False)
        try:
            process_bithumb_assets()
        except:
            print("failed to process bithumb assets")
            bithumb_active.set(False)
        try:
            process_hitbtc_assets()
        except:
            print("failed to process hitbtc assets")
            hitbtc_active.set(False)
        try:
            process_coinex_assets()
        except:
            print("failed to process coinex assets")
            coinex_deposits.set(False)
            coinex_withdrawals.set(False)
        try:
            process_bitmax_assets()
        except:
            print("failed to process bitmax assets")
            bitmax_active.set(False)
        try:
            process_bkex_assets()
        except:
            print("failed to process bkex assets")
            bkex_deposits.set(False)
            bkex_withdraws.set(False)
        try:
            process_bitrue_assets()
        except:
            print("failed to process bitrue assets")
            bitrue_active.set(False)
        try:
            process_exx_assets()
        except:
            print("failed to process exx assets")
            exx_active.set(False)
        try:
            process_mxc_assets()
        except:
            print("failed to process mxc assets")
            mxc_active.set(False)
         #try:
           # process_get_height()
        #except:
         #   print("failed to process chainwalker")
         #   chainwalker_active.set(False)
        time.sleep(SLEEP_TIME)
