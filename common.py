from random import choice
import string
import copy
import inspect
import re
import ui

CHR_TYPES = {"uppercase": string.ascii_uppercase,
             "lowercase": string.ascii_lowercase,
             "digit": string.digits,
             "symbol": "!@#$%^&*()?",
             "char": string.ascii_letters
             }

CURRENT_YEAR = 2017


def random_char(chr_type):
    return choice(CHR_TYPES[chr_type])


def index_of(item, in_list):
    '''Finds the index of the item parameter in the list.'''
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

    for index in range(len(table)):
        if table[index][col] == value:
            return index

    return -1


def index_of_id(table, id_to_find):
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
    return qsort(table,
                 key=lambda row: kwargs["key"](row[col]) if "key" in kwargs and inspect.isfunction(
                     kwargs["key"]) else row[col],
                 reversed=True if "reversed" in kwargs and kwargs["reversed"] else False)


def qsort(array, **kwargs):
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
    array_copy = list(copy.deepcopy(array))

    key = kwargs["key"] if "key" in kwargs else None

    __qsort(array_copy, 0, len(array) - 1, key)

    return array_copy if not ("reversed" in kwargs and kwargs["reversed"]) else array_copy[::-1]


def __qsort(array, lo, hi, key):
    if lo < hi:
        p = __qsort_partition(array, lo, hi, key)
        __qsort(array, lo, p, key)
        __qsort(array, p + 1, hi, key)


def __qsort_keyed_value(value, key):
    return key(value) if inspect.isfunction(key) else value


def __qsort_partition(array, lo, hi, key):
    pivot = array[lo]
    i = lo - 1
    j = hi + 1
    while True:

        while True:
            i = i + 1
            if not __qsort_keyed_value(array[i], key) < __qsort_keyed_value(pivot, key):
                break

        while True:
            j = j - 1
            if not __qsort_keyed_value(array[j], key) > __qsort_keyed_value(pivot, key):
                break

        if i >= j:
            return j

        # swap A[i] with A[j]
        temp = array[i]
        array[i] = array[j]
        array[j] = temp


def get_longest(table, column):
    """Returns the length of the longest item in a given column as integer."""
    return max([len(str(row[column])) for row in table])


def get_sum(table, column):
    """ Returns the sum of the data of the given column."""
    return get_sum_list([row[column] for row in table])


def get_sum_list(collection):
    '''
    A very basic replacement for sum().

    Crashes if any list item is not an integer.

    Returns an integer.
    '''
    summary = 0

    for item in collection:
        summary += int(item)

    return summary


def generate_random(table):
    """Generates a random ID with a length of 8.
       It contains 2 number, 2 special, 2 lower- and 2 uppercase characters."""
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
    "Check if parameter is an integer and whether it's less or equal than the current year."

    if not validate_int(year):
        return False
    if int(year) > CURRENT_YEAR:
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
    Validates e-mail address using a simplified version of the RFC 5322 standard. \t
    cf. http://www.regular-expressions.info/email.html

    Args:
        email: The email address to validate.

    Returns:
        True, if email is a valid email address
    '''
    return re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email) is not None


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


def remove_line(table, id):
    """Takes the table given as a parameter, seeks the line with the given ID and removes it."""

    index = index_of_id(table, id)
    if index == -1:
        ui.print_error_message("Wrong ID!")
        return table

    del table[index]
    return table


def apply_update_to_line(original_line, user_input):
    """
    Applies data received from mass_valid_update to the original table line.
    """
    if user_input is None:
        return original_line

    for col_idx in range(len(user_input)):
        if user_input[col_idx]:
            original_line[col_idx + 1] = user_input[col_idx]
        # col_idx + 1 because the first item is always the ID that is not changed

    return original_line


def validate_string(text):
    if text == "":
        return False
    return True


def get_item(index):
    def func(row):
        return row[index]
    return func


class dtime:

    def __init__(self, year, month, day):
        if not validate_byear(year):
            raise ValueError("Invalid year parameter!")
        if not validate_month(month):
            raise ValueError("Invalid month parameter!")
        if not validate_day(day):
            raise ValueError("Invalid day parameter!")

        self.year = int(year)
        self.month = int(month)
        self.day = int(day)

    def __str__(self):
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
