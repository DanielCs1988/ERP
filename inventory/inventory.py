# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# manufacturer: string
# purchase_date: number (year)
# durability: number (year)


# importing everything you need
import os
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

import enum

from datetime import datetime

from statistics import mean
from copy import deepcopy


class InvCols(enum.IntEnum):
    ID = 0,
    NAME = 1,
    MANUFACTURER = 2,
    PURCHASE_DATE = 3,
    DURABILITY = 4


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file("inventory/inventory.csv")

    menuitem = -1
    while menuitem != "0":
        ui.print_menu("Inventory",
                      ["Add item", "Display item", "Update item", "Delete item", "Show table"],
                      "Back to main menu")

        menuitem = ui.getch()

        if(menuitem == "1"):
            add(table)
        elif(menuitem == "4"):
            id_to_remove = ui.get_inputs(["Enter ID to remove:"], "")[0]
            remove(table, id_to_remove)
        elif(menuitem == "5"):
            show_table(table)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    ui.print_table(table, ["ID", "Name", "Manufacturer", "Purchase date", "Durability"])


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """

    new_item = [common.generate_random(table)]
    new_item.extend(ui.get_inputs(["Name:", "Manufacturer:"], "Please enter item details"))

    while True:
        value = ui.get_inputs(["Purchase date:"], "")[0]
        if not common.validate_byear(value):
            continue  # validation comes here
        new_item.append(value)
        break

    while True:
        value = ui.get_inputs(["Durability:"], "")[0]
        try:
            new_durability = int(value)  # validation comes here
        except ValueError:
            continue
        new_item.append(new_durability)
        break

    table.append(new_item)

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

    idx = common.index_of_id(table, id_)

    if idx >= 0:
        del table[idx]

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

# the question: Which items have not exceeded their durability yet?
# return type: list of lists (the inner list contains the whole row with their actual data types)
#
# @table: list of lists
def get_available_items(table):

    now = datetime.now()
    current_year = now.year

    return [row for row in table if current_year - int(row[InvCols.PURCHASE_DATE]) < int(row[InvCols.DURABILITY])]


# the question: What are the average durability times for each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [avg] }
#
# @table: list of lists
def get_average_durability_by_manufacturers(table):

    manufacturers = {row[InvCols.MANUFACTURER] for row in table}

    durability_by_manufacturers = {}

    for manufacturer in manufacturers:
        durabilities = [int(row[InvCols.DURABILITY]) for row in table if row[InvCols.MANUFACTURER] == manufacturer]
        durability_by_manufacturers[manufacturer] = mean(durabilities)

    return durability_by_manufacturers
