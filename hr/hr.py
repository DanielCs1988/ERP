"""
Human resources module. Data structure:
1. ID of employee
2. Name of employee
3. Birth year of employee
"""

import os
import ui
import data_manager
import common

ID = 0
NAME = 1
B_YEAR = 2


def start_module():
    """Starts the module and displays its menu."""

    options = ["Show Table",
               "Add Entry",
               "Update Entry",
               "Remove Entry",
               "Show Oldest Person",
               "Show Persons Closest to Average Age"]

    hr_file = "hr/persons.csv"
    hr_data = data_manager.get_table_from_file(hr_file)
    ui.clear_scr()

    while True:
        try:
            ui.print_menu("HR Department: Main menu", options, "Back to main menu")
            option = ui.valid_in("Please enter a number: ", common.validate_string)

            if option == "1":
                show_table(hr_data)
            elif option == "2":
                menuaction_add(hr_data)
            elif option == "3":
                menuaction_update(hr_data)
            elif option == "4":
                menuaction_remove(hr_data)
            elif option == "5":
                menuaction_oldest_ppl(hr_data)
            elif option == "6":
                menuaction_ppl_closest_to_avg(hr_data)
            elif option == "0":
                data_manager.write_table_to_file(hr_file, hr_data)
                ui.clear_scr()
                break
            else:
                ui.clear_scr()

        except (KeyboardInterrupt, EOFError):
            common.handle_kb_interrupt(hr_file, hr_data)


def menuaction_ppl_closest_to_avg(hr_data):
    ui.clear_scr()
    ui.print_result(get_persons_closest_to_average(hr_data), "People closest to the average age")


def menuaction_oldest_ppl(hr_data):
    ui.clear_scr()
    ui.print_result(get_oldest_person(hr_data), "Oldest people in the database")


def menuaction_remove(hr_data):
    to_remove = ui.valid_in(
        "What is the ID of the item that you would like to remove? ", common.validate_string)
    remove(hr_data, to_remove)
    ui.clear_scr()


def menuaction_update(hr_data):
    to_update = ui.valid_in(
        "What is the ID of the item that you would like to update? ", common.validate_string)
    update(hr_data, to_update)
    ui.clear_scr()


def menuaction_add(hr_data):
    add(hr_data)
    ui.clear_scr()


def show_table(table):
    """Display the table given as parameter."""
    titles = ["ID", "Name", "Birth Year"]
    ui.clear_scr()
    ui.print_table(table, titles, NAME)


def add(table):
    """Asks user for input and adds it to the table. Returns table with the new record."""
    return common.add_line(table, [("Name: ", None),
                                   ("Birth year: ", common.validate_byear)
                                   ])


def remove(table, id_):
    """Remove a record with a given id from the table. Returns table without the specified record."""
    return common.remove_line(table, id_)


def update(table, id_):
    """Updates specified record in the table. Asks users for new data. Returns table with the updated record."""
    return common.update_line(table, id_, [("Name: ", None),
                                           ("Birth year: ", common.validate_byear)
                                           ])


def get_oldest_person(table):
    """Return a list of the oldest people in the group."""

    max_age = min([int(person[B_YEAR]) for person in table])
    return [person[NAME] for person in table if int(person[B_YEAR]) == max_age]


def get_persons_closest_to_average(table):
    """Returns a list of the people closest to the average age in the group."""

    average_age = common.szum(table, B_YEAR) // len(table)
    closest_age = min([abs(average_age - int(person[B_YEAR])) for person in table])
    return [person[NAME] for person in table if abs(average_age - int(person[B_YEAR])) == closest_age]
