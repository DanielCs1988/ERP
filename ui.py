from common import *
import platform
import os


def clear_scr():
    """
    Cross platform clear screen. 
    Source: https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# cross-platform getch https://gist.github.com/jfktrey/8928865
if platform.system() == "Windows":
    import msvcrt

    def getch():
        return msvcrt.getch()
else:
    import tty
    import termios
    import sys

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def print_table(table, title_list):
    """
    Prints table with data. Sample output:
        /-----------------------------------\
        |   id   |      title     |  type   |
        |--------|----------------|---------|
        |   0    | Counter strike |    fps  |
        |--------|----------------|---------|
        |   1    |       fo       |    fps  |
        \-----------------------------------/

    Args:
        table: list of lists - table to display
        title_list: list containing table headers

    Returns:
        This function doesn't return anything it only prints to console.
    """

    lenghts = [get_longest(table, column) for column in range(len(table[0]))]
    # gets the lengths of each column (in a list)
    for x in range(len(title_list)):
        if len(title_list[x]) > lenghts[x]:
            lenghts[x] = len(title_list[x])
        lenghts[x] += 4
    # if the title bar is longer, then it uses its lenght instead
    # then, it adds four to make it pretty
    table_width = sum(lenghts) + len(lenghts) - 1    # the lenght of the whole table

    print("/{0}\\".format("-"*table_width, end=""))    # the topmost row, which is just a graphic

    num = 0
    for item in title_list:    # this prints the title list
        print("|{:^{width}}".format(item, width=lenghts[num]), end="")
        num += 1
    print("|")

    for row in table:
        count = 0
        for item in row:    # this prints each divider row
            print("|{0}".format("-"*lenghts[count]), end="")
            count += 1
        print("|")    # end of row, also a new line
        count = 0
        for item in row:    # this prints each data row
            print("|{:^{width}}".format(item, width=lenghts[count]), end="")
            count += 1
        print("|")    # end of row, also a new line

    print("\\{0}/".format("-"*table_width, end=""))    # the bottommost row, which is just a graphic


def print_result(result, label=None):
    """
    Displays results of the special functions.

    Args:
        result: string, list or dictionary - result of the special function
        label: label of the result

    Returns:
        This function doesn't return anything it only prints to console.
    """

    if label:
        print("\n{}: ".format(label), end='')

    if isinstance(result, (list, set, tuple)):
        print(", ".join(result))
    elif isinstance(result, dict):
        print("\n"+"\n".join("{} = {}".format(name, value) for name, value in result.items()))
    else:
        print(result)


def print_menu(title, list_options, exit_message):
    """
    Displays a menu. Sample output:
        Main menu:
            (1) Store manager
            (2) Human resources manager
            (3) Inventory manager
            (4) Accounting manager
            (5) Sales manager
            (6) Customer relationship management (CRM)
            (0) Exit program

    Args:
        title (str): menu title
        list_options (list): list of strings - options that will be shown in menu
        exit_message (str): the last option with (0) (example: "Back to main menu")

    Returns:
        This function doesn't return anything it only prints to console.
    """

    print("{}:".format(title))
    for option in range(len(list_options)):
        print("\t({}) {}".format(option + 1, list_options[option]))
    print("\t(0) {}".format(exit_message))


def get_inputs(list_labels, title):
    """
    Gets list of inputs from the user.
    Sample call:
        get_inputs(["Name","Surname","Age"],"Please provide your personal information")
    Sample display:
        Please provide your personal information
        Name <user_input_1>
        Surname <user_input_2>
        Age <user_input_3>

    Args:
        list_labels: list of strings - labels of inputs;
        title: title of the "input section", the first line

    Returns:
        List of data given by the user. Sample return:
            [<user_input_1>, <user_input_2>, <user_input_3>]
    """
    print(title)
    return [input(label) for label in list_labels]


# This function displays an error message. (example: Error: @message)
#
# @message: string - the error message
def print_error_message(message):
    """
    Displays an error message

    Args:
        message(str): error message to be displayed

    Returns:
        This function doesn't return anything it only prints to console.
    """

    print('[\033[1;31m{}\033[1;m]'.format(message))
