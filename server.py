from flask import request, url_for
import flask_api
from models import Wish
from flask_api import FlaskAPI, status
from collections import defaultdict
from flask_pymongo import PyMongo
import json
database = {}


app = FlaskAPI(__name__)
app.config["MONGO_URI"] = "mongodb://awesome1:awesome1@ds063789.mlab.com:63789/awesomeproject"
mongo = PyMongo(app)

mongo.db.users.delete_many({})

mongo.db.users.insert({
    "username": "ivan",
    "preferences": {
        "cheap": 0.5,
        "sustainability": 0.2,
        "comfort": 3
    },
    "wishlist": [12312312, 124123123, 1231234123]
})

mongo.db.users.insert({
    "username": "freya",
    "preferences": {
        "cheap": 0.5,
        "sustainability": 0.2,
        "comfort": 3
    },
    "wishlist": [12312312, 124123123, 1231234123]
})


@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.data.get("username")
    preferences = request.data.get("preferences")
    friends = request.data.get("friends")


@app.route("/update-wish-list", methods=["POST"])
def update_wish_list():
    username = request.data.get("username")
    wishlist = json.loads(request.data.get("wishlist"))
    data = mongo.db.users.find_one({"username": username})
    print(data["_id"])
    a = mongo.db.users.update({"username": username}, {
        "$set": {"wishlist": wishlist}})
    # database[username] = wishlist
    print(a)
    print(wishlist)
    data = mongo.db.users.find_one({"username": username})
    del data["_id"]
    return data, status.HTTP_200_OK


@app.route("/get-wish-list")
def get_wish_list():
    username = request.data.get("username")
    data = mongo.db.users.find_one({"username": username})
    del data["_id"]
    return data, status.HTTP_200_OK


@app.route("/get_suggestion")
def get_suggestion():
    user = request.data.get("username")
    x = request.data.get("x_loc")
    y = request.data.get("y_loc")
    data = mongo.db.users.find({"username": user})
    # get preferences from db
    preference = "cheaper"
    #
    wishlist = ["334242", "5643534", "4524324"]

    execute_query()


if __name__ == "__main__":
    app.run(debug=True)
