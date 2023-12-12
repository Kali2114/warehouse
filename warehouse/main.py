from warehouse import Warehouse
import click
warehouse = Warehouse()
@click.group()
def cli():
    pass

@cli.command()
@click.option('--username', prompt='Enter username')
@click.option('--password', prompt='Enter password', hide_input=True, confirmation_prompt=True)
def login(username, password):
    warehouse.login(username, password)

@cli.command()
@click.option('--product_name', prompt='Enter product name')
@click.option('--quantity', prompt='Enter quantity', type=int)
@click.option('--price', prompt='Enter price', type=float)
def receive_product(product_name, quantity, price):
    warehouse.load_inventory_from_database()
    warehouse.receive_product(product_name, quantity, price)
    warehouse.save_inventory_to_database()

@cli.command()
@click.option('--product_name', prompt='Enter product name')
@click.option('--quantity', prompt='Enter quantity', type=int)
def issue_product(product_name, quantity):
    warehouse.load_inventory_from_database()
    warehouse.issue_product(product_name, quantity)
    warehouse.save_inventory_to_database()

@cli.command()
def display_product_list():
    warehouse.load_inventory_from_database()
    warehouse.display_product_list()


if __name__ == '__main__':
    cli()