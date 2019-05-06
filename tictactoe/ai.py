"""
Tic-Tac-Toe AI module

Implementation of the AI
"""

import numpy as np
from tictactoe import Mark, State
from itertools import chain
from .util import apply_xforms


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
        if state.winner is None:
            down = branch1(state, mark)
            next_mark = Mark.get_next(mark)
            yield from branch(list(down), next_mark, depth - 1)


def cache_state_desirability(cache, root_state, mark):
    # Calculate branch states for root state
    branched = list(branch1(root_state, mark))
    # Limit operations to cached polymorphs
    branched_cached = set(cache[state][0] for state in branched)

    if root_state.winner is not None:
        root_state.desirability = State.calculate_desirability(root_state)
        return

    for state in branched_cached:
        if state.winner is not None:
            state.desirability = State.calculate_desirability(state)
            cache.update_state(state)

    # Calculate the desirability of the root state
    desirability = {Mark.OMARK: 0, Mark.XMARK: 0}
    next_mark = Mark.get_next(mark)
    for state in branched_cached:
        # Dynamically calculate desirability if needed
        if state.desirability is None:
            cache_state_desirability(cache, state, next_mark)
            cache.update_state(state)
        # Sum of branched scores
        desirability[Mark.OMARK] += state.desirability[Mark.OMARK]
        desirability[Mark.XMARK] += state.desirability[Mark.XMARK]
    root_state.desirability = desirability


def calculate_next_state_for(cache, root_state, mark):
    branched = branch1(root_state, mark)
    branched_cached = list(cache[state] for state in branched)
    best, xf, ixf = max(branched_cached, key=lambda x: x[0].desirability[mark])
    return State(apply_xforms(ixf, best[:]))