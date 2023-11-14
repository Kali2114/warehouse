# Warehouse Project

The Warehouse Project is a simple command-line application for managing inventory in a warehouse. This application provides various features to receive, issue, and manage products within the warehouse. It is designed for users who need an efficient way to keep track of inventory in a warehouse setting.

## Table of Contents

- [Features](#features)
- [Technical Details](#technical-details)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Login System**: Users can log in with a username and password. Only authorized users have access to the inventory management system.

- **Receive Products**: Authorized users can receive products into the warehouse. They can specify the product name, quantity, and price.

- **Issue Products**: Authorized users can issue products from the warehouse. They can specify the product name and quantity. The application checks if there is sufficient stock.

- **Inventory Management**: The application keeps track of the inventory, including product quantities and prices.

- **Save and Load Inventory**: Users can save the current inventory to a file and load it when needed. This ensures data persistence.

-  **Database Integration**: The application utilizes an SQLite database for persistent storage of inventory data. It includes methods to initialize the database, save the inventory to the database, and load the inventory from the database.

- **Simple Command-Line Interface**: The application provides a user-friendly command-line interface for easy interaction.


## Technical Details

- **Programming Language**: Python
- **External Libraries**: None
- **Data Storage**: Inventory is stored in memory and can be saved to and loaded from JSON files.
- **Database**: In each shutdown, the program saves the inventory state in an SQLite3 database, and during startup, it loads it (initializing it if the database doesn't exist).

## Installation

1. Clone the repository to your local machine.<br>
   Git clone: https://github.com/Kali2114/warehouse-project.git
2. Navigate to the project directory.<br>
   `cd warehouse-project`
3. Install required dependencies:<br>
   `pip install -r requirements.txt`

## Usage

To run the application, open a command prompt or terminal and navigate to the project directory. Then, execute the following command:

```bash
python main.py login --username=admin --password=553355
```
## Contributing

Contributions to this project are welcome. Feel free to open issues and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.