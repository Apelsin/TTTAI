"""
Tic-Tac-Toe game state cache module

Module for caching game states for efficiency
"""

import numpy as np
import json
from tictactoe import Mark, State
from tictactoe.ai import branch
from tictactoe.util import apply_xforms
from .util import rot270


class StateCache:
    """
    Caches game states according to their isomorphic states
    """

    def __init__(self):
        self._cache = set()

    def write(self, file_path):
        """
        Write this cache to a JSON file at the specified path
        :param file_path: (string) file path
        """
        data = {
            'Format': '002',
            'States': sorted([c.to_code2() for c in self])
        }
        with open(file_path, 'w', encoding='ascii') as fp:
            json.dump(data, fp)

    def load(self, file_path):
        """
        Read a JSON file at the specified path into this cache
        :param file_path: (string) file path
        """
        with open(file_path, 'r') as fp:
            data = json.load(fp)
        _format = int(data['Format'])
        codes = data['States']
        if _format == 1:
            for code in codes:
                self.add(State.from_code1(code))
        elif _format == 2:
            for code in codes:
                self.add(State.from_code2(code))

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
    def _get_isomorphs(cls, state):
        """
        Get the geometrically isomorphic states of a given state
        :param state: (State) the state
        :return: (generator) of transformed State objects
        """
        xforms = next(zip(*cls._get_iso_xforms()))
        for xform in xforms:
            yield State(apply_xforms(xform, state[:]))

    def add(self, state):
        """
        Add a State to the cache
        :param state: (State) the state
        """
        if state not in self:
            self._cache.add(state)

    def update_state(self, state):
        """
        Update a State object reference in the backing cache
        :param state: (State) the state
        """
        if state not in self._cache:
            raise LookupError('State must already be a direct element of the '
                              'backing cache set')
        self._cache.remove(state)
        self._cache.add(state)

    def clear_desirability(self):
        """
        Set the desirability of all States in the cache to None
        """
        for state in self._cache:
            state.desirability = None

    def __contains__(self, item):
        isos = set(self._get_isomorphs(item))
        return any(isos & self._cache)

    def __getitem__(self, item):
        for xforms, ixforms in self._get_iso_xforms():
            iso = State(apply_xforms(xforms, item[:]))
            if iso in self._cache:

                # TODO: HACK ALERT! FIX THIS!
                # Comment out this line before invoking
                # ai.cache_state_desirability
                iso = next(state for state in self._cache if state == iso)

                return iso, xforms, ixforms
        return None, None, None

    def __iter__(self):
        yield from self._cache

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
