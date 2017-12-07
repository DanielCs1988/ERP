"""
Partner registry module. Data structure:
1. ID of partner
2. Partner's name
3. Name of partner's contact person
4. Partner's e-mail
5. Partner's phone number
6. Address of partner's base of operations (that concerns our dealings).
"""

import os
import ui
import data_manager
import common

ID = 0
NAME = 1
CONTACT_PERSON = 2
EMAIL = 3
PHONE = 4
ADDRESS = 5


def start_module():
    """Starts the module and displays its menu."""

    ui.clear_scr()
    partner_options = ["Show table",
                       "Add entry",
                       "Update entry",
                       "Remove entry"]

    partners_file = "partners/partners.csv"
    partner_data = data_manager.get_table_from_file(partners_file)
    ui.clear_scr()

    while True:
        try:
            ui.print_menu("Partner informations module", partner_options, "Back to main menu")
            option = ui.valid_in("Please enter a number: ", common.validate_string)

            if option == "1":
                show_table(partner_data)
            elif option == "2":
                menuaction_add(partner_data)
            elif option == "3":
                menuaction_update(partner_data)
            elif option == "4":
                menuaction_remove(partner_data)
            elif option == "0":
                data_manager.write_table_to_file(partners_file, partner_data)
                ui.clear_scr()
                break
            else:
                ui.clear_scr()
        except (KeyboardInterrupt, EOFError):
            common.handle_kb_interrupt(partners_file, partner_data)


def menuaction_remove(partner_data):
    remove_id = ui.get_inputs(["Please enter the ID of the partner you want to delete: "], "")[0]
    remove(partner_data, remove_id)
    ui.clear_scr()


def menuaction_update(partner_data):
    update_id = ui.get_inputs(["Please enter the ID of the person you want to update: "], "")[0]
    update(partner_data, update_id)
    ui.clear_scr()


def menuaction_add(partner_data):
    add(partner_data)
    ui.clear_scr()


def show_table(table):
    """Display the table given as parameter."""
    ui.clear_scr()
    ui.print_table(table, ["ID", "Name", "Contact Person", "E-mail", "Phone number", "Address"])


def add(table):
    """Asks user for input and adds it to the table. Returns table with the new record."""
    return common.add_line(table, [("Name: ", common.validate_string),
                                   ("Contact Person: ", common.validate_string),
                                   ("E-mail: ", common.validate_email),
                                   ("Phone number: ", common.validate_string),
                                   ("Address: ", common.validate_string)])


def remove(table, id_):
    """Remove a record with a given id from the table. Returns table without the specified record."""
    return common.remove_line(table, id_)


def update(table, id_):
    """Updates specified record in the table. Asks users for new data. Returns table with the updated record."""
    return common.update_line(table, id_, [("Name: ", common.validate_string),
                                           ("Contact Person: ", common.validate_string),
                                           ("E-mail: ", common.validate_email),
                                           ("Phone number: ", common.validate_string),
                                           ("Address: ", common.validate_string)])


def get_info_by_id(id, req_info):
    """Returns the queried information of the partner with the given id, None in case of non-existing id."""

    partner_data = data_manager.get_table_from_file("partners/partners.csv")
    for line in partner_data:
        if line[ID] == id:
            return line[req_info]
    return None
