__author__ = 'Conor'

import logging
import unittest
import main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestGameFunctions(unittest.TestCase):
    def test_init(self):
        g = main.Game()

    def test_get_current_state(self):
        g = main.Game()
        self.assertEqual(g.get_current_state(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(main.Game("rnbqkbnr/pppp1ppp/4p3/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1").get_current_state(),
                         "rnbqkbnr/pppp1ppp/4p3/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")

    def test_change_player(self):
        g = main.Game()
        g.change_player()
        self.assertEqual(g.get_current_state().split(' ')[1], 'b')
        g.change_player()
        self.assertEqual(g.get_current_state().split(' ')[1], 'w')

    def test_get_piece_at(self):
        g = main.Game()
        # White pieces
        self.assertEqual(g.get_piece_at('a1'), 'R')
        self.assertEqual(g.get_piece_at('b1'), 'N')
        self.assertEqual(g.get_piece_at('c1'), 'B')
        self.assertEqual(g.get_piece_at('d1'), 'Q')
        self.assertEqual(g.get_piece_at('e1'), 'K')
        self.assertEqual(g.get_piece_at('f1'), 'B')
        self.assertEqual(g.get_piece_at('g1'), 'N')
        self.assertEqual(g.get_piece_at('h1'), 'R')

        # White pawns
        self.assertEqual(g.get_piece_at('a2'), 'P')
        self.assertEqual(g.get_piece_at('b2'), 'P')
        self.assertEqual(g.get_piece_at('c2'), 'P')
        self.assertEqual(g.get_piece_at('d2'), 'P')
        self.assertEqual(g.get_piece_at('e2'), 'P')
        self.assertEqual(g.get_piece_at('f2'), 'P')
        self.assertEqual(g.get_piece_at('g2'), 'P')
        self.assertEqual(g.get_piece_at('h2'), 'P')

        # Black pieces
        self.assertEqual(g.get_piece_at('a8'), 'r')
        self.assertEqual(g.get_piece_at('b8'), 'n')
        self.assertEqual(g.get_piece_at('c8'), 'b')
        self.assertEqual(g.get_piece_at('d8'), 'q')
        self.assertEqual(g.get_piece_at('e8'), 'k')
        self.assertEqual(g.get_piece_at('f8'), 'b')
        self.assertEqual(g.get_piece_at('g8'), 'n')
        self.assertEqual(g.get_piece_at('h8'), 'r')

        # Black pawns
        self.assertEqual(g.get_piece_at('a7'), 'p')
        self.assertEqual(g.get_piece_at('b7'), 'p')
        self.assertEqual(g.get_piece_at('c7'), 'p')
        self.assertEqual(g.get_piece_at('d7'), 'p')
        self.assertEqual(g.get_piece_at('e7'), 'p')
        self.assertEqual(g.get_piece_at('f7'), 'p')
        self.assertEqual(g.get_piece_at('g7'), 'p')
        self.assertEqual(g.get_piece_at('h7'), 'p')

    def test_is_valid_space(self):
        g = main.Game()
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
        g = main.Game()
        self.assertItemsEqual(g.get_possible_moves_for_space('b4'), [])
        self.assertItemsEqual(g.get_possible_moves_for_space('a1'), [])
        self.assertItemsEqual(g.get_possible_moves_for_space('a2'), ['a3', 'a4'])
        self.assertItemsEqual(g.get_possible_moves_for_space('h2'), ['h3', 'h4'])
        self.assertItemsEqual(g.get_possible_moves_for_space('a7'), ['a5', 'a6'])
        self.assertItemsEqual(g.get_possible_moves_for_space('h7'), ['h5', 'h6'])

        # Rook at B4
        test_game = main.Game("rnbqkbnr/pppppppp/8/8/1R6/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertItemsEqual(test_game.get_possible_moves_for_space('b4'), ['a4', 'c4', 'd4', 'e4', 'f4', 'g4',
                                                                             'h4', 'b3', 'b5', 'b6', 'b7'])

        # TODO Uncomment when diagonal is finished
        # Queen at D4
        # test_game = main.Game("rnbqkbnr/pppppppp/8/8/3Q4/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        # self.assertItemsEqual(test_game.get_possible_moves_for_space('d4'), ['a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'h4',
        #                                                                      'd3', 'd5', 'd6', 'd7', 'c3', 'c5', 'b6',
        #                                                                      'a7', 'd3', 'd5', 'e6', 'f7'])

    def test_get_all_movable_pieces(self):
        g = main.Game()
        all_white_pieces = g.get_all_movable_pieces().values()
        self.assertEqual(len(all_white_pieces), 16)
        all_white_pieces_explicit = g.get_all_movable_pieces_for_color('w').values()
        self.assertEqual(len(all_white_pieces_explicit), 16)
        for piece in all_white_pieces:
            self.assertTrue(piece.isupper())
        for piece in all_white_pieces_explicit:
            self.assertTrue(piece.isupper())
        g.change_player()

        all_black_pieces = g.get_all_movable_pieces().values()
        self.assertEqual(len(all_black_pieces), 16)
        all_black_pieces_explicit = g.get_all_movable_pieces_for_color('b').values()
        self.assertEqual(len(all_black_pieces_explicit), 16)
        for piece in all_black_pieces:
            self.assertTrue(piece.islower())
        for piece in all_black_pieces_explicit:
            self.assertTrue(piece.islower())

    # TODO Uncomment when diagonal is implemented
    # def test_get_possible_moves_diagonal(self):
    #     g = main.Game()
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('a1'), [])
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('h1'), [])
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('a8'), [])
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('h8'), [])
    #
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('a2'), ['b3', 'c4', 'd5', 'e6'])
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('h2'), ['g3', 'f4', 'e5', 'd6'])
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('a7'), ['b6', 'c5', 'd4', 'e3'])
    #     self.assertItemsEqual(g._get_possible_moves_diagonal('h7'), ['g6', 'f5', 'e4', 'd3'])
    #
    #     test_game = main.Game("rnbqkbnr/pppppppp/8/8/1B6/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
    #     self.assertItemsEqual(test_game._get_possible_moves_diagonal('b4'), ['a3', 'c5', 'd6', 'a5', 'c4', 'd3'])
    # TODO Add a few more tests

    def test_get_possible_moves_horizontal(self):
        g = main.Game()
        self.assertItemsEqual(g._get_possible_moves_horizontal('a1'), [])
        self.assertItemsEqual(g._get_possible_moves_horizontal('h1'), [])
        self.assertItemsEqual(g._get_possible_moves_horizontal('a8'), [])
        self.assertItemsEqual(g._get_possible_moves_horizontal('h8'), [])

        test_game = main.Game("rnbqkbnr/pppppppp/8/8/1R6/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertItemsEqual(test_game._get_possible_moves_horizontal('b4'),
                              ['a4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'])

    def test_get_possible_moves_vertical(self):
        g = main.Game()
        self.assertItemsEqual(g._get_possible_moves_vertical('a1'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('h1'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('a8'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('h8'), [])
        self.assertItemsEqual(g._get_possible_moves_vertical('a2'), ['a3', 'a4', 'a5', 'a6', 'a7'])
        self.assertItemsEqual(g._get_possible_moves_vertical('a7'), ['a2', 'a3', 'a4', 'a5', 'a6'])
        self.assertItemsEqual(g._get_possible_moves_vertical('h2'), ['h3', 'h4', 'h5', 'h6', 'h7'])
        self.assertItemsEqual(g._get_possible_moves_vertical('h7'), ['h2', 'h3', 'h4', 'h5', 'h6'])

        test_game = main.Game("rnbqkbnr/pppppppp/8/8/R7/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertItemsEqual(test_game._get_possible_moves_vertical('a4'), ['a3', 'a5', 'a6', 'a7'])

        test_game = main.Game("rnbqkbnr/pppppppp/8/8/7R/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertItemsEqual(test_game._get_possible_moves_vertical('h4'), ['h3', 'h5', 'h6', 'h7'])


if __name__ == '__main__':
    unittest.main()
