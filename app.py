# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
import sys
from flask_pymongo import PyMongo

app = Flask(__name__)

# create instance of Flask app
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

#  create route that renders index.html template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)