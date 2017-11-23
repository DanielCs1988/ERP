"""
data structure:
-id: string
 Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
-name: string
-birth_date: number (year)
"""

import os
import ui
import data_manager
import common

ID = 0
NAME = 1
B_YEAR = 2


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """
    options = ["Show Table",
               "Add Entry",
               "Update Entry",
               "Remove Entry",
               "Show Oldest Person",
               "Show Persons Closest to Average Age"]

    hr_data = data_manager.get_table_from_file("hr/persons.csv")
    ui.clear_scr()

    while True:
        ui.print_menu("HR Department: Main menu", options, "Back to main menu")
        try:
            option = ui.valid_in("Please enter a number: ", common.validate_string)
        except (KeyboardInterrupt, EOFError):
            data_manager.write_table_to_file("hr/persons.csv", hr_data)
            ui.clear_scr()
            exit()

        if option == "1":
            show_table(hr_data)
        elif option == "2":
            hr_data = add(hr_data)
            ui.clear_scr()
        elif option == "3":
            to_update = ui.valid_in(
                "What is the ID of the item that you would like to update? ", common.validate_string)
            hr_data = update(hr_data, to_update)
            ui.clear_scr()
        elif option == "4":
            to_remove = ui.valid_in(
                "What is the ID of the item that you would like to remove? ", common.validate_string)
            hr_data = remove(hr_data, to_remove)
            ui.clear_scr()
        elif option == "5":
            ui.clear_scr()
            ui.print_result(get_oldest_person(hr_data), "Oldest people in the database: ")
        elif option == "6":
            ui.clear_scr()
            ui.print_result(get_persons_closest_to_average(hr_data), "People closest to the average age: ")
        elif option == "0":
            data_manager.write_table_to_file("hr/persons.csv", hr_data)
            ui.clear_scr()
            break
        else:
            ui.clear_scr()


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    titles = ["ID", "Name", "Birth Year"]
    ui.clear_scr()
    ui.print_table(table, titles)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """
    new_person = [common.generate_random(table)]

    input_list = ui.mass_valid_in([("Name: ", None),
                                      ("Birth year: ", common.validate_byear)
                                      ])

    if input_list is None:
        return table

    new_person.extend(input_list)
    table.append(new_person)

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

    input_list = ui.mass_valid_in([("Name: ", None),
                                      ("Birth year: ", common.validate_byear)
                                      ], update_mode=True)

    table[index] = common.apply_update_to_line(table[index], input_list)
    return table


def get_oldest_person(table):
    """Return a list of the oldest people in the group."""

    max_age = min([int(person[B_YEAR]) for person in table])
    return [person[NAME] for person in table if int(person[B_YEAR]) == max_age]


def get_persons_closest_to_average(table):
    """Returns a list of the people closest to the average age in the group."""

    average_age = common.szum(table, B_YEAR) // len(table)
    closest_age = min([abs(average_age - int(person[B_YEAR])) for person in table])
    return [person[NAME] for person in table if abs(average_age - int(person[B_YEAR])) == closest_age]
