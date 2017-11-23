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
                show_table(store_data)
            elif option == "2":
                store_data = add(store_data)
                ui.clear_scr()
            elif option == "3":
                to_update = ui.get_inputs(["Please enter the ID of the game you want updated: "], "")
                store_data = update(store_data, to_update[0])
                ui.clear_scr()
            elif option == "4":
                to_remove = ui.get_inputs(["Please enter the ID of the game you want removed: "], "")
                store_data = remove(store_data, to_remove[0])
                ui.clear_scr()
            elif option == "5":
                ui.clear_scr()
                count_by_manufacturer_dict = get_counts_by_manufacturers(store_data)
                count_by_manufacturer_table = [(manufacturer, num)
                                               for manufacturer, num in count_by_manufacturer_dict.items()]
                ui.print_table(count_by_manufacturer_table, ["Manufacturer", "Count"])
            elif option == "6":
                ui.clear_scr()
                manufacturer = ui.get_inputs(["Please enter the manufacturer: "], "")[0]
                ui.print_result("The average game number of {0} is {1}".format(
                    manufacturer, get_average_by_manufacturer(store_data, manufacturer)))
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
        ui.clear_scr()
        data_manager.write_table_to_file("store/games.csv", store_data)
        ui.print_error_message("Keyboard interrupt. If you want to got back to main menu, use the menu.")
        exit()


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    ui.clear_scr()
    ui.print_table(table, ["ID", "Title", "Manufacturer", "Price", "In Stock"])


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """

    new_item = [common.generate_random(table)]

    user_input = ui.mass_valid_in([("Title: ", common.validate_string),
                                   ("Manufacturer: ", common.validate_string),
                                   ("Price: ", common.validate_int),
                                   ("In Stock: ", common.validate_int)])
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

    update_input = ui.mass_valid_in([("Title: ", common.validate_string),
                                     ("Manufacturer: ", common.validate_string),
                                     ("Price: ", common.validate_int),
                                     ("In Stock: ", common.validate_int)], True)

    table[index] = common.apply_update_to_line(table[index], update_input)

    return table


# special functions:
# ------------------

def get_counts_by_manufacturers(table):
    """
    Get number of games per manufacturer.

    Args:
        table: The input data table.

    Returns:
        A dictionary of manufacturer name / item count table.
    """
    manufacturers = {row[MANUFACTURER] for row in table}

    count_by_manufacturers = {}

    for manufacturer in manufacturers:
        num_games = len([row for row in table if row[MANUFACTURER] == manufacturer])
        count_by_manufacturers[manufacturer] = num_games

    return count_by_manufacturers


def get_average_by_manufacturer(table, manufacturer):
    """Returns average number of a manufacturer's items in stock.

        Args:
            table: The input data table.
            manufacturer: The manufacturer name.
    """

    if manufacturer == '':
        return None
    items_for_manufacturer = [item for item in table if item[MANUFACTURER] == manufacturer]

    if len(items_for_manufacturer) == 0:
        return 0

    summed = common.szum(items_for_manufacturer, IN_STOCK)
    return summed / len(items_for_manufacturer)
