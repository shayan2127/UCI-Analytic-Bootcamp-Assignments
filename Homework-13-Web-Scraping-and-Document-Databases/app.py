import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data


@app.route('/scrape')
def scrape():
    
    print("\n\n\n")
    mars = scrape_mars.scrape()
    print("The scrape is working!")

    db.mars_data.insert_one(mars)
    return "Some scrapped data"

@app.route("/")
def home():
    mars = list(db.mars_data.find())
    print(mars)
    return render_template("index.html", mars = mars)


if __name__ == "__main__":
	app.run(debug=True)