import numpy as np
from copy import deepcopy


# the main class which holds all information about current position and generates legal moves
class Generator:
    def __init__(self):
        # board representation
        # starts from "a1" (=27), "b1" (=28), .... "h8" (=118)
        self.squares = [27, 28, 29, 30, 31, 32, 33, 34,
                        39, 40, 41, 42, 43, 44, 45, 46,
                        51, 52, 53, 54, 55, 56, 57, 58,
                        63, 64, 65, 66, 67, 68, 69, 70,
                        75, 76, 77, 78, 79, 80, 81, 82,
                        87, 88, 89, 90, 91, 92, 93, 94,
                        99, 100, 101, 102, 103, 104, 105, 106,
                        111, 112, 113, 114, 115, 116, 117, 118]
        # these two lists hold current locations of pieces in the form:
        # [ [pawns], [knights], [bishops], [rooks], [queen], [king]
        self.white_pieces = [[39, 40, 41, 42, 43, 44, 45, 46], [33, 28], [32, 29], [27, 34], [30], [31]]
        self.black_pieces = [[99, 100, 101, 102, 103, 104, 105, 106], [112, 117], [113, 116], [111, 118], [114], [115]]
        # castling allowed
        # initialised with all castling allowed as the king or rooks have not moved yet
        self.w_short_castle, self.w_long_castle = [True], [True]
        self.b_short_castle, self.b_long_castle = [True], [True]
        # stores a square if enpassant is possible
        self.enpassant_square = []
        # stores which squares are occupied by white and black
        self.white_occupation, self.black_occupation = None, None
        # temporary variables that will be needed to generate moves in many functions of this class
        self.my_pieces = None
        self.my_occupation = None
        self.enemy_occupation = None
        self.opponents_pieces = None
        self.short_castle = None
        self.long_castle = None
        self.up, self.down = None, None
        self.second_row, self.last_row, self.first_row = None, None, None

    # returns list of occupied squares
    @staticmethod
    def create_occupation_list(nested_list):
        occup_list = []
        for piece_type in nested_list:
            for piece_pos in piece_type:
                occup_list.append(piece_pos)
        return occup_list

    # save current position and return it in a dictionary
    def return_current_position(self):
        current_position = {
            'white': self.white_pieces,
            'black': self.black_pieces,
            'w_short': self.w_short_castle,
            'w_long': self.w_long_castle,
            'b_short': self.b_short_castle,
            'b_long': self.b_long_castle,
            'enpassant': self.enpassant_square}
        return current_position

    # return to previous position given previous position in a dictionary and side to move
    def go_back_to_previous_position(self, previous_position, side_to_move):
        if side_to_move == 'white':
            self.white_pieces = self.my_pieces = previous_position.get('white')
            self.black_pieces = self.opponents_pieces = previous_position.get('black')
            self.w_short_castle = self.short_castle = previous_position.get('w_short')
            self.w_long_castle = self.long_castle = previous_position.get('w_long')

        else:
            self.white_pieces = self.opponents_pieces = previous_position.get('white')
            self.black_pieces = self.my_pieces = previous_position.get('black')
            self.b_short_castle = self.short_castle = previous_position.get('b_short')
            self.b_long_castle = self.long_castle = previous_position.get('b_long')
        self.enpassant_square = previous_position.get('enpassant')
        self.set_up_attributes(side_to_move, create_occupation=False)


    # return True if given square is on the board
    def on_board(self, square):
        if square not in self.squares:
            return False
        else:
            return True

    def set_up_attributes(self, side_to_move, create_occupation=True):
        # create a list of pieces that is not nested, so we don't have to loop over the nested lists
        if create_occupation:
            self.white_occupation = self.create_occupation_list(self.white_pieces)
            self.black_occupation = self.create_occupation_list(self.black_pieces)
        if side_to_move == "white":
            self.my_pieces = self.white_pieces
            self.my_occupation = self.white_occupation
            self.enemy_occupation = self.black_occupation
            self.opponents_pieces = self.black_pieces
            self.short_castle = self.w_short_castle
            self.long_castle = self.w_long_castle
            self.up, self.down = 12, -12
            self.second_row, self.last_row, self.first_row = self.squares[8:16], self.squares[56:64], self.squares[0:8]
        else:
            self.my_pieces = self.black_pieces
            self.my_occupation = self.black_occupation
            self.enemy_occupation = self.white_occupation
            self.opponents_pieces = self.white_pieces
            self.short_castle = self.b_short_castle
            self.long_castle = self.b_long_castle
            self.up, self.down = -12, 12
            self.second_row, self.last_row, self.first_row = self.squares[48:56], self.squares[0:8], self.squares[56:64]

    def generate_moves(self, side_to_move, generate_only="all", opponents_attacks=None):
        self.set_up_attributes(side_to_move)
        # skip sliding pieces if we are only generating other attacks
        if generate_only != "other_attacks":
            # generate diagonal moves
            for move in self.sliding_pieces("diagonal", generate_only):
                yield move
            # generate rook moves for rooks and queens
            for move in self.sliding_pieces("heavy", generate_only):
                yield move
            # if we want to generate only sliding pieces, cut the function here
            if generate_only == "only_sliding":
                return
        # generate pawn moves
        for pawn_move in self.pawn_moves(generate_only):
            yield pawn_move

        # generate knight moves
        for knight_move in self.knight_moves(generate_only):
            yield knight_move

        # create king moves
        for king_move in self.king_moves(generate_only, opponents_attacks):
            yield king_move

        # castling does not attack anything
        if generate_only == "all":
            # castling
            if self.short_castle[0] and self.first_row[7] in self.my_pieces[3]:
                for move in self.castling(True, opponents_attacks):
                    yield move
            if self.long_castle[0] and self.first_row[0] in self.my_pieces[3]:
                for move in self.castling(False, opponents_attacks):
                    yield move

    # get moves of bishops, queens, and rooks
    # pass argument "diagonal" to get diagonal moves, anything else to get horizontal and vertical moves
    # pass "only_sliding" to get attacks, anything else to get moves
    def sliding_pieces(self, piece_type, generate_only):
        # there are two piece types that can move diagonally - bishops and the queen
        if piece_type == "diagonal":
            slide_pieces = [self.my_pieces[2], self.my_pieces[4]]
            # a single vertical step
            # e.g. 13 is up and right, -11 is down and right
            directions = [13, 11, -11, -13]
        # there are two piece types that can move horizontally & vertically - rooks and the queen
        else:
            slide_pieces = [self.my_pieces[3], self.my_pieces[4]]
            # 12 and -12 are vertical moves, 1 and -1 are horizontal moves
            directions = [12, 1, -1, -12]
        # for both piece types
        for x in slide_pieces:
            # for every piece of current piece type
            for piece_pos in x:
                # for every direction
                for dir in directions:
                    # save current position of the piece to variable "next_square"
                    next_square = piece_pos
                    # slide the piece in current direction until there is a piece
                    # in the way or end of the board
                    while True:
                        next_square += dir
                        # check if the next square is on board
                        if not (self.on_board(next_square)):
                            break
                        # if friendly piece in the way
                        if next_square in self.my_occupation:
                            # if we are generating attacks, then yield even our defended pieces
                            # (if we are using this function to find defended squares)
                            if generate_only == "only_sliding":
                                yield [piece_pos, next_square]
                            # break, because we are not allowed to take our own piece
                            break
                        # if opponents piece in the way
                        if next_square in self.enemy_occupation:
                            # yield the move and break
                            # this is different to "if friendly piece in the way" because
                            # we can take enemy piece
                            yield [piece_pos, next_square]
                            # break because it is not allowed to jump over enemy pieces
                            break
                        # if there is nothing in the way or end of the board, yield the move
                        # and continue sliding to the next square
                        yield [piece_pos, next_square]

    # generates long or short castling moves
    def castling(self, short, opponents_attacks):
        # if we want to generate short castling
        if short:
            # there squares has to be empty
            castle_occup_squares = [self.first_row[5], self.first_row[6]]
            # there squares cannot be under opponents
            # attack, otherwise castling would be illegal
            castle_check_squares = [self.first_row[4], self.first_row[5], self.first_row[6]]
        # if we want to generate long castling
        else:
            castle_occup_squares = [self.first_row[3], self.first_row[2], self.first_row[1]]
            castle_check_squares = [self.first_row[4], self.first_row[3], self.first_row[2]]
        # check if are the castling squares occupied
        stop = False
        for square in castle_occup_squares:
            if square in self.my_occupation or square in self.enemy_occupation:
                stop = True
                break
            # check if are castling squares attacked
            for square in castle_check_squares:
                if square in opponents_attacks:
                    stop = True
                    break
        # if there is nothing "wrong" with the critical squares
        # yield the move
        if not stop:
            yield [self.my_pieces[5][0], castle_check_squares[-1]]

    def pawn_moves(self, generate_only):
        # generate pawn moves
        # for every pawn:
        for pawn in self.my_pieces[0]:
            # pawns always attack squares diagonally in front of them
            # yield all attacked squares if generating attacks
            # (this piece of code (next 6 lines) is only used if we
            #  need to find attacked squares and not all possible moves)
            if generate_only == "other_attacks":
                if self.on_board(pawn + self.up + 1):
                    yield [pawn, pawn + self.up + 1]
                if self.on_board(pawn + self.up + -1):
                    yield [pawn, pawn + self.up + -1]
                continue

            # yield that it is possible to take enemy piece if there is an enemy piece on the square
            # or if the horizontal up move is in "enpassant_square"
            # up and right
            if (pawn + self.up + 1) in self.enemy_occupation or (pawn + self.up + 1) in self.enpassant_square:
                yield [pawn, pawn + self.up + 1]
            # up and left
            if (pawn + self.up + -1) in self.enemy_occupation or (pawn + self.up - 1) in self.enpassant_square:
                yield [pawn, pawn + self.up + -1]
            # move up
            # pawns do not attack squares in front of them, therefore we want to skip next few lines if we are
            # using this function only to generate attacks
            if generate_only != "other_attacks":
                # if there is no piece in front of the pawn
                if (pawn + self.up) not in self.enemy_occupation and (pawn + self.up) not in self.my_occupation:
                    yield [pawn, pawn + self.up]
                    # yield possible double move if pawns on initial squares
                    if pawn in self.second_row:
                        if (pawn + self.up * 2) not in self.enemy_occupation and (
                                pawn + self.up * 2) not in self.my_occupation:
                            yield [pawn, pawn + self.up * 2]

    def knight_moves(self, generate_only):
        # for every knight
        for knight in self.my_pieces[1]:
            directions = [25, -25, 23, -23, 14, -14, 10, -10]
            # for every direction
            for dir in directions:
                next_square = knight + dir
                # if the next square exist
                if self.on_board(next_square):
                    # append defended squares if argument generate_only
                    # is "other_attacks"
                    if generate_only == "other_attacks":
                        yield [knight, next_square]
                        continue
                    #  do not yield moves that would result in taking our own piece
                    if next_square not in self.my_occupation:
                        yield [knight, next_square]

    def king_moves(self, generate_only, opponents_attacks):
        directions = [-11, -12, -13, -1, 1, 11, 12, 13]
        # for every direction
        for direction in directions:
            next_square = self.my_pieces[5][0] + direction
            if self.on_board(next_square):
                # even kings do attack squares, this is useful especially
                # to not allow kings to attack each other
                # (kings cannot take each other)
                if generate_only == "other_attacks":
                    yield [self.my_pieces[5][0], next_square]
                    continue

                # don't allow king to enter attacked squares
                if next_square not in opponents_attacks:
                    # don't allow the king to take its own pieces
                    if next_square not in self.my_occupation:
                        yield [self.my_pieces[5][0], next_square]

    def make_a_move(self, move):
        # enpassant
        self.play_enpassant(move)

        # castling
        self.play_castling(move)

        # if the move is a pawn double move, append the square
        # that is one place behind the pawn's final position to self.enpassant.
        # self.enpassant will always hold the variable only for one turn
        # because the pawn can be taken only immediately (rules of chess)
        # the "enpassant_square" variable is reset in the function self.play_enpassant
        if move[0] in self.my_pieces[0] and (15 < (move[1] - move[0]) or (move[1] - move[0]) < -15):
            self.enpassant_square.append(move[0] + 0.5 * (move[1] - move[0]))

        # the move representation does not tell us which piece do we need to move
        # therefore, we need to cycle through all piece positions and check
        # if any of them equals the initial square

        # replace old position of our piece with a new one
        # for piece type in friendly pieces
        for i, piece_type in enumerate(self.my_pieces):
            # for a piece position in the piece type
            for index, position in enumerate(piece_type):
                # if the position is equal to the square to move the piece from
                if position == move[0]:
                    # replace the initial position with a new one
                    self.my_pieces[i][index] = move[1]
                    # the move is made

        # promote pawns
        self.promote_pawn()

        # delete taken pieces
        # if any black piece position equals the final square "move[1]"
        # delete the piece, because it is taken
        for x, enemy_piece_type in enumerate(self.opponents_pieces[:5]):
            for index, position in enumerate(enemy_piece_type):
                if position == move[1]:
                    self.opponents_pieces[x].pop(index)

    # play enpassant
    def play_enpassant(self, move):
        # if it is possible to play enpassant]
        # try:
        if self.enpassant_square:
            # if given move is enpassant
            if move[0] in self.my_pieces[0] and move[1] in self.enpassant_square and move[1] - move[0] \
                    in [11, -11, 13, -13]:
                # replace old position of friendly pawn with a new one
                self.my_pieces[0][self.my_pieces[0].index(move[0])] = move[1]
                # remove enemy pawn that is taken during enpassant
                self.opponents_pieces[0].remove(move[1] + self.down)

        # except ValueError:
        #     pass
        # enpassant can be played only immediately, therefore
        # clear the enpassant square
        self.enpassant_square.clear()

    def play_castling(self, move):
        # if short castle is possible
        if self.short_castle[0]:
            # don't allow castling from now on if a rook or king is moved
            if move[0] == self.first_row[7] or move[0] == self.first_row[4]:
                self.short_castle[0] = False
            # detect whether given move annotates castling
            if move == [self.first_row[4], self.first_row[6]] and move[0] in self.my_pieces[5]:
                # update king position
                self.my_pieces[5][0] = self.first_row[6]
                # update rook position
                self.my_pieces[3][self.my_pieces[3].index(self.first_row[7])] = self.first_row[5]
                self.short_castle[0] = False
                return

        # if long castle is possible
        if self.long_castle[0]:
            # don't allow castling from now on if a rook or king is moved
            if move[0] == self.first_row[0] or move[0] == self.first_row[4]:
                self.long_castle[0] = False
            if move == [self.first_row[4], self.first_row[2]] and move[0] in self.my_pieces[5]:
                # update king position
                self.my_pieces[5][0] = self.first_row[2]
                # update rook position
                self.my_pieces[3][self.my_pieces[3].index(self.first_row[0])] = self.first_row[3]
                self.long_castle[0] = False
                return

    def promote_pawn(self):
        for position in self.my_pieces[0]:
            if position in self.last_row:
                self.my_pieces[0].remove(position)
                self.my_pieces[4].append(position)

    def detect_check(self, enemy_attacks):
        if self.my_pieces[5][0] in enemy_attacks:
            return True

    def reset_board(self):
        self.white_pieces = [[39, 40, 41, 42, 43, 44, 45, 46], [33, 28], [32, 29], [27, 34], [30], [31]]
        self.black_pieces = [[99, 100, 101, 102, 103, 104, 105, 106], [112, 117], [113, 116], [111, 118], [114], [115]]
        self.w_short_castle, self.w_long_castle = [True], [True]
        self.b_short_castle, self.b_long_castle = [True], [True]
        self.enpassant_square = []


