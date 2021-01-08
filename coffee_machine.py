#!/usr/bin/python3
import json
import os
from pprint import pprint

# pycov


class CoffeeMachine:
    """ """

    def __init__(self, persist=False):
        internals = self.get_internals()
        self.menu = internals.get("menu")
        self.resources = internals.get("resources")
        self.money = internals.get("money")
        self.offerings = list(self.menu.keys())
        self.accepted_coins = internals.get("accepted_coins")

    def make_drink(self, ingredients):
        for k in self.resources:
            old_val = self.resources.get(k)
            self.resources.update({k: old_val - ingredients.get(k)})

    def check_resources(self, request_ingredients):
        """ """
        for key, value in request_ingredients.items():
            if value > self.resources.get(key):
                return False, key
        return True, None

    def handle_coins(self, coins):
        coins = coins.replace(" ", "")
        unparsed_quantity = ""
        denom = None
        for index, c in enumerate(coins):
            if c.isdigit():
                unparsed_quantity += c
            else:
                denom = coins[index:].lower()
                break
        quantity = int(unparsed_quantity)
        money_supplied = quantity * self.translate(denom, self.accepted_coins)
        return money_supplied

    def translate(self, val, table):
        for k, v in table.items():
            if k == val:
                return v
        return 0

    def report(self):
        money = self.money
        water = self.resources.get("water")
        milk = self.resources.get("milk")
        coffee = self.resources.get("coffee")
        return {
            "money": f"${money}",
            "water": f"{water}ml",
            "milk": f"{milk}ml",
            "coffee": f"{coffee}g",
        }

    def raw_report(self):
        return {"money": self.money, **self.resources}

    def handle_request(self, request):
        """ """
        request = request.lower()
        request_ingredients = self.menu.get(request).get("ingredients")
        ok, culprit = self.check_resources(request_ingredients)
        if not ok:
            return f"Sorry, there is not enough {culprit.capitalize()}"
        request_cost = self.menu.get(request).get("cost")
        coins = input("Please insert coins: ")
        money_supplied = self.handle_coins(coins)
        if money_supplied < request_cost:
            return "Sorry that’s not enough money. Money refunded"
        self.money += request_cost
        self.make_drink(request_ingredients)
        return f"{request.capitalize()} served. Thank you and have a nice day"

    def get_internals(self):
        with open("internals.json", "r") as internals:
            result = json.loads(internals.read())
        return result


if __name__ == "__main__":
    print("Coffee Machine")
    coffee_machine = CoffeeMachine()
    while True:
        request = input(f"What would you like? ({coffee_machine.offerings}):   ")
        request = request.lower().strip()
        if request == "off":
            print("Good bye")
            break
        if request == "report":
            pprint(coffee_machine.report())
        elif request in coffee_machine.offerings:
            coffee_machine.handle_request(request)
