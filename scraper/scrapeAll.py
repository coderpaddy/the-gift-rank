# Scrape amazon for basic info.
# Then scrapes for full data
# Then Amazon links
from requests import post
# import urllib3
import re
from bs4 import BeautifulSoup
import time

# from imageTools import makeImage
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver import Firefox


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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"
}

count = 0
outof = 0


def getSoup(url):
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    return soup


def stripped(item):
    return (
        item.replace("\n", "").replace("    ", "").replace("   ", "").replace("  ", "")
    )


def myPost(data):
    try:
        r = post(url="http://127.0.0.1:8000/add/new", data=data)
        return r.status_code
    except Exception as ex:
        print(ex)
        time.sleep(5)
        myPost(data)


def getMoreData(rank, category, asin):
    # send details to api
    global count
    global outof
    store = "amazon"
    url = "https://www.{}.co.uk/dp/{}".format(store, asin)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    price = soup.find_all(string=re.compile(r"£"))
    price = stripped(price[0].replace("£", "").replace(".", "").replace(" ", ""))
    if "-" in price:
        prices = price.split("-")
        price = prices[1]
    mycategory = category
    categories = soup.select("#wayfinding-breadcrumbs_feature_div > ul > li > span > a")
    if categories:
        realcategory = stripped(categories[0].get_text())
        subcategory = stripped(categories[1].get_text())
    else:
        realcategory = "None"
        subcategory = "None"
    name = soup.find("span", id="productTitle").get_text()
    name = stripped(name)
    short_name = name[:25]
    img_thumb = soup.select("#imgTagWrapperId > img")[0].get("data-old-hires")
    img_full = img_thumb
    data = {
        "name": name,
        "short_name": short_name,
        "description": "None",
        "short_description": "None",
        "img_thumb": img_thumb,
        "img_full": img_full,
        "rank": int(rank),
        "mycategory": mycategory,
        "realcategory": realcategory,
        "subcategory": subcategory,
        "price": price,
        "clicks": 0,
        "url": url,
    }
    outof += 1
    r = myPost(data)
    if r == 200:
        count += 1
    print(f"{count} out of {outof} succesful \t {category}: {rank} \t {r}")


def asinScrape(category):
    # scrape the basic details
    products = []
    urls = [
        "https://www.amazon.co.uk/gp/most-gifted/{}".format(category),
        "https://www.amazon.co.uk/gp/most-gifted/{}/?pg=2".format(category),
    ]
    for url in urls:
        soup = getSoup(url)
        products += soup.find_all("span", class_="a-list-item")
    for product in products:
        rank = product.find("span", class_="zg-badge-text").get_text().strip("#")
        asin = (
            product.find("span", class_="aok-inline-block")
            .find("a", class_="a-link-normal")
            .get("href")
            .split("/")[3]
            .split("?")[0]
        )
        print(f"{rank} {category} {asin}")
        getMoreData(rank=rank, category=category, asin=asin)
    # makeImage(category)
    return f"{category} finished"


options = Options()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)

CATEGORIES = ["beauty", "kids", "electronics", "health", "drugstore", "outdoors"]
# CATEGORIES = ['health']
for category in CATEGORIES:
    try:
        this = asinScrape(category)
        print(this)
    except Exception as ex:
        browser.quit()
        print(ex)
