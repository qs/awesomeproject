from collections import OrderedDict


class Suggestions:
    def __init__(self, db):
        self.db = db
        self.healthy_replacements = {
            '6410405082657': '6410405113153'
        }

    def get_ranked_suggestions(self, username, user_preferences, grocery_list, geolocation):
        """
        :param user_preferences: dict like { "cheap" : 0.5, "sustainability" : 0.2, "comfort" : 3 }
        :param grocery_list: dict like {"7311311015304": 1, "6410405082657": 2, "6408641027488": 1}
        :param geolocation: tuple of floats (x, y)
        :return: dict {
            "7311311015304": {"type": "borrow", "location": "Some address", "availability": "6pm-10pm every day", "description": "details from the fridge keeper", "photo": "http://url"},
            "6410405082657": {"type": "replace", "product_ean": "6410405113153"},
            "6408641027488": {"type": "coop", "friends": ["friend1", "friend2", "friend3"]}
        }
        """
        suggerstions = []
        for product_ean, amount in grocery_list.items():
            suggerstions += self.get_borrow_suggestions(product_ean, amount)
            suggerstions += self.get_replace_suggestions(product_ean)
            suggerstions += self.get_coop_suggestions(username, product_ean, amount)

            suggerstions += [
                {product_ean: self.get_borrow_suggestions(product_ean, amount)}]
            suggerstions += self.get_replace_suggestions(product_ean)
            suggerstions += [{product_ean:
                              self.get_coop_suggestions(username, product_ean, amount)}]
        return self.ranked_suggestions(suggerstions, user_preferences)

    def get_borrow_suggestions(self, product_ean, amount):
        sugges = []
        for fridge in self.db.fridge.find():
            for fridge_product_ean, fridge_product_data in fridge["products"].items():
                if fridge_product_ean == product_ean:
                    sugges.append(
                        {fridge_product_ean:
                             {
                                 "type": "borrow",
                                 "location": fridge["location"],
                                 "availability": fridge["availability"],
                                 "description": fridge_product_data["description"]
                             }})
        return sugges

        for fridge in self.db.fridge.find():
            for product_dict in fridge["products"]:
                product = list(product_dict.keys())[0]
                properties = list(product_dict.values())[0]
                print(properties)
                if product == product_ean and properties["amount"] >= amount:
                    sugges.append({
                        "type": "borrow",
                        "location": fridge["location"],
                        "availability": str(fridge["availability"]["from_hours"]) + " to " + str(fridge["availability"]["to_hours"]),
                        "description": properties["description"],
                        "image": properties["image"]

                    })
        return [{product_ean: i} for i in sugges]

    def get_replace_suggestions(self, product_ean):
        # should actually go to the kesko database and smartly compare which products are similar and healthier
        if product_ean in self.healthy_replacements:
            return [{product_ean: {'type': 'replace', 'product_ean': self.healthy_replacements[product_ean]}}]
        return []

    def get_coop_suggestions(self, username, product_ean, amount):
        friends = [user for user in self.db.users.find() if username != user['username']]
        friends_to_buy_the_same = []
        for user in friends:
            if product_ean in user["wishlist"]:
                friends_to_buy_the_same.append(user['username'])
        if friends_to_buy_the_same:
            return [{product_ean: {"type": "coop", "friends": friends_to_buy_the_same}}]
        return []

    def ranked_suggestions(self, suggerstions, user_preferences):
        pref_lookup = {'coop': 'cheap', 'replace': 'sustainability', 'borrow': 'comfort'}
        result_suggestions = OrderedDict()
        for suggerstion in suggerstions:
            for k, v in suggerstion.items():
                if v and k not in result_suggestions:
                    result_suggestions[k] = v
        print(result_suggestions)
        return result_suggestions
