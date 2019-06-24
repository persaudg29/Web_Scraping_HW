from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
import scrape_mars



app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
db = client.mars_db
coll = db.mars_data_coll


@app.route("/")
def index():
    mars_mission_data = coll.find_one()

    return render_template("index.html", mars_mission_data=mars_mission_data)

from scrape_mars import scrape_mars
@app.route("/scrape")
def scrape():
    mars_mission_data = scrape_mars()

    # Insert mars_mission_data into database
    coll.update({"id": 1}, {"$set": mars_mission_data}, upsert = True)

    # Redirect back to home page
    #return redirect("/", code=302)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
