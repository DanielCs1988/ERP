# data structure:
# id: string
#     Unique and randomly generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# email: string
# subscribed: boolean (Is she/he subscribed to the newsletter? 1/0 = yes/not)


# importing everything you need
import os
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
# itemgetter
from operator import itemgetter

ID = 0
NAME = 1
EMAIL = 2
SUBSCRIBED = 3


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """
    crm_options = ["Show table",
                   "Add",
                   "Remove",
                   "Update",
                   "Who has the longest name?",
                   "Subscribed emails"]

    crm_data = data_manager.get_table_from_file("crm/customers.csv")

    while True:
        ui.print_menu("Customer relationship management:", crm_options, "Back to main menu")
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]

        if option == "1":
            show_table(crm_data)
        elif option == "2":
            crm_data = add(crm_data)
        elif option == "3":
            remove_id = ui.get_inputs(["Please enter the ID of the person you want to delete: "])
            crm_data = remove(crm_data, remove_id)
        elif option == "4":
            update_id = ui.get_inputs(["Please enter the ID of the person you want to update: "])
            crm_data = update(crm_data, update_id)
        elif option == "5":
            ui.print_result(get_longest_name_id(crm_data))
        elif option == "6":
            ui.print_result(get_subscribed_emails(crm_data))
        elif option == "0":
            data_manager.write_table_to_file("crm/customers.csv", hr_data)
            break
        else:
            ui.print_error_message(err)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    ui.print_table(table, ["ID", "Name", "E-mail", "Subscribed"])


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """
    new_customer_data = [common.generate_random(table)]
    new_customre_data.append(ui.get_inputs(["Name: "])[0])
    while True:
        email = ui.get_inputs(["E-mail: "], "")[0]
        if common.validate_email(email):
            new_customer_data.append(email)
            break
    while True:
        boolean = ui.get_inputs(["Is he subscribed?: "])[0]
        if common.validate_boolean(boolean):
            new_customer_data.append(boolean)
            break

    table.append(new_customer_data)

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

    index = common.index_of_id(table, id_)
    if index == -1:
        ui.print_error_message("Wrong ID!")
        return table

    del table[index]

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
    if index == -1:
        ui.print_error_message("Wrong ID!")
        return table

    table[index][NAME] = new_customer_data(ui.get_inputs(["Name: "])[0])
    while True:
        new_email = ui.get_inputs(["E-mail: "], "")[0]
        if common.validate_email(email):
            table[index][EMAIL] = email
            break
    while True:
        new_boolean = ui.get_inputs(["Is he subscribed?: "])[0]
        if common.validate_boolean(boolean):
            table[index][SUBSCRIBED] = new_boolean
            break

    return table


# special functions:
# ------------------


# the question: What is the id of the customer with the longest name ?
# return type: string (id) - if there are more than one longest name, return the first by descending alphabetical order
def get_longest_name_id(table):
    """Returns the ID of the person who has the longest name. If there are more people it returns the first in
       descending alphabetical order"""
    names_lengths = [(line[ID], len(line[NAME], line[NAME])) for line in table]
    max_length = max(names_lengths, key=itemgetter(1))[1]
    max_length_names = [(name[0], name[2]) for name in names_lengths if name[1] == max_length]

    return common.qsort(max_length_names, key=itemgetter(1), reversed=True)[0]


# the question: Which customers has subscribed to the newsletter?
# return type: list of strings (where string is like email+separator+name, separator=";")
def get_subscribed_emails(table):
    """Returns a list of subscribed customers with their name and e-mail seperated by ";" """
    return ["; ".join(line[NAME], line[EMAIL]) for line in table if line[SUBSCRIBED] == 1]
