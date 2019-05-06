"""
TTTAI

Tic-Tac-Toe AI runner
"""

import numpy as np
from tictactoe import State, Mark
from tictactoe.cache import StateCache
from tictactoe.ai import cache_state_desirability, calculate_next_state_for


def main():
    cache = StateCache()
    cache.load('state-cache.json')
    state = State(np.array([[0, 0, 0], [0, 0, 1], [0, 0, 0]]))
    print(state)
    state = calculate_next_state_for(cache, state, Mark.XMARK)
    print(state)
    state.set_mark(1, 1, Mark.OMARK)
    print(state)
    state = calculate_next_state_for(cache, state, Mark.XMARK)
    print(state)
    state.set_mark(2, 2, Mark.OMARK)
    print(state)
    state = calculate_next_state_for(cache, state, Mark.XMARK)
    print(state)
    state.set_mark(0, 1, Mark.OMARK)
    print(state)
    state = calculate_next_state_for(cache, state, Mark.XMARK)
    print(state)

    # cache.clear_desirability()
    # cache_state_desirability(cache, State(), Mark.OMARK)
    # cache_state_desirability(cache, State(), Mark.XMARK)
    # cache.write('state-cache2.json')


if __name__ == '__main__':
    main()
