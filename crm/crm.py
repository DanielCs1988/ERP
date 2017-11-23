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
        try:
            inputs = ui.get_inputs(["Please enter a number: "], "")
        except (KeyboardInterrupt, EOFError):
            data_manager.write_table_to_file("crm/customers.csv", crm_data)
            common.exit()

        option = inputs[0]

        if option == "1":
            show_table(crm_data)
        elif option == "2":
            crm_data = add(crm_data)
        elif option == "3":
            remove_id = ui.get_inputs(["Please enter the ID of the person you want to delete: "], "")[0]
            crm_data = remove(crm_data, remove_id)
        elif option == "4":
            update_id = ui.get_inputs(["Please enter the ID of the person you want to update: "], "")[0]
            crm_data = update(crm_data, update_id)
        elif option == "5":
            ui.print_result(get_longest_name_id(crm_data))
        elif option == "6":
            ui.print_result(get_subscribed_emails(crm_data))
        elif option == "0":
            data_manager.write_table_to_file("crm/customers.csv", crm_data)
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
    #    Table with a new record
    #"""
    new_customer_data = [common.generate_random(table)]

    new_customer_data.extend(ui.mass_valid_input([("Name: ", None),
                                                  ("E-mail: ", common.validate_email)
                                                  ("Subscribed?(1 for yes, 0 for no): ", common.validate_boolean)]))
    if new_customer_data is None:
        return table

    table.extend(new_customer_data)

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
    if index == -1:
        ui.print_error_message("Wrong ID!")
        return table

    update_input = ui.mass_valid_input([("Name: ", None),
                                        ("E-mail: ", common.validate_email),
                                        ("Subscribed?(1 for yes, 0 for no", common.validate_boolean)])
    
    if update_input is None:
        return table

    for item in range(len(update_input)):
        if update_input[input] is None:
            continue
        table[index][item+1] = update_input[item]

    return table


# special functions:
# ------------------


# the question: What is the id of the customer with the longest name ?
# return type: string (id) - if there are more than one longest name, return the first by descending alphabetical order
def get_longest_name_id(table):
    """Returns the ID of the person who has the longest name. If there are more people it returns the first in
       descending alphabetical order"""
    names_lengths = [(line[ID], len(line[NAME]), line[NAME]) for line in table]
    max_length = max(names_lengths, key=itemgetter(1))[1]
    max_length_names = [(name[0], name[2]) for name in names_lengths if name[1] == max_length]

    return common.qsort(max_length_names, key=itemgetter(1), reversed=True)[0][0]


# the question: Which customers has subscribed to the newsletter?
# return type: list of strings (where string is like email+separator+name, separator=";")
def get_subscribed_emails(table):
    """Returns a list of subscribed customers with their name and e-mail seperated by ";" """
    return ["; ".join((line[NAME], line[EMAIL])) for line in table if line[SUBSCRIBED] == '1']
