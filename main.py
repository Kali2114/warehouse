from warehouse import Warehouse

import click
@click.group()
def cli():
    pass

@cli.command()
@click.option('--username', prompt='Enter username')
@click.option('--password', prompt='Enter password', hide_input=True, confirmation_prompt=True)
def login(username, password):
    warehouse = Warehouse()
    warehouse.login(username, password)

if __name__ == '__main__':
    cli()