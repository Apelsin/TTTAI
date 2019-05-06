"""
Utilities Module

Contains helper functions and classes, or highly-reusable code
"""

from itertools import chain

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


def roll(x):
    return zip(x[::2], x[1::2])


def roll_dict(x):
    return dict(roll(x))


def unroll_dict(x):
    return list(chain(*x.items()))
