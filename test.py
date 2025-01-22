import time
from waveshare_epd import epd2in7
from PIL import Image, ImageDraw, ImageFont

# Inicializar a tela
epd = epd2in7.EPD()
epd.init()
epd.Clear()

# Criar uma imagem para desenhar no display
image = Image.new('1', (epd.width, epd.height), 255)  # Criar uma imagem branca
draw = ImageDraw.Draw(image)

# Usar uma fonte padrão
font = ImageFont.load_default()
draw.text((10, 10), "Olá, Mundo!", font=font, fill=0)

# Atualizar a tela com a imagem criada
epd.display(epd.getbuffer(image))

# Manter a imagem na tela
time.sleep(2)

# Limpar a tela
epd.sleep()
