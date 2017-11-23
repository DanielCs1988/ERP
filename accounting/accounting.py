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


def start_module(table_file=None, table_cont=None):
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    If no argument given, uses items.csv

    Args:
        table_file: use a 2d list instead, overwritten by table_cont
        table_cont: use the previously opened table,
            in case of keyboead interrupt

    Returns:
        None
    """
    ui.clear_scr()

    if not table_file and not table_cont:
        table = data_manager.get_table_from_file("accounting/items.csv")
    elif not table_cont:
        table = table_file
    else:
        table = table_cont

    paid_version = True    # an easter-egg, leave it True and it should (hopefully) cause no problems
    if paid_version:    # uses the options based on the easter-egg
        menu_options = ["Show table",
                        "Add entry",
                        "Update entry",
                        "Remove entry",
                        "Which year has the highest profit?",
                        "What is the average (per item) profit in a given year?"]
    else:
        menu_options = ["Show table",
                        "Add entry",
                        "Update entry",
                        "Remove entry",
                        "Buy the full version of the software to unlock more options"]
    try:
        while True:
            ui.print_menu("Accounting", menu_options, "Back to main menu")
            option = ui.get_inputs(["Please enter a number: "], "")[0]

            if option == "1":
                show_table(table)
            elif option == "2":
                ui.clear_scr()
                add(table)
            elif option == "3":
                input_id = ui.get_inputs(["Please enter the id of the one you want to change: "], "")[0]
                update(table, input_id)
                ui.clear_scr()
            elif option == "4":
                input_id = ui.get_inputs(["Please enter the id of the one you want to remove: "], "")[0]
                remove(table, input_id)
                ui.clear_scr()
            elif option == "5":
                ui.print_result("The year with the highest profit is {0}".format(which_year_max(table)))
            elif option == "6":
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

            elif option == "0":
                data_manager.write_table_to_file("accounting/items.csv", table)
                ui.clear_scr()
                break
            else:
                ui.clear_scr()
    except (KeyboardInterrupt, EOFError):
        ui.print_error_message('''\nKeyboard interrupt.\n\nYou will lose all changes.''')
        while True:
            decision = ui.get_inputs(["Are you sure you want to quit?.(Y/N)"], "")[0]
            if decision in ['Y', 'y']:
                break
            elif decision in ['N', 'n']:
                start_module(table_cont=table)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    ui.clear_scr()
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

    new_data = ui.mass_valid_in([("Please enter the month: ", common.validate_month),
                                 ("Please enter the day: ", common.validate_day),
                                 ("Please enter the year: ", common.validate_byear),
                                 ("Please enter the type (in or out): ", common.validate_type),
                                 ("Please enter the amount (in US dollars): ", common.validate_int)
                                 ])

    if new_data is None:
        return table
    new_line = [common.generate_random(table)]
    new_line.extend(new_data)

    table.append(new_line)
    ui.clear_scr()

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

    index = common.index_of_id(table, id_)
    if index < 0:
        return table

    new_data = ui.mass_valid_in([("Please enter the new month: ", common.validate_month),
                                 ("Please enter the new day: ", common.validate_day),
                                 ("Please enter the new year: ", common.validate_byear),
                                 ("Please enter the new type (in or out): ", common.validate_type),
                                 ("Please enter the new amount (in US dollars): ", common.validate_int)
                                 ], True)

    common.apply_update_to_line(table[index], new_data)
    show_table(table)
    return table


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
