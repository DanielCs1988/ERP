from random import choice
import ui
import data_manager

CHR_TYPES = {"uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
             "lowercase": "abcdefghijklmnopqrstuvwxyz",
             "digit": "0123456789",
             "symbol": "!@#$%^&*()?"
             }

CURRENT_YEAR = 2017


def random_char(chr_type):
    '''Generates a random character based on dictionary key given in the parameter.'''
    return choice(CHR_TYPES[chr_type])


def index_of(item, in_list):
    '''
    Finds the index of the item parameter in the list.

    Args:
        item: the item to find in the list

        in_list: the list to find it in
    Returns:
        The index of item in list, or -1 if not found.
    '''
    for index in range(len(in_list)):
        if in_list[index] == item:
            return index
    return -1


def id_exists(table, id_to_find):
    """
    Checks if an id already exists in the table.

    Args:
        table: a data table (list of lists)

        id_to_find: The id to find. It is assumed that the first column contains the ID.
    Returns:
        True, if the ID is found in the table. False if not.
    """
    return id_to_find in [row[0] for row in table]


def index_of_value(table, col, value):
    '''
    Finds the index of a specific value in a specific column.

    Args:
        table: a list in a list

        col: the column to check

        value: the value it needs to find

    Returns:
        The index of the value, or -1 if not found.
    '''
    for index in range(len(table)):
        if table[index][col] == value:
            return index

    return -1


def index_of_id(table, id_to_find):
    '''
    Finds the index of the id in a table.

    Args:
        table: a list in a list

        id_to_find: the value it needs to find

    Returns:
        The index of the id, or -1 if not found.
    '''
    return index_of_value(table, 0, id_to_find)


def qsort_table(table, col, **kwargs):
    """
    Sorts a table based on the value of one of its columns.

    Args:
        table: The table to sort.

        col: The index of the column.

        kwargs: Keyword arguments. Accepts "key" and "reversed", just like the default qsort function.\
            Note that the value passed to the key function will be the value of the given cell (row, column)\
            of the table.
    """
    return srt(table,
               key=lambda row: kwargs["key"](row[col]) if "key" in kwargs else row[col],
               reversed=True if "reversed" in kwargs and kwargs["reversed"] else False)


def deepcopy(array):
    """
    Our humble imitation of deepcopy.
    """
    retval = []
    for item in array:
        if isinstance(item, (list, set)):
            retval.append(deepcopy(item))
        else:
            retval.append(item)

    return retval


def srt(array, **kwargs):
    """
    Sorts the array using the Quicksort algorithm (with Hoare partition scheme). \
    The original array will not be modified.

    Args:
        array: The array to sort.
        kwargs: The keyword argument "key" can be used to specify a key function. \
            The boolean value "reversed" can be used to get a reverse-ordered list.

    Returns:
        The sorted array (list).
    """
    array_copy = deepcopy(array)

    key = kwargs["key"] if "key" in kwargs else None

    __qsrt(array_copy, 0, len(array) - 1, key)

    return array_copy if not ("reversed" in kwargs and kwargs["reversed"]) else array_copy[::-1]


def __qsrt(array, lo, hi, key):
    """The core qsort algorithm, see https://en.wikipedia.org/wiki/Quicksort#Algorithm"""
    if lo < hi:
        p = __qsrt_partition(array, lo, hi, key)
        __qsrt(array, lo, p, key)
        __qsrt(array, p + 1, hi, key)


def __qsrt_keyed_value(value, key):
    """Helper function to key values if needed."""
    return key(value) if key else value


def __qsrt_partition(array, lo, hi, key):
    """Hoare partition scheme, see https://en.wikipedia.org/wiki/Quicksort#Hoare_partition_scheme"""
    pivot = array[lo]
    i = lo - 1
    j = hi + 1
    while True:

        while True:
            i = i + 1
            if not __qsrt_keyed_value(array[i], key) < __qsrt_keyed_value(pivot, key):
                break

        while True:
            j = j - 1
            if not __qsrt_keyed_value(array[j], key) > __qsrt_keyed_value(pivot, key):
                break

        if i >= j:
            return j

        temp = array[i]
        array[i] = array[j]
        array[j] = temp


def get_longest(table, column):
    """
    Returns the length of the longest item in a given column as integer.

    Args:

    """
    return max([len(str(row[column])) for row in table])


