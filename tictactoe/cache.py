"""
Tic-Tac-Toe game state cache module

Module for caching game states for efficiency
"""

import numpy as np
import json
from tictactoe import Mark, State
from ai import branch


def rot270(a):
    """
    Rotate an array clockwise by 90 degrees
    :param a: (ndarray) the array
    :return: (ndarray) the array rotated 90 degrees clockwise
    """
    return np.rot90(a, 3)


class StateCache:
    """
    Caches game states according to their isomorphic states
    """

    def __init__(self):
        self._cache = set()

    def write(self, file_path):
        with open(file_path, 'w', encoding='ascii') as fp:
            json.dump(sorted([c.to_code() for c in self]), fp)

    def load(self, file_path):
        with open(file_path, 'r') as fp:
            data = json.load(fp)
        for code in data:
            self.add(State.from_code(code))

    @classmethod
    def _get_iso_xforms(cls):
        """
        Get the transformation and inverse transformation sequences for
        generating all geometrical isomorphs of a game state.
        :return: (generator) of tuples (xform sequence, inv. xform seq.)
        """
        yield [], []
        a = [np.rot90]
        ainv = [rot270]
        yield a, ainv
        b = [np.transpose]
        binv = [np.transpose]
        yield b, binv
        c = a + [np.transpose]
        cinv = [np.transpose] + ainv
        yield c, cinv
        d = a + [np.rot90]
        dinv = [rot270] + ainv
        yield d, dinv
        e = b + [np.rot90]
        einv = [rot270] + binv
        yield e, einv
        f = c + [np.rot90]
        finv = [rot270] + cinv
        yield f, finv
        g = d + [np.transpose]
        ginv = [np.transpose] + dinv
        yield g, ginv
        h = f + [np.rot90]
        hinv = [rot270] + finv
        yield h, hinv
        i = e + [np.transpose]
        iinv = [np.transpose] + einv
        yield i, iinv

    @classmethod
    def _apply_xforms(cls, xforms, a):
        """
        Applies a sequence of transformations to an array
        :param xforms: (iterable) of transformation functions
        :param a: (ndarray) the array
        :return: (ndarray) the transformed array
        """
        for xf in xforms:
            a = xf(a)
        return a

    @classmethod
    def _get_isomorphs(cls, state):
        """
        Get the geometrically isomorphic states of a given state
        :param state: (State) the state
        :return: (generator) of transformed State objects
        """
        xforms = next(zip(*cls._get_iso_xforms()))
        for xform in xforms:
            yield State(cls._apply_xforms(xform, state[:]))

    def __contains__(self, item):
        isos = set(self._get_isomorphs(item))
        return any(isos & self._cache)

    def __getitem__(self, item):
        for xforms, ixforms in self._get_iso_xforms():
            iso = State(self._apply_xforms(xforms, item[:]))
            if iso in self._cache:
                return iso, xforms, ixforms
        return None, None, None

    def __iter__(self):
        yield from self._cache

    def add(self, state):
        """
        Add a State to the cache
        :param state: (State) the state
        """
        if state not in self:
            self._cache.add(state)

    def __len__(self):
        return len(self._cache)


def generate_cache_file(file_path):
    """
    Generates a cache of all geometrically dissimilar states of the
    game. This generally takes a few minutes.
    """
    cache = StateCache()
    for state in branch([State()], Mark.OMARK, 9):
        cache.add(state)
    for state in branch([State()], Mark.XMARK, 9):
        cache.add(state)
    cache.write(file_path)
