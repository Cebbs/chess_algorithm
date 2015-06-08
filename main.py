import bisect

class Game(object):
    # Initialize as a new game
    def __init__(self):
        # TODO - Switch the white and black pieces, as it should be
        self.state = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr w KQkq - 0 1"

    def get_possible_moves(self, space):
        piece = self.get_piece_at(space)
        print "Possible moves for " + piece + "[" + space + "]: " + ','.join(
            map(str, self.get_possible_moves_for_piece(piece, space)))
        # TODO - Need to check if all of the moves are valid (for pawns, kings, knights)

    def is_valid_space(self, space):
        return len(space) == 2 and 'a' <= space[:1] <= 'h' and 1 <= int(space[1:]) <= 8

    # TODO - Make function shorter
    # TODO - Allow it to handle spaces that aren't a piece
    def get_possible_moves_for_piece(self, piece, space):

        direction = 1 if piece.isupper() else -1
        p = piece.lower()

        # Check if the piece is a pawn and is on a starting space, and therefore can move two spaces
        if (piece == 'p' and int(space[1:]) == 7) or (piece == 'P' and int(space[1:]) == 2):
            p += "_start"
        # if p == 'r':


        return {
            'p': [space[:1] + str(int(space[1:]) + (1 * direction))],  # TODO - Still need to check diagonal takes
            'p_start': [space[:1] + str(int(space[1:]) + (1 * direction)),  # TODO - Put in a new function
                        space[:1] + str(int(space[1:]) + (2 * direction))],
            'r': [self.get_possible_moves_for_rook(space)],
            'n': [str(ord(space[:1]) + 1) + str(int(space[1:]) + 2),  # TODO - Put in a new function
                  str(ord(space[:1]) - 1) + str(int(space[1:]) + 2),
                  str(ord(space[:1]) + 1) + str(int(space[1:]) - 2),
                  str(ord(space[:1]) - 1) + str(int(space[1:]) - 2),
                  str(ord(space[:1]) + 2) + str(int(space[1:]) + 1),
                  str(ord(space[:1]) - 2) + str(int(space[1:]) + 1),
                  str(ord(space[:1]) + 2) + str(int(space[1:]) - 1),
                  str(ord(space[:1]) - 2) + str(int(space[1:]) - 1)],
            'b': [self.get_possible_moves_for_bishop(space)],
            'q': [],  # TODO
            'k': [chr(ord(space[:1]) + 1) + str(int(space[1:]) + 1),  # TODO - Put in a new function
                  chr(ord(space[:1]) + 1) + str(int(space[1:])),
                  chr(ord(space[:1]) + 1) + str(int(space[1:]) - 1),
                  chr(ord(space[:1]) - 1) + str(int(space[1:]) + 1),
                  chr(ord(space[:1]) - 1) + str(int(space[1:])),
                  chr(ord(space[:1]) - 1) + str(int(space[1:]) - 1),
                  chr(ord(space[:1])) + str(int(space[1:]) + 1),
                  chr(ord(space[:1])) + str(int(space[1:]) - 1)
                  ]
        }[p]

    # Get all of the possible move for a rook at the given space
    def get_possible_moves_for_rook(self, space):
        return self.get_possible_moves_horizontal_and_vertical(space)

    # Get all of the possible moves for a queen at the given space
    def get_possible_moves_for_queen(self, space):
        return self.get_possible_moves_horizontal_and_vertical(space) + self.get_possible_moves_diagonal(space)

    # Get all of the possible moves for a bishop at the given space
    def get_possible_moves_for_bishop(self, space):
        return self.get_possible_moves_diagonal(space)

    def get_possible_moves_horizontal_and_vertical(self, space):

        split_state = self.state.split(" ")[0].split("/")  # Split the board into rows
        occupied_spaces_in_row = []  # Keep track of the pieces in the row by their index
        counter = 1  # Initialize counter

        # TODO - Clean up / divide into functions
        if len(split_state) > int(space[1:]):  # If the row is not empty       # TODO, will never be true (?)
            for piece in split_state[int(space[1:]) - 1]:  # For each of the pieces in this piece's row...
                if piece.isdigit():  # If the piece is a number (blank space(s))...
                    counter += int(piece)  # Increase the counter by the number of blank space
                elif (piece.isupper() and self.get_piece_at(space).isupper()) or \
                        (piece.islower() and self.get_piece_at(space).islower()):
                    # If the pieces are the same color
                    print "elif piece: " + piece + " -- " + self.get_piece_at(space)
                    occupied_spaces_in_row.append(chr(counter + 96))
                    counter += 1
                else:
                    # If the pieces are not the same color
                    # Go one space further and append that space (need to check if left or right)
                    counter += 1
        else:
            print "Row was empty, skipped"

        print "Occupied spaces in row: "
        print occupied_spaces_in_row
        piece_index = bisect.bisect(occupied_spaces_in_row, space[:1])
        # print piece_index
        first_piece_to_right = occupied_spaces_in_row[piece_index] if len(
            occupied_spaces_in_row) > piece_index else 'i'  # TODO Check logic i dont wanna im tired    # bug bug bug
        first_piece_to_left = occupied_spaces_in_row[piece_index - 1] if piece_index >= 1 else space[:1]

        print "first piece to right:" + first_piece_to_right
        print "first piece to left:" + first_piece_to_left

        possible_moves = []
        for letter in "abcdefgh":
            if first_piece_to_left < letter < first_piece_to_right:
                possible_moves.append(letter)

        # Make sure we can't move to the same space
        if space[:1] in possible_moves:  # TODO - kinda hacky
            possible_moves.remove(space[:1])

        possible_moves = map((lambda x: x + space[1:]), possible_moves)

        return possible_moves

    def get_possible_moves_diagonal(self, space):
        pass

    def get_piece_at(self, space):
        if self.is_valid_space(space):
            state_split = self.state[:(self.state.find(' '))].split("/")
            state_split = state_split[int(space[1:]) - 1]
            piece = self.get_piece_at_index_in_row(state_split, ord(space[:1]) - 97)
            # print "Piece at " + space + ": " + piece
            return piece
        else:
            print "Error, invalid space"  # TODO - Throw error
            return None

    def get_piece_at_index_in_row(self, row, index):
        counter = 0
        for piece in row:  # For each of the pieces in this piece's row
            if counter == index:
                return piece
            elif piece.isdigit():
                counter += int(piece)
            else:
                counter += 1

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
g.get_possible_moves("a1")  # White Rook 1
print
g.get_possible_moves("h1")  # White Rook 2


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
