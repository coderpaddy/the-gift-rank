from PIL import Image
from datetime import datetime
import requests


api = "https://thegiftrank.com/api/product/read_one.php"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
}


def getImage(category, rank):
    params = {'category': category, 'rank': rank}
    r = requests.get(api, params=params, headers=headers)
    url = r.json()['product_img']
    im = Image.open(requests.get(url, stream=True).raw)
    return im


def makeImage(category):
    img = Image.new('RGB', (600, 200), color='white')
    width = 0
    for i in range(1, 4):
        img.paste(getImage(category, i), (width, 0))
        width += 200
    tdate = datetime.today().strftime('%Y-%m-%d')
    img.save(f"{tdate}-{category}.jpg")
    return img

# makeImage("kids")
