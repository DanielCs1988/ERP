"""This module provides comprehensive information to answer complex queries using multiple other modules."""

import os
import ui
import common

from sales import sales
from crm import crm
from logistics import logistics

NAME = 0
MONEY = 1


def start_module():
    """"Starts the module and displays its menu."""

    options = ["Show Last Buyer's ID",
               "Show Last Buyer's Name",
               "Show ID and Spendings of Person Who Paid the Most",
               "Show Name and Spendings of Person Who Paid the Most",
               "Show Most Frequent Buyer's ID",
               "Show Most Frequent Buyer's Name",
               "Show Idle Customers",
               "Show Buyer E-mails",
               "Show Contacts for Earliest Arrivals",
               "Show Contact Information per Payment"]
    ui.clear_scr()

    while True:
        try:
            ui.print_menu("Data Analyser: Main menu", options, "Back to main menu")
            option = ui.valid_in("Please enter a number: ", common.validate_string)
            ui.clear_scr()

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
            elif option == '8':
                ui.print_table(get_buyer_emails(), ["Name", "E-mail"])
            elif option == '9':
                menuaction_earlist_arrival_contacts()
            elif option == '10':
                menuaction_most_expensive_orders()
            elif option == "0":
                break
            else:
                ui.clear_scr()

        except (KeyboardInterrupt, EOFError):
            common.handle_kb_interrupt()


def menuaction_earlist_arrival_contacts():
    num_earliest = max(1, int(ui.valid_in("Enter the number of entries to show:", ui.validate_int)))
    arrival_data = get_earliers_arrivals_contact_info(num_earliest)
    ui.print_table(arrival_data, ["Date", "Contact person", "Phone"])


def menuaction_most_expensive_orders():
    number_of_entries = max(1, int(ui.valid_in("Enter the number of entries to show:", ui.validate_int)))
    payments_data = get_most_expensive_orders_info(number_of_entries)
    ui.print_table(payments_data, ["Partner", "E-mail", "Bank Account Number", "Payments Due"])


def get_the_last_buyer_name():
    """Returns the name of the customer who made the last purchase."""
    sold_last = sales.get_item_id_sold_last()
    last_customer = sales.get_customer_id_by_sale_id(sold_last)
    return crm.get_name_by_id(last_customer)


def get_the_last_buyer_id():
    """Returns the ID of the customer who made the last purchase."""
    sold_last = sales.get_item_id_sold_last()
    last_customer = sales.get_customer_id_by_sale_id(sold_last)
    return last_customer


def get_the_buyer_name_spent_most_and_the_money_spent():
    """Returns the customer's name who spent the most in sum and the money (s)he spent as a tuple."""
    customer_sales = sales.get_sum_of_sales_per_customer().items()
    most_spent_customer = max(customer_sales, key=common.get_item(1))
    return crm.get_name_by_id(most_spent_customer[NAME]), most_spent_customer[MONEY]


def get_the_buyer_id_spent_most_and_the_money_spent():
    """Returns the customer's ID who spent the most in sum and the money (s)he spent as a tuple."""
    customer_sales = sales.get_sum_of_sales_per_customer().items()
    return max(customer_sales, key=common.get_item(1))


def get_the_most_frequent_buyers_names(num=1):
    """Returns an ordered (descending) list of tuples of customer IDs and the number of their sales."""
    buy_frequencies = sales.get_num_of_sales_per_customer_names()
    buy_frequencies = common.srt(buy_frequencies, key=common.get_item(1), reversed=True)
    return buy_frequencies[:num]


def get_the_most_frequent_buyers_ids(num=1):
    """Returns an ordered (descending) list of tuples of customer names and the number of their sales."""
    buy_frequencies = sales.get_num_of_sales_per_customer_ids()
    buy_frequencies = common.srt(buy_frequencies.items(), key=common.get_item(1), reversed=True)
    return buy_frequencies[:num]


def get_idle_customers():
    """Returns an ordered list of tuples of customer names and their IDs, with customers who have made no purchase."""
    all_customers = crm.get_all_customer_ids()
    paying_customers = sales.get_all_customer_ids()
    idle_customers = all_customers - paying_customers
    return common.srt([(crm.get_name_by_id(id), id) for id in idle_customers])


def get_buyer_emails():
    """Returns an abc ordered list of tuples with buying customer names and their e-mails."""
    return common.srt(list(sales.get_buyer_emails()))


def get_earliers_arrivals_contact_info(num=1):
    """Returns a list of tuples containing order arrival dates (ordered based on this parameter), 
       corresponding contact person names and phone numbers."""
    arrival_data = logistics.get__arrivals_contact_info()
    arrival_data = common.qsort_table(arrival_data, 0)

    return arrival_data if len(arrival_data) < num else arrival_data[:num]


def get_most_expensive_orders_info(num=1):
    """Returns a list of tuples containing partner names, e-mails,
       addresses and their relevant payment (due) information."""
    orders_data = logistics.get__payment_total_contacts()
    orders_data = common.qsort_table(orders_data, 3, reversed=True)

    return orders_data if len(orders_data) < num else orders_data[:num]
