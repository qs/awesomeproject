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

mongo.db.fridge.insert({"location": "Otakaari 24, 02150 Espoo", "availability": "6pm-10pm",
                        "products": {"7311311015304": {"amount": 3, "description": "some spice"}}})


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


@app.route("/get_suggestion", methods=["POST", "GET"])
def get_suggestion():
    user = request.data.get("username")
    grocery_list = request.data.get("grocery_list")
    x = request.data.get("x_loc")
    y = request.data.get("y_loc")
    user_data = mongo.db.users.find_one({"username": user})
    return suggestions.get_ranked_suggestions(user, user_data['preferences'], grocery_list, (x, y)), status.HTTP_200_OK


@app.route("/")
def index():
    return """

<!doctype html>
<html class="no-js" lang="">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title></title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <!-- Place favicon.ico in the root directory -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <link href='http://fonts.googleapis.com/css?family=Lato:100,400,100italic,400italic' rel='stylesheet' type='text/css'>
    <script src="http://rohitbsehgal.github.io/HHcomunity-landing-page/js/jquery.particleground.js"></script>

    <link rel="stylesheet" href="//rohitbsehgal.github.io/HHcomunity-landing-page/css/style.css">
  </head>
  <body>
  <!--[if lt IE 8]>
  <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
  <![endif]-->
  <div>
    <img class="logo" src="https://res.cloudinary.com/hackjunction/image/upload/c_crop,g_custom/v1543101698/zrh7hy4eckluagh9dl4b.gif" />
    <span class="hackathon-hackers-text">Grocery List Complete</span><br/>
    <span class="hackathon-hackers-text-under">The smart way to do it. <br/><a href="#" style="text-decoration: underline;">Download app</a></span>
  </div>
  <script src="http://rohitbsehgal.github.io/HHcomunity-landing-page/js/functions.js"></script>
  </body>
</html>    
"""


if __name__ == "__main__":
    app.run(debug=True)
