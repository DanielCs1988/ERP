"""
Sales module. Data structure:
1. ID of sale
2. Name of sold item
3. Price of sold item
4-6. Date when the item was sold
"""
# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# price: number (the actual sale price in $)
# month: number
# day: number
# year: number
# month,year and day combined gives the date the sale was made
# customer_id: string, id from the crm

import os
import ui
import data_manager
import common
from crm import crm

ID = 0
TITLE = 1
PRICE = 2
MONTH = 3
DAY = 4
YEAR = 5
CUSTOMER_ID = 6


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
               "Show Lowest Price ID",
               "Show Sold Items Between Dates",
               "Show Sale Number per Customer Name",
               "Sum of prices",
               "Get id of latest sold",
               "Get title of latest sold",
               "All customer IDs",
               "All sales for customers"]

    sales_file = "sales/sales.csv"
    sales_data = data_manager.get_table_from_file(sales_file)
    ui.clear_scr()

    while True:
        try:
            ui.print_menu("Sales Department: Main menu", options, "Back to main menu")
            option = ui.valid_in("Please enter a number: ", common.validate_string)

            if option == "1":
                show_table(sales_data)
            elif option == "2":
                sales_data = add(sales_data)
                ui.clear_scr()
            elif option == "3":
                to_update = ui.valid_in(
                    "What is the ID of the entry that you would like to update? ", common.validate_string)
                sales_data = update(sales_data, to_update)
                ui.clear_scr()
            elif option == "4":
                to_remove = ui.valid_in(
                    "What is the ID of the entry that you would like to remove? ", common.validate_string)
                sales_data = remove(sales_data, to_remove)
                ui.clear_scr()
            elif option == "5":
                ui.clear_scr()
                ui.print_result(get_lowest_price_item_id(sales_data), "ID of the item with the lowest price: ")
            elif option == "6":
                ui.clear_scr()
                params = ui.mass_valid_in([("Month from:", common.validate_month),
                                        ("Day from: ", common.validate_day),
                                        ("Year from: ", common.validate_byear),
                                        ("Month to:", common.validate_month),
                                        ("Day to: ", common.validate_day),
                                        ("Year to: ", common.validate_byear)
                                        ])
                if params:
                    show_table(get_items_sold_between(sales_data, *params))
                    ui.print_result("Table: items sold between specified dates")
                else:
                    ui.print_result("No items found between specified dates.")
            elif option == "7":
                ui.clear_scr()
                ui.print_table(get_num_of_sales_per_customer_names_from_table(
                    sales_data), ["Customer ID", "Total Number of Sales"])
            elif option == "8":
                show_table(sales_data)
                ui.print_result("Please enter item IDs. Press Enter (with empty input) to finish.")
                item_ids = []
                while True:
                    new_id = ui.valid_in("ID:", lambda inp: common.id_exists(sales_data, inp), True)
                    if not new_id or new_id == "__exit__":
                        break
                    item_ids.append(new_id)

                if len(item_ids) > 0:
                    sum_prices = get_the_sum_of_prices_from_table(sales_data, item_ids)
                    ui.print_result("Sum of prices: {}".format(sum_prices))
            elif option == "9":
                ui.print_result(get_item_id_sold_last_from_table(sales_data))
            elif option == "10":
                ui.print_result(get_item_title_sold_last_from_table(sales_data))
            elif option == "11":
                ui.clear_scr()
                ui.print_result("List of customer IDs:")
                ui.print_result(get_all_customer_ids_from_table(sales_data))
            elif option == "12":
                ui.clear_scr()
                ui.print_result("Sales for customers")
                sales_for_customers = get_all_sales_ids_for_customer_ids_form_table(sales_data).items()
                sales_for_customers = list({row[0]: ", ".join(row[1]) for row in sales_for_customers}.items())
                ui.print_table(sales_for_customers, ["Customer ID", "Sales IDs"])
            elif option == "0":
                data_manager.write_table_to_file(sales_file, sales_data)
                ui.clear_scr()
                break
            else:
                ui.clear_scr()
        except (KeyboardInterrupt, EOFError):
                common.handle_kb_interrupt(sales_file, sales_data)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    titles = ["ID", "Title", "Price", "Date", "Customer ID"]
    output_table = [[row[ID], row[TITLE], row[PRICE],
                     '/'.join((str(row[YEAR]), str(row[MONTH]), str(row[DAY]))), row[CUSTOMER_ID]] for row in table]
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
    return common.add_line(table, [("Title: ", common.validate_string),
                                   ("Price: ", common.validate_int),
                                   ("Month of sale: ", common.validate_month),
                                   ("Day of sale: ", common.validate_date),
                                   ("Year of sale: ", common.validate_byear),
                                   ("Customer ID: ", common.validate_id_possible)])


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
    return common.update_line(table, id_, [("Title: ", None),
                                           ("Price: ", common.validate_int),
                                           ("Month of sale: ", common.validate_month),
                                           ("Day of sale: ", common.validate_day),
                                           ("Year of sale: ", common.validate_byear),
                                           ("Customer ID: ", common.validate_id_possible)])


