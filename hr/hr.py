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
import datetime

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
               "Add Person",
               "Remove Person",
               "Update Person",
               "Show Oldest Person",
               "Show Persons Closest to Average Age"]

    hr_data = data_manager.get_table_from_file("persons.csv")
    for person in hr_data:
        person[B_YEAR] = int(person[B_YEAR])

    while True:
        ui.print_menu("HR Department: Main menu", options, "Exit program")
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]

        if option == "1":
            show_table(hr_data)
        elif option == "2":
            hr_data = add(hr_data)
        elif option == "3":
            to_remove = ui.get_inputs(["Please enter the ID of the person you want removed: "], "")
            hr_data = remove(hr_data, to_remove[0])
        elif option == "4":
            to_update = ui.get_inputs(["Please enter the ID of the person you want updated: "], "")
            hr_data = update(hr_data, to_update[0])
        elif option == "5":
            ui.print_result(get_oldest_person(hr_data))
        elif option == "6":
            ui.print_result(get_persons_closest_to_average(hr_data))
        elif option == "0":
            data_manager.write_table_to_file("persons.csv", hr_data)
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
    titles = ["ID", "Name", "Birth Year"]
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
    new_person.append(ui.get_inputs(["Name: "], "New Person's Information")[0])
    while True:
        b_year = ui.get_inputs(["Birth Year: "], "")[0]
        if common.validate_byear(b_year):
            new_person.append(int(b_year))
            break

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
    index = common.index_of_id(table, id_)
    if index == -1:
        ui.print_error_message("Wrong ID!")
        return table  # That was the most ridiculous mistake ever, period.

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
        return

    table[index][1] = ui.get_inputs(["Name: "], "")[0]

    while True:
        b_year = ui.get_inputs(["Birth Year: "], "")[0]
        if common.validate_byear(b_year):
            table[index][B_YEAR] = int(b_year)
            break

    return table


def get_oldest_person(table):
    """Return a list of the oldest people in the group."""

    max_age = min([person[B_YEAR] for person in table])
    return [person[NAME] for person in table if person[B_YEAR] == max_age]


def get_persons_closest_to_average(table):
    """Returns a list of the people closest to the average age in the group."""

    average_age = common.get_sum(table, B_YEAR) // len(table)
    closest_age = min([abs(average_age-person[B_YEAR]) for person in table])
    return [person[NAME] for person in table if abs(average_age-person[B_YEAR]) == closest_age]
