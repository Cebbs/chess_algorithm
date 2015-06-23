__author__ = 'Conor'

import pickle
import logging
import chess_board

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Algorithm(object):
    def __init__(self, ai_color):
        # TODO - Put into SQL Database
        self.loaded_dict = {}
        self.ai_color = ai_color
        # TODO - Add multiple heuristics with possibility for weightings
        # Example: {(heuristic_1: .6), (heuristic_2: .25), (heuristic_3:.15)}

    def load_best_moves_from_file(self):
        logger.info("Loading best moves from file")
        with open('best_moves.pickle', 'rb') as handle:
            self.loaded_dict = pickle.load(handle)
        logger.info("Done loading best moves from file: [%s] moves loaded in total", len(self.loaded_dict))

    def write_best_moves_to_file(self):
        logger.info("Writing best moves to file")
        with open('best_moves.pickle', 'wb') as handle:
            pickle.dump(self.loaded_dict, handle)
        logger.info("Done writing best moves to file: [%s] moves written in total", len(self.loaded_dict))

    def play(self, board, depth_to_search_to, load_files_is_true):
        print 'play'

        # Load the dict of best moves from a file
        if load_files_is_true:
            self.load_best_moves_from_file()

        best_move = self.get_best_move(board, depth_to_search_to)

        # Write our dict of best moves to a file
        self.write_best_moves_to_file()

        # new_board = self.

        logger.info("Best move: %s", best_move)

        return best_move

    def get_best_move(self, board, depth_to_search_to):
        if not str(board) in self.loaded_dict:
            logger.info("No precomputed best move for the given board [%s].", board)
            logger.info("Generating decision tree to [%s] depth...", depth_to_search_to)
            global DEPTH_TO_RECUR_TO
            DEPTH_TO_RECUR_TO = depth_to_search_to
            t = StateTree(None, board, depth_to_search_to)
            t.set_possible_moves(t.game_state.get_all_possible_moves())
            min_init = -100
            max_init = 100
            global COUNTER
            COUNTER = 0

            result = self.minimax(t, depth_to_search_to, min_init, max_init)

            count_by_depth = {}
            all_nodes = t.get_all_nodes_below()
            all_nodes.append(t)
            for node in all_nodes:
                if node.get_depth() in count_by_depth:
                    count_by_depth[node.get_depth()] += 1
                else:
                    count_by_depth[node.get_depth()] = 1
            # logger.debug("Number of nodes generated: ", len(all_nodes))
            logger.debug("Number of nodes generated: ", COUNTER)
            # results = count_by_depth.items()
            # results.reverse()
            # logger.info("Count of nodes by level: %s", results)
            print "Minimax: " + str(result) + " :: " + str(COUNTER) + "/" + str(len(all_nodes)) + " nodes searched"

        return self.loaded_dict[str(board)]

    # Minimax algorithm with alpha/beta pruning (AKA Alpha-Beta Search) so we don't search unecessary parts of the tree
    def minimax(self, node, depth, min_score, max_score):
        global COUNTER
        if node.depth == 0:
            result = node.evaluate_board_state()
            # TODO - When returned, can we add it to dict?
            return result
        elif node.is_a_max_node():
            node.generate_child_nodes()
            v = min_score
            for child in node.children:
                COUNTER += 1
                child.score = self.minimax(child, depth - 1, v, max_score)
                if child.score > v:
                    v = child.score
                if v > max_score:
                    # if not str(node.game_state) in self.loaded_dict:
                    self.loaded_dict[str(node.game_state)] = child.initializing_move
                    return max_score
            # if not str(node.game_state) in self.loaded_dict:
            self.loaded_dict[str(node.game_state)] = child.initializing_move
            return v
        elif node.is_a_min_node():
            node.generate_child_nodes()
            v = max_score
            for child in node.children:
                COUNTER += 1
                child.score = self.minimax(child, depth - 1, min_score, v)
                if child.score < v:
                    v = child.score
                if v < min_score:
                    # if not str(node.game_state) in self.loaded_dict:
                    #     self.loaded_dict[str(node.game_state)] = child.initializing_move
                    return min_score
            # if not str(node.game_state) in self.loaded_dict:
            #     self.loaded_dict[str(node.game_state)] = child.initializing_move
            return v


