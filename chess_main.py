__author__ = 'Conor'
import chess_board
import algorithm

class ChessMain (object):

    def __init__(self, depth_to_recur_to, load_best_moves_from_file):
        self.current_board = chess_board.Game()
        self.depth_to_recur_to = depth_to_recur_to
        self.load_best_moves_from_file = load_best_moves_from_file

    def main(self):
        a = algorithm.Algorithm('b')

        while not self.game_is_finished():
            # Player turn
            self.player_turn()

            # AI Turn
            new_board = a.play(self.current_board, self.depth_to_recur_to, self.load_best_moves_from_file)
            self.current_board = new_board

    def player_turn(self):
        return True
        # read input from player

    def game_is_finished(self):
        return False

if __name__ is '__main__':

    game = ChessMain(4, True)

    game.main()