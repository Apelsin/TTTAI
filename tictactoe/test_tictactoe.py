"""
Tic-Tac-Toe unit tests

Tests various classes and functions in the tictactoe modules
"""

from unittest import TestCase
from tictactoe import Mark, State
from tictactoe.ai import branch
from tictactoe.cache import StateCache
from tictactoe.util import apply_xforms
import numpy as np
from itertools import chain


class TicTacToeTester(TestCase):
    def setUp(self):
        self.brancho = list(branch([State()], Mark.OMARK, 2))
        self.branchx = list(branch([State()], Mark.XMARK, 2))
        self.state1 = State(np.array([[0, 1, 2], [0, 2, 1], [1, 0, 0]]))
        self.state2 = State(np.array([[0, 1, 2], [0, 2, 1], [1, 2, 1]]))
        self.stateo = State(np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))
        self.statex = State(np.array([[2, 0, 0], [0, 0, 0], [0, 0, 0]]))
        self.xwins1 = State(np.array([[2, 0, 0], [1, 2, 1], [1, 0, 2]]))
        self.owins1 = State(np.array([[0, 1, 2], [2, 1, 0], [0, 1, 0]]))
        self.cache = StateCache()
        self.cache.load('state-cache.json')

    def test_isomorphs(self):
        for state in self.branchx:
            for xforms, ixforms in StateCache._get_iso_xforms():
                iso = apply_xforms(xforms, state[:])
                orig = apply_xforms(ixforms, iso)
                message = f'xforms = {xforms}, ixforms = {ixforms}'
                self.assertEqual(state, State(orig), msg=message)

    def test_cache_lookup(self):
        cache = StateCache()
        cache.add(self.state1)
        state1_iso = State(np.transpose(np.rot90(self.state1[:])))
        cached, xf, ixf = cache[state1_iso]
        self.assertEqual(self.state1, cached)

    def test_to_code1(self):
        self.assertEqual(self.state1.to_code1(), '.OX.XOO..')

    def test_branching(self):
        self.assertNotEqual(self.brancho, self.branchx)

    def test_cache(self):
        iso, xf, ixf = self.cache[self.state1]
        self.assertIsNotNone(iso)
        self.assertIsNotNone(xf)
        self.assertIsNotNone(ixf)
        self.assertEqual(len(xf), len(ixf))

    def test_branching_in_cache(self):
        cache = StateCache()
        branches = chain(branch([State()], Mark.OMARK, depth=2),
                         branch([State()], Mark.XMARK, depth=2))
        for s in branches:
            cache.add(s)

        self.assertTrue(all(s in cache for s in branches))

    def test_full_state_branch(self):
        b9 = [s for s in self.cache if Mark.EMPTY not in s]
        sample9 = b9[0]
        b10 = list(branch([sample9], Mark.OMARK))
        self.assertEqual(len(b10), 1)

    def test_branching_of_cache(self):
        # Branch to legal board states
        b1 = chain(*(branch([s], m)
                     for s in self.cache
                     for m in s.next_marks()))
        self.assertTrue(all(s in self.cache for s in b1))

    def test_winner(self):
        self.assertEqual(self.xwins1.winner, Mark.XMARK)
        self.assertEqual(self.owins1.winner, Mark.OMARK)
