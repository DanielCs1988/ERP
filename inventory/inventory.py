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
    __order__ = "ID NAME MANUFACTURER PURCHASE_DATE DURABILITY"
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
    inv_file = "inventory/inventory.csv"
    table = data_manager.get_table_from_file(inv_file)

    menuitem = -1
    try:
        while menuitem != "0":
            ui.print_menu("Inventory",
                          ["Add item", "Update item", "Remove item", "Show table", "Available item",
                           "Durability/manufacturer"], "Back to main menu")

            menuitem = ui.getch()
            ui.clear_scr()
            if(menuitem == "1"):
                add(table)
            elif(menuitem == "2"):
                id_to_remove = ui.get_inputs(["Enter ID of item to update:"], "")[0]
                update(table, id_to_remove)
            elif(menuitem == "3"):
                id_to_remove = ui.get_inputs(["Enter ID to remove:"], "")[0]
                remove(table, id_to_remove)
            elif(menuitem == "4"):
                show_table(table)
            elif menuitem == "5":
                availables = get_available_items(table)
                if len(availables) == 0:
                    ui.print_result("No available items found.")
                else:
                    show_table(availables)
            elif menuitem == "6":
                avg_durabilities = get_average_durability_by_manufacturers(table)
                avg_durabilities = [(manufacturer, avg_dur) for manufacturer, avg_dur in avg_durabilities.items()]
                ui.print_table(avg_durabilities, ["Manufacturer", "Durability"])
    except (KeyboardInterrupt, EOFError):  # Ctrl-C, Ctrl-D
        pass
    finally:
        data_manager.write_table_to_file(inv_file, table)


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
    new_item.extend(ui.get_inputs(["Name:"], "Please enter item details. Type ESC to cancel."))

    if "ESC" in new_item:
        return table

    new_item.extend(ui.get_inputs(["Manufacturer:"], ""))

    if "ESC" in new_item:
        return table

    while True:
        value = ui.get_inputs(["Purchase date:"], "")[0]
        if not common.validate_byear(value):
            continue  # validation comes here
        new_item.append(value)
        break

    if "ESC" in new_item:
        return table

    while True:
        value = ui.get_inputs(["Durability:"], "")[0]
        try:
            new_durability = int(value)  # validation comes here
        except ValueError:
            continue
        new_item.append(value)
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
    ui.clear_scr()
    index = common.index_of_id(table, id_)
    if index < 0:
        ui.print_error_message("Invalid ID: {}.".format(id_))
        return table

    itemname = table[index][1]
    ui.print_result("Enter new data for {} ({}). Leave input empty to keep existing values.".format(itemname, id_))

    for col in InvCols:
        colname = col.name
        colindex = col.value

        if colindex == 0:
            continue

        current_input = ui.get_inputs([colname+":"], "")[0]

        if len(current_input) == 0:
            ui.print_result("{} not changed.".format(colname))
        elif col == InvCols.PURCHASE_DATE:
            year_valid = common.validate_byear(current_input)
            if not year_valid:
                ui.print_error_message("Invalid value '{}' for {}".format(current_input, colname))
                continue
            table[index][colindex] = current_input

        elif col == InvCols.DURABILITY:
            try:
                int(current_input)
            except ValueError:
                ui.print_error_message("Invalid value '{}' for {}".format(current_input, colname))
                continue
            table[index][colindex] = current_input

        else:
            table[index][colindex] = current_input

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
