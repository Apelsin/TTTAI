"""
TTTAI

Tic-Tac-Toe AI runner
"""

from tictactoe.cache import StateCache


def main():
    cache = StateCache()
    cache.load('state-cache.json')


if __name__ == '__main__':
    main()
