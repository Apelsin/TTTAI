"""
Tic-Tac-Toe module

Contains classes for modeling a game of Tic-Tac-Toe
"""

from enum import Enum
import numpy as np
from copy import copy
from .util import *


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
        self._desirability = None
        self._cached_winner = None

    def set_mark(self, row, col, mark):
        """
        Update this State by setting the mark at the specified row and
        column
        :param row: (int)
        :param col: (int)
        :param mark: (Mark)
        """
        self._array[row][col] = mark

    def to_code1(self):
        """
        Get the serializable string for this State
        :return: (string)
        """
        return ''.join(str(Mark(int(x))) for x in self._array.flatten())

    @classmethod
    def from_code1(cls, code):
        """
        Return a State given a serialized string (code)
        :param code: (string) the code to parse
        :return: (State)
        """
        lookup = {repr(mark): mark for mark in Mark}
        array = np.array([lookup[c] for c in code]).reshape(3, 3)
        return State(array)

    def to_code2(self):
        """
        Get the serializable string for this State
        :return: (string)
        """
        array_code = ''.join(str(Mark(int(x))) for x in self._array.flatten())
        desirability = self.desirability or {}
        des_code = ','.join([str(x) for x in unroll_dict(desirability)])
        return '|'.join([array_code, des_code])

    @classmethod
    def from_code2(cls, code):
        """
        Return a State given a serialized string (code)
        :param code: (string) the code to parse
        :return: (State)
        """
        lookup = {repr(mark): mark for mark in Mark}
        array_code, des_code = code.split('|')
        array = np.array([lookup[c] for c in array_code]).reshape(3, 3)
        state = State(array)
        if des_code:
            des_list = des_code.split(',')
            state.desirability = {lookup[k]: int(v) for k, v in roll(des_list)}
        return state

    @property
    def is_full(self):
        return Mark.EMPTY not in list(np.unique(self._array.flatten()))

    def next_marks(self):
        """
        Get the next valid marks that could be replace a blank space in
        this state
        :return: (set) of Mark objects
        """
        unique, cnt = np.unique(self._array.flatten(), return_counts=True)
        if Mark.EMPTY not in unique:
            return set()
        count = dict(zip(unique, cnt))
        os = count.get(Mark.OMARK, 0)
        xes = count.get(Mark.XMARK, 0)
        if os == xes:
            return {Mark.OMARK, Mark.XMARK}
        else:
            return {Mark.OMARK} if xes > os else {Mark.XMARK}

    @property
    def desirability(self):
        """
        The desirability values for each Mark for this state
        :return: (dict)
        """
        return self._desirability

    @desirability.setter
    def desirability(self, value):
        if value is None:
            self._desirability = None
            return
        if not hasattr(value, '__getitem__'):
            raise TypeError('desirability object must sliceable')
        self._desirability = dict(value)

    @classmethod
    def _roll_rows(cls, array, step=1):
        """
        Rolls each row in a (2D) array by a step value
        :param array: (ndarray) the array
        :param step: (int) number of columns to shift by
        :return: (ndarray)
        """
        for idx, row in enumerate(array):
            yield np.roll(row, step * idx)

    @classmethod
    def calculate_desirability(cls, state):
        """
        Calculates the immediately-known desirability for a state
        without any branching
        :param state: (State) the state
        :return: (dict) of {Mark: score}
        """
        # If we have a winner
        if state.winner:
            return {
                Mark.OMARK: 1 if state.winner is Mark.OMARK else -1,
                Mark.XMARK: 1 if state.winner is Mark.XMARK else -1
            }

        # If this game is a draw (no more moves can be made)
        if state.is_full:
            return {
                Mark.OMARK: 0,
                Mark.XMARK: 0
            }

        # We just don't know
        return None

    def _calculate_winner(self):
        """
        Calculates the winning mark, or None if no winner in this state
        :return: (Mark) the winning mark
        """
        rows = self._array
        columns = self._array.transpose()
        diagonal1 = np.array(list(self._roll_rows(rows, -1)))[:, 0]
        diagonal2 = np.array(list(self._roll_rows(rows, 1)))[:, -1]
        diagonals = [diagonal1, diagonal2]
        rows_cols_diags = chain(rows, columns, diagonals)
        for line in rows_cols_diags:
            unique, cnt = np.unique(line, return_counts=True)
            win_cnt = len(line)
            if win_cnt in cnt:
                winner = unique[list(cnt).index(win_cnt)]
                if winner != Mark.EMPTY:
                    return Mark(winner)
        return None

    @property
    def winner(self):
        """
        Returns the winning Mark, or None if no winner in this state
        :return: (Mark) the winning mark
        """
        # Lazy evaluation
        if self._cached_winner is None:
            self._cached_winner = self._calculate_winner()
        return copy(self._cached_winner)

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

