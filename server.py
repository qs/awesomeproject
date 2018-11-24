from flask import request, url_for
import flask_api
from models import Wish
from flask_api import FlaskAPI, status
from collections import defaultdict
from flask_pymongo import PyMongo
import json
from suggestions import Suggestions
database = {}


'''
"7311311015304": {"type": "borrow", "location": "Some address", "availability": "6pm-10pm every day", "description": "details from the fridge keeper", "photo": "http://url"},
"6410405082657": {"type": "replace", "product_ean": "6410405113153"},
"6408641027488": {"type": "coop", "friends": ["friend1", "friend2", "friend3"]}
'''

app = FlaskAPI(__name__)
app.config["MONGO_URI"] = "mongodb://awesome1:awesome1@ds063789.mlab.com:63789/awesomeproject"
mongo = PyMongo(app)
suggestions = Suggestions(mongo.db)

mongo.db.users.delete_many({})
mongo.db.fridge.delete_many({})

mongo.db.users.insert({
    "username": "ivan",
    "preferences": {
        "cheap": 0.5,
        "sustainability": 0.2,
        "comfort": 3
    },
    "wishlist": ["7311311015304", "6410405082657", "6408641027488"]
})

mongo.db.users.insert({
    "username": "freya",
    "preferences": {
        "cheap": 0.5,
        "sustainability": 0.2,
        "comfort": 3
    },
    "wishlist": ["6410405082657", "6408641027488"]
})

mongo.db.fridge.insert({
    "fridge_id": "ivan",
    "availability": {
        "from_hours": 10,
        "to_hours": 14
    },
    "location": "finnland street 12",
    "products": [
        {"4001724819608": {
            "amount": 2,
            "exp_date": "21-12-2018",
            "image": "http://fotopotato.com/wp-content/uploads/2016/04/Baby-Carrot-825x510.jpg",
            "description": "long durability"

        }},
        {"6411402202208": {
            "amount": 1,
            "exp_date": "26-11-2018",
            "image": "",
            "description": "will throw out on monday"
        }}

    ]
})

mongo.db.fridge.insert({
    "fridge_id": "johannes",
    "availability": {
        "from_hours": 14,
        "to_hours": 21
    },
    "location": "helsinki road 100",
    "products": [
        {"6411402202208": {
            "amount": 1,
            "exp_date": "21-12-2018",
            "image": "",
            "description": "great product, hurry up"
        }},
        {"6416046654123": {
            "amount": 1,
            "exp_date": "26-11-2018",
            "image": "",
            "description": "dont want it anymore"
        }}

    ]
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
    username = request.args.get("username")
    data = mongo.db.users.find_one({"username": username})
    del data["_id"]
    return data, status.HTTP_200_OK


@app.route("/get_suggestion")
def get_suggestion():
    user = request.data.get("username")
    grocery_list = request.data.get("grocery_list")
    x = request.data.get("x_loc")
    y = request.data.get("y_loc")
    user_data = mongo.db.users.find({"username": user})
    return suggestions.get_ranked_suggestions(user_data['preferences'], grocery_list, (x, y)), status.HTTP_200_OK


if __name__ == "__main__":
    app.run(debug=True)
