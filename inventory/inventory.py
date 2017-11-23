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


ID = 0
NAME = 1
MANUFACTURER = 2
PURCHASE_DATE = 3
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
        ui.clear_scr()
        while menuitem != "0":
            ui.print_menu("Inventory",
                          ["Show table", "Add entry", "Update entry", "Delete entry", "Available items",
                           "Durability/manufacturer"], "Back to main menu")

            menuitem = ui.get_inputs(["Please choose an option:"], "")[0]
            
            if(menuitem == "1"):
                ui.clear_scr()
                show_table(table)
            elif(menuitem == "2"):
                add(table)
                ui.clear_scr()
            elif(menuitem == "3"):
                id_to_update = ui.get_inputs(["Enter ID of item to update:"], "")[0]
                if id_to_update:
                    update(table, id_to_update)
                ui.clear_scr()
            elif(menuitem == "4"):
                id_to_remove = ui.get_inputs(["Enter ID to remove:"], "")[0]
                if id_to_remove:
                    remove(table, id_to_remove)
                ui.clear_scr()
            elif menuitem == "5":
                ui.clear_scr()
                availables = get_available_items(table)
                if len(availables) == 0:
                    ui.print_result("No available items found.")
                else:
                    ui.print_result("Available items")
                    show_table(availables)
            elif menuitem == "6":
                ui.clear_scr()
                avg_durabilities = get_average_durability_by_manufacturers(table)
                avg_durabilities = [(manufacturer, avg_dur) for manufacturer, avg_dur in avg_durabilities.items()]
                ui.print_result("Average durability per manufacturer")
                ui.print_table(avg_durabilities, ["Manufacturer", "Durability"])
            else:
                ui.clear_scr()
    except (KeyboardInterrupt, EOFError):  # Ctrl-C, Ctrl-D
        ui.clear_scr()
        data_manager.write_table_to_file("store/games.csv", table)
        ui.print_error_message("Keyboard interrupt. If you want to got back to main menu, use the menu.")
        exit()
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

    user_input = ui.mass_valid_in([("Name:", common.validate_string),
                                   ("Manufacturer:", common.validate_string),
                                   ("Purchase year: ", common.validate_byear),
                                   ("Durability: ", common.validate_int)])

    if user_input is None:
        return table

    new_item.extend(user_input)

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

    return common.remove_line(table, id_)


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        table with updated record
    """
    index = common.index_of_id(table, id_)
    if index < 0:
        ui.print_error_message("Invalid ID: {}.".format(id_))
        return table

    user_input = ui.mass_valid_in([("Name:", common.validate_string),
                                   ("Manufacturer:", common.validate_string),
                                   ("Purchase year: ", common.validate_byear),
                                   ("Durability: ", common.validate_int)], True)

    common.apply_update_to_line(table[index], user_input)

    return table


# special functions:
# ------------------

# the question: Which items have not exceeded their durability yet?
# return type: list of lists (the inner list contains the whole row with their actual data types)
#
# @table: list of lists
def get_available_items(table):

    current_year = common.CURRENT_YEAR

    return [row for row in table if current_year - int(row[PURCHASE_DATE]) < int(row[DURABILITY])]


# the question: What are the average durability times for each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [avg] }
#
# @table: list of lists
def get_average_durability_by_manufacturers(table):

    manufacturers = {row[MANUFACTURER] for row in table}

    durability_by_manufacturers = {}

    for manufacturer in manufacturers:
        durabilities = [int(row[DURABILITY]) for row in table if row[MANUFACTURER] == manufacturer]
        durability_by_manufacturers[manufacturer] = common.szum_list(durabilities) / len(durabilities)

    return durability_by_manufacturers
