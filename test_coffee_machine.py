#!/usr/bin/python3
import unittest
from coffee_machine import CoffeeMachine
from unittest.mock import patch


class TestCoffeeMachine(unittest.TestCase):
    def setUp(self):
        """ """
        self.coffee_machine = CoffeeMachine()

    @patch("builtins.input", return_value="500 nickels")
    def test_make_expresso(self, mock_input):
        self.coffee_machine.handle_request("espresso")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 82)
        self.assertEqual(data.get("milk"), 195)
        self.assertEqual(data.get("water"), 250)
        self.assertEqual(data.get("money"), 1.5)

    @patch("builtins.input", return_value="500 nickels")
    def test_make_latte(self, mock_input):
        self.coffee_machine.handle_request("latte")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 76)
        self.assertEqual(data.get("milk"), 50)
        self.assertEqual(data.get("water"), 100)
        self.assertEqual(data.get("money"), 2.5)

    @patch("builtins.input", return_value="500 nickels")
    def test_make_cappuccino(self, mock_input):
        self.coffee_machine.handle_request("cappuccino")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 76)
        self.assertEqual(data.get("milk"), 100)
        self.assertEqual(data.get("water"), 50)
        self.assertEqual(data.get("money"), 3)

    @patch("builtins.input", return_value="5 nickels")
    def test_make_expresso_with_insufficient_coins(self, mock_input):
        result = self.coffee_machine.handle_request("espresso")
        self.assertEqual(result, "Sorry that’s not enough money. Money refunded")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 100)
        self.assertEqual(data.get("milk"), 200)
        self.assertEqual(data.get("water"), 300)
        self.assertEqual(data.get("money"), 0)

    @patch("builtins.input", return_value="5 nickels")
    def test_make_latte_with_insufficient_coins(self, mock_input):
        result = self.coffee_machine.handle_request("latte")
        self.assertEqual(result, "Sorry that’s not enough money. Money refunded")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 100)
        self.assertEqual(data.get("milk"), 200)
        self.assertEqual(data.get("water"), 300)
        self.assertEqual(data.get("money"), 0)

    @patch("builtins.input", return_value="5 nickels")
    def test_make_cappuccino_with_insufficient_coins(self, mock_input):
        result = self.coffee_machine.handle_request("cappuccino")
        self.assertEqual(result, "Sorry that’s not enough money. Money refunded")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 100)
        self.assertEqual(data.get("milk"), 200)
        self.assertEqual(data.get("water"), 300)
        self.assertEqual(data.get("money"), 0)

    @patch("builtins.input", return_value="500 nickels")
    def test_insufficient_resources(self, mock_input):
        self.coffee_machine.handle_request("cappuccino")
        self.coffee_machine.handle_request("cappuccino")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 76)
        self.assertEqual(data.get("milk"), 100)
        self.assertEqual(data.get("water"), 50)
        self.assertEqual(data.get("money"), 3)
        self.coffee_machine.handle_request("espresso")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 58)
        self.assertEqual(data.get("milk"), 95)
        self.assertEqual(data.get("water"), 0)
        self.assertEqual(data.get("money"), 4.5)

    @patch("builtins.input", return_value="500 nickels")
    def test_multiple_requests(self, mock_input):
        self.coffee_machine.handle_request("latte")
        self.coffee_machine.handle_request("espresso")
        self.coffee_machine.handle_request("espresso")
        data = self.coffee_machine.raw_report()
        self.assertEqual(data.get("coffee"), 40)
        self.assertEqual(data.get("milk"), 40)
        self.assertEqual(data.get("water"), 0)
        self.assertEqual(data.get("money"), 5.5)

    @patch("builtins.input", return_value="500 nickels")
    def test_report(self, mock_input):
        report = self.coffee_machine.report()
        self.assertDictEqual(
            report, {"money": "$0", "milk": "200ml", "water": "300ml", "coffee": "100g"}
        )


if __name__ == "__main__":
    unittest.main()