def get_lowest_price_item_id(table):
    """Returns the ID of the item that was sold for the lowest price.
       If there are more than one with the lowest price, return the first by descending alphabetical order."""

    prices = [(line[ID], line[TITLE], int(line[PRICE])) for line in table]
    min_price = min(prices, key=common.get_item(2))[2]
    min_price_items = [(item[ID], item[TITLE], item[PRICE]) for item in prices if item[2] == min_price]

    return common.srt(min_price_items, key=common.get_item(1), reversed=True)[0][ID]


def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """Returns a list of sold items (as lists) between the given date boundaries."""

    min_date = common.dtime(year_from, month_from, day_from)
    max_date = common.dtime(year_to, month_to, day_to)

    return [[line[ID], line[TITLE], int(line[PRICE]), int(line[MONTH]), int(line[DAY]), int(line[YEAR])]
            for line in table if min_date < common.dtime(line[YEAR], line[MONTH], line[DAY]) < max_date]


# functions supports data abalyser
# --------------------------------


def get_title_by_id(id):
    """
    Reads the table with the help of the data_manager module.
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the item

    Returns:
        str the title of the item
    """

    sales_data = data_manager.get_table_from_file("sales/sales.csv")
    for line in sales_data:
        if line[ID] == id:
            return line[TITLE]
    return None


def get_title_by_id_from_table(table, id):
    """
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the sales table
        id (str): the id of the item

    Returns:
        str the title of the item
    """

    for line in sales_data:
        if line[ID] == id:
            return line[TITLE]
    return None


def get_item_id_sold_last():
    """
    Reads the table with the help of the data_manager module.
    Returns the _id_ of the item that was sold most recently.

    Returns:
        (str) the _id_ of the item that was sold most recently.
    """
    return common.get_last_by_date(data_manager.get_table_from_file("sales/sales.csv"), YEAR, MONTH, DAY)[0]


def get_item_id_sold_last_from_table(table):
    """
    Returns the _id_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        (str) the _id_ of the item that was sold most recently.
    """
    return common.get_last_by_date(table, YEAR, MONTH, DAY)[0]


def get_item_title_sold_last_from_table(table):
    """
    Returns the _title_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        (str) the _title_ of the item that was sold most recently.
    """
    return common.get_last_by_date(table, YEAR, MONTH, DAY)[1]


def get_the_sum_of_prices(item_ids):
    """
    Reads the table of sales with the help of the data_manager module.
    Returns the sum of the prices of the items in the item_ids.

    Args:
        item_ids (list of str): the ids

    Returns:
        (number) the sum of the items' prices
    """

    table = data_manager.get_table_from_file("sales/sales.csv")
    return get_the_sum_of_prices_from_table(table, item_ids)


def get_the_sum_of_prices_from_table(table, item_ids):
    """
    Returns the sum of the prices of the items in the item_ids.

    Args:
        table (list of lists): the sales table
        item_ids (list of str): the ids

    Returns:
        (number) the sum of the items' prices
    """
    return common.szum(table, PRICE, lambda row: row[ID] in item_ids)


