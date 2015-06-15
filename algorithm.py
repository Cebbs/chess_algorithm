__author__ = 'Conor'

import logging
import main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Algorithm(object):
    def __init__(self):
        self.heuristic_weighting = {}
        # TODO - Add multiple heuristics with possibility for weightings
        # Example: {(heuristic_1: .6), (heuristic_2: .25), (heuristic_3:.15)}

    def run(self, depth_to_search_to):
        logger.info("Generating decision tree to [%s] depth", depth_to_search_to)
        global DEPTH_TO_RECUR_TO
        DEPTH_TO_RECUR_TO = depth_to_search_to
        t = StateTree(main.Game(), None)
        t.generate_decision_tree()
        # print "---- ::: Done ::: ----"
        count_by_depth = {}
        all_nodes = t.get_all_nodes_below()
        all_nodes.append(t)
        for node in all_nodes:
            if node.get_depth() in count_by_depth:
                count_by_depth[node.get_depth()] += 1
            else:
                count_by_depth[node.get_depth()] = 1
        logger.debug("Number of nodes generated: ", len(all_nodes))
        logger.info("Count of nodes by level: %s", count_by_depth.items())

        return len(all_nodes)

class StateTree(object):
    # Initialize the decision tree
    def __init__(self, game_state, parent, depth=0):
        self.game_state = game_state
        self.parent = parent
        self.depth = depth
        self.children = []
        self.game_state_score = 0

    def get_depth(self):
        return self.depth

    # Is this a max node? (A game state where the player is WHITE)
    def _is_max_node(self):
        return self.game_state.get_current_state().split(' ')[1] == 'w'

    # Is this a min node? (A game state where the player is BLACK)
    def _is_min_node(self):
        return self.game_state.get_current_state().split(' ')[1] == 'b'

    # Generate one level of a decision tree from every possible move from this state
    def generate_decision_tree(self):
        if self.depth + 1 <= DEPTH_TO_RECUR_TO:
            all_possible_moves = self.game_state.get_all_possible_moves()
            # self._get_game_state_score_for_color(all_possible_moves)
            # self.assign_game_state_score()
            all_possible_game_states = []
            for original_space in all_possible_moves.keys():
                for possible_move in all_possible_moves[original_space]:
                    all_possible_game_states.append(self.new_game_state(original_space, possible_move, self.game_state))

            # print [str(item) for item in all_possible_game_states]
            for state in all_possible_game_states:
                new_child = StateTree(state, self, self.depth + 1)
                new_child.assign_game_state_score()
                self.children.append(new_child)

            if self._is_min_node():
                min_child_score = 1000.0
                for child in self.children:
                    if child.get_game_score() < min_child_score:
                        min_child_score = child.get_game_score()

                self.children = [child for child in self.children if child.get_game_score() == min_child_score]

                # print "Min Node"
                # print "Number of children: " + str(len(self.children))

            # else:
                # print "Regular Max node"
                # print "Number of children: " + str(len(self.children))

            for child in self.children:
                child.generate_decision_tree()  # Recur

    def get_game_score(self):
        # print "Debug game score: " + str(self.game_state_score)
        return self.game_state_score

    def assign_game_state_score(self):
        # all_possible_white_moves = self.game_state.get_all_possible_moves()
        # all_possible_black_moves = self.game_state.get_all_possible_moves()
        white_score = self._get_game_state_score_for_color('w')
        black_score = self._get_game_state_score_for_color('b')
        # self.game_state_score = 0 - white_score
        # print "White score: " + str(white_score)
        # print "Black score: " + str(black_score)
        self.game_state_score = white_score - black_score
        # print "Total score: " + str(self.game_state_score)
        # if self.game_state_score == (white_score - black_score):
        #     print "DOne twice tard : " + str(self.game_state_score)
        return white_score - black_score

    def _get_game_state_score_for_color(self, color):
        # enemy_color = 'b' if color == 'w' else 'w'
        # print "getting pieces for " + color
        all_possible_moves = self.game_state.get_all_possible_moves_for_color(color)
        all_current_pieces = self.game_state.get_all_movable_pieces_for_color(color)
        # if len(all_current_pieces) == 0:
        #     print "Empty CURRENT PIECES"
        # print all_current_pieces.items()
        # print "All possible moves:"
        # print all_possible_moves
        # print "All Enemy Pieces:"
        # print all_enemy_pieces

        # possible_move_values = []

        possible_move_counter = 0
        for original_space in all_possible_moves:
            possible_move_counter += len(all_possible_moves[original_space])
            # for possible_move in all_possible_moves[original_space]:
            # possible_move_values.append(possible_move)
            # possible_move_counter += 1

        # all_takable_pieces = []

        # for move in possible_move_values:
        #     if move in all_enemy_pieces.keys():
        #         all_takable_pieces.append(all_enemy_pieces[move])

        # if len(all_takable_pieces) > 0:
        #     print "Takeable pieces:"
        #     print all_takable_pieces
        #
        #     for piece in all_takable_pieces:
        #         p = piece.lower()
        #         game_state_score += {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9, 'k': 1000}[p]

        game_state_score = 0

        score_dict = {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9, 'k': 200}

        for space in all_current_pieces:
            p = all_current_pieces[space].lower()
            game_state_score += score_dict[p]

        game_state_score += (possible_move_counter / 10.0)
        # self.game_state_score = game_state_score
        return game_state_score

    # Get all the nodes below this one
    def get_all_nodes_below(self):
        result = []
        for child in self.children:
            result.append(child)

        for child in self.children:
            result += child.get_all_nodes_below()

        # print "ALl nodes:"
        # print result

        return result

    def count_nodes_below(self):

        result = len(self.children)

        for child in self.children:
            result = result + child.count_nodes_below()

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
    a.run(2)
