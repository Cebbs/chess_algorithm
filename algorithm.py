__author__ = 'Conor'

import logging
import main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GLOBAL_COUNTER = 0
DEPTH_TO_RECUR_TO = 2


class Algorithm(object):
    def __init__(self):
        self.heuristic_weighting = {}
        # TODO - Add multiple heuristics with possibility for weightings
        # Example: {(heuristic_1: .6), (heuristic_2: .25), (heuristic_3:.15)}

    def run(self):
        t = StateTree(main.Game(), None)
        t.generate_decision_tree()
        print "---- ::: Done ::: ----"
        num = t.count_nodes_below()
        print "Number of nodes generated: " + str(num)


class StateTree(object):
    # Initialize the decision tree
    def __init__(self, game_state, parent, depth=0):
        self.game_state = game_state
        self.parent = parent
        self.depth = depth
        self.children = []
        self.game_state_score = 0

    # Is this a max node? (A game state where the player is WHITE and is looking at all possible moves)
    def _is_max_node(self):
        return self.game_state.get_current_state().split(' ')[1] == 'w'

    # Is this a min node? (A game state where the player is BLACK and is looking at all possible moves)
    def _is_min_node(self):
        return not self._is_max_node()

    # Generate one level of a decision tree from every possible move from this state
    def generate_decision_tree(self):

        all_possible_moves = self.game_state.get_all_possible_moves()
        # self._get_game_state_score_for_color(all_possible_moves)
        self.assign_game_state_score()
        all_possible_game_states = []
        for original_space in all_possible_moves.keys():
            for possible_move in all_possible_moves[original_space]:
                all_possible_game_states.append(self.new_game_state(original_space, possible_move, self.game_state))

        # print [str(item) for item in all_possible_game_states]
        for state in all_possible_game_states:
            new_child = StateTree(state, self, self.depth + 1)
            # print "New child created - game state score: " + str(new_child.get_game_score())
            # new_child._get_game_state_score_for_color()
            new_child.assign_game_state_score()
            # print "New child assigned score - new game state score: " + str(new_child.get_game_score())
            # print "new Child game score:" + str(new_child.get_game_score())
            self.children.append(new_child)

        # Debug
        # for child in self.children:
        #     if child.get_game_score() == 0:
        #         print "GAME SCORE IS 0 THOUGH"

        # print "test"
        # print [str(x.game_state) for x in self.children]

        # TODO - Run minmax and remove children we don't want

        if self.depth < DEPTH_TO_RECUR_TO:
            if self._is_min_node():
                min_child_score = float("inf")
                for child in self.children:
                    if child.get_game_score() < min_child_score:
                        min_child_score = child.get_game_score()

                print "min node score: " + str(min_child_score)

                self.children = [child for child in self.children if child.get_game_score() == min_child_score]

                print "Children nodes:"
                print [x.get_game_score() for x in self.children]

            print "Regular Max node"
            for child in self.children:
                child.generate_decision_tree()  # Recur

    def get_game_score(self):
        return self.game_state_score

    def assign_game_state_score(self):
        # all_possible_white_moves = self.game_state.get_all_possible_moves()
        all_possible_black_moves = self.game_state.get_all_possible_moves(color='w')
        white_score = self._get_game_state_score_for_color(all_possible_black_moves, 'w')
        black_score = self._get_game_state_score_for_color(all_possible_black_moves, 'b')
        # self.game_state_score = 0 - white_score
        # print "White score: " + str(white_score)
        # print "Black score: " + str(black_score)
        print "Total score: " + str(self.game_state_score)
        return 0

    def _get_game_state_score_for_color(self, all_possible_moves, color):
        enemy_color = 'b' if color == 'w' else 'w'
        all_enemy_pieces = self.game_state.get_all_movable_pieces(color=enemy_color)
        # print "All possible moves:"
        # print all_possible_moves
        # print "All Enemy Pieces:"
        # print all_enemy_pieces

        possible_move_values = []

        possible_move_counter = 0
        for original_space in all_possible_moves:
            for possible_move in all_possible_moves[original_space]:
                possible_move_values.append(possible_move)
                possible_move_counter += 1

        all_takable_pieces = []

        for move in possible_move_values:
            if move in all_enemy_pieces.keys():
                all_takable_pieces.append(all_enemy_pieces[move])

        game_state_score = 0

        if len(all_takable_pieces) > 0:
            print "Takeable pieces:"
            print all_takable_pieces

            for piece in all_takable_pieces:
                p = piece.lower()
                game_state_score += {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9, 'k': 1000}[p]

                # TODO - Subtract the score of the pieces that can be taken from you

        game_state_score += (possible_move_counter / 10.0)
        # self.game_state_score = game_state_score
        return game_state_score

    def count_nodes_below(self):
        result = 1
        for child in self.children:
            result += child.count_nodes_below()

        return result

    def new_game_state(self, original_space, possible_move, root_state):
        new_game_state = self.make_new_hypothetical_state(original_space, possible_move)
        return new_game_state

    def make_new_hypothetical_state(self, original_space, new_move):

        board = self._move_piece(original_space, new_move)

        new_game = main.Game(board)
        # print new_game.get_current_state()
        new_game.change_player()
        # print new_game.get_current_state()
        return new_game

    def _move_piece(self, original_space, new_move):
        moving_piece = self.game_state.get_piece_at(original_space)
        board = self.game_state.get_current_state()[:(self.game_state.get_current_state().find(' '))]
        board_split = board.split('/')
        logger.debug("Creating possible game state by moving piece [%s] from [%s] to [%s]", moving_piece,
                     original_space, new_move)

        row_of_original_piece = list(board_split[8 - int(original_space[1:])])

        new_row_of_original_piece = []
        for piece in row_of_original_piece:
            if piece.isdigit():
                num_of_empty_spaces = int(piece)
                for x in range(num_of_empty_spaces):
                    new_row_of_original_piece.append('1')
            else:
                new_row_of_original_piece.append(piece)

        new_row_of_original_piece[ord(original_space[:1]) - 97] = '1'
        new_row_of_original_piece = ''.join(new_row_of_original_piece)

        row_of_new_space = list(board_split[8 - int(new_move[1:])])

        new_row_of_new_space = []
        for piece in row_of_new_space:
            if piece.isdigit():
                num_of_empty_spaces = int(piece)
                for x in range(num_of_empty_spaces):
                    new_row_of_new_space.append('1')
            else:
                new_row_of_new_space.append(piece)

        new_row_of_new_space[ord(new_move[:1]) - 97] = moving_piece
        # print "Debug :: "
        # print new_row_of_new_space
        new_row_of_new_space = ''.join(new_row_of_new_space)

        board_split[8 - int(original_space[1:])] = new_row_of_original_piece
        board_split[8 - int(new_move[1:])] = new_row_of_new_space

        cleaned_board_split = []

        for row in board_split:
            if '1' not in row:
                cleaned_board_split.append(row)
            else:
                cleaned_row = []
                for piece in row:
                    if piece.isdigit():
                        if len(cleaned_row) > 0:  # If the list is not empty
                            if cleaned_row[len(cleaned_row) - 1].isdigit():
                                last_digit = cleaned_row[len(cleaned_row) - 1]
                                cleaned_row[len(cleaned_row) - 1] = str(int(last_digit) + int(piece))
                            else:
                                cleaned_row.append(piece)
                        else:
                            cleaned_row.append(piece)
                    else:
                        cleaned_row.append(piece)
                cleaned_row = ''.join(cleaned_row)
                cleaned_board_split.append(cleaned_row)

        board = '/'.join(cleaned_board_split)

        board = board + self.game_state.get_current_state()[self.game_state.get_current_state().find(' '):]
        # print "BOARD:"
        logger.debug("Created new possible game state: %s", board)
        # print

        return board

    def __str__(self):
        parent_string = self.parent.game_state if self.parent is not None else "None"  # hacky
        return "State: {0} | Parent: {1} | Number of Children: {2}".format(str(self.game_state), parent_string,
                                                                           self.children.__sizeof__())


if __name__ == '__main__':
    a = Algorithm()
    a.run()
