# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# manufacturer: string
# price: number (dollars)
# in_stock: number

# importing everything you need
import os
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

ID = 0
TITLE = 1
MANUFACTURER = 2
PRICE = 3
IN_STOCK = 4


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """
    options = ["Show Table",
               "Add Game",
               "Remove Game",
               "Update Game",
               "Show Game Count Per Manufacturer",
               "Show Average Game Count of a Manufacturer"]

    store_data = data_manager.get_table_from_file("games.csv")
    for game in store_data:
        game[PRICE] = int(game[PRICE])
        game[IN_STOCK] = int(game[IN_STOCK])

    while True:
        ui.print_menu("Store: Main menu", options, "Exit program")
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]

        if option == "1":
            show_table(store_data)
        elif option == "2":
            store_data = add(store_data)
        elif option == "3":
            to_remove = ui.get_inputs(["Please enter the ID of the game you want removed: "], "")
            store_data = remove(store_data, to_remove[0])
        elif option == "4":
            to_update = ui.get_inputs(["Please enter the ID of the game you want updated: "], "")
            store_data = update(store_data, to_update[0])
        elif option == "5":
            ui.print_result(get_counts_by_manufacturers(store_data))
        elif option == "6":
            ui.print_result(get_average_by_manufacturer(store_data))
        elif option == "0":
            data_manager.write_table_to_file("games.csv", store_data)
            break
        else:
            ui.print_error_message(err)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    # your code

    pass


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """

    # your code

    return table


def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table: table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        Table without specified record.
    """

    # your code

    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        table with updated record
    """

    # your code

    return table


# special functions:
# ------------------

# the question: How many different kinds of game are available of each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [count] }
def get_counts_by_manufacturers(table):

    manufacturers = {row[MANUFACTURER] for row in table}

    count_by_manufacturers = {}

    for manufacturer in manufacturers:
        num_games = len([row for row in table if row[MANUFACTURER] == manufacturer])
        count_by_manufacturers[manufacturer] = num_games

    return count_by_manufacturers


# the question: What is the average amount of games in stock of a given manufacturer?
# return type: number
def get_average_by_manufacturer(table, manufacturer):
    """Returns average value of a manufacturer's items in stock."""

    summed = common.get_sum([item for item in table if item[MANUFACTURER] == manufacturer], IN_STOCK)
    return summed / len(summed)
