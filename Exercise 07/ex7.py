

########## ~ IMPORTS ~ ##########
from typing import *
import typing
from ex7_helper import *

########## ~ MAGIC ~ ##########
N = typing.TypeVar('N', int, float)
Any = typing.Any


def mult(x: N, y: int) -> N:
    """
    Returns the multlipication of x and y.
    """
    if y == 0:
        return 0
    elif y == 1:
        return x
    return add(x, mult(x, subtract_1(y)))


def is_even(n: int) -> bool:
    """
    Returns;
    n := even - True
    n := odd - False
    """
    if n < 1:
        return True
    elif n == 1:
        return False
    return is_even(subtract_1(subtract_1(n)))


def log_mult(x: N, y: int) -> N:
    """
    Returns the result of x*y, in a complexity time of O(logn).
    """
    if y == 0:
        return 0
    n = log_mult(x, divide_by_2(y))
    if is_odd(y):
        return add(n, add(n, x))
    else:
        return add(n, n)


def _multlipication(b: int, c: int, x: int) -> bool:
    """
    Applies multlipications to c by c constantly in recursion until a break rule is met.
    """
    if c > x:
        return False
    elif c == x:
        return True
    return _multlipication(b, log_mult(c, b), x)


def is_power(b: int, x: int) -> bool:
    """
    Returns if b is a naturl log base of x.
    """
    if b == x:
        return True
    elif b > 0 and x == 1:
        return True
    elif b == 0 and x == 1:
        return True
    elif b == 0 and x > 1:
        return False
    elif b == 1 and x > 1:
        return False
    result = _multlipication(b, b, x)
    return result


def reverse(s: str) -> str:
    length = len(s) - 1
    if length == 0 or length == -1:
        return s
    return _reverse_side_chick(s, s[length], length - 1, length)


def _reverse_side_chick(s: str, reversed_s: str, i: int, length: int) -> str:
    if i == 0:
        return append_to_end(reversed_s, s[i])
    reversed_s = append_to_end(reversed_s, s[i])
    return _reverse_side_chick(s, reversed_s, i - 1, length)


def play_hanoi(hanoi: Any, n: int, src: Any, dest: Any, temp: Any) -> None:
    """
    This function solves the hanoi game. Based on an algorithm that was showed to us in a recitaion of the intro2cs
    course at week 7.
    """
    # src = A, dest = C, temp = B, n = discs
    if n <= 0:
        return
    else:
        play_hanoi(hanoi, n - 1, src, temp, dest)
        hanoi.move(src, dest)
        play_hanoi(hanoi, n - 1, temp, dest, src)


def number_of_ones(n: int) -> int:
    """This function returns how many times 1 shows in all the numbers from 1 to n"""
    if n == 0:
        return 0
    if 1 < n < 10:
        return 1
    return _counter_for_number_of_ones(n, 1, 0)


def _counter_for_number_of_ones(n: int, interval: int, ones: int) -> int:
    """
    Counts how many times the digit 1 is in each number from 1 to n
    """
    if n == 1:
        return 1
    elif n <= 0:
        return 0
    if interval > n:
        return ones
    else:
        c = log_mult(interval, 10)
        if ((n % c) - interval) + 1 > 0:
            if ((n % c) - interval) + 1 < interval:
                ones += ((n % c) - interval) + 1
            else:
                ones += interval
        else:
            if 0 < interval:
                ones += 0
            else:
                ones += interval
        ones += log_mult(n // c, interval)
        interval = log_mult(interval, 10)
    return _counter_for_number_of_ones(n, interval, ones)


def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    """
    Returns wether every object within the lists are identical.
    If the lists are identical, the func will return True. Else -> False.
    """
    if len(l1) != len(l2):
        return False
    elif len(l1) == 0 and len(l2) == 0:
        return True
    elif len(l1[0]) != len(l2[0]):
        return False
    return _compare_inner_lists(l1, l2, 0, 0)


def _compare_inner_lists(l1: List[List[int]], l2: List[List[int]], row_i: int , col_i: int) -> bool:
    """
    A function that compares the numbers within the lists in the list.
    """
    if len(l1) != len(l2):
        return False
    elif len(l1) == 0 and len(l2) == 0:
        return True
    elif row_i >= len(l1):
        return True
    elif col_i >= len(l1[row_i]) and col_i >= len(l2[row_i]):
        return _compare_inner_lists(l1, l2, row_i + 1, 0)
    elif len(l1[row_i]) != len(l2[row_i]):
        return False
    curr = l1[row_i][col_i] == l2[row_i][col_i]
    recursion = _compare_inner_lists(l1, l2, row_i, col_i + 1)
    if curr == True and recursion == True:
        return True
    else:
        return False


def magic_list(n: int) -> List[Any]:
    """
    Returns a list with lists at each [index] that contain the list from the previous index.
    Starts with [] for index 0.
    """
    if n == 0:
        return []
    return _tragic_list(n, 0)


def _tragic_list(n: int, i: int) -> List[Any]:
    """
    Creates a list of lists in recursion.
    """
    if i == n:
        return []
    curr = _tragic_list(n - 1, 0)
    curr.append(_tragic_list(n - 1, 0))
    return curr