# crete an instance of the class Generator
generator = Generator()


# create a list of all possible moves
def create_moves(side_to_move, validate=True):
    if side_to_move == "white":
        enemy_side = "black"
    else:
        enemy_side = "white"
    moves = []
    sliding_attacks = []
    other_attacks = []
    defended_squares = []
    check = False
    # generate squares that are attacked by black sliding pieces
    for move in generator.generate_moves(enemy_side, generate_only="only_sliding"):
        sliding_attacks.append(move[-1])
    # generate squares that are attacked by every other black piece
    for move in generator.generate_moves(enemy_side, generate_only="other_attacks"):
        other_attacks.append(move[-1])
    # generate white defended squares (this is only for creating datasets:
    for move in generator.generate_moves(side_to_move, generate_only="other_attacks"):
        defended_squares.append(move[1])
    for move in generator.generate_moves(side_to_move, generate_only="only_sliding"):
        defended_squares.append(move[1])
    # generate all white moves
    for move in generator.generate_moves(side_to_move, opponents_attacks=sliding_attacks + other_attacks):
        moves.append(move)

    if not validate:
        return moves
    trial_attacks = []
    moves_to_be_deleted = []
    if generator.detect_check(other_attacks + sliding_attacks):
        for move in moves:
            for x in validate_legality(side_to_move, enemy_side, move, trial_attacks):
                moves_to_be_deleted.append(x)
    else:
        # if we are not in check, then check for validate only pieces that are under attacks of sliding pieces
        for move in moves:
            if move[0] in sliding_attacks:
                for x in validate_legality(side_to_move, enemy_side, move, trial_attacks):
                    moves_to_be_deleted.append(x)

    moves = [x for x in moves if x not in moves_to_be_deleted]

    return moves


