from flask import request, url_for
import flask_api
from models import Wish
from flask_api import FlaskAPI, status
from collections import defaultdict
from flask_pymongo import PyMongo
database = {}


app = FlaskAPI(__name__)
app.config["MONGO_URI"] = "mongodb://awesome1:awesome1@ds063789.mlab.com:63789/awesomeproject"
mongo = PyMongo(app)


@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.data.get("username")
    preferences = request.data.get("preferences")
    friends = request.data.get("friends")


@app.route("/update-wish-list", methods=["POST"])
def update_wish_list():
    username = request.data.get("username")
    wishlist = request.data.get("wishlist")
    database[username] = wishlist
    print(database[username])
    return "", status.HTTP_200_OK


@app.route("/get_wish_list")
def get_wish_list():
    username = request.data.get("username")
    return database[username], status.HTTP_200_OK


@app.route("/get_suggestion")
def get_suggestion():
    user = request.data.get("username")
    # get preferences from db
    preference = "cheaper"
    #
    wishlist = ["334242", "5643534", "4524324"]

    execute_query()


if __name__ == "__main__":
    app.run(debug=True)