def get_customer_id_by_sale_id(sale_id):
    """
    Reads the sales table with the help of the data_manager module.
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.
    Args:
         sale_id (str): sale id to search for
    Returns:
         customer_id that belongs to the given sale id
    """
    sales_data = data_manager.get_table_from_file("sales/sales.csv")
    return get_customer_id_by_sale_id_from_table(sales_data, sale_id)


def get_customer_id_by_sale_id_from_table(table, sale_id):
    """
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.
    Args:
        table: table to remove a record from
        sale_id (str): sale id to search for
    Returns:
         customer_id that belongs to the given sale id
    """
    for row in table:
        if row[ID] == sale_id:
            return row[CUSTOMER_ID]
    return None


def get_all_customer_ids():
    """
    Reads the sales table with the help of the data_manager module.
    Returns a set of customer_ids that are present in the table.
    Returns:
         set of customer_ids that are present in the table
    """

    table = data_manager.get_table_from_file("sales/sales.csv")
    return get_all_customer_ids_from_table(table)


def get_all_customer_ids_from_table(table):
    """
    Returns a set of customer_ids that are present in the table.
    Args:
        table (list of list): the sales table
    Returns:
         set of customer_ids that are present in the table
    """

    return {row[CUSTOMER_ID] for row in table}


def get_all_sales_ids_for_customer_ids():
    """
    Reads the customer-sales association table with the help of the data_manager module.
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)
    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
         all the sales id belong to the given customer_id
    """

    table = data_manager.get_table_from_file("sales/sales.csv")
    return get_all_sales_ids_for_customer_ids_form_table(table)


def get_all_sales_ids_for_customer_ids_form_table(table):
    """
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)
    Args:
        table (list of list): the sales table
    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
         all the sales id belong to the given customer_id
    """

    customer_ids = get_all_customer_ids_from_table(table)
    return {customer_id: [row[ID] for row in table if row[CUSTOMER_ID] == customer_id] for customer_id in customer_ids}


def get_num_of_sales_per_customer_ids():
    """
     Reads the customer-sales association table with the help of the data_manager module.
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """
    sales_data = data_manager.get_table_from_file("sales/sales.csv")
    return get_num_of_sales_per_customer_ids_from_table(sales_data)


def get_num_of_sales_per_customer_ids_from_table(table):
    """
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Args:
        table (list of list): the sales table
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """
    sales_per_customers = {}
    for row in table:
        if row[CUSTOMER_ID] not in sales_per_customers:
            sales_per_customers[row[CUSTOMER_ID]] = 1
        else:
            sales_per_customers[row[CUSTOMER_ID]] += 1
    return sales_per_customers


def get_num_of_sales_per_customer_names_from_table(table):
    """
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Args:
        table (list of list): the sales table
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """
    sales_per_customers = {}
    for row in table:
        customer_name = crm.get_name_by_id(row[CUSTOMER_ID])
        if customer_name not in sales_per_customers:
            sales_per_customers[customer_name] = 1
        else:
            sales_per_customers[customer_name] += 1
    return sales_per_customers


def get_sum_of_sales_per_customer():
    sales_data = data_manager.get_table_from_file("sales/sales.csv")
    return get_sum_of_sales_per_customer_from_table(sales_data)


def get_sum_of_sales_per_customer_from_table(table):
    summed_sales_per_customer = {}
    for customer in {line[CUSTOMER_ID] for line in table}:
        sum_of_sales = common.szum_list([line[PRICE] for line in table if line[CUSTOMER_ID] == customer])
        summed_sales_per_customer[customer] = sum_of_sales
    return summed_sales_per_customer


def get_num_of_sales_per_customer_names():
    """
     Reads the customer-sales association table with the help of the data_manager module.
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """
    sales_data = data_manager.get_table_from_file("sales/sales.csv")
    return get_num_of_sales_per_customer_names_from_table(sales_data)