def szum(table, column, condition=None):
    """ Returns the sum of the data of the given column.

    Args:
        table: a list in a list

        column: the column, that will be summed.

    Returns:
        the sum of the values, integer type
    """
    return szum_list([row[column] for row in table if condition is None or condition(row)])


def szum_list(collection):
    '''
    A very basic replacement for summary function.
    Crashes if any list item is not an integer.

    Args:
        a list of integers and/or floats

    Returns:
        the sum of the values, integer type
    '''
    summary = 0

    for item in collection:
        summary += int(item)

    return summary


def generate_random(table):
    """
    Generates a random ID with a length of 8.
    It contains 2 numbers, 2 special characters, 2 lower- and 2 uppercase letters in random order.

    Args:
        table
    """
    while True:
        hat = ["uppercase", "lowercase", "digit", "symbol"] * 2
        temp_str = ""
        for i in range(8):
            hchoice = choice(hat)
            temp_str += random_char(hchoice)
            del hat[index_of(hchoice, hat)]
        if id_exists(table, temp_str):
            continue
        return temp_str


def validate_byear(year):
    "Check if parameter is an integer and whether it's less or equal to the current year."

    if not validate_int(year):
        return False
    if int(year) > CURRENT_YEAR:
        return False
    return True


def validate_fyear(year):
    "Check if parameter is integer and whether it's more or equal to the current year."

    if not validate_int(year):
        return False
    if int(year) < CURRENT_YEAR:
        return False
    return True


def validate_type(tp):
    """Check if parameter is 'in' or 'out', returns false otherwise."""

    if tp not in ("in", "out"):
        return False
    return True


def validate_boolean(boolean):
    """Check if parameter is 1 or 0, returns false otherwise."""

    if not validate_int(boolean):
        return False
    if int(boolean) not in (0, 1):
        return False
    return True


def validate_month(month):
    """Check if parameter is a valid month by number (1-12), returns false otherwise."""

    if not validate_int(month):
        return False
    if not (0 < int(month) < 13):
        return False
    return True


def validate_day(day):
    """
    Check if parameter is a valid day by number (1-31), returns false otherwise
    Does not differentiate between months, so february 31 is possible.
    """

    if not validate_int(day):
        return False
    if not (0 < int(day) < 32):
        return False
    return True


def validate_email(email):
    '''
    Validates e-mail address using.
    Args:
        email: The email address to validate.

    Returns:
        True, if email is a valid email address
    '''
    is_valid = True

    at_index = index_of("@", email)

    if at_index == 0 or at_index < 0 or at_index == len(email) - 1:
        return False
    if len([char for char in email if char == "@"]) > 1:
        return False

    email_split = email.split("@")
    dot_index = index_of(".", email_split[1])

    if dot_index == 0 or dot_index < 0 or dot_index == len(email_split[1]) - 1:
        return False

    return is_valid


def validate_int(integer):
    '''
    Checks if the parameter is a valid integer, returns false otherwise.
    '''
    try:
        integer = int(integer)
    except ValueError:
        return False
    return True


def validate_empty(userinput):
    '''
    Checks if the given parameter is an empty string. If so, returns true.
    '''
    if userinput is '':
        return True
    return False


def validate_id_possible(userinput):
    '''
    Validates if it is a proper id.
    Does not check if it exists anywhere
    '''
    valid = {"upper": 0, "lower": 0, "digit": 0, "symbol": 0}
    for char in userinput:
        if char in CHR_TYPES["uppercase"]:
            valid["upper"] += 1
        elif char in CHR_TYPES["lowercase"]:
            valid["lower"] += 1
        elif char in CHR_TYPES["digit"]:
            valid["digit"] += 1
        elif char in CHR_TYPES["symbol"]:
            valid["symbol"] += 1
    if 0 not in valid.values() and 1 not in valid.values():
        return True
    return False


# def handle_interrupt_alt():
#    """
#    Requires load_table as well.
#    """
#    ui.print_error_message('''\nKeyboard interrupt.\n\nYou will lose all changes.''')
#    while True:
#        decision = ui.get_inputs(["Are you sure you want to quit without saving?.(Y/N)"], "")[0]
#        if decision in ['Y', 'y']:
#            break
#        elif decision in ['N', 'n']:
#            start_module(table_cont=table)
#            break


def load_data(module_name, table_continue=None):
    '''
    Loads data from the module's file. Used with handle_interrupt_alt.
    If table is given, uses that instead.
    '''
    ui.clear_scr()
    data = (table_continue if table_continue else "{0}/items.csv".format(module_name.lower()))


