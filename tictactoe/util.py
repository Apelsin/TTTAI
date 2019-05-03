"""
Utilities Module

Contains helper functions and classes, or highly-reusable code
"""

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
