"""
Tic-Tac-Toe AI module

Implementation of the AI
"""

import numpy as np
from tictactoe import Mark, State


def branch1(state, mark):
    """
    Yield results for making the next move on a given game state
    :param state: (State) the current state
    :param mark: (Mark) the player's mark
    :return: (generator) of State objects as result of all possible
    subsequent moves with the given mark
    """
    assert(isinstance(state, State))
    array = state[:]
    coords = np.transpose(np.indices(array.shape), axes=(1, 2, 0))
    blank_coords = coords[array == Mark.EMPTY]

    def option(a, idx, m):
        o = a.copy()
        o[idx] = m
        return o

    # The tuple is the spice
    possibilities = [option(array, tuple(idx), mark) for idx in blank_coords]
    yield from (State(p) for p in possibilities)


def branch(states, mark, depth=1):
    """
    Yield results for making the next move on a given game state to a
    given depth.
    :param states: (iterable) of States to branch from
    :param mark: (Mark) the player's mark at the supplied depth
    :param depth: (int) the ply by which to branch
    :return: (generator) of State objects as the result of all possible
    subsequent moves to the degree of the supplied depth
    """
    yield from states
    if depth <= 0:
        return
    for state in states:
        down = branch1(state, mark)
        next_mark = Mark.get_next(mark)
        yield from branch(list(down), next_mark, depth - 1)
