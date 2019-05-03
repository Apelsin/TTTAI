"""
Tic-Tac-Toe module

Contains classes for modeling a game of Tic-Tac-Toe
"""

from enum import Enum
import numpy as np


class Mark(int, Enum):
    """
    Represents a board cell state (empty, O, or X)
    """
    EMPTY = 0
    OMARK = 1
    XMARK = 2

    def __repr__(self):
        return ['.', 'O', 'X'][self]

    def __str__(self):
        return repr(self)

    @classmethod
    def get_next(cls, mark):
        """
        Given a player's mark, returns the opposite player's mark
        :param mark: (Mark) the player's mark
        :return: (Mark) opposite player's mark
        """
        if mark == cls.OMARK:
            return cls.XMARK
        if mark == cls.XMARK:
            return cls.OMARK
        return None


class State:
    """
    Class representing the Tic-Tac-Toe board game (state)
    """
    def __init__(self, array=None):
        if array is not None:
            assert(array.shape == (3, 3))
            self._array = array
        else:
            self._array = np.full((3, 3), Mark.EMPTY, dtype=Mark)

    def set_mark(self, row, col, mark):
        """
        Update this State by setting the mark at the specified row and
        column
        :param row: (int)
        :param col: (int)
        :param mark: (Mark)
        """
        self._array[row][col] = mark

    def to_code(self):
        """
        Get the serializable string for this State
        :return: (string)
        """
        return ''.join(str(Mark(int(x))) for x in self._array.flatten())

    def next_marks(self):
        """
        Get the next valid marks that could be replace a blank space in
        this state
        :return: (set) of Mark objects
        """
        unique, cnt = np.unique(self._array.flatten(), return_counts=True)
        count = dict(zip(unique, cnt))
        os = count.get(Mark.OMARK, 0)
        xes = count.get(Mark.XMARK, 0)
        if os == xes:
            return {Mark.OMARK, Mark.XMARK}
        else:
            return {Mark.OMARK} if xes > os else {Mark.XMARK}

    @classmethod
    def from_code(cls, code):
        """
        Return a State given a serialized string (code)
        :param code: (string) the code to parse
        :return: (State)
        """
        lookup = {repr(mark): mark for mark in Mark}
        array = np.array([lookup[c] for c in code]).reshape(3, 3)
        return State(array)

    def __getitem__(self, item):
        return self._array[item]

    def __repr__(self):
        f = np.vectorize(Mark.__repr__)
        result = repr(f(self._array).tolist())
        return result

    def __str__(self):
        f = np.vectorize(Mark.__repr__)
        stuff = f(self._array)
        return '\n'.join('|' + ' '.join(r) + '|' for r in stuff)

    def __eq__(self, other):
        return np.array_equal(self._array, other._array)

    def __hash__(self):
        return hash(tuple(self._array.flatten()))

    def __contains__(self, item):
        return item in self._array.flatten()

