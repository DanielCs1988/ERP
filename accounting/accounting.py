# data structure:
# id: string
#     Unique and randomly generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# month: number
# day: number
# year: number
# type: string (in = income, out = outcome)
# amount: number (dollar)
import sys
sys.path.append("/home/leblayd/python/TW3/pbwp-3rd-tw-lightweight-erp-enterprise_coffee_planner")

# importing everything you need
import os
# User interface module
import ui
# data manager module
import data_manager
# common module
import common


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file("accounting/items.csv")
    paid_version = True    # an easter-egg, leave it True and it should (hopefully) cause no problems
    if paid_version:    # uses the options based on the easter-egg
        options = ["Add entry",
                   "Remove entry",
                   "Update",
                   "Display table",
                   "Which year has the highest profit?",
                   "What is the average (per item) profit in a given year?"]
    else:
        options = ["Add entry",
                   "Remove entry",
                   "Update",
                   "Display table",
                   "Buy the full version of the software to unlock more options"]

    while True:
        ui.print_menu("Accounting module", options, "Back to main menu")

        try:
            choose(table)
        except KeyError as err:
            ui.print_error_message(err)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    titles = ["id", "month", "day", "year", "type", "amount"]
    ui.print_table(table, titles)

    pass


def choose(table):    # still needs error checking as well
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    if option == "1":
        add(table)
    elif option == "2":
        input_id = ui.get_inputs(["Please enter the id of the one you want to remove: "], "")[0]
        remove(table, input_id)
    elif option == "3":
        input_id = ui.get_inputs(["Please enter the id of the one you want to change: "], "")[0]
        update(table, input_id)
    elif option == "4":
        show_table(table)
    elif option == "5":
        which_year_max(table)        
    elif option == "6":
        # sales.start_module()    # TO DO
        pass
    elif option == "0":
        data_manager.write_table_to_file("accounting/items.csv", table)
        
    else:
        raise KeyError("There is no such option.")


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """
    while True:
        input_month = ui.get_inputs(["Please enter the month: "], "")[0]
        if not common.validate_month(input_month):
            continue
        break

    while True:
        input_day = ui.get_inputs(["Please enter the day: "], "")[0]
        if not common.validate_day(input_day):
            continue
        break

    while True:
        input_year = ui.get_inputs(["Please enter the year: "], "")[0]
        if not common.validate_byear(input_year):
            continue
        break

    while True:
        input_type = ui.get_inputs(["Please enter the type (in or out): "], "")[0]
        if not common.validate_type(input_type):
            continue
        break

    while True:
        input_amount = ui.get_inputs(["Please enter the amount (in US dollars): "], "")[0]
        if not common.validate_int(input_amount):
            continue
        break

    while True:
        random_id = common.generate_random(table)
        if common.id_exists(table, random_id):
            continue
        break

    table.append([random_id, input_month, input_day, input_year, input_type, input_amount])

    show_table(table)
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

    id_to_delete = common.index_of_id(table, id_)

    if id_to_delete >= 0:
        del table[id_to_delete]

    show_table(table)
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

    id_to_change = common.index_of_id(table, id_)

    if id_to_change < 0:
        return

    while True:
        input_month = ui.get_inputs(["Please enter the new month: "], "")[0]
        if common.validate_empty(input_month):
            input_month = table[id_to_change][1]
        elif not common.validate_month(input_month):
            continue
        break

    while True:
        input_day = ui.get_inputs(["Please enter the new day: "], "")[0]
        if common.validate_empty(input_day):
            input_day = table[id_to_change][2]
        elif not common.validate_day(input_day):
            continue
        break

    while True:
        input_year = ui.get_inputs(["Please enter the new year: "], "")[0]
        if common.validate_empty(input_year):
            input_year = table[id_to_change][3]
        elif not common.validate_byear(input_year):
            continue
        break

    while True:
        input_type = ui.get_inputs(["Please enter the new type (in or out): "], "")[0]
        if common.validate_empty(input_type):
            input_type = table[id_to_change][4]
        elif not common.validate_type(input_type):
            continue
        break

    while True:
        input_amount = ui.get_inputs(["Please enter the new amount (in US dollars): "], "")[0]
        if common.validate_empty(input_amount):
            input_amount = table[id_to_change][5]
        elif not common.validate_int(input_amount):
            continue
        break

    table[id_to_change] = [id_, input_month, input_day, input_year, input_type, input_amount]
    show_table(table)
    return table


# special functions:
# ------------------

# the question: Which year has the highest profit? (profit=in-out)
# return the answer (number)
def which_year_max(table):
    years = [table[x][3] for x in range(len(table))]

    for year in set(years):
        




# the question: What is the average (per item) profit in a given year? [(profit)/(items count) ]
# return the answer (number)
def avg_amount(table, year):

    # your code

    pass


if __name__ == '__main__':
    start_module()
