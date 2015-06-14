__author__ = 'Conor'

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Game(object):
    # Initialize as a new game
    def __init__(self, state="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):  # put in constants
        self.state = state

    # Gets the current state of this game board
    def get_current_state(self):
        return self.state

    # TODO Cleanup
    def change_player(self):
        state = self.state
        state = state.split(' ')
        if self.state.split(' ')[1] == 'w':
            state[1] = 'b'
        else:
            state[1] = 'w'
        state = ' '.join(state)
        self.state = state

    def get_all_possible_moves(self, **kwargs):
        if 'color' in kwargs:
            player_color = kwargs.get('color')
        else:
            player_color = self.state.split(' ')[1]

        player = 'WHITE' if player_color == 'w' else 'BLACK'
        logger.info("Getting all possible moves for the current game board for %s player...", player)
        movable_pieces = self.get_all_movable_pieces(color=player_color)
        all_possible_moves = {}
        for space in movable_pieces:
            logger.info("Debug ::: Getting possible moves for piece [%s] at [%s]", movable_pieces[space], space)
            all_possible_moves[space] = self.__get_possible_moves_for_piece(movable_pieces[space], space)

        # Remove dictionary entries without any values
        all_possible_moves = dict((k, v) for k, v in all_possible_moves.iteritems() if v)

        counter = 0  # TODO - Clean up
        for set_of_moves in all_possible_moves.values():
            counter += len(set_of_moves)

        logger.info("Finished getting all possible moves for %s. There are %s possible moves in total.", player,
                    counter)
        logger.debug("All possible moves: %s", ', '.join(map(str, all_possible_moves.items())))
        return all_possible_moves

    def get_all_movable_pieces(self, **kwargs):
        if 'color' in kwargs:
            color = kwargs.get('color')
        else:
            color = self.state.split(' ')[1]

        board_by_row = self.state.split(' ')[0].split('/')
        all_movable_pieces = {}

        if color == 'w':
            row_counter = 8
            for row in board_by_row:
                col_counter = 1
                for piece in row:
                    if piece.isdigit():
                        col_counter += int(piece)
                    elif piece.isupper():
                        space = str(chr(col_counter + 96)) + str(row_counter)
                        all_movable_pieces[space] = piece
                        col_counter += 1
                    else:
                        col_counter += 1
                row_counter -= 1
        elif color == 'b':
            row_counter = 8
            for row in board_by_row:
                col_counter = 1
                for piece in row:
                    if piece.isdigit():
                        col_counter += int(piece)
                    elif piece.islower():
                        space = str(chr(col_counter + 96)) + str(row_counter)
                        all_movable_pieces[space] = piece
                        col_counter += 1
                    else:
                        col_counter += 1
                row_counter -= 1
        else:
            logger.error("Neither black nor white's turn")

        logger.debug("All movable pieces: %s", ', '.join(map(str, all_movable_pieces.items())))

        return all_movable_pieces

    # Get the possible moves for a piece at the given space
    def get_possible_moves_for_space(self, space):
        logger.debug("Getting possible moves for the piece at [%s]...", space)
        possible_moves = []
        if self.is_valid_space(space):
            piece = self.get_piece_at(space)
            if not isinstance(piece, int):
                possible_moves = self.__get_possible_moves_for_piece(piece, space)
                logger.debug("Possible moves for %s at space [%s]: [%s]", piece, space,
                             ', '.join(map(str, possible_moves)))
            else:
                logger.error("Could not get possible moves for the piece at [%s]: there is no piece at this space." +
                             " The returned piece was [%s] - Here is the current state: %s", space, piece, self.state)
        else:
            logger.error("Could not get possible moves for the piece at [%s]: this is not a valid space. Here is" +
                         " the current state: %s", space, self.state)

        return possible_moves

    # Check if the given space is valid
    def is_valid_space(self, space):
        return len(space) == 2 and 'a' <= space[:1] <= 'h' and 1 <= int(space[1:]) <= 8

    # Check if the moves are valid, and removes whichever moves are not valid
    def check_validity_of_possible_moves(self, moves):

        result = []
        for move in moves:
            if not self.is_valid_space(move):
                logger.debug("[%s] is not a valid move. Removing it from the list of possible moves.", move)
            elif self.is_occupied_by_teammate(move):
                logger.debug("[%s] is occupied by a teammate piece. Removing it from the list of possible moves.", move)
            else:
                result.append(move)

        return result

    # Check if the given space is occupied by a piece on the same team
    def is_occupied_by_teammate(self, space):
        piece = self.get_piece_at(space)
        if piece == -1:
            return False
        else:
            current_color = 'W' if self.state.split(' ')[1] == 'w' else 'b'
            # print "space debug" + str(space)
            # print "piece debug:" + str(piece)
            # print "color debug:" + current_color
            return self.same_color_pieces(piece, current_color)

    # Get all of the possible moves for the given piece at the given space
    def __get_possible_moves_for_piece(self, piece, space):

        direction = 1 if piece.isupper() else -1
        p = piece.lower()

        possible_moves = []
        if p == 'p':  # If the given piece is a Pawn...
            possible_moves = self.__get_possible_moves_for_pawn(space, direction)
        elif p == 'r':  # If the given piece is a Rook...
            possible_moves = self.__get_possible_moves_for_rook(space)
        elif p == 'n':  # If the given piece is a Knight...
            possible_moves = self.__get_possible_moves_for_knight(space)
        elif p == 'b':  # If the given piece is a Bishop...
            possible_moves = self.__get_possible_moves_for_bishop(space)
        elif p == 'q':  # If the given piece is a Queen...
            possible_moves = self.__get_possible_moves_for_queen(space)
        elif p == 'k':  # If the given piece is a King...
            possible_moves = self.__get_possible_moves_for_king(space)
        else:
            logger.error("Was given an invalid piece [%s], can not find possible moves for it.", piece)

        return possible_moves

    def __get_possible_moves_for_pawn(self, space, direction):

        result = [space[:1] + str(int(space[1:]) + (1 * direction))]

        if (direction == -1 and int(space[1:]) == 7) or (direction == 1 and int(space[1:]) == 2):
            result.append(space[:1] + str(int(space[1:]) + (2 * direction)))

        # TODO Handle fancy pawn move

        result = self.check_validity_of_possible_moves(result)
        return result

    # Get all possible moves for a Knight
    def __get_possible_moves_for_knight(self, space):
        logger.debug("Getting possible moves for a Knight at [%s]", space)
        result = [chr(ord(space[:1]) + 1) + str(int(space[1:]) + 2),
                  chr(ord(space[:1]) - 1) + str(int(space[1:]) + 2),
                  chr(ord(space[:1]) + 1) + str(int(space[1:]) - 2),
                  chr(ord(space[:1]) - 1) + str(int(space[1:]) - 2),
                  chr(ord(space[:1]) + 2) + str(int(space[1:]) + 1),
                  chr(ord(space[:1]) - 2) + str(int(space[1:]) + 1),
                  chr(ord(space[:1]) + 2) + str(int(space[1:]) - 1),
                  chr(ord(space[:1]) - 2) + str(int(space[1:]) - 1)]
        result = self.check_validity_of_possible_moves(result)
        return result

    # Get all possible moves for a King
    def __get_possible_moves_for_king(self, space):
        logger.debug("Getting possible moves for a King at [%s]", space)
        result = [chr(ord(space[:1]) + 1) + str(int(space[1:]) + 1),
                  chr(ord(space[:1]) + 1) + str(int(space[1:])),
                  chr(ord(space[:1]) + 1) + str(int(space[1:]) - 1),
                  chr(ord(space[:1]) - 1) + str(int(space[1:]) + 1),
                  chr(ord(space[:1]) - 1) + str(int(space[1:])),
                  chr(ord(space[:1]) - 1) + str(int(space[1:]) - 1),
                  chr(ord(space[:1])) + str(int(space[1:]) + 1),
                  chr(ord(space[:1])) + str(int(space[1:]) - 1)]
        result = self.check_validity_of_possible_moves(result)
        return result

    # Get all of the possible move for a rook at the given space
    def __get_possible_moves_for_rook(self, space):
        logger.debug("Getting possible moves for Rook at [%s]", space)
        return self._get_possible_moves_horizontal_and_vertical(space)

    # Get all of the possible moves for a queen at the given space
    def __get_possible_moves_for_queen(self, space):
        logger.debug("Getting possible moves for Queen at [%s]", space)
        return self._get_possible_moves_horizontal_and_vertical(space) + self._get_possible_moves_diagonal(space)

    # Get all of the possible moves for a bishop at the given space
    def __get_possible_moves_for_bishop(self, space):
        logger.debug("Getting possible moves for Bishop at [%s]", space)
        return self._get_possible_moves_diagonal(space)

    # Get the possible horizontal and vertical moves from the given space
    def _get_possible_moves_horizontal_and_vertical(self, space):
        logger.debug("Getting horizontal and vertical moves from space [%s]", space)
        return self._get_possible_moves_horizontal(space) + self._get_possible_moves_vertical(space)

    def log_current_game_state(self):
        logger.error("Current game state: %s", self.state)

    # Get the possible horizontal moves from the given space
    def _get_possible_moves_horizontal(self, space):
        logger.debug("Getting possible moves in row")

        split_state = self.state.split(" ")[0].split("/")  # Split the board into rows
        occupied_spaces_in_row = {}  # Keep track of the pieces by their column number
        counter = 1  # Initialize counter

        # TODO - Clean up
        # if len(split_state[8 - int(space[1:])]) >= int(space[1:]):  # If the row is not empty # TODO - Super wrong
        for piece in split_state[8 - int(space[1:])]:  # For each of the pieces in this piece's row...
            if piece.isdigit():  # If the piece is a number (blank space(s))...
                counter += int(piece)  # Increase the counter by the number of blank space
            else:
                occupied_spaces_in_row[(chr(counter + 96))] = piece
                counter += 1
        # else:
        #     logger.error("While trying to get the horizontal moves for the given space [%s], the row of the given " +
        #                  "space was not long enough to contain the space", space)
        #     self.log_current_game_state()

        logger.debug("Occupied spaces in row: %s", ','.join(map(str, occupied_spaces_in_row.items())))

        occupied_columns = occupied_spaces_in_row.keys()
        occupied_columns.sort()  # Since the dictionary is ordered arbitrarily
        piece_index = occupied_columns.index(space[:1])
        logger.debug("Piece index: %s", str(piece_index))

        logger.debug("Occupied columns: %s", ','.join(map(str, occupied_columns)))

        if len(occupied_columns) == 1:
            first_piece_to_left = '`'
            first_piece_to_right = 'i'
        elif piece_index == 0:
            first_piece_to_left = occupied_columns[piece_index]
            first_piece_to_right = occupied_columns[piece_index + 1]
        elif piece_index == (len(occupied_columns) - 1):
            first_piece_to_right = occupied_columns[piece_index]
            first_piece_to_left = occupied_columns[piece_index - 1]
        else:
            first_piece_to_right = occupied_columns[piece_index + 1]
            first_piece_to_left = occupied_columns[piece_index - 1]

        logger.debug("First piece to left: %s", first_piece_to_left)
        logger.debug("First piece to right: %s", first_piece_to_right)

        possible_moves = []
        for letter in "abcdefgh":
            if first_piece_to_left < letter < first_piece_to_right:
                possible_moves.append(letter)

        if len(occupied_columns) > 1:
            if not self.same_color_pieces(occupied_spaces_in_row[first_piece_to_left],
                                          occupied_spaces_in_row[space[:1]]):
                possible_moves.append(first_piece_to_left)
            if not self.same_color_pieces(occupied_spaces_in_row[first_piece_to_right],
                                          occupied_spaces_in_row[space[:1]]):
                possible_moves.append(first_piece_to_right)

        if space[:1] in possible_moves:
            possible_moves.remove(space[:1])

        possible_moves.sort()
        possible_moves = map((lambda x: x + space[1:]), possible_moves)

        return possible_moves

    # Get all of the possible vertical moves for the piece at the given space
    def _get_possible_moves_vertical(self, space):
        logger.debug("Getting possible vertical moves from space [%s]", space)

        state_split = self.state.split(' ')[0].split('/')

        logger.info("Debug - Veritical ::: row: %s", '/'.join(map(str,state_split)))

        occupied_spaces_in_column = {}
        counter = 8
        for row in state_split:
            if len(row) > ord(space[:1]) - 97:  # If there enough pieces in the row
                if not row[ord(space[:1]) - 97].isdigit():
                    occupied_spaces_in_column[counter] = row[ord(space[:1]) - 97]
            counter -= 1

        logger.debug("Occupied spaces in column: %s", ','.join(map(str, occupied_spaces_in_column.items())))

        print occupied_spaces_in_column
        occupied_row = occupied_spaces_in_column.keys()
        occupied_row.sort()  # Since the dictionary items are ordered arbitrarily

        print "debug :: " + ','.join(map(str, occupied_row))
        piece_index = occupied_row.index(int(space[1:]))

        logger.debug("Piece index: %s", str(piece_index))

        if len(occupied_row) == 1:
            first_piece_below = 0
            first_piece_above = 9
        elif piece_index == 0:
            first_piece_below = occupied_row[piece_index]
            first_piece_above = occupied_row[piece_index + 1]
        elif piece_index == len(occupied_row) - 1:
            first_piece_above = occupied_row[piece_index]
            first_piece_below = occupied_row[piece_index - 1]
        else:
            first_piece_below = occupied_row[piece_index - 1]
            first_piece_above = occupied_row[piece_index + 1]

        logger.debug("First piece below: %s", first_piece_below)
        logger.debug("First piece above: %s", first_piece_above)

        possible_moves = []

        for n in "12345678":
            if first_piece_below < int(n) < first_piece_above:
                possible_moves.append(n)

        if len(occupied_row) > 1:
            if not self.same_color_pieces(occupied_spaces_in_column[first_piece_below],
                                          occupied_spaces_in_column[int(space[1:])]):
                possible_moves.append(first_piece_below)
            if not self.same_color_pieces(occupied_spaces_in_column[first_piece_above],
                                          occupied_spaces_in_column[int(space[1:])]):
                possible_moves.append(first_piece_above)

        if space[1:] in possible_moves:  # Just insurance, ever really true?
            possible_moves.remove(space[1:])

        possible_moves = map((lambda x: space[:1] + str(x)), possible_moves)
        possible_moves.sort()

        # print "possible vertical moves from space " + space
        print possible_moves

        return possible_moves

    # Check to see if the given pieces are the same color (same case)
    def same_color_pieces(self, piece_1, piece_2):
        # print piece_1
        # print piece_2
        return (piece_1.isupper() and piece_2.isupper()) or (piece_1.islower() and piece_2.islower())

    # Get all possible diagonal moves from the given space
    def _get_possible_moves_diagonal(self, space):
        return []

    # Get the piece at the given space
    # If there is no piece at the given space, returns -1   # TODO - Should this return None instead?
    def get_piece_at(self, space):
        logger.debug("Getting piece at space [%s]", space)
        if self.is_valid_space(space):
            state_split = self.state[:(self.state.find(' '))].split("/")
            state_split = state_split[8 - int(space[1:])]
            piece = self._get_piece_at_index_in_row(state_split, ord(space[:1]) - 96)
            logger.debug("Piece at space [%s] is %s", space, piece)
            return piece
        else:
            logger.error("Invalid space: %s", space)
            return -1

    # Get the piece at the given index in the given row
    def _get_piece_at_index_in_row(self, row, index):
        counter = 1
        for piece in row:  # For each of the pieces in this piece's row
            if counter == index:
                return piece  # If it's the piece we're looking for, return it
            elif piece.isdigit():
                counter += int(piece)  # If the current piece is a digit, increment our counter accordingly
            else:
                counter += 1  # If the piece is not a digit or the one we're looking for, increment by 1
        logger.debug("piece not found at index [%s] of row [%s]", index, row)
        return -1

    # String representation override
    def __str__(self):
        return str(self.state)

# Won't get run if we import this as a reusable module
if __name__ == '__main__':
    # TODO - Turn these all into legit tests and put them in their own file

    g = Game()
    # g.get_possible_moves("a2")  # White Pawn 1
    # g.get_possible_moves("b2")  # White Pawn 2
    # print
    # g.get_possible_moves("a7")  # Black Pawn 1
    # g.get_possible_moves("b7")  # Black Pawn 2
    # print
    # g.get_possible_moves("e5")  # Nothing - Middle of board
    # print
    # g.get_possible_moves("e1")  # White King
    # print
    # g.get_possible_moves("e8")  # Black King
    # print
    # g.get_possible_moves("a1")  # White Rook 1
    # logger.info("-----------------------")
    # g.get_possible_moves("h1")  # White Rook 2

    # g.get_possible_moves('a1')

    g.get_all_possible_moves()

    # g.get_all_movable_pieces()

    # g.get_piece_at('a1')
    # g.get_piece_at('a2')
    # g.get_piece_at('b2')
    # g.get_piece_at('c2')
    # g.get_piece_at('d2')
    # g.get_piece_at('e2')
    # g.get_piece_at('f2')
    # g.get_piece_at('g2')
    # g.get_piece_at('h2')
    # g.get_piece_at('h1')

    # g.get_possible_moves("a1")  # White Rook
    # g.get_possible_moves("h1")  # White Rook
    # print
    # g.get_possible_moves("a8")  # Black Rook
    # g.get_possible_moves("h8")  # Black Rook
