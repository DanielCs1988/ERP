import sys
import os
import ui

from store import store
from hr import hr
from inventory import inventory
from accounting import accounting
from sales import sales
from crm import crm
from logistics import logistics
from data_analyser import data_analyser


def choose():
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    if option == "1":
        store.start_module()
    elif option == "2":
        hr.start_module()
    elif option == "3":
        inventory.start_module()
    elif option == "4":
        accounting.start_module()
    elif option == "5":
        sales.start_module()
    elif option == "6":
        crm.start_module()
    elif option == "7":
        logistics.start_module()
    elif option == "8":
        data_analyser.start_module()
    elif option == "0":
        sys.exit(0)
    else:
        raise KeyError("There is no such option.")


def handle_menu():
    options = ["Store manager",
               "Human resources manager",
               "Inventory manager",
               "Accounting manager",
               "Sales manager",
               "Customer Relationship Management (CRM)",
               "Logistics manager",
               "Data analyzer"
               ]

    ui.print_menu("Main menu", options, "Exit program")


def main():
    while True:
        handle_menu()
        try:
            choose()
        except KeyError as err:
            ui.print_error_message(err)


if __name__ == '__main__':
    main()
