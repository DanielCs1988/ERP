# This module creates reports for marketing department.
# This module can run independently from other modules.
# Has no own datastructure but uses other modules.
# Avoud using the database (ie. .csv files) of other modules directly.
# Use the functions of the modules instead.

# todo: importing everything you need

# importing everything you need
import os
import ui
import common
from sales import sales
from crm import crm

NAME = 0
MONEY = 1


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """
    options = ["Show Last Buyer's ID",
               "Show Last Buyer's Name",
               "Show ID and Spendings of Person Who Paid the Most",
               "Show Name and Spendings of Person Who Paid the Most",
               "Show Most Frequent Buyer's ID",
               "Show Most Frequent Buyer's Name",
               "Show Idle Customers"]
    ui.clear_scr()

    while True:
        ui.print_menu("Data Analyser: Main menu", options, "Back to main menu")
        try:
            option = ui.valid_in("Please enter a number: ", common.validate_string)
        except (KeyboardInterrupt, EOFError):
            ui.clear_scr()
            exit()

        if option == "1":
            ui.print_result(get_the_last_buyer_id())
        elif option == "2":
            ui.print_result(get_the_last_buyer_name())
        elif option == "3":
            ui.print_result(get_the_buyer_id_spent_most_and_the_money_spent())
        elif option == "4":
            ui.print_result(get_the_buyer_name_spent_most_and_the_money_spent())
        elif option == "5":
            num = int(ui.valid_in("How many of the top customers would you like to see? ", common.validate_int))
            ui.print_table(get_the_most_frequent_buyers_ids(num), ["Customer ID", "Number of Sales"])
        elif option == "6":
            num = int(ui.valid_in("How many of the top customers would you like to see? ", common.validate_int))
            ui.print_table(get_the_most_frequent_buyers_names(num), ["Customer Name", "Number of Sales"])
        elif option == "7":
            ui.print_table(get_idle_customers(), ["Name", "ID"])
        elif option == "0":
            ui.clear_scr()
            break
        else:
            ui.clear_scr()


def get_the_last_buyer_name():
    """
    Returns the customer _name_ of the customer made sale last.

    Returns:
        Customer name of the last buyer
    """

    # your code

    pass


def get_the_last_buyer_id():
    """
    Returns the customer _id_ of the customer made sale last.

    Returns:
        Customer id of the last buyer
    """

    # your code

    pass


def get_the_buyer_name_spent_most_and_the_money_spent():
    """
    Returns the customer's _name_ who spent the most in sum and the money (s)he spent.
    Returns a tuple of customer name and the sum the customer spent.
    eg.: (aH34Jq#&, 42)

   Returns:
        Tuple of customer name and the sum the customer spent
    """
    customer_sales = sales.get_sum_of_sales_per_customer().items()
    most_spent_customer = max(customer_sales, key=common.get_item(1))
    return crm.get_name_by_id(most_spent_customer[NAME]), most_spent_customer[MONEY]


def get_the_buyer_id_spent_most_and_the_money_spent():
    """
    Returns the customer's _id_ who spent more in sum and the money (s)he spent.
    Returns a tuple of customer id and the sum the customer spent.
    eg.: (aH34Jq#&, 42)

   Returns:
        Tuple of customer id and the sum the customer spent
    """

    customer_sales = sales.get_sum_of_sales_per_customer().items()
    return max(customer_sales, key=common.get_item(1))


def get_the_most_frequent_buyers_names(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customers' name) who bought most frequently.
    Returns an ordered list of tuples of customer names and the number of their sales.
    (The first one bought the most frequent.)
    eg.: [(aH34Jq#&, 8), (bH34Jq#&, 3)]

    Args:
        num: the number of the customers to return.

    Returns:
        Ordered list of tuples of customer names and num of sales
    """
    buy_frequencies = sales.get_num_of_sales_per_customer_names()
    buy_frequencies = common.srt(buy_frequencies.items(), key=common.get_item(1), reversed=True)
    return buy_frequencies[:num]


def get_the_most_frequent_buyers_ids(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customer ids of them) who bought more frequent.
    Returns an ordered list of tuples of customer id and the number their sales.
    (The first one bought the most frequent.)
    eg.: [(aH34Jq#&, 8), (bH34Jq#&, 3)]

    Args:
        num: the number of the customers to return.

    Returns:
        Ordered list of tuples of customer ids and num of sales
    """
    buy_frequencies = sales.get_num_of_sales_per_customer_ids()
    buy_frequencies = common.srt(buy_frequencies.items(), key=common.get_item(1), reversed=True)
    return buy_frequencies[:num]


def get_idle_customers():
    all_customers = crm.get_all_customer_ids()
    paying_customers = sales.get_all_customer_ids()
    idle_customers = all_customers - paying_customers
    return common.srt([(crm.get_name_by_id(id), id) for id in idle_customers], key=common.get_item(0))