# Play given move on the board and find which squares are attacked
# by enemy pieces.
# If our king would end up being in a check, the move is illegal
def validate_legality(side_to_move, enemy_side, move, trial_attacks):
    moves_to_be_deleted = []
    current_position = deepcopy(generator.return_current_position())

    generator.make_a_move(move)
    # generate squares that are attacked by black sliding pieces
    for attack in generator.generate_moves(enemy_side, generate_only="only_sliding"):
        trial_attacks.append(attack[1])
    for attack in generator.generate_moves(enemy_side, generate_only="other_attacks"):
        trial_attacks.append(attack[1])
    generator.set_up_attributes(side_to_move)
    if generator.detect_check(trial_attacks):
        moves_to_be_deleted.append(move)
    generator.go_back_to_previous_position(current_position, side_to_move)
    trial_attacks.clear()

    return moves_to_be_deleted


# get a matrix representation of current position
def convert_to_matrix(side_to_move, enemy_attacks=None, defended_squares=None, check=None):
    square_list = []
    board_list = []
    ranks = []
    board = [[111, 112, 113, 114, 115, 116, 117, 118],
          [99, 100, 101, 102, 103, 104, 105, 106],
          [87, 88, 89, 90, 91, 92, 93, 94],
          [75, 76, 77, 78, 79, 80, 81, 82],
          [63, 64, 65, 66, 67, 68, 69, 70],
          [51, 52, 53, 54, 55, 56, 57, 58],
          [39, 40, 41, 42, 43, 44, 45, 46],
          [27, 28, 29, 30, 31, 32, 33, 34]]

    # *8
    for rank_index, rank in enumerate(board):
        # *8
        for square_index, square in enumerate(rank):
            # *6
            for i in range(6):
                if square in generator.white_pieces[i]:
                    square_list.append(1)
                else:
                    square_list.append(0)
                if square in generator.black_pieces[i]:
                    square_list.append(-1)
                else:
                    square_list.append(0)

            square_array = np.asarray(square_list)
            ranks.append(square_array)
            square_list.clear()
        ranks_array = np.asarray(ranks)
        board_list.append(ranks_array)
        ranks.clear()

    board_array = np.asarray(board_list)
    return board_array

