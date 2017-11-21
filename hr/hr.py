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
        person[2] = int(person[2])

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
            break
        else:
            ui.print_error_message(err)
            # Wait here


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    ui.print_table(table)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """
    new_person = [common.generate_random(table)]
    new_person.append(ui.get_inputs(["Name: "], "New Person's Information"))
    while True:
        b_year = ui.get_inputs(["Birth Year: "], "")
        if common.validate_year(b_year):
            new_person.append(b_year)
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
        return

    del table[common.index_of_id(table, id_)]
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

    table[index][1](ui.get_inputs(["Name: "], ""))
    while True:
        b_year = ui.get_inputs(["Birth Year: "], "")
        if common.validate_year(b_year):
            table[index][2] = b_year
            break

    return table


# special functions:
# ------------------

# the question: Who is the oldest person ?
# return type: list of strings (name or names if there are two more with the same value)
def get_oldest_person(table):
    max_age = min([person[2] for person in table])
    return [person[1] for person in table if person[2] == max_age]


# the question: Who is the closest to the average age ?
# return type: list of strings (name or names if there are two more with the same value)
def get_persons_closest_to_average(table):
    average_age = common.get_sum(table, 2) // common.count(table)
    closest_age = min([abs(average_age-person[2]) for person in table])
    return [person[1] for person in table if abs(average_age-person[2]) == closest_age]
