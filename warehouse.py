import json
import sqlite3

class Warehouse:
    """
     Warehouse class represents a simple inventory management system.

    This class allows users to log in as administrators, receive and issue products,
    check the inventory, save the inventory to a database, and load the inventory from a database or file.


    Attributes:
        inventory (dict): A dictionary representing the inventory of the warehouse.
                         Keys are product names, and values are dictionaries with keys
                         'quantity' and 'price' representing the quantity and price of the product.
        logged_in_user (str): Stores the username of the currently logged-in user.

    """
    def __init__(self):
        self.inventory = {}
        self.logged_in_user = None

    def login(self, username, password):
        """Log in to the warehouse management system.

        This method allows the user to log in with a username and password.
        It checks if the provided credentials match 'admin' and '553355' for successful login.
        """
        if username == 'admin' and password == '553355':
            self.logged_in_user = username
            self.load_inventory_from_db()
            self.warehouse_menu()
            if self.logged_in_user:
                print('Login successful.')
            return
        else:
            print('Login failed.')

    def logout(self):
        self.logged_in_user = None

    def initialize_database(self):
        """
        Initialize the SQLite database for the inventory.

        This method creates an SQLite database file named 'warehouse.db' if it does not exist,
        and creates a table named 'inventory' to store product information.
        """
        with sqlite3.connect('warehouse.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
            product_name TEXT PRIMARY KEY,
            quantity INTEGER,
            price REAL
            )''')

    def save_inventory_to_db(self):
        """
       Save the current inventory to the SQLite database.

       This method connects to the 'warehouse.db' SQLite database and saves the product inventory.
       """
        with sqlite3.connect('warehouse.db') as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM inventory')
            for product_name, product_info in self.inventory.items():
                cursor.execute('''INSERT INTO inventory (product_name, quantity, price) VALUES (?, ?, ?)''',
                                (product_name, product_info['quantity'], product_info['price']))

    def load_inventory_from_db(self):
        """
        Load the product inventory from the SQLite database.

        This method connects to the 'warehouse.db' SQLite database, checks if the 'inventory' table exists,
        and updates the internal inventory attribute with the data retrieved from the table.

        If the 'inventory' table does not exist, it initializes the database by creating the 'inventory' table.
        """
        with sqlite3.connect('warehouse.db') as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")
            table_exists = cursor.fetchone()
            if not table_exists:
                self.initialize_database()
                return

            cursor.execute('SELECT * FROM inventory')
            rows = cursor.fetchall()
            self.inventory = {}
            for row in rows:
                product_name, quantity, price = row
                self.inventory[product_name] = {'quantity': quantity, 'price': price}

    def receive_product(self):
        """Receive a product into the warehouse.

        This method allows the user to add products to the inventory.
        It prompts for the product name, quantity, and price, and performs validation checks.
        """
        while True:
            product_name = input('Enter product name or press "x" to exit: ')
            if product_name.lower() == 'x':
                return
            try:
                quantity = int(input('Enter quantity: '))
                price = float(input('Enter price: '))
                if quantity <= 0 or price <= 0:
                    print('Error. Quantity and price should be a positive value.')
                    continue
            except ValueError:
                print('Wrong format. Quantity should be an integer and price should be a float.')
                continue

            if product_name in self.inventory:
                self.inventory[product_name]['quantity'] += quantity
            else:
                self.inventory[product_name] = {'quantity': quantity, 'price': price}

            print(f'{quantity} x {product_name} added.')

            while True:
                choice = input('Add another product? y/n: ').lower()
                if choice == 'y':
                    break
                elif choice == 'n':
                    return
                else:
                    print('Wrong choice.')

    def issue_product(self):
        """Issue a product from the warehouse.

        This method allows the user to remove products from the inventory.
        It prompts for the product name and quantity, performs validation checks, and updates the inventory.
        """
        while True:
            if not self.inventory:
                print('Warehouse empty.')
                return
            self.display_product_list()
            product_name = input('Enter product name or press "x" to exit: ')
            if product_name.lower() == 'x':
                return
            elif product_name not in self.inventory:
                print('Product not found in inventory.')
                continue
            try:
                quantity = int(input('Enter quantity: '))
                if quantity <= 0:
                    print('Error. Quantity should be a positive value.')
            except ValueError:
                print('Wrong format. Quantity should be an integer.')
                continue

            if self.inventory[product_name]['quantity'] >= quantity:
                if self.inventory[product_name]['quantity'] > quantity:
                    self.inventory[product_name]['quantity'] -= quantity
                else:
                    del self.inventory[product_name]
                print(f'{quantity} x {product_name} issued.')
            else:
                print('Insufficient stock.')

            while True:
                choice = input('Remove another product? y/n: ').lower()
                if choice == 'y':
                    break
                elif choice == 'n':
                    return
                else:
                    print('Wrong choice.')

    def save_inventory_to_file(self):
        """Save the inventory to a JSON file.

        This method allows the user to save the current inventory to a JSON file.
        It prompts for the filename and performs the saving operation.
        """
        filename = input('Enter filename or press "x" to exit: ')
        if filename.lower() == 'x':
            return
        try:
            with open(filename, 'w') as file:
                json.dump(self.inventory, file)
        except Exception as e:
            print(f'Error: {e}')
        else:
            print(f'Inventory saved to {filename}')

    def load_inventory_from_file(self):
        """Load the inventory from a JSON file.

        This method allows the user to load the inventory from a JSON file.
        It prompts for the filename and performs the loading operation.
        """
        filename = input('Enter filename or press "x" to exit: ')
        if filename.lower() == 'x':
            return
        try:
            with open(filename, 'r') as file:
                loaded_inventory = json.load(file)
                self.inventory = loaded_inventory
        except FileNotFoundError:
            print(f'File {filename} not found.')
        except Exception as e:
            print(f'Error: {e}')
        else:
            print(f'Inventory loaded from {filename}')

    def display_product_list(self):
        """Display the list of products in the inventory.

        This method displays the product list, including product names, quantities, and prices.
        """
        if self.inventory:
            print('Product list:')
            print(30 * '=')
            for product_name, product_info in self.inventory.items():
                print(f'{product_name:7} - Quantity: {product_info["quantity"]:3}, Price: ${product_info["price"]:3}')
            print(30 * '=')
        else:
            print('The warehouse is empty.')

    def warehouse_menu(self):
        """Manage the warehouse operations.

        This method provides a menu for various warehouse operations, including receiving, issuing,
        checking inventory, saving to file, loading from file, and logging out.
        """
        while self.logged_in_user:
            print('Warehouse Menu:')
            print('1. Receive Product\n2. Issue Product\n3. Check Inventory\n4. Save Inventory\n5. Load Inventory\n6. Logout')
            choice = input('Enter your choice: ')
            if choice == '1':
                self.receive_product()
            elif choice == '2':
                self.issue_product()
            elif choice == '3':
                self.display_product_list()
            elif choice == '4':
                self.save_inventory_to_file()
            elif choice == '5':
                self.load_inventory_from_file()
            elif choice == '6':
                self.logout()
                print('Logged out.')
                self.save_inventory_to_db()
                return
            else:
                print('Wrong choice.')