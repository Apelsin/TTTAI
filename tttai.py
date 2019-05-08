"""
TTTAI

Tic-Tac-Toe AI runner
"""

import numpy as np
from tictactoe import State, Mark
from tictactoe.cache import StateCache
from tictactoe.ai import cache_state_desirability, calculate_next_state_for
import time


def play_self_game(cache):
    mark = Mark.OMARK
    states = [State()]
    start_time = time.time()
    while states[-1].winner is None and not states[-1].is_full:
        states.append(calculate_next_state_for(cache, states[-1], mark))
        mark = Mark.get_next(mark)
    milliseconds = round(1000 * (time.time() - start_time))
    print('Calculated', len(states) - 1, "moves in", milliseconds, "ms")

    for state in states:
        print()
        print(state)


def recalculate_desirability(cache):
    cache.clear_desirability()
    cache_state_desirability(cache, State(), Mark.OMARK)
    cache_state_desirability(cache, State(), Mark.XMARK)
    cache.write('state-cache.json')


def main():
    cache = StateCache()
    cache.load('state-cache.json')
    play_self_game(cache)
    #recalculate_desirability(cache)


if __name__ == '__main__':
    main()
