# Scrape amazon for basic info.
# Then scrapes for full data
# Then Amazon links
import requests
from bs4 import BeautifulSoup
from datetime import datetime
# from imageTools import makeImage
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox

# Now this script or any imported module can use any part of Django it needs.
from models import Product, PriceLink, Store

settings.configure()
STORE = Store.objects.get(name="Amazon")

# Basic Variables
# name
# img_thumb
# rank
# category
# subcategory
# asin
# release_date

# Link Extra Variables
# asin
# store
# price

API_URL = "https://thegiftrank.com/api/product/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
}


def getSoup(url):
    # r = requests.get(url, headers=headers)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    return soup


def getMoreData(rank, category, asin):
    # send details to api
    store = "amazon"
    url = 'https://www.{}.co.uk/dp/{}'.format(store, asin)
    soup = getSoup(url)
    price = soup.find(
        "span", class_="p13n-sc-price").get_text().strip("£").strip(".")
    print(price)
    mycategory = category
    realcategory = soup.select(
        "ul.a-size-small:nth-of-type(1) > li:nth-of-type(1) > span:nth-of-type(1) > a:nth-of-type(1)")[0].get_text()
    print(realcategory)
    subcategory = soup.select(
        "ul.a-size-small:nth-of-type(1) > li:nth-of-type(3) > span:nth-of-type(1) > a:nth-of-type(1)")[0].get_text()
    name = soup.find("span", id="productTitle").get_text()
    short_name = name[:6]
    print(short_name)
    img_thumb = soup.find("img", id="imgBlkFront").get("src")
    img_full = img_thumb
    # send_product = {'name': name, 'img_thumb': img_thumb, 'real_category': real_category,
    #                'subcategory': subcategory, 'asin': asin, 'release_date': release_date}
    # send_price_link = {'asin': asin, 'price': price, 'store': store}
    full = Product(
        name=name,
        short_name=short_name,
        description="None",
        short_description="None",
        img_thumb=img_thumb,
        img_full=img_full,
        rank=rank,
        mycategory=mycategory,
        realcategory=realcategory,
        subcategory=subcategory
    )
    full.save()
    sendpricelink = PriceLink(
        product=full,
        store=STORE,
        price=price,
        clicks=0,
        url=url
    )
    sendpricelink.save()
    print(f"{full}: {sendpricelink}")
    # post_link = postLink(send_price_link)


def asinScrape(category):
    # scrape the basic details
    products = []
    urls = ["https://www.amazon.co.uk/gp/most-gifted/{}".format(category),
            "https://www.amazon.co.uk/gp/most-gifted/{}/?pg=2".format(category)]
    for url in urls:
        soup = getSoup(url)
        products += soup.find_all("span", class_="a-list-item")
    for product in products:
        rank = product.find(
            "span", class_="zg-badge-text").get_text().strip("#")
        asin = product.find("span", class_="aok-inline-block").find(
            "a", class_="a-link-normal").get("href").split("/")[3].split("?")[0]
        print(f"{rank} {category} {asin}")
        getMoreData(rank=rank, category=category, asin=asin)
    # makeImage(category)
    return f"{category} finished"


options = Options()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)
try:
    this = asinScrape("electronics")
    print(this)
except:
    browser.quit()

# CATEGORIES = ['beauty', 'kids', 'electronics']

# for category in CATEGORIES:
#	asinScrape(category)
