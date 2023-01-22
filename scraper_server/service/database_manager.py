import sqlite3
import threading

db = sqlite3.connect("/Users/PRGM78/PycharmProjects/scraper_server/data3.db", check_same_thread=False)
lock = threading.Lock()
cursor = db.cursor()


def create_offers_table():
    try:
        lock.acquire(True)
        cursor.execute('''CREATE TABLE IF NOT EXISTS offers
                   (url text, name text, address text, price text, size text, price_per_meter integer)''')
        db.commit()
    finally:
        lock.release()


def add_offer_to_database(url, title, address, price, size, price_per_meter):
    try:
        lock.acquire(True)
        print("add3")
        cursor.execute('INSERT INTO offers VALUES(?, ?, ?, ?, ?, ?)',
                    (url, title, address, price, size, price_per_meter))
        db.commit()
    finally:
        lock.release()


def get_offers_from_database():
    try:
        lock.acquire(True)
        data = cursor.execute("SELECT * FROM offers ").fetchall()
    finally:
        lock.release()
    return data


def get_avg_price_per_meter_offers_with_address(address):
    try:
        lock.acquire(True)
        data = cursor.execute("SELECT AVG(price_per_meter) FROM offers WHERE address = \"{}\"".format(address)).fetchall()
    finally:
        lock.release()
    return data


def if_offer_exists(url):
    try:
        lock.acquire(True)
        if_exists = len(cursor.execute("SELECT * FROM offers WHERE url=?", (url,)).fetchall()) != 0
    finally:
        lock.release()
    return if_exists

create_offers_table()




