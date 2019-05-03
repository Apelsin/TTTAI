from unittest import TestCase
from tictactoe import Mark, State
from ai import branch
from tictactoe.cache import StateCache
import numpy as np


class TicTacToeTester(TestCase):
    def setUp(self):
        self.brancho = list(branch([State()], Mark.OMARK, 2))
        self.branchx = list(branch([State()], Mark.XMARK, 2))
        self.state1 = State(np.array([[0, 1, 2], [0, 2, 1], [1, 0, 0]]))
        self.stateo = State(np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))
        self.statex = State(np.array([[2, 0, 0], [0, 0, 0], [0, 0, 0]]))
        self.cache = StateCache()
        self.cache.load('state-cache.json')

    def test_isomorphs(self):
        for state in self.branchx:
            for xforms, ixforms in StateCache._get_iso_xforms():
                iso = StateCache._apply_xforms(xforms, state[:])
                orig = StateCache._apply_xforms(ixforms, iso)
                message = f'xforms = {xforms}, ixforms = {ixforms}'
                self.assertEqual(state, State(orig), msg=message)

    def test_cache_lookup(self):
        cache = StateCache()
        cache.add(self.state1)
        state1_iso = State(np.transpose(np.rot90(self.state1[:])))
        cached, xf, ixf = cache[state1_iso]
        self.assertEqual(self.state1, cached)

    def test_to_code(self):
        self.assertEqual(self.state1.to_code(), '.OX.XOO..')

    def test_branching(self):
        self.assertNotEqual(self.brancho, self.branchx)

    def test_cache(self):
        iso, xf, ixf = self.cache[self.state1]
        self.assertIsNotNone(iso)
        self.assertIsNotNone(xf)
        self.assertIsNotNone(ixf)
        self.assertEqual(len(xf), len(ixf))
