"""
Store module. Data structure:
1. ID of item
2. Name of item
3. Manufacturer of item
4. Price of item
5. Whether the item is in stock. (1 for yes, 0 for no)
"""

import os
import ui
import data_manager
import common

ID = 0
TITLE = 1
MANUFACTURER = 2
PRICE = 3
IN_STOCK = 4

INPUT_DESCRIPTIONS = [("Title: ", common.validate_string),
                      ("Manufacturer: ", common.validate_string),
                      ("Price: ", common.validate_int),
                      ("In Stock: ", common.validate_int)]


def menuaction_show(table):
    show_table(table)


def menuaction_add(table):
    add(table)
    ui.clear_scr()


def menuaction_update(table):
    to_update = ui.get_inputs(["Please enter the ID of the game you want updated: "], "")
    update(table, to_update[0])
    ui.clear_scr()


def menuaction_remove(table):
    to_remove = ui.get_inputs(["Please enter the ID of the game you want removed: "], "")
    remove(table, to_remove[0])
    ui.clear_scr()


def menuaction_count_by_manufacturer(table):
    ui.clear_scr()
    count_by_manufacturer_dict = get_counts_by_manufacturers(table)
    count_by_manufacturer_table = [(manufacturer, num)
                                   for manufacturer, num in count_by_manufacturer_dict.items()]
    ui.print_table(count_by_manufacturer_table, ["Manufacturer", "Count"])


def menuaction_average_by_manufacturer(table):
    ui.clear_scr()
    manufacturer = ui.get_inputs(["Please enter the manufacturer: "], "")[0]
    ui.print_result("The average game number of {0} is {1}".format(
        manufacturer, get_average_by_manufacturer(table, manufacturer)))


def start_module():
    """Starts the module and displays its menu."""

    ui.clear_scr()
    options = ["Show Table",
               "Add Entry",
               "Update Entry",
               "Remove Entry",
               "Show Game Count Per Manufacturer",
               "Show Average Game Count of a Manufacturer"]

    store_data = data_manager.get_table_from_file("store/games.csv")

    try:
        ui.clear_scr()
        while True:
            ui.print_menu("Store: Main menu", options, "Back to main menu")
            option = ui.get_inputs(["Please enter a number: "], "")[0]

            if option == "1":
                menuaction_show(store_data)
            elif option == "2":
                menuaction_add(store_data)
            elif option == "3":
                menuaction_update(store_data)
            elif option == "4":
                menuaction_remove(store_data)
            elif option == "5":
                menuaction_count_by_manufacturer(store_data)
            elif option == "6":
                menuaction_average_by_manufacturer(store_data)
            elif option == "0":
                for game in store_data:
                    game[PRICE] = str(game[PRICE])
                    game[IN_STOCK] = str(game[IN_STOCK])
                data_manager.write_table_to_file("store/games.csv", store_data)
                ui.clear_scr()
                break
            else:
                ui.clear_scr()
    except (KeyboardInterrupt, EOFError):
        common.handle_kb_interrupt("store/games.csv", store_data)


def show_table(table):
    """Display the table given as parameter."""
    ui.clear_scr()
    ui.print_table(table, ["ID", "Title", "Manufacturer", "Price", "In Stock"])


def add(table):
    """Asks user for input and adds it to the table. Returns table with the new record."""
    return common.add_line(table, INPUT_DESCRIPTIONS)


def remove(table, id_):
    """Remove a record with a given id from the table. Returns table without the specified record."""
    return common.remove_line(table, id_)


def update(table, id_):
    """Updates specified record in the table. Asks users for new data. Returns table with the updated record."""
    return common.update_line(table, id_, INPUT_DESCRIPTIONS)


def get_counts_by_manufacturers(table):
    """Returns dictionary containing the number of games (value) per manufacturer (key)."""
    manufacturers = {row[MANUFACTURER] for row in table}

    count_by_manufacturers = {}

    for manufacturer in manufacturers:
        num_games = len([row for row in table if row[MANUFACTURER] == manufacturer])
        count_by_manufacturers[manufacturer] = num_games

    return count_by_manufacturers


def get_average_by_manufacturer(table, manufacturer):
    """Returns average number of a manufacturer's items in stock."""

    if manufacturer == '':
        return None
    items_for_manufacturer = [item for item in table if item[MANUFACTURER] == manufacturer]

    if len(items_for_manufacturer) == 0:
        return 0

    summed = common.szum(items_for_manufacturer, IN_STOCK)
    return summed / len(items_for_manufacturer)
