import os
import shutil
from math import ceil

import json
from urllib.request import urlopen, urlretrieve

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from requests import get
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs, BeautifulSoup
import sqlite3
import smtplib, ssl
from database_manager import add_offer_to_database, if_offer_exists, get_offers_from_database

from model.offer import Offer

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "otodomscraper0000@gmail.com"  # Enter your address
receiver_email = "rafalk1703@gmail.com"  # Enter receiver address

offersPerPage = 24

# db = sqlite3.connect("data3.db")

# cursor = db.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS offers
#                (url text, name text, address text, price text, size text, price_per_meter text)''')


# return parsed html file
def download_page(url):
    # try:
    #     request = Request(url, headers={
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 ' +
    #                       '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
    #     sauce = urlopen(request).read()
    #     soup = bs(sauce.decode('utf-8', 'ignore'), 'lxml')
    # except HTTPError:
    #
    #     soup = None

    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome()

    # browser = webdriver.Chrome(options=options)
    driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.visibility_of_element_located((By.ID, "signin-email")))
    # driver.implicitly_wait(35)
    html_source = driver.page_source
    driver.quit()

    soup = bs(html_source, 'html.parser')
    return soup


# return amount of ofers in specific category
def get_offers_amount(url):
    html = download_page(url)

    offers_amount = html.find('strong', {"data-cy": "search.listing-panel.label.ads-number"}).select_one(
        "strong span:nth-of-type(2)").text if html else '0'
    return int(''.join(offers_amount.split()))


# return list of offers on page
def get_offers(url):
    html = download_page(url)
    div_container = html.find('div', {'data-cy': 'search.listing.organic'})

    for article in div_container.find_all('li'):
        if article.get('data-cy') == 'listing-item':
            parse_article(article)


def parse_article(article):
    title = article \
        .find("article") \
        .find('h3', {'data-cy': 'listing-item-title'}) \
        .getText()
    address = article \
        .find("article") \
        .findChildren('p', recursive=False)[0] \
        .find('span') \
        .getText()
    price = article \
        .find("article") \
        .findChildren('div', recursive=False)[1] \
        .findChildren('span', recursive=False)[0] \
        .getText()
    price_per_meter = article \
        .find("article") \
        .findChildren('div', recursive=False)[1] \
        .findChildren('span', recursive=False)[1] \
        .getText()
    size = article \
        .find("article") \
        .findChildren('div', recursive=False)[1] \
        .findChildren('span', recursive=False)[3] \
        .getText()
    url = article \
        .find('a', {'data-cy': 'listing-item-link'}) \
        .get('href')
    print(title)
    district = ""
    price_per_meter_no_whitespaces = ""
    address_elements = address.split(",")
    if address_elements[0] == "Kraków":
        if address_elements[1].strip() not in ["Kraków", "małopolskie"]:
            district = address_elements[1].strip()
            print(address_elements[1].strip())

    print("!!!!!ADDRESSSSSSSSS!!!!!")
    print(price_per_meter)

    if price_per_meter:
        price_per_meter_no_whitespaces = price_per_meter.split("z")[0].replace(" ", "").replace(" ", "")
        print(price_per_meter_no_whitespaces)



    if district and price_per_meter:
        add_offer(title, district, price, price_per_meter_no_whitespaces, size, url)
        print("add1")
        # print(address)
        # print(price)
        # print(price_per_meter)
        # print(size)
        # print(url)


def add_offer(title, address, price, price_per_meter, size, url):
    if not if_offer_exists(url):
        print("add2")
        add_offer_to_database(url, title, address, price, size, int(price_per_meter))


def send_email(offer):
    context = ssl.create_default_context()
    message = """\
    Subject: nowe mieszkanie\n\n
    Nowe mieszkanie: {}

    Adres: {}
    Cena: {}
    Nazwa: {} """.format(offer.url, offer.address, offer.price, offer.name).encode('utf-8', errors='ignore')

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, "ksoo dwkz qkla rmig")
        server.sendmail(sender_email, receiver_email, message)
    print(offer.url)
    print(offer.name)
    print(offer.price)
    print(offer.address)


# generate page url
def get_page_url(url, page_number):
    return url if page_number == 1 else f'{url}&limit={offersPerPage}&page={page_number}'


def get_pages_amount(url):
    return ceil(get_offers_amount(url) / offersPerPage)


def scrape_data_to_database():

    print(get_offers_from_database)
    offers_to_buy_url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/krakow?distanceRadius=0&market=ALL&areaMax=45&locations=%5Bcities_6-38%5D&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&searchingCriteria=cala-polska"

    pages_amount = get_pages_amount(offers_to_buy_url)

    for page_number in range(70, 80):
        page_url = get_page_url(offers_to_buy_url, page_number)
        get_offers(page_url)


if __name__ == "__main__":

    scrape_data_to_database()

    # cursor = db.cursor()
    #
    # print(cursor.execute("SELECT * FROM offers ").fetchall())
    #
    # offers_to_buy_url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/krakow?distanceRadius=0&market=ALL&areaMax=45&locations=%5Bcities_6-38%5D&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&searchingCriteria=cala-polska"
    #
    # pages_amount = get_pages_amount(offers_to_buy_url)
    #
    # for page_number in range(1, 3):
    #     page_url = get_page_url(offers_to_buy_url, page_number)
    #     get_offers(page_url)

    # s = "Kraków, Podgórze Duchackie, ul. Walerego Sławka"
    # address_elements = s.split(",")
    # if (address_elements[0] == "Kraków"):
    #     print(address_elements[1].strip())
    # print()
    # print(el)
    # for e in el:
    #     print(e)
    #     e2 = e.strip()
    #     print(e2)
    # print(el)

    # print(page_number)

    # # main()
    # offers_url = "https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/krakow?distanceRadius=0&page=1&limit=72&market=ALL&ownerTypeSingleSelect=ALL&locations=%5Bcities_6-38%5D&priceMin=1700&priceMax=2800&viewType=listing"
    # url = "https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/krakow?distanceRadius=0&page=1&limit=24&market=ALL&ownerTypeSingleSelect=ALL&locations=%5Bcities_6-38%5D&viewType=listing"
    #
    # offers_to_buy_url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/krakow?distanceRadius=0&market=ALL&areaMax=45&locations=%5Bcities_6-38%5D&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&searchingCriteria=cala-polska&limit=24"
    #
    # # print(get_offers_amount(url))
    # # print(get_offers(url))
    # # get_offers(url)
    #
    # urls = get_offers(offers_to_buy_url)
    # print(len(urls))
    # for url in urls:
    #     # url = '/pl/oferta/wynajme-lokal-mieszkalny-z-jednym-pokojem-krakow-ID4i1Co'
    #
    #     offer_url = f'https://www.otodom.pl{url}'
    #
    #     parse_offer(offer_url)

    # db.close()