class StateTree(object):
    # Initialize the decision tree
    def __init__(self, initializing_move, game_state, depth):
        self.initializing_move = initializing_move
        self.game_state = game_state
        self.children = []
        self.score = 0
        self.possible_moves = {}
        self.is_max_node = False
        self.depth = depth

    def get_depth(self):
        return self.depth

    def set_max_or_min(self):
        if self.game_state.get_color() == 'b':
            self.is_max_node = True
        else:
            self.is_max_node = False

    def is_a_max_node(self):
        return self.is_max_node

    def is_a_min_node(self):
        return not self.is_max_node

    def generate_child_nodes(self):
        # logger.info("Generating child nodes...")
        # if len(self.possible_moves) == 0:
        #     print "No possible moves?"

        self.possible_moves = self.game_state.get_all_possible_moves()

        all_possible_game_states = {}
        for original_space in self.possible_moves.keys():
            for possible_move in self.possible_moves[original_space]:
                # all_possible_game_states.append(self.new_game_state(original_space, possible_move))
                all_possible_game_states[original_space + ' ' + possible_move] = self.new_game_state(original_space,
                                                                                                     possible_move)

        for move in all_possible_game_states:
            # Create a new child, analyze it's board score, and add it to the list of children
            new_child = StateTree(move, all_possible_game_states[move], self.depth - 1)
            # new_child.set_possible_moves(new_child.game_state.get_all_possible_moves())
            # new_child.assign_game_state_score()
            new_child.set_max_or_min()
            self.children.append(new_child)

    def set_possible_moves(self, possible_moves):
        self.possible_moves = possible_moves

    def get_game_score(self):
        # print "Debug game score: " + str(self.game_state_score)
        return self.score

    def evaluate_board_state(self):
        self.possible_moves = self.game_state.get_all_possible_moves()
        self.score = self._get_board_score_for_color('w') - self._get_board_score_for_color('b')
        # print "Total score: " + str(self.game_state_score)
        # if self.game_state_score == (white_score - black_score):
        #     print "DOne twice tard : " + str(self.game_state_score)
        return self.score

    def _get_board_score_for_color(self, color):
        # enemy_color = 'b' if color == 'w' else 'w'
        # print "getting pieces for " + color
        # If we're trying to get the score for the color that is currently this state's turn...
        if self.game_state.get_color() == color:
            all_possible_moves_for_color = self.possible_moves
        else:
            all_possible_moves_for_color = self.game_state.get_all_possible_moves_for_color(color)

        all_current_pieces_for_color = self.game_state.get_all_movable_pieces_for_color(color)

        # if self.game_state.get_current_state().split(' ')[1] == color:
        # if len(self.possible_moves) > 0:
        # print "Already set possible moves.."
        # self.set_possible_moves(all_possible_moves_for_color)
        # self.possible_moves = all_possible_moves_for_color

        possible_move_counter = 0
        for original_space in all_possible_moves_for_color:
            possible_move_counter += len(all_possible_moves_for_color[original_space])
            # for possible_move in all_possible_moves[original_space]:
            # possible_move_values.append(possible_move)
            # possible_move_counter += 1

        mobility_score = (possible_move_counter / 10.0)

        # all_takable_pieces = []

        # for move in possible_move_values:
        #     if move in all_enemy_pieces.keys():
        #         all_takable_pieces.append(all_enemy_pieces[move])

        game_state_score = 0

        for space in all_current_pieces_for_color:
            p = all_current_pieces_for_color[space].lower()
            game_state_score += self.get_score_for_piece(p)

        game_state_score += mobility_score
        # self.game_state_score = game_state_score
        return game_state_score

    def get_score_for_piece(self, piece):
        if piece == 'p':
            return 1
        elif piece == 'r':
            return 5
        elif piece == 'n':
            return 3
        elif piece == 'b':
            return 3
        elif piece == 'q':
            return 9
        elif piece == 'k':
            return 200

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

    def new_game_state(self, original_space, possible_move):
        new_game_state = self.make_new_hypothetical_state(original_space, possible_move)
        return new_game_state

    def make_new_hypothetical_state(self, original_space, new_move):

        current_board = self.game_state.get_current_state()[:(self.game_state.get_current_state().find(' '))]

        board = self._move_piece(current_board, original_space, new_move)

        new_game = chess_board.Game(board)
        # print new_game.get_current_state()
        new_game.change_player()
        # print new_game.get_current_state()
        return new_game

    def _move_piece(self, board, original_space, new_move):
        moving_piece = self.game_state.get_piece_at(original_space)
        # board = self.game_state.get_current_state()[:(self.game_state.get_current_state().find(' '))]
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
        logger.debug("Created new possible game state: %s", board)

        return board

if __name__ == '__main__':
    import cProfile
    import time

    a = Algorithm('b')
    start = time.clock()
    do_load_files = False
    a.play(chess_board.Game(), 3, do_load_files)
    end = time.clock()
    # cProfile.run('a.play(2)', sort=True)
    print "total time: " + str(end - start)
