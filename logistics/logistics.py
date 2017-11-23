# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# amount: number
# price: number (the actual sale price in $ per piece of item)
# retailer: string
# month: number
# day: number
# year: number
# month,year and day combined gives the date the item is due to arrive

import os
import ui
import data_manager
import common

ID = 0
TITLE = 1
AMOUNT = 2
PRICE = 3
RETAILER = 4
YEAR = 5
MONTH = 6
DAY = 7


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
               "Show Payment Total Per Retailers",
               "Date Ordered List of Arrivals"]

    order_data = data_manager.get_table_from_file("logistics/orders.csv")
    ui.clear_scr()

    while True:
        ui.print_menu("Logistics Department: Main menu", options, "Exit program")
        try:
            option = ui.valid_in("Please enter a number: ", common.validate_string)
        except (KeyboardInterrupt, EOFError):
            data_manager.write_table_to_file("logistics/orders.csv", order_data)
            ui.clear_scr()
            exit()

        if option == "1":
            show_table(order_data)
        elif option == "2":
            order_data = add(order_data)
            ui.clear_scr()
        elif option == "3":
            to_update = ui.valid_in(
                "What is the ID of the entry that you would like to update? ", common.validate_string)
            order_data = update(order_data, to_update)
            ui.clear_scr()
        elif option == "4":
            to_remove = ui.valid_in(
                "What is the ID of the entry that you would like to remove? ", common.validate_string)
            order_data = remove(order_data, to_remove)
            ui.clear_scr()
        elif option == "5":
            payments = [item for item in get_price_total_per_retailer(order_data).items()]
            ui.print_table(payments, ["Retailer", "Total Payment"])
        elif option == "6":
            ui.print_table(date_ordered_payments(order_data),
                           ["ID", "Title", "Amount", "Price per Item", "Retailer", "Date"])
        elif option == "0":
            data_manager.write_table_to_file("logistics/orders.csv", order_data)
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
    titles = ["ID", "Title", "Amount", "Price per Item", "Retailer", "Date"]
    output_table = [[row[ID], row[TITLE], row[AMOUNT], row[PRICE], row[RETAILER],
                     '/'.join((row[YEAR], row[MONTH], row[DAY]))] for row in table]
    ui.clear_scr()
    ui.print_table(output_table, titles)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """
    new_order = [common.generate_random(table)]

    input_list = ui.mass_valid_in([("Title: ", common.validate_string),
                                   ("Amount: ", common.validate_int),
                                   ("Price per Item: ", common.validate_int),
                                   ("Retailer: ", common.validate_string),
                                   ("Year of arrival: ", common.validate_byear),
                                   ("Month of arrival: ", common.validate_month),
                                   ("Day of arrival: ", common.validate_day)
                                   ])

    if input_list is None:
        return table

    new_order.extend(input_list)
    table.append(new_order)

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

    input_list = ui.mass_valid_in([("Title: ", None),
                                   ("Amount: ", common.validate_int),
                                   ("Price per Item: ", common.validate_int),
                                   ("Retailer: ", common.validate_string),
                                   ("Year of arrival: ", common.validate_byear),
                                   ("Month of arrival: ", common.validate_month),
                                   ("Day of arrival: ", common.validate_day)
                                   ], update_mode=True)

    table[index] = common.apply_update_to_line(table[index], input_list)
    return table


def get_price_total_per_retailer(table):

    r_payments = {}

    for retailer in {line[RETAILER] for line in table}:
        sm = common.szum_list([int(line[PRICE]) * int(line[AMOUNT]) for line in table if line[RETAILER] == retailer])
        r_payments[retailer] = sm

    return r_payments


def date_ordered_payments(table):

    temp_table = [[line[ID], line[TITLE], line[AMOUNT], line[PRICE], line[RETAILER],
                  common.dtime(line[YEAR], line[MONTH], line[DAY])] for line in table]
    return common.srt(temp_table, key=common.get_item(5))
