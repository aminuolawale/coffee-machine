#!/usr/bin/python3
import os
import sys
import math
import json
from pprint import pprint
from utils import SuggestionsMixin


class CoffeeMachine(SuggestionsMixin):
    """ """

    def __init__(self, persist=False):
        self.persist = persist
        internals = self._get_internals(persist)
        self.menu = internals.get("menu")
        self.resources = internals.get("resources")
        self.money = internals.get("money")
        self.offerings = list(self.menu.keys())
        self.accepted_coins = internals.get("accepted_coins")

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
        money_supplied = quantity * self._translate(denom, self.accepted_coins)
        return money_supplied

    def make_drink(self, ingredients):
        for k in self.resources:
            old_val = self.resources.get(k)
            self.resources.update({k: old_val - ingredients.get(k)})

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

    def run(self):
        print("========== Coffee Machine ==========\n")
        while True:
            request = input(f"What would you like? (options:{self.offerings}):   ")
            request = request.lower().strip()
            if request == "off":
                self.shut_down()
                break
            elif request == "report":
                pprint(self.report())
            elif request == "reset":
                pprint(self.reset())
            elif request in self.offerings:
                result = self.handle_request(request)
                print(result)
            else:
                print(f"Unrecognized request, do you mean {self._parse(request)}?\n")

    def reset(self):
        """ """
        if self.persist:
            internals = self._get_internals()
            self.resources = internals.get("resources")
            self.money = internals.get("money")
        return "Memory reset"

    def shut_down(self):
        """ """
        if self.persist:
            memory = {"money": self.money, "resources": self.resources}
            with open("internals/memory.json", "w") as mem:
                mem.write(json.dumps(memory))
        print("Good bye")

    def _translate(self, val, table):
        for k, v in table.items():
            if k == val:
                return v
        return 0

    def _get_internals(self, persist=False):
        with open("internals/internals.json", "r") as internals, open(
            "internals/memory.json"
        ) as memory:
            result = json.loads(internals.read())
            if persist:
                memory = json.loads(memory.read())
                result.update(
                    money=memory.get("money"), resources=memory.get("resources")
                )
        return result


if __name__ == "__main__":
    persist = False
    if len(sys.argv) == 2 and sys.argv[1] == "--persist":
        persist = True
    coffee_machine = CoffeeMachine(persist)
    coffee_machine.run()
