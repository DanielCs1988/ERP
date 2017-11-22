# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# price: number (the actual sale price in $)
# month: number
# day: number
# year: number
# month,year and day combined gives the date the sale was made

import os
import ui
import data_manager
import common

ID = 0
TITLE = 1
PRICE = 2
MONTH = 3
DAY = 4
YEAR = 5


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
               "Show Lowest Price ID",
               "Show Sold Items Between Dates"]

    sales_data = data_manager.get_table_from_file("sales.csv")
    for sale in sales_data:
        sale[PRICE] = int(sale[PRICE])
        sale[MONTH] = int(sale[MONTH])
        sale[DAY] = int(sale[DAY])
        sale[YEAR] = int(sale[YEAR])

    while True:
        ui.print_menu("Sales Department: Main menu", options, "Exit program")
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]

        if option == "1":
            show_table(sales_data)
        elif option == "2":
            sales_data = add(sales_data)
        elif option == "3":
            to_remove = ui.get_inputs(["Please enter the ID of the sale you want removed: "], "")
            sales_data = remove(sales_data, to_remove[0])
        elif option == "4":
            to_update = ui.get_inputs(["Please enter the ID of the sale you want updated: "], "")
            sales_data = update(sales_data, to_update[0])
        elif option == "5":
            ui.print_result(get_lowest_price_item_id(sales_data))
        elif option == "6":
            ui.print_result(get_items_sold_between(sales_data))
        elif option == "0":
            data_manager.write_table_to_file("sales.csv", sales_data)
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
    titles = ["ID", "Title", "Price", "Date"]
    output_table = [[row[ID], row[TITLE], row[PRICE], '/'.join(row[YEAR], row[MONTH], row[DAY])] for row in table]
    ui.print_table(output_table, titles)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """
    new_sale = [common.generate_random(table)]
    new_sale.append(ui.get_inputs(["Title: "], "New Sale Information")[0])

    while True:
        price = ui.get_inputs(["Price: "], "")[0]
        if common.validate_int(price):
            new_sale.append(int(price))
            break

    while True:
        year = ui.get_inputs(["Year of sale: "], "")[0]
        if common.validate_byear(year):
            new_sale.append(int(year))
            break

    while True:
        month = ui.get_inputs(["Month of sale: "], "")[0]
        if common.validate_month(month):
            new_sale.append(int(month))
            break

    while True:
        day = ui.get_inputs(["Day of sale: "], "")[0]
        if common.validate_day(day):
            new_sale.append(int(day))
            break

    table.append(new_sale)
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

    table[index][TITLE] = ui.get_inputs(["Title: "], "")[0]

    while True:
        price = ui.get_inputs(["Price: "], "")[0]
        if common.validate_int(price):
            table[index][PRICE] = int(price)
            break

    while True:
        year = ui.get_inputs(["Year of sale: "], "")[0]
        if common.validate_byear(year):
            table[index][YEAR] = int(year)
            break

    while True:
        month = ui.get_inputs(["Month of sale: "], "")[0]
        if common.validate_month(month):
            table[index][MONTH] = int(month)
            break

    while True:
        day = ui.get_inputs(["Day of sale: "], "")[0]
        if common.validate_day(day):
            table[index][DAY] = int(day)
            break

    return table


# special functions:
# ------------------

# the question: What is the id of the item that was sold for the lowest price ?
# return type: string (id)
# if there are more than one with the lowest price, return the first by descending alphabetical order
def get_lowest_price_item_id(table):

    # your code

    pass


# the question: Which items are sold between two given dates ? (from_date < sale_date < to_date)
# return type: list of lists (the filtered table)
def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):

    # your code

    pass
