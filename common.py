from random import choice
from datetime import datetime
import string
import copy
import inspect

CHR_TYPES = {"uppercase": string.ascii_uppercase,
             "lowercase": string.ascii_lowercase,
             "digit": string.digits,
             "symbol": "!@#$%^&*()?",
             "char": string.ascii_letters
             }


def random_char(chr_type):
    return choice(CHR_TYPES[chr_type])


def index_of(item, in_list):
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
                 key=lambda row: kwargs["key"](row[col]) if "key" in kwargs and inspect.isfunction(kwargs["key"]) else row[col],
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
    summary = 0
    for row in range(len(table)):
        summary += table[row][column]
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

    try:
        year = int(year)
    except ValueError:
        return False
    else:
        if year > datetime.now().year:
            return False
        return True


def validate_type(tp):
    """Check if parameter is 'in' or 'out', returns false otherwise."""

    if tp not in ("in", "out"):
        return False
    return True
