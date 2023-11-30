import json
import unittest
from io import StringIO
from unittest.mock import patch
from warehouse import Warehouse

class TestWarehouse(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse()

    def test_receive_product(self):
        with patch('builtins.input', side_effect=['product1', '5', '10.0', 'n']):
            self.warehouse.receive_product()
        self.assertEqual(self.warehouse.inventory['product1']['quantity'], 5)

    def test_issue_product(self):
        self.warehouse.inventory = {'product1': {'quantity': 10, 'price': 5.0}}
        with patch('builtins.input', side_effect=['product1', '5', 'n']):
            self.warehouse.issue_product()
        self.assertEqual(self.warehouse.inventory['product1']['quantity'], 5)

    def test_display_product_list(self):
        self.warehouse.inventory = {'product1': {'quantity': 10, 'price': 5.0}}
        expected_output = "Product list:\n==============================\nproduct1 - Quantity:  10, Price: $5.0\n==============================\n"
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.warehouse.display_product_list()
            actual_output = mock_stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

    def test_save_inventory_to_file(self):
        with patch('builtins.input', return_value='test_inventory.json'):
            self.warehouse.save_inventory_to_file()

        with open('test_inventory.json', 'r') as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data, self.warehouse.inventory)


    def test_load_inventory_from_file(self):
        test_data = {'product1': {'quantity': 5, 'price': 10.0}}
        with open('test_inventory.json', 'w') as file:
            json.dump(test_data, file)

        with patch('builtins.input', return_value='test_inventory.json'):
            self.warehouse.load_inventory_from_file()

        self.assertEqual(self.warehouse.inventory, test_data)

if __name__ == '__main__':
    unittest.main(verbosity=2)

