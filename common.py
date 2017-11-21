# implement commonly used functions here

import random
import copy
import inspect


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


def qsort(array, **kwargs):
    """
    Sorts the array using the Quicksort algorithm (with Hoare partition scheme). \
    The original array will not be modified.

    Args:
        array: The array to sort.
        kwargs: The keyword argument "key" can be used to specify a key function.

    Returns:
        The sorted array (list).
    """
    array_copy = list(copy.deepcopy(array))

    key = kwargs["key"] if "key" in kwargs else None

    __qsort(array_copy, 0, len(array) - 1, key)

    return array_copy


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

# generate and return a unique and random string
# other expectation:
# - at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter
# - it must be unique in the list
#
# @table: list of lists
# @generated: string - randomly generated string (unique in the @table)
def generate_random(table):
    """
    Generates random and unique string. Used for id/key generation.

    Args:
        table: list containing keys. Generated string should be different then all of them

    Returns:
        Random and unique string
    """

    generated = ''

    # your code

    return generated
