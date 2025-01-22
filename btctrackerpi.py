import time
import requests

# Fetch Bitcoin price from CoinGecko
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            return response.json()['bitcoin']['usd']
        except KeyError as e:
            print(f"Erro ao acessar a chave {e} na resposta da API.")
            return None
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

# Fetch Bitcoin transaction fee (sat/vbyte)
def get_btc_transaction_fee():
    url = "https://mempool.space/api/v1/fees/recommended"
    response = requests.get(url)
    return response.json()['fastestFee']

# Calculate USD in BTC
def get_usd_in_btc(btc_price):
    return 1 / btc_price

# Calculate 1 satoshi in USD
def get_satoshi_in_usd(btc_price):
    return btc_price / 100000000

# Update every second
while True:
    # Get data from API functions
    btc_price = get_btc_price()
    if btc_price is None:
        print("Erro ao obter o preço do Bitcoin.")
        break

    transaction_fee = get_btc_transaction_fee()
    usd_in_btc = get_usd_in_btc(btc_price)
    satoshi_in_usd = get_satoshi_in_usd(btc_price)

    # Print to console (just for testing)
    print(f"BTC: ${btc_price:,.2f}")
    print(f"1 USD = {usd_in_btc:,.8f} BTC")
    print(f"1 Satoshi = ${satoshi_in_usd:,.8f}")
    print(f"Fee: {transaction_fee} sat/vbyte")

    time.sleep(1)
