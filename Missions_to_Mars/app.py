from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars  #this is scrape_mars.py containing scrape_all function
import pymongo


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection // mars_app is the db
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
   web_data = mongo.db.web_data.find_one()
   news_title = web_data['title']
   news_p = web_data['text']
   featured_img = web_data['featured_img']
   facts = web_data['facts']
   hems = web_data['hems']

   return render_template("index.html", news_title = news_title, news_p = news_p, featured_img = featured_img, facts = facts, hems = hems)

# this route is a trick to make the button execute the scrape and then reload the index with the scraped data present.
@app.route("/scrape")
def scraper():
   web_data = mongo.db.web_data
   web_data_dict = scrape_mars.scrape_all()
   web_data.update({}, web_data_dict, upsert=True)
   return redirect("/", code=302)


if __name__ == "__main__":
   app.run(debug=True)