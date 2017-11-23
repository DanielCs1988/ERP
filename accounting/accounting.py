# data structure:
# id: string
#     Unique and randomly generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# month: number
# day: number
# year: number
# type: string (in = income, out = outcome)
# amount: number (dollar)

import os
import ui
import data_manager
import common

ID = 0
MONTH = 1
DAY = 2
YEAR = 3
TYPE = 4
AMOUNT = 5


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
        menu_options = ["Add entry",
                        "Remove entry",
                        "Update",
                        "Display table",
                        "Which year has the highest profit?",
                        "What is the average (per item) profit in a given year?"]
    else:
        menu_options = ["Add entry",
                        "Remove entry",
                        "Update",
                        "Display table",
                        "Buy the full version of the software to unlock more options"]

    while True:
        ui.print_menu("Accounting", menu_options, "Back to main menu")
        try:
            inputs = ui.get_inputs(["Please enter a number: "], "")
        except (KeyboardInterrupt, EOFError):
            data_manager.write_table_to_file("accounting/items.csv", table)
            common.exit()

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
            ui.print_result(which_year_max(table))
        elif option == "6":
            while True:
                input_year = ui.get_inputs(["Which year do you want to know about: "], "")[0]
                if not common.validate_byear(input_year):
                    continue
                if common.index_of_value(table, YEAR, input_year) == -1:
                    continue
                break
            ui.print_result(avg_amount(table, input_year),
                            "The average amount of profit per game in {0}".format(input_year))
        elif option == "0":
            data_manager.write_table_to_file("accounting/items.csv", table)
            break
        else:
            ui.print_error_message("There is no such option.")


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    titles = ["ID", "Month", "Day", "Year", "Type", "Amount"]
    ui.print_table(table, titles)


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

    random_id = common.generate_random(table)

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


def update(table, id_):  # Constants could be used here, also needs a bit of reviewing.
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
        ui.print_error_message("The given ID doesn't exist.")
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

    # Could be updated dinamically at the input points, but I decided not to.
    table[id_to_change] = [id_, input_month, input_day, input_year, input_type, input_amount]
    show_table(table)
    return table


# special functions:
# ------------------

# the question: Which year has the highest profit? (profit=in-out)
# return the answer (number)
def which_year_max(table):
    '''
    Goes through each unique year, counting the sum of the profits.
    Then subtracts the 'out' values.
    Compares and returns the year with the highest profit.
    '''
    max_profit, current_year = 0, 0
    for year in {row[YEAR] for row in table}:
        temp_sum = common.get_sum_list(
            [int(row[AMOUNT]) for row in table if row[YEAR] == year and row[TYPE] == 'in'])
        temp_sum -= common.get_sum_list(
            [int(row[AMOUNT]) for row in table if row[YEAR] == year and row[TYPE] == 'out'])
        if temp_sum > max_profit:
            max_profit, current_year = temp_sum, year

    return current_year, max_profit


# the question: What is the average (per item) profit in a given year? [(profit)/(items count) ]
# return the answer (number)
def avg_amount(table, input_year):
    profit = []
    current_year = 0

    temp_sum = common.get_sum_list(
        [int(row[AMOUNT]) for row in table if row[YEAR] == input_year and row[TYPE] == 'in'])
    temp_sum -= common.get_sum_list(
        [int(row[AMOUNT]) for row in table if row[YEAR] == input_year and row[TYPE] == 'out'])
    temp_count = common.get_sum_list(
        [1 for row in table if row[YEAR] == input_year])

    return temp_sum / temp_count

if __name__ == '__main__':
    start_module()
