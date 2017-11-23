# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# price: number (the actual sale price in $)
# month: number
# day: number
# year: number
# month,year and day combined gives the date the sale was made

from datetime import datetime
from operator import itemgetter
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
               "Add Sale",
               "Remove Sale",
               "Update Sale",
               "Show Lowest Price ID",
               "Show Sold Items Between Dates"]

    sales_data = data_manager.get_table_from_file("sales/sales.csv")

    while True:
        ui.print_menu("Sales Department: Main menu", options, "Exit program")
        try:
            inputs = ui.get_inputs(["Please enter a number: "], "")
        except (KeyboardInterrupt, EOFError):
            data_manager.write_table_to_file("sales/sales.csv", sales_data)
            common.exit()

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
            params = ui.mass_valid_input([
                
            ])
            ui.print_table(get_items_sold_between(sales_data, 12, 4, 2015, 2, 7, 2016), ["1", "2", "3", "4", "5", "6"])
        elif option == "0":
            data_manager.write_table_to_file("sales/sales.csv", sales_data)
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
    output_table = [[row[ID], row[TITLE], row[PRICE],
                     '/'.join((row[YEAR], row[MONTH], row[DAY]))] for row in table]
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

    input_list = ui.mass_valid_input([("Title: ", None),
                                      ("Price: ", common.validate_int),
                                      ("Month of sale: ", common.validate_month),
                                      ("Day of sale: ", common.validate_day),
                                      ("Year of sale: ", common.validate_byear)
                                      ])

    if input_list is None:
        return table

    new_sale.extend(input_list)
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

    input_list = ui.mass_valid_input([("Title: ", None),
                                      ("Price: ", common.validate_int),
                                      ("Month of sale: ", common.validate_month),
                                      ("Day of sale: ", common.validate_day),
                                      ("Year of sale: ", common.validate_byear)
                                      ], update_mode=True)

    if input_list is None:
        return table

    for new_item in range(len(input_list)):
        if input_list[new_item]:
            table[index][new_item+1] = input_list[new_item]

    return table


# special functions:
# ------------------

# the question: What is the id of the item that was sold for the lowest price ?
# return type: string (id)
# if there are more than one with the lowest price, return the first by descending alphabetical order
def get_lowest_price_item_id(table):

    prices = [(line[ID], line[TITLE], int(line[PRICE])) for line in table]
    min_price = min(prices, key=itemgetter(2))[2]
    min_price_items = [(item[ID], item[TITLE], item[PRICE]) for item in prices if item[2] == min_price]
    # IMPORTANT NOTE: Assignment not clear on whether we should take the alpha-order of IDs or titles.
    return common.qsort(min_price_items, key=itemgetter(1), reversed=True)[0][ID]


# the question: Which items are sold between two given dates ? (from_date < sale_date < to_date)
# return type: list of lists (the filtered table)
def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):

    min_date = datetime(int(year_from), int(month_from), int(day_from))
    max_date = datetime(int(year_to), int(month_to), int(day_to))

    return [line for line in table if min_date < datetime(int(line[YEAR]), int(line[MONTH]), int(line[DAY])) < max_date]