def trial_version(menu_options, characters):
    '''
    Displays a different set of menu options if the random chance succeds.
    Chooses a random character from uppercase list,
    the chance will depend on the characters argument. (string or list)
    '''
    if common.random_char("uppercase") in characters:
        menu_options = menu_options[:4]
        menu_options.append("Buy the full version of the software to unlock more options")


def handle_kb_interrupt(filename=None, table_to_save=None):
    """
    Handles keyboard interrupt exceptions. Display a message to the user, save the current module's data \
        and exits the program.

    Args:
        table_to_save: The data table to save.
        filename: The file name where the table is saved.

    Returns:
        None
    """
    ui.clear_scr()
    if filename and table_to_save:
        data_manager.write_table_to_file(filename, table_to_save)
    ui.print_error_message("Keyboard interrupt. If you want to got back to main menu, use the menu.")
    exit()


def remove_line(table, id):
    """Takes the table given as a parameter, seeks the line with the given ID and removes it."""

    index = index_of_id(table, id)
    if index == -1:
        ui.print_error_message("Wrong ID!")
        return table

    del table[index]
    return table


def add_line(table, input_specifiers):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to
        input_specifiers (list of tuples): A list of tuples containing request message-validator function pairs. \
            Passed to ui.mass_valid_input.

    Returns:
        Table with a new record
    """

    new_item = [generate_random(table)]

    user_input = ui.mass_valid_in(input_specifiers)

    if user_input is None:
        return table

    new_item.extend(user_input)

    table.append(new_item)

    return table


def update_line(table, id_, input_specifiers):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
        id_ (str): id of a record to update
        input_specifiers (list of tuples): A list of tuples containing request message-validator function pairs. \
            Passed to ui.mass_valid_input.

    Returns:
        table with updated record
    """
    index = index_of_id(table, id_)
    if index < 0:
        ui.print_error_message("Invalid ID: {}.".format(id_))
        return table

    user_input = ui.mass_valid_in(input_specifiers, True)

    apply_update_to_line(table[index], user_input)

    return table


def apply_update_to_line(original_line, user_input):
    """
    Applies data received from mass_valid_update to the original table line.
    Don't add the original ID to user_input.
    """
    if user_input is None:
        return original_line

    for col_idx in range(len(user_input)):
        if user_input[col_idx]:
            original_line[col_idx + 1] = user_input[col_idx]
        # col_idx + 1 because the first item is always the ID that is not changed

    return original_line


def validate_string(text):
    '''
    Checks if the given parameter is an empty string. If so, returns false.
    '''
    if text == "":
        return False
    return True


def get_item(index):
    '''
    Our own original idea that has absolutely nothing to do with itemgetter.

    © 2017 Enterprise Coffe Planner All Rights Reserved
    '''
    def func(row):
        return row[index]
    return func


def get_last_by_date(table, year, month, day, reverse=False):
    '''
    Gets the newest or oldest entry or entries.

    Args:
        table
        year, month and day: the numbers (constant) of the columns
        reverse: if true, gives the newest entry instead

    Returns:
        the row in that table
    '''
    DAYS_SUMMED = 7
    new_table = deepcopy(table)
    for row in new_table:
        row.append(str(int(row[year]) * 365 + int(row[month]) * 31 + int(row[day])))
    return qsort_table(new_table, DAYS_SUMMED, reversed=not reverse)[0]


class dtime:
    """A lightweight date management class."""
    def __init__(self, year, month, day):
        if not validate_int(year):
            raise ValueError("Invalid year parameter!")
        if not validate_month(month):
            raise ValueError("Invalid month parameter!")
        if not validate_day(day):
            raise ValueError("Invalid day parameter!")

        self.year = int(year)
        self.month = int(month)
        self.day = int(day)

    def __repr__(self):
        return "{}/{}/{}".format(self.year, self.month, self.day)

    def __eq__(self, other):
        if not isinstance(other, dtime):
            raise TypeError("Can only compare dtime object to other dtime objects!")
        if self.year == other.year and self.month == other.month and self.day == other.day:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if not isinstance(other, dtime):
            raise TypeError("Can only compare dtime object to other dtime objects!")
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
            elif self.month == other.month:
                if self.day > other.day:
                    return True
        return False

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        return not self >= other

    def __len__(self):
        return len(str(self))

    def __format__(self, f_arg):
        return str(self).__format__(f_arg)
