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

    # your code

    pass


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

    ui.clear_scr()
    index = common.index_of_id(table, id_)
    if index < 0:
        ui.print_error_message("Invalid ID: {}.".format(id_))
        return table

    itemname = table[index][TITLE]
    ui.print_result("Enter new data for {} ({}). Leave input empty to keep existing values.".format(itemname, id_))

    #  gametitle
    gametitle = ui.get_inputs(["Game title:"], "")[0]

    if len(gametitle) > 0:
        table[index][TITLE] = gametitle
    else:
        ui.print_result("Title not changed.")

    #  manufacturer
    manufacturer = ui.get_inputs(["Game manufacturer:"], "")[0]

    if len(manufacturer) > 0:
        table[index][MANUFACTURER] = manufacturer
    else:
        ui.print_result("Manufacturer not changed.")

    #  price

    price_str = ui.get_inputs(["Price:"], "")[0]

    if len(price_str) > 0:
        try:
            int(price_str)
            table[index][PRICE] = price_str
        except ValueError:
            ui.print_error_message("{} is not a valid integer. Price not changed.".format(price_str))
    else:
        ui.print_result("Price not changed.")

    
    # price

    in_stock_str = ui.get_inputs(["In stock:"], "")[0]

    if len(in_stock_str) > 0:
        try:
            int(in_stock_str)
            table[index][IN_STOCK] = in_stock_str
        except ValueError:
            ui.print_error_message("{} is not a valid integer. In stock not changed.".format(in_stock_str))
    else:
        ui.print_result("In stock not changed.")

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
