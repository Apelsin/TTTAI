"""
Utilities Module

Contains helper functions and classes, or highly-reusable code
"""

from itertools import chain
from numpy import rot90


def apply_xforms(xforms, a):
    """
    Applies a sequence of transformations to an array
    :param xforms: (iterable) of transformation functions
    :param a: (ndarray) the array
    :return: (ndarray) the transformed array
    """
    for xf in xforms:
        a = xf(a)
    return a


def rot270(a):
    """
    Rotate an array clockwise by 90 degrees
    :param a: (ndarray) the array
    :return: (ndarray) the array rotated 90 degrees clockwise
    """
    return rot90(a, 3)


def roll(x):
    return zip(x[::2], x[1::2])


def roll_dict(x):
    return dict(roll(x))


def unroll_dict(x):
    return list(chain(*x.items()))
