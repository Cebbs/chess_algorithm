__author__ = 'Conor'

import logging
import unittest
import main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

g = main.Game()  # yuck


class TestGameFunctions(unittest.TestCase):
    def test_init(self):
        pass

    def test_get_current_state(self):
        self.assertEqual(g.get_current_state(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(main.Game("rnbqkbnr/pppp1ppp/4p3/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1").get_current_state(),
                         "rnbqkbnr/pppp1ppp/4p3/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")

    def test_change_player(self):
        g.change_player()
        self.assertEqual(g.get_current_state().split(' ')[1], 'b')
        g.change_player()
        self.assertEqual(g.get_current_state().split(' ')[1], 'w')
        pass

    def test_get_piece_at(self):
        self.assertEqual(g.get_piece_at('a1'), 'R')

    def test_is_valid_space(self):
        self.assertTrue(g.is_valid_space('a1'))
        self.assertTrue(g.is_valid_space('a8'))
        self.assertTrue(g.is_valid_space('h1'))
        self.assertTrue(g.is_valid_space('h8'))
        self.assertTrue(g.is_valid_space('b4'))

        self.assertFalse(g.is_valid_space('i2'))
        self.assertFalse(g.is_valid_space('1a'))
        self.assertFalse(g.is_valid_space('#?'))
        self.assertFalse(g.is_valid_space('a3a6'))
        self.assertFalse(g.is_valid_space(''))

    def test_get_possible_moves_for_space(self):
        self.assertEqual(g.get_possible_moves_for_space('b4'), [])
        self.assertEqual(g.get_possible_moves_for_space('a1'), [])
        self.assertEqual(g.get_possible_moves_for_space('a2'), ['a3', 'a4'])
        pass

    def test_get_all_movable_pieces(self):
        logger.info(g.get_all_movable_pieces())
        logger.info(g.get_all_movable_pieces(color='w'))
        logger.info(g.get_all_movable_pieces(color='b'))

    def test_get_all_possible_moves(self):
        pass

    def test_get_possible_moves_horizontal(self):
        self.assertItemsEqual(g._get_possible_moves_horizontal('a1'), [])
        self.assertItemsEqual(g._get_possible_moves_horizontal('h1'), [])
        self.assertItemsEqual(g._get_possible_moves_horizontal('a8'), [])
        self.assertItemsEqual(g._get_possible_moves_horizontal('h8'), [])

    def test_get_possible_moves_vertical(self):
        self.assertItemsEqual(g._get_possible_moves_vertical('a1'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('h1'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('a8'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('h8'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('a2'), ['a3', 'a4', 'a5', 'a6', 'a7'])
        self.assertItemsEqual(g._get_possible_moves_vertical('a7'), ['a2', 'a3', 'a4', 'a5', 'a6'])

        # game = main.Game("rnbqkbnr/pppppppp/8/8/1R6/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        # self.assertItemsEqual(game._get_possible_moves_vertical('b4'), ['b3', 'b5', 'b6', 'b7'])


if __name__ == '__main__':
    unittest.main()
