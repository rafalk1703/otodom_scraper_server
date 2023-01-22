from flask import Flask
from service.data_analize import most_popular_districts, district_per_price
from service.scraper import scrape_data_to_database
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/scrape_data")
def scrape_data():
    scrape_data_to_database()
    return "<p>Hello, World!</p>"


@app.route("/most_popular_districts")
def most_popular():
    print(most_popular_districts())
    return most_popular_districts()


@app.route("/district_per_price")
def district():
    return district_per_price()


if __name__ == "__main__":
    app.run()
