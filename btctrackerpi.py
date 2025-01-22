import time
import requests
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd import epd
import adafruit_inkypHAT

# Inicializa o display E Ink
epd = adafruit_inkypHAT.InkyPHAT('black', rotation=180)  # 'black' para usar a cor preta
epd.set_border(epd.WHITE)

# Função para buscar o preço do Bitcoin
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

# Função para buscar a taxa de transação do Bitcoin
def get_btc_transaction_fee():
    url = "https://mempool.space/api/v1/fees/recommended"
    response = requests.get(url)
    return response.json()['fastestFee']

# Função para calcular USD para BTC
def get_usd_in_btc(btc_price):
    return 1 / btc_price

# Função para calcular 1 satoshi em USD
def get_satoshi_in_usd(btc_price):
    return btc_price / 100000000

# Função para atualizar o display E Ink
def update_display(btc_price, transaction_fee, usd_in_btc, satoshi_in_usd):
    # Cria uma imagem para desenhar
    image = Image.new('1', (epd.width, epd.height))
    draw = ImageDraw.Draw(image)

    # Define a fonte
    font = ImageFont.load_default()

    # Limpa a tela (branca)
    epd.fill(epd.WHITE)

    # Escreve as informações no display
    draw.text((10, 10), f"BTC: ${btc_price:,.2f}", font=font, fill=255)
    draw.text((10, 40), f"1 USD = {usd_in_btc:,.8f} BTC", font=font, fill=255)
    draw.text((10, 70), f"1 Satoshi = ${satoshi_in_usd:,.8f}", font=font, fill=255)
    draw.text((10, 100), f"Fee: {transaction_fee} sat/vbyte", font=font, fill=255)

    # Atualiza a tela
    epd.image(image)
    epd.display()

# Atualiza a cada 5 segundos
while True:
    # Pega os dados das funções
    btc_price = get_btc_price()
    if btc_price is None:
        print("Erro ao obter o preço do Bitcoin.")
        break

    transaction_fee = get_btc_transaction_fee()
    usd_in_btc = get_usd_in_btc(btc_price)
    satoshi_in_usd = get_satoshi_in_usd(btc_price)

    # Exibe as informações na tela
    update_display(btc_price, transaction_fee, usd_in_btc, satoshi_in_usd)

    # Espera 5 segundos antes de atualizar novamente
    time.sleep(5)
