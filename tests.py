import unittest
from CoffeeMachine import CoffeeMachinePlus, NoCoinException, NoElementsException, NoSugarException

class CoffeeMachinePlusTest(unittest.TestCase):
    def test_make_product_no_coin(self):
        machine = CoffeeMachinePlus()
        with self.assertRaises(NoCoinException):
            machine.get_product('coffee_alone')

    def test_make_simple_product_no_resources(self):
        machine = CoffeeMachinePlus()
        machine.insert_coin()
        with self.assertRaises(NoElementsException):
            machine.get_product('coffee_alone')

    def test_make_complex_product_no_resources(self):
        machine = CoffeeMachinePlus()
        machine.insert_coin()
        with self.assertRaises(NoElementsException):
            machine.get_product('coffee_with_milk')

    def test_make_simple_product_ok(self):
        machine = CoffeeMachinePlus()
        machine.insert_coin()
        machine.add_resource('coffee', 100)
        machine.get_product('coffee_alone')
        self.assertEqual(machine.resources['coffee'], 70)
        self.assertEqual(machine.coins, 0)

    def test_make_complex_product_ok(self):
        machine = CoffeeMachinePlus()
        machine.insert_coin()
        machine.add_resource('coffee', 100)
        machine.add_resource('milk', 100)
        machine.get_product('coffee_with_milk')
        self.assertEqual(machine.resources['coffee'], 70)
        self.assertEqual(machine.resources['milk'], 80)
        self.assertEqual(machine.coins, 0)

    def test_no_sugar(self):
        machine = CoffeeMachinePlus()
        self.assertEqual(machine.sugar_level_seleted, 0)

    def test_sugar_level_top(self):
        machine = CoffeeMachinePlus()
        machine.suger_level(5)
        self.assertEqual(machine.sugar_level_seleted, 5)

    def test_make_simple_product_no_sugar(self):
        machine = CoffeeMachinePlus()
        machine.insert_coin()
        machine.suger_level(5)
        machine.add_resource('coffee', 100)
        with self.assertRaises(NoSugarException):
            machine.get_product('coffee_alone')
        self.assertEqual(machine.coins, 1)

    def test_make_simple_product_with_sugar(self):
        machine = CoffeeMachinePlus()
        machine.insert_coin()
        machine.suger_level(5)
        machine.add_resource('coffee', 100)
        machine.add_sugar(100)
        machine.get_product('coffee_alone')
        self.assertEqual(machine.sugar, 85)
        self.assertEqual(machine.coins, 0)


class CoffeeMachine:
    def __init__(self):
        self.coins = 0
        self.coffee = 0
        self.sugar = 0

    def insert_coin(self):
        self.coins += 1

    def insert_coffee(self, coffee):
        self.coffee += coffee

    def insert_sugar(self, sugar):
        self.sugar += sugar

    def get_coffee(self):
        if self.coins == 0:
            raise NoCoinException('No hay monedas')
        if self.count_coffee_left() == 0:
            raise NoElementsException('No hay elementos')
        # DESCONTAR
        self.coffee -= 30
        self.sugar -= 5
        self.coins -= 1
        return True

    def count_coffee_left(self):
        count_coffee_because_coffee = self.coffee // 30
        count_coffee_because_sugar = self.sugar // 5
        return min(count_coffee_because_coffee, count_coffee_because_sugar)


class CoffeMachineTest(unittest.TestCase):
    def test_initial(self):
        machine = CoffeeMachine()
        self.assertEqual(machine.coins, 0)

    def test_insert_coin(self):
        machine = CoffeeMachine()
        machine.insert_coin()
        self.assertEqual(machine.coins, 1)

    def test_insert_coffee(self):
        machine = CoffeeMachine()
        machine.insert_coffee(1000)
        self.assertEqual(machine.coffee, 1000)

    def test_insert_coffee_second_time(self):
        machine = CoffeeMachine()
        machine.insert_coffee(1000)
        machine.insert_coffee(1000)
        self.assertEqual(machine.coffee, 2000)

    def test_insert_sugar(self):
        machine = CoffeeMachine()
        machine.insert_sugar(1000)
        self.assertEqual(machine.sugar, 1000)

    def test_insert_coffee_second_time(self):
        machine = CoffeeMachine()
        machine.insert_sugar(1000)
        machine.insert_sugar(1000)
        self.assertEqual(machine.sugar, 2000)

    def test_get_coffee_ok(self):
        machine = CoffeeMachine()
        machine.insert_coin()
        machine.insert_coin()
        machine.insert_coffee(1000)
        machine.insert_sugar(1000)
        coffee_result = machine.get_coffee()
        self.assertTrue(coffee_result)
        self.assertEqual(machine.coffee, 1000-30)
        self.assertEqual(machine.sugar, 1000-5)
        self.assertEqual(machine.coins, 1)

    def test_get_coffee_error_no_coffee(self):
        machine = CoffeeMachine()
        machine.insert_coin()
        machine.insert_coin()
        machine.insert_sugar(1000)
        with self.assertRaises(NoElementsException):
            coffee_result = machine.get_coffee()
        self.assertEqual(machine.coffee, 0)
        self.assertEqual(machine.sugar, 1000)
        self.assertEqual(machine.coins, 2)

    def test_get_coffee_error_no_sugar(self):
        machine = CoffeeMachine()
        machine.insert_coin()
        machine.insert_coin()
        machine.insert_coffee(1000)
        with self.assertRaises(NoElementsException):
            coffee_result = machine.get_coffee()
        self.assertEqual(machine.sugar, 0)
        self.assertEqual(machine.coffee, 1000)
        self.assertEqual(machine.coins, 2)

    def test_get_coffee_error_no_coin(self):
        machine = CoffeeMachine()
        machine.insert_coffee(1000)
        machine.insert_sugar(1000)
        # try:
        #     machine.get_coffee()
        # except Exception as e:
        #     pass

        # deberia lanzar una exception
        with self.assertRaises(NoCoinException):
            machine.get_coffee()

        self.assertEqual(machine.sugar, 1000)
        self.assertEqual(machine.coffee, 1000)
        self.assertEqual(machine.coins, 0)

    def test_count_coffee_no_left(self):
        machine = CoffeeMachine()
        coffee_left = machine.count_coffee_left()
        self.assertEqual(
            coffee_left,
            0,
        )

    def test_count_coffee_no_left_because_sugar(self):
        machine = CoffeeMachine()
        machine.insert_coffee(30)
        coffee_left = machine.count_coffee_left()
        self.assertEqual(
            coffee_left,
            0,
        )

    def test_count_coffee_no_left_because_coffee(self):
        machine = CoffeeMachine()
        machine.insert_sugar(30)
        coffee_left = machine.count_coffee_left()
        self.assertEqual(
            coffee_left,
            0,
        )

    def test_count_coffee_left_1(self):
        machine = CoffeeMachine()
        machine.insert_coffee(50)
        machine.insert_sugar(5)
        coffee_left = machine.count_coffee_left()
        self.assertEqual(
            coffee_left,
            1,
        )

    def test_count_coffee_left_2(self):
        machine = CoffeeMachine()
        machine.insert_coffee(70)
        machine.insert_sugar(12)
        coffee_left = machine.count_coffee_left()
        self.assertEqual(
            coffee_left,
            2,
        )


if __name__ == '__main__':
    unittest.main()
