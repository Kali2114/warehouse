import json
import pytest
from unittest.mock import patch
from warehouse import Warehouse


@pytest.fixture
def warehouse():
    return Warehouse()

def test_receive_product(warehouse):
    user_input = ['product1', '5', '10.0', 'n']

    with patch('builtins.input', side_effect=user_input):
        warehouse.receive_product()
    assert warehouse.inventory['product1']['quantity'] == 5


def test_issue_product(warehouse, monkeypatch):
    warehouse.inventory = {'product1': {'quantity': 10, 'price': 5.0}}
    warehouse.issue_product('product1', 5)
    assert warehouse.inventory.get('product1') is not None
    assert warehouse.inventory['product1']['quantity'] == 5

def test_display_product_list(capfd, warehouse):
    warehouse.inventory = {'product1': {'quantity': 10, 'price': 5.0}}
    expected_output = "Product list:\n==============================\nproduct1 - Quantity: 10, Price: $ 5.0\n==============================\n"

    warehouse.display_product_list()
    actual_output = capfd.readouterr().out
    assert actual_output == expected_output


def test_save_inventory_to_file(tmp_path, warehouse, monkeypatch):
    test_file_path = tmp_path / 'test_inventory.json'

    # Przechwytujemy input, dostarczając poprawne dane
    with monkeypatch.context() as m:
        m.setattr('builtins.input', lambda _: str(test_file_path))
        warehouse.save_inventory_to_file()

    with open(test_file_path, 'r') as file:
        saved_data = json.load(file)

    assert saved_data == warehouse.inventory


def test_load_inventory_from_file(tmp_path, warehouse, monkeypatch):
    test_data = {'product1': {'quantity': 5, 'price': 10.0}}
    test_file_path = tmp_path / 'test_inventory.json'
    with open(test_file_path, 'w') as file:
        json.dump(test_data, file)

    # Przechwytujemy input, dostarczając poprawne dane
    with monkeypatch.context() as m:
        m.setattr('builtins.input', lambda _: str(test_file_path))
        warehouse.load_inventory_from_file()

    assert warehouse.inventory == test_data