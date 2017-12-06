"""
Logistics module. Data structure:
1. ID of order
2. Name of ordered item
3. Amount of ordered item
4. Unit price of ordered item
5. Retailer of ordered item
6-8. Date when item is due to arrive
"""

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
    """Starts the module and displays its menu."""

    options = ["Show Table",
               "Add Entry",
               "Update Entry",
               "Remove Entry",
               "Show Payment Total Per Retailers",
               "Date Ordered List of Arrivals"]

    logistics_file = "logistics/orders.csv"
    order_data = data_manager.get_table_from_file(logistics_file)
    ui.clear_scr()

    while True:
        try:
            ui.print_menu("Logistics Department: Main menu", options, "Back to main menu")
            option = ui.valid_in("Please enter a number: ", common.validate_string)

            if option == "1":
                show_table(order_data)
            elif option == "2":
                menuaction_add(order_data)
            elif option == "3":
                menuaction_update(order_data)
            elif option == "4":
                menuaction_remove(order_data)
            elif option == "5":
                menuaction_payment_total_per_retailers(order_data)
            elif option == "6":
                menuaction_date_ordered_list_of_arrivals(order_data)
            elif option == "0":
                data_manager.write_table_to_file(logistics_file, order_data)
                ui.clear_scr()
                break
            else:
                ui.clear_scr()
        except (KeyboardInterrupt, EOFError):
            common.handle_kb_interrupt(logistics_file, order_data)


def menuaction_add(order_data):
    add(order_data)
    ui.clear_scr()


def menuaction_update(order_data):
    to_update = ui.valid_in(
        "What is the ID of the entry that you would like to update? ", common.validate_string)
    update(order_data, to_update)
    ui.clear_scr()


def menuaction_remove(order_data):
    to_remove = ui.valid_in(
        "What is the ID of the entry that you would like to remove? ", common.validate_string)
    remove(order_data, to_remove)
    ui.clear_scr()


def menuaction_payment_total_per_retailers(order_data):
    ui.clear_scr()
    payments = [item for item in get_price_total_per_retailer(order_data).items()]
    ui.print_result("Payments due for individual retailers:")
    ui.print_table(payments, ["Retailer", "Total Payment"])


def menuaction_date_ordered_list_of_arrivals(order_data):
    ui.clear_scr()
    ui.print_result("Payments due in a timely order:")
    ui.print_table(date_ordered_payments(order_data),
                   ["ID", "Title", "Amount", "Price per Item", "Retailer", "Date"])


def show_table(table):
    """Display the table given as parameter."""
    titles = ["ID", "Title", "Amount", "Price per Item", "Retailer", "Date"]
    output_table = [[row[ID], row[TITLE], row[AMOUNT], row[PRICE], row[RETAILER],
                     '/'.join((row[YEAR], row[MONTH], row[DAY]))] for row in table]
    ui.clear_scr()
    ui.print_table(output_table, titles)


def add(table):
    """Asks user for input and adds it to the table. Returns table with the new record."""
    return common.add_line(table, [("Title: ", common.validate_string),
                                   ("Amount: ", common.validate_int),
                                   ("Price per Item: ", common.validate_int),
                                   ("Retailer: ", common.validate_string),
                                   ("Year of arrival: ", common.validate_fyear),
                                   ("Month of arrival: ", common.validate_month),
                                   ("Day of arrival: ", common.validate_day)
                                   ])


def remove(table, id_):
    """Remove a record with a given id from the table. Returns table without the specified record."""
    return common.remove_line(table, id_)


def update(table, id_):
    """Updates specified record in the table. Asks users for new data. Returns table with the updated record."""
    return common.update_line(table, id_, [("Title: ", None),
                                           ("Amount: ", common.validate_int),
                                           ("Price per Item: ", common.validate_int),
                                           ("Retailer: ", common.validate_string),
                                           ("Year of arrival: ", common.validate_fyear),
                                           ("Month of arrival: ", common.validate_month),
                                           ("Day of arrival: ", common.validate_day)
                                           ])


def get_price_total_per_retailer(table):
    """Returns a dictionary with retailers as keys and their due payments added up as values."""

    r_payments = {}

    for retailer in {line[RETAILER] for line in table}:
        sm = common.szum_list([int(line[PRICE]) * int(line[AMOUNT]) for line in table if line[RETAILER] == retailer])
        r_payments[retailer] = sm

    return r_payments


def date_ordered_payments(table):
    """Orders items based on their arrival dates. Returns a list of lists."""

    temp_table = [[line[ID], line[TITLE], line[AMOUNT], line[PRICE], line[RETAILER],
                   common.dtime(line[YEAR], line[MONTH], line[DAY])] for line in table]
    return common.srt(temp_table, key=common.get_item(5))
