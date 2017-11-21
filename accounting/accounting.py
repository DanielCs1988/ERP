# data structure:
# id: string
#     Unique and randomly generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# month: number
# day: number
# year: number
# type: string (in = income, out = outcome)
# amount: number (dollar)


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
                   "Which year has the highest profit?",
                   "What is the average (per item) profit in a given year?"]
    else:
        options = ["Add entry",
                   "Remove entry",
                   "Update",
                   "Buy the full version of the software to unlock more options"]
    ui.print_menu("Accounting module", options, "Back to main menu")

    while True:
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
    
    ui.print_table(table)

    pass


def choose(table):    # still needs error checking as well
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    if option == "1":
        add(table)
    elif option == "2":
        input_id = inputs[1]
        remove(table, input_id)
    elif option == "3":
        input_id = inputs[1]
        update(table, input_id)
    elif option == "4":
        # which_year_max()    # TO DO
        pass
    elif option == "5":
        # sales.start_module()    # TO DO
        pass
    elif option == "0":
        handle_menu()
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

    # your code

    return table


# special functions:
# ------------------

# the question: Which year has the highest profit? (profit=in-out)
# return the answer (number)
def which_year_max(table):

    # your code

    pass


# the question: What is the average (per item) profit in a given year? [(profit)/(items count) ]
# return the answer (number)
def avg_amount(table, year):

    # your code

    pass
