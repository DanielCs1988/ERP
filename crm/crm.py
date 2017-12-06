"""
Customer relations module. Data structure:
1. ID of contact
2. Name of contact
3. E-mail of contact
4. Contact subscribed to mailing list or not (0: no, 1: yes)
"""

import os
import ui
import data_manager
import common

ID = 0
NAME = 1
EMAIL = 2
SUBSCRIBED = 3


def start_module():
    """Starts the module and displays its menu."""

    ui.clear_scr()
    crm_options = ["Show table",
                   "Add entry",
                   "Update entry",
                   "Remove entry",
                   "What is the ID of the longest name person?",
                   "Subscribed emails"]

    crm_data = data_manager.get_table_from_file("crm/customers.csv")

    ui.clear_scr()
    while True:
        ui.print_menu("Customer relationship management", crm_options, "Back to main menu")

        try:
            option = ui.valid_in("Please enter a number: ", common.validate_string)
        except (KeyboardInterrupt, EOFError):
            data_manager.write_table_to_file("crm/customers.csv", crm_data)
            ui.clear_scr()
            exit()

        if option == "1":
            show_table(crm_data)
        elif option == "2":
            crm_data = add(crm_data)
            ui.clear_scr()
        elif option == "3":
            update_id = ui.get_inputs(["Please enter the ID of the person you want to update: "], "")[0]
            crm_data = update(crm_data, update_id)
            ui.clear_scr()
        elif option == "4":
            remove_id = ui.get_inputs(["Please enter the ID of the person you want to delete: "], "")[0]
            crm_data = remove(crm_data, remove_id)
            ui.clear_scr()
        elif option == "5":
            ui.clear_scr()
            ui.print_result("ID of longest name:")
            ui.print_result(get_longest_name_id(crm_data))
        elif option == "6":
            ui.clear_scr()
            temp_crm_data = get_subscribed_emails(crm_data)
            temp_crm_data = [line.split(";") for line in temp_crm_data]
            ui.print_result("Subscribed email")
            ui.print_table(temp_crm_data, ["E-mail", "Name"])
        elif option == "0":
            data_manager.write_table_to_file("crm/customers.csv", crm_data)
            ui.clear_scr()
            break
        else:
            ui.clear_scr()


def show_table(table):
    """Display the table given as parameter."""
    ui.clear_scr()
    ui.print_table(table, ["ID", "Name", "E-mail", "Subscribed"])


def add(table):
    """Asks user for input and adds it to the table. Returns table with the new record."""
    return common.add_line(table, [("Name: ", common.validate_string),
                                   ("E-mail: ", common.validate_email),
                                   ("Subscribed? (1 for yes, 0 for no): ", common.validate_boolean)])


def remove(table, id_):
    """Remove a record with a given id from the table. Returns table without the specified record."""
    return common.remove_line(table, id_)


def update(table, id_):
    """Updates specified record in the table. Asks users for new data. Returns table with the updated record."""
    return common.update_line(table, id_, [("Name: ", common.validate_string),
                                           ("E-mail: ", common.validate_email),
                                           ("Subscribed? (1 for yes, 0 for no) ", common.validate_boolean)])


def get_longest_name_id(table):
    """Returns the ID of the person who has the longest name. If there are more people it returns the first in
       ascending alphabetical order"""

    names_lengths = [(line[ID], len(line[NAME]), line[NAME]) for line in table]
    max_length = max(names_lengths, key=common.get_item(1))[1]
    max_length_names = [(name[0], name[2]) for name in names_lengths if name[1] == max_length]

    return common.srt(max_length_names, key=common.get_item(1))[0][0]


def get_subscribed_emails(table):
    """Returns a list of subscribed customers with their name and e-mail seperated by ";" """
    return [";".join((line[EMAIL], line[NAME])) for line in table if line[SUBSCRIBED] == '1']


def get_name_by_id(id):
    """Returns the name (str) of the customer with the given id (str), None in case of non-existing id."""
    crm_data = data_manager.get_table_from_file("crm/customers.csv")
    return get_name_by_id_from_table(crm_data, id)


def get_name_by_id_from_table(table, id):
    """Returns the name (str) of the customer with the given id (str), None in case of non-existing id."""

    for line in table:
        if line[ID] == id:
            return line[NAME]
    return None


def get_all_customer_ids():
    """Returns a set of customer_ids that are present in the table."""
    table = data_manager.get_table_from_file("crm/customers.csv")
    return {row[ID] for row in table}
