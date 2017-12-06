"""
Accounting module. Data structure:
1. ID of transaction
2-4. Date of transaction
5. Type of transaction (in: income, out: outcome)
6. Transaction amount in dollars
"""

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

INPUT_DESCRIPTIONS = [("Please enter the month: ", common.validate_month),
                      ("Please enter the day: ", common.validate_day),
                      ("Please enter the year: ", common.validate_byear),
                      ("Please enter the type (in or out): ", common.validate_type),
                      ("Please enter the amount (in US dollars): ", common.validate_int)
                      ]


def menuaction_show(table):
    show_table(table)


def menuaction_add(table):
    add(table)
    ui.clear_scr()


def menuaction_update(table):
    id_to_update = ui.get_inputs(["Enter ID of item to update:"], "")[0]
    if id_to_update:
        update(table, id_to_update)
    ui.clear_scr()


def menuaction_remove(table):
    id_to_remove = ui.get_inputs(["Enter ID to remove:"], "")[0]
    if id_to_remove:
        remove(table, id_to_remove)
    ui.clear_scr()


def menuaction_highest_profit(table):
    ui.print_result("The year with the highest profit is {0}".format(which_year_max(table)))


def menuaction_profit_per_year(table):
    while True:    # checks if the year exists in the table at all
        ui.clear_scr()
        years = {line[YEAR] for line in table}
        input_year = ui.get_inputs(["The options are {0}\n".format(", ".join(years))],
                                   "Which year do you want to know about?")[0]
        if not common.validate_byear(input_year):
            continue
        if common.index_of_value(table, YEAR, input_year) == -1:
            continue
        break
    ui.print_result(avg_amount(table, input_year),
                    "The average amount of USD profit per game in {0} is".format(input_year))


def menuaction_exit(table):
    data_manager.write_table_to_file("accounting/items.csv", table)
    ui.clear_scr()


def start_module(table_cont=None):
    """
    Starts this module and displays its menu.

    If no argument given, uses items.csv

    Args:
        table_cont: use the previously opened table,
            in case of keyboard interrupt
    """
    # data = (table_cont if table_cont else "accounting/items.csv")
    common.load_data("accounting", table_cont)

    if not table_cont:
        table = data_manager.get_table_from_file("accounting/items.csv")
    elif not table_cont:
        table = table_file
    else:
        table = table_cont

    options = ["Show table",
               "Add entry",
               "Update entry",
               "Remove entry",
               "Which year has the highest profit?",
               "What is the average (per item) profit in a given year?"]

    # options = common.trial_version(options, "X")

    try:
        while True:
            ui.print_menu("Accounting", options, "Back to main menu")
            option = ui.get_inputs(["Please enter a number: "], "")[0]

            if option == "1":
                menuaction_show(table)
            elif option == "2":
                menuaction_add(table)
            elif option == "3":
                menuaction_update(table)
            elif option == "4":
                menuaction_remove(table)
            elif option == "5":
                menuaction_highest_profit(table)
            elif option == "6":
                menuaction_profit_per_year(table)
            elif option == "0":
                menuaction_exit(table)
                break
            else:
                ui.clear_scr()
    except (KeyboardInterrupt, EOFError):
        ui.print_error_message('''\nKeyboard interrupt.\n\nYou will lose all changes.''')
        while True:
            decision = ui.get_inputs(["Are you sure you want to quit without saving?.(Y/N)"], "")[0]
            if decision in ['Y', 'y']:
                break
            elif decision in ['N', 'n']:
                start_module(table_cont=table)
                break


def show_table(table):
    """Display the table given as parameter."""
    ui.clear_scr()
    titles = ["ID", "Month", "Day", "Year", "Type", "Amount"]
    ui.print_table(table, titles)


def add(table):
    """Asks user for input and adds it to the table. Returns table with the new record."""
    return common.add_line(table, INPUT_DESCRIPTIONS)


def remove(table, id_):
    """Remove a record with a given id from the table. Returns table without the specified record."""
    return common.remove_line(table, id_)


def update(table, id_):
    """Updates specified record in the table. Asks users for new data. Returns table with the updated record."""
    return common.update_line(table, id_, INPUT_DESCRIPTIONS)


def which_year_max(table):
    '''
    Goes through each unique year, counting the sum of the profits.
    Then subtracts the 'out' values.
    Compares and returns the year with the highest profit.
    '''
    ui.clear_scr()
    max_profit, current_year = 0, 0
    for year in {row[YEAR] for row in table}:
        temp_sum = common.szum_list(
            [int(row[AMOUNT]) for row in table if row[YEAR] == year and row[TYPE] == 'in'])
        temp_sum -= common.szum_list(
            [int(row[AMOUNT]) for row in table if row[YEAR] == year and row[TYPE] == 'out'])
        if temp_sum > max_profit:
            max_profit, current_year = temp_sum, year

    current_year = int(current_year)
    return current_year


def avg_amount(table, input_year):
    '''
    Goes through each unique year, counting the sum of the profits.
    Then subtracts the 'out' values.
    Divides that by the number of lines
    and returns the year with the average profit. (float)
    '''
    ui.clear_scr()
    input_year = str(input_year)
    years = {line[YEAR] for line in table}
    if input_year not in years:
        ui.print_error_message("Not a valid year.")
        return
    profit = []
    current_year = 0

    temp_sum = common.szum_list(
        [int(row[AMOUNT]) for row in table if row[YEAR] == input_year and row[TYPE] == 'in'])
    temp_sum -= common.szum_list(
        [int(row[AMOUNT]) for row in table if row[YEAR] == input_year and row[TYPE] == 'out'])
    temp_count = common.szum_list(
        [1 for row in table if row[YEAR] == input_year])

    return temp_sum / temp_count
