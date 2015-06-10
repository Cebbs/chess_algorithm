__author__ = 'Conor'

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Game(object):
    # Initialize as a new game
    def __init__(self):
        self.state = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def get_all_possible_moves(self):
        movable_pieces = self.get_all_moveable_pieces()

    def get_all_movable_pieces(self):
        color = self.state.split(' ')[1]
        board_by_row = self.state.split(' ')[0].split('/')
        all_movable_pieces = {}

        if color == 'w':
            row_counter = 8
            for row in board_by_row:
                col_counter = 'a'
                for piece in row:
                    if piece.isupper():
                        all_movable_pieces[col_counter + str(row_counter)] = piece
                    col_counter = chr(ord(col_counter) + 1)
                row_counter -= 1
        else:
            row_counter = 8
            for row in board_by_row:
                col_counter = 'a'
                for piece in row:
                    if piece.islower():
                        all_movable_pieces[col_counter + str(row_counter)] = piece
                    col_counter = chr(ord(col_counter) + 1)
                row_counter -= 1

        print "All movable pieces:"
        print all_movable_pieces
        print
        print all_movable_pieces.keys()
        print all_movable_pieces.values()

        return all_movable_pieces

    # Get the possible moves for a piece at the given space
    def get_possible_moves(self, space):
        logger.debug("Getting possible moves for the piece at [%s]...", space)
        if self.is_valid_space(space):
            piece = self.get_piece_at(space)
            if not isinstance(piece, int):
                possible_moves = self.__get_possible_moves_for_piece(piece, space)
                logger.info("Possible moves for %s at space [%s]: [%s]", piece, space,
                            ', '.join(map(str, possible_moves)))
                return possible_moves
            else:
                logger.error("Could not get possible moves for the piece at [%s]: there is no piece at this space.",
                             space)
        else:
            logger.error("Could not get possible moves for the piece at [%s]: this is not a valid space", space)

    # Check if the given space is valid
    def is_valid_space(self, space):
        return len(space) == 2 and 'a' <= space[:1] <= 'h' and 1 <= int(space[1:]) <= 8

    # Check if the moves are valid
    def check_validity_of_moves(self, moves):
        return moves  # TODO -- Need for knight, pawn, and king -- is already handled by rook, queen, and bishop

    # Get all of the possible moves for the given piece at the given space
    def __get_possible_moves_for_piece(self, piece, space):

        direction = 1 if piece.isupper() else -1
        p = piece.lower()

        # Check if the piece is a pawn and is on a starting space, and therefore can move two spaces
        if (piece == 'p' and int(space[1:]) == 7) or (piece == 'P' and int(space[1:]) == 2):
            p += "_start"

        # Removed the dictionary lookup return block here because it built all possibilities on every lookup

        possible_moves = []
        if p == 'p':
            possible_moves = [space[:1] + str(int(space[1:]) + (1 * direction))]
        elif p == 'p_start':
            possible_moves = [space[:1] + str(int(space[1:]) + (1 * direction)),
                              space[:1] + str(int(space[1:]) + (2 * direction))]
        elif p == 'r':
            possible_moves = self.__get_possible_moves_for_rook(space)
        elif p == 'n':
            possible_moves = self.__get_possible_moves_for_knight(space)
        elif p == 'b':
            possible_moves = self.__get_possible_moves_for_bishop(space)
        elif p == 'q':
            possible_moves = self.__get_possible_moves_for_queen(space)
        elif p == 'k':
            possible_moves = self.__get_possible_moves_for_king(space)

        possible_moves = self.check_validity_of_moves(possible_moves)

        return possible_moves

    # Get all possible moves for a Knight
    def __get_possible_moves_for_knight(self, space):
        logger.debug("Getting possible moves for a Knight at [%s]", space)
        return [str(ord(space[:1]) + 1) + str(int(space[1:]) + 2),
                str(ord(space[:1]) - 1) + str(int(space[1:]) + 2),
                str(ord(space[:1]) + 1) + str(int(space[1:]) - 2),
                str(ord(space[:1]) - 1) + str(int(space[1:]) - 2),
                str(ord(space[:1]) + 2) + str(int(space[1:]) + 1),
                str(ord(space[:1]) - 2) + str(int(space[1:]) + 1),
                str(ord(space[:1]) + 2) + str(int(space[1:]) - 1),
                str(ord(space[:1]) - 2) + str(int(space[1:]) - 1)]

    # Get all possible moves for a King
    def __get_possible_moves_for_king(self, space):
        logger.debug("Getting possible moves for a King at [%s]", space)
        return [str(ord(space[:1]) + 1) + str(int(space[1:]) + 1),
                str(ord(space[:1]) + 1) + str(int(space[1:])),
                str(ord(space[:1]) + 1) + str(int(space[1:]) - 1),
                str(ord(space[:1]) - 1) + str(int(space[1:]) + 1),
                str(ord(space[:1]) - 1) + str(int(space[1:])),
                str(ord(space[:1]) - 1) + str(int(space[1:]) - 1),
                str(ord(space[:1])) + str(int(space[1:]) + 1),
                str(ord(space[:1])) + str(int(space[1:]) - 1)]

    # Get all of the possible move for a rook at the given space
    def __get_possible_moves_for_rook(self, space):
        logger.debug("Getting possible moves for Rook at [%s]", space)
        return self.__get_possible_moves_horizontal_and_vertical(space)

    # Get all of the possible moves for a queen at the given space
    def __get_possible_moves_for_queen(self, space):
        logger.debug("Getting possible moves for Queen at [%s]", space)
        return self.__get_possible_moves_horizontal_and_vertical(space) + self.get_possible_moves_diagonal(space)

    # Get all of the possible moves for a bishop at the given space
    def __get_possible_moves_for_bishop(self, space):
        logger.debug("Getting possible moves for Bishop at [%s]", space)
        return self.get_possible_moves_diagonal(space)

    # Get the possible horizontal and vertical moves from the given space
    def __get_possible_moves_horizontal_and_vertical(self, space):
        logger.debug("Getting horizontal and vertical moves from space [%s]", space)
        return self.__get_possible_moves_horizontal(space) + self.__get_possible_moves_vertical(space)

    # Get the possible horizontal moves from the given space
    def __get_possible_moves_horizontal(self, space):
        logger.debug("Getting possible moves in row")

        split_state = self.state.split(" ")[0].split("/")  # Split the board into rows
        occupied_spaces_in_row = {}  # Keep track of the pieces by their column number
        counter = 1  # Initialize counter

        # TODO - Clean up
        if len(split_state) > int(space[1:]):  # If the row is not empty       # TODO, will never be true (?)
            for piece in split_state[8 - int(space[1:])]:  # For each of the pieces in this piece's row...
                if piece.isdigit():  # If the piece is a number (blank space(s))...
                    counter += int(piece)  # Increase the counter by the number of blank space
                else:
                    occupied_spaces_in_row[(chr(counter + 96))] = piece
                    counter += 1
        else:
            print "Row was empty, skipped"  # TODO does this ever even happen?

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
    def __get_possible_moves_vertical(self, space):
        logger.debug("Getting possible vertical moves from space [%s]", space)

        state_split = self.state.split(' ')[0].split('/')

        occupied_spaces_in_column = {}
        counter = 8
        for row in state_split:
            if len(row) > ord(space[:1]) - 97:  # If there enough pieces in the row
                if not row[ord(space[:1]) - 97].isdigit():
                    occupied_spaces_in_column[counter] = row[ord(space[:1]) - 97]
            counter -= 1

        logger.debug("Occupied spaces in column: %s", ','.join(map(str, occupied_spaces_in_column.items())))

        occupied_row = occupied_spaces_in_column.keys()
        occupied_row.sort()  # Since the dictionary items are ordered arbitrarily

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

        if space[:1] in possible_moves:  # Just insurance, ever really true?
            possible_moves.remove(space[:1])

        possible_moves = map((lambda x: space[:1] + str(x)), possible_moves)
        possible_moves.sort()

        return possible_moves

    # Check to see if the given pieces are the same color (same case)
    def same_color_pieces(self, piece_1, piece_2):
        return (piece_1.isupper() and piece_2.isupper()) or (piece_1.islower() and piece_2.islower())

    # Get all possible diagonal moves from the given space
    def get_possible_moves_diagonal(self, space):
        return []

    # Get the piece at the given space
    def get_piece_at(self, space):
        logger.debug("Getting piece at space [%s]", space)
        if self.is_valid_space(space):
            state_split = self.state[:(self.state.find(' '))].split("/")
            state_split = state_split[8 - int(space[1:])]
            piece = self.__get_piece_at_index_in_row(state_split, ord(space[:1]) - 97)
            logger.debug("Piece at space [%s] is %s", space, piece)
            return piece
        else:
            logger.error("Invalid space: %s", space)
            return None

    # Get the piece at the given index in the given row
    def __get_piece_at_index_in_row(self, row, index):
        counter = 0
        for piece in row:  # For each of the pieces in this piece's row
            if counter == index:
                return piece
            elif piece.isdigit():
                counter += int(piece)
            else:
                counter += 1
        # print "Error: piece not found at index [" + str(index) + "] of row " + row
        logger.error("piece not found at index [%s] of row %s", index, row)
        return -1  # Handled

# TODO - Turn these all into legit tests

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

g.get_all_movable_pieces()

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
