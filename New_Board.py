# Chessboard is represented by numbers from 27 to 118.
# We don't start from 0 because we would not be able
# to easily detect edges of the board.


class Board:
    squares = {
        27: "a1",
        28: "b1",
        29: "c1",
        30: "d1",
        31: "e1",
        32: "f1",
        33: "g1",
        34: "h1",
        39: "a2",
        40: "b2",
        41: "c2",
        42: "d2",
        43: "e2",
        44: "f2",
        45: "g2",
        46: "h2",
        51: "a3",
        52: "b3",
        53: "c3",
        54: "d3",
        55: "e3",
        56: "f3",
        57: "g3",
        58: "h3",
        63: "a4",
        64: "b4",
        65: "c4",
        66: "d4",
        67: "e4",
        68: "f4",
        69: "g4",
        70: "h4",
        75: "a5",
        76: "b5",
        77: "c5",
        78: "d5",
        79: "e5",
        80: "f5",
        81: "g5",
        82: "h5",
        87: "a6",
        88: "b6",
        89: "c6",
        90: "d6",
        91: "e6",
        92: "f6",
        93: "g6",
        94: "h6",
        99: "a7",
        100: "b7",
        101: "c7",
        102: "d7",
        103: "e7",
        104: "f7",
        105: "g7",
        106: "h7",
        111: "a8",
        112: "b8",
        113: "c8",
        114: "d8",
        115: "e8",
        116: "f8",
        117: "g8",
        118: "h8"}

    # This subroutine checks whether is given square on the board.
    def square_on_board(self, square):
        none_true = self.squares.get(square)
        return none_true


# Positions of white pieces and generation of moves is stored in this class.
class WhitePieces(Board):
    def __init__(self):
        self.w_bishops = [32, 29]
        self.w_rooks = [27, 34]
        self.w_knights = [33, 28]
        self.w_king = [31]
        self.w_queen = [30]
        self.w_pawns = [39, 40, 41, 42, 43, 44, 45, 46]
        self.w_short_castling = True
        self.w_long_castling = True
        self.enpassant_can_be_taken_from = []
        self.last_row = [111, 112, 113, 114, 115, 116, 117, 118]
        self.w_moves = {}
        self.w_moves_list = []
        self.w_lists = [self.w_knights, self.w_pawns, self.w_queen, self.w_bishops, self.w_rooks, self.w_king]

    # moves pieces around the board
    # is used for making a move and checking if our king would be in check
    # if we are using this function only for the "check-check",then we have to pass
    # argument "trial"
    def move_a_piece(self, notation, trial):
        # this block of code handles castling
        # if king or rook moves, don't allow castling anymore
        if trial != "trial":
            if self.w_short_castling:
                if notation[0] == 31 or notation[0] == 34:
                    self.w_short_castling = False
                    if notation[1] == 33:
                        self.w_king[0] = 33
                        self.w_rooks.remove(34)
                        self.w_rooks.append(32)
                        return
            if self.w_long_castling:
                if notation[0] == 27 or notation[0] == 31:
                    self.w_long_castling = False
                    if notation[1] == 29:
                        self.w_king[0] = 29
                        self.w_rooks.remove(27)
                        self.w_rooks.append(30)
                        return
            if notation[1] == 118:
                b_pieces.b_short_castling = False
            if notation[1] == 111:
                b_pieces.b_long_castling = False
            if b_pieces.enpassant_can_be_taken_from:
                if notation[1] in b_pieces.enpassant_can_be_taken_from and notation[0] in self.w_pawns:
                    self.w_pawns.remove(notation[0])
                    self.w_pawns.append(notation[1])
                    b_pieces.b_pawns.remove(notation[1]-12)
                    b_pieces.enpassant_can_be_taken_from.clear()
                    return
                b_pieces.enpassant_can_be_taken_from.clear()

            # this block of code handles opponent's en passant
            # detect pawn double move
            if (notation[1] - notation[0]) == 24 and notation[0] in self.w_pawns:
                self.enpassant_can_be_taken_from.append(notation[1] - 12)

        # replace old position of the piece with new position
        for x in self.w_lists:
            counter = 0
            for z in x:
                if z == notation[0]:
                    x[counter] = notation[1]
                counter += 1

    # creates a dictionary with all possible moves in the position
    def create_moves_dict(self, trial):
        w_pawn = Pawns("white")
        w_knight = Knights("white")
        w_rook = LongRangePieces("rook", "white")
        w_bishop = LongRangePieces("bishop", "white")
        w_queen = LongRangePieces("queen", "white")
        w_king = King("white")
        w_knights_moves = w_knight.create_moves()
        w_rooks_moves = w_rook.create_moves()
        w_bishops_moves = w_bishop.create_moves()
        w_queen_moves = w_queen.create_moves()
        w_pawns_moves = w_pawn.create_basic_moves()
        w_king_moves = w_king.create_moves()
        # if we are only testing if our king would be hanging, we do not need to worry about opponents castling, because
        # you cannot take a piece with castling
        if trial == "create":
            w_king.create_castling("short")
            w_king.create_castling("long")
        self.w_moves = {**w_bishops_moves, **w_rooks_moves, **w_queen_moves, **w_knights_moves, **w_pawns_moves,
                        **w_king_moves}
        return self.w_moves

    # after a move is made, check if there are two pieces on one square
    # if so, delete the piece that was there first
    def delete_taken_pieces(self):
        b_pieces_counter = -1
        self.b_lists = [b_pieces.b_bishops, b_pieces.b_knights, b_pieces.b_pawns, b_pieces.b_queen, b_pieces.b_rooks]
        for b_piece_list in self.b_lists:
            b_pieces_counter += 1
            for b_position in b_piece_list:
                for w_piece_list in self.w_lists:
                    for w_position in w_piece_list:
                        if w_position == b_position:
                            b_piece_list.remove(b_position)
                            # This line is for the function that checks whether is certain move legal.
                            # If we delete a piece during the legal check, we have to revive it afterwards.
                            return [b_pieces_counter, b_position]

        # # promotion
        # for i in self.w_pawns:
        #     if i in self.last_row:
        #         self.w_pawns.remove(i)
        #         self.w_queen.append(i)

    # deletes illegal moves
    def delete_move_if_check(self):
        # create a nested list containing lists in the form [selected piece, next square]
        nested_list_of_moves = []
        delete_these_moves = []
        for x, y in self.w_moves.items():
            for i in y:
                piece_square_list = [x, i]
                nested_list_of_moves.append(piece_square_list)
        # try to make the move and generate black's threats, if one of the black's pieces attacks our king, then delete
        # the move from the list of possible moves
        for move in nested_list_of_moves:
            w_pieces.move_a_piece(move, "trial")
            # try to delete a piece if we take one, this variable stores information about the piece so we can return it
            # afterwards
            deleted_piece = w_pieces.delete_taken_pieces()
            b_attacks = b_pieces.create_moves_dict("trial")
            for lists in b_attacks.values():
                for square in lists:
                    if square == self.w_king[0]:
                        delete_these_moves.append(move)
            if deleted_piece:
                self.b_lists[deleted_piece[0]].append(deleted_piece[1])
            # we tried to execute the move to check if our king would be hanging, therefore we have to take the move
            # back
            reverse_move = [move[1], move[0]]
            w_pieces.move_a_piece(reverse_move, "trial")
        # it is not possible to delete an item directly in the process because it would mess up the 'for' loop
        for t in delete_these_moves:
            for u in nested_list_of_moves:
                if t == u:
                    nested_list_of_moves.remove(u)
        print(nested_list_of_moves)
        moves_in_dict = nested_list_to_dictionary(nested_list_of_moves)
        return moves_in_dict

def nested_list_to_dictionary(nested_list_of_moves):
    moves_dict = {}
    for x in nested_list_of_moves:
        print("x", x)
        if x[0] in moves_dict.keys():
            moves_dict[x[0]].append(x[1])
        else:
            moves_dict[x[0]] = [x[1]]
    return moves_dict


class BlackPieces(Board):
    def __init__(self):
        self.b_bishops = [113, 116]
        self.b_rooks = [111, 118]
        self.b_knights = [112, 117]
        self.b_king = [115]
        self.b_queen = [114]
        self.b_pawns = [99, 100, 101, 102, 103, 104, 105, 106]
        self.b_lists = [self.b_knights, self.b_pawns, self.b_queen, self.b_bishops, self.b_rooks, self.b_king]
        self.last_row = [27, 28, 29, 30, 31, 32, 33, 34]
        self.b_short_castling = True
        self.b_long_castling = True
        self.enpassant_can_be_taken_from = []
        self.b_moves = {}

    def move_a_piece(self, notation, trial):
        if trial != "trial":
            if self.b_short_castling:
                if notation[0] == 115 or notation[0] == 118:
                    self.b_short_castling = False
                    if notation[1] == 117:
                        self.b_king[0] = 117
                        self.b_rooks.remove(118)
                        self.b_rooks.append(116)
                        return
            if self.b_long_castling:
                if notation[0] == 111 or notation[0] == 115:
                    self.b_long_castling = False
                    if notation[1] == 113:
                        self.b_king[0] = 113
                        self.b_rooks.remove(111)
                        self.b_rooks.append(114)
                        return
            if notation[1] == 34:
                w_pieces.w_short_castling = False
            if notation[1] == 27:
                w_pieces.w_long_castling = False
            if w_pieces.enpassant_can_be_taken_from:
                if notation[1] in w_pieces.enpassant_can_be_taken_from and notation[0] in self.b_pawns:
                    self.b_pawns.remove(notation[0])
                    self.b_pawns.append(notation[1])
                    w_pieces.w_pawns.remove(notation[1]+12)
                    w_pieces.enpassant_can_be_taken_from.clear()
                    return
                w_pieces.enpassant_can_be_taken_from.clear()

            if (notation[1] - notation[0]) == -24 and notation[0] in self.b_pawns:
                self.enpassant_can_be_taken_from.append(notation[1] + 12)

        for x in self.b_lists:
            counter = 0
            for z in x:
                if z == notation[0]:
                    x[counter] = notation[1]
                counter += 1

    def create_moves_dict(self, trial):
        b_knight = Knights("black")
        b_rook = LongRangePieces("rook", "black")
        b_bishop = LongRangePieces("bishop", "black")
        b_queen = LongRangePieces("queen", "black")
        b_pawn = Pawns("black")
        b_king = King("black")
        b_knights_moves = b_knight.create_moves()
        b_rooks_moves = b_rook.create_moves()
        b_bishops_moves = b_bishop.create_moves()
        b_queen_moves = b_queen.create_moves()
        b_pawns_moves = b_pawn.create_basic_moves()
        b_king_moves = b_king.create_moves()
        if trial == "create":
            b_king.create_castling("short")
            b_king.create_castling("long")
        self.b_moves = {**b_bishops_moves, **b_rooks_moves,
                        **b_queen_moves, **b_knights_moves, **b_pawns_moves, **b_king_moves}
        return self.b_moves

    def delete_taken_pieces(self):
        # # promotion
        # for i in self.b_pawns:
        #     if i in self.last_row:
        #         self.b_pawns.remove(i)
        #         self.b_queen.append(i)

        w_pieces_counter = - 1
        self.w_lists = [w_pieces.w_bishops, w_pieces.w_knights, w_pieces.w_pawns, w_pieces.w_queen, w_pieces.w_rooks]
        for w_piece_list in self.w_lists:
            w_pieces_counter += 1
            for w_position in w_piece_list:
                for b_piece_list in self.b_lists:
                    for b_position in b_piece_list:
                        if b_position == w_position:
                            w_piece_list.remove(w_position)
                            return [w_pieces_counter, b_position]

    def delete_move_if_check(self):
        nested_list_of_moves = []
        delete_these_moves = []
        for x, y in self.b_moves.items():
            for i in y:
                piece_square_list = [x, i]
                nested_list_of_moves.append(piece_square_list)
        for move in nested_list_of_moves:
            b_pieces.move_a_piece(move, "trial")
            deleted_piece = b_pieces.delete_taken_pieces()
            w_attacks = w_pieces.create_moves_dict("trial")
            for lists in w_attacks.values():
                for square in lists:
                    if square == self.b_king[0]:
                        delete_these_moves.append(move)
            if deleted_piece:
                self.w_lists[deleted_piece[0]].append(deleted_piece[1])
            reverse_move = [move[1], move[0]]
            b_pieces.move_a_piece(reverse_move, "trial")
        for t in delete_these_moves:
            for u in nested_list_of_moves:
                if t == u:
                    nested_list_of_moves.remove(u)
        print(nested_list_of_moves)
        moves_in_dict = nested_list_to_dictionary(nested_list_of_moves)
        return moves_in_dict


class Occupation:
    def __init__(self):
        self.positions = []

    def get_occupation(self, white_or_black):
        if white_or_black == "w":
            self.positions = w_pieces.w_bishops + w_pieces.w_rooks + w_pieces.w_knights \
                             + w_pieces.w_king + w_pieces.w_queen + w_pieces.w_pawns
        if white_or_black == "b":
            self.positions = b_pieces.b_bishops + b_pieces.b_rooks + b_pieces.b_knights \
                             + b_pieces.b_king + b_pieces.b_queen + b_pieces.b_pawns
        occupation_list = []
        square_counter = 27
        while square_counter < 119:
            if square_counter in self.positions:
                occupation_list.append(square_counter)
            square_counter += 1
        return occupation_list


w_pieces = WhitePieces()
b_pieces = BlackPieces()
occupation = Occupation()
board = Board


class LongRangePieces(Board):
    def __init__(self, piece_type, side_to_move):
        Board.__init__(self)
        self.w_occupation = occupation.get_occupation("w")
        self.b_occupation = occupation.get_occupation("b")
        if side_to_move == "white":
            self.friendly_occup = self.w_occupation
            self.enemy_occup = self.b_occupation
            self.white = True
            self.black = False
        else:
            self.friendly_occup = self.b_occupation
            self.enemy_occup = self.w_occupation
            self.black = True
            self.white = False
        if piece_type == "rook":
            self.directions = [1, -1, 12, -12]
            if self.white:
                self.piece_position = w_pieces.w_rooks
            else:
                self.piece_position = b_pieces.b_rooks
        if piece_type == "bishop":
            self.directions = [-11, -13, 11, 13]
            if self.white:
                self.piece_position = w_pieces.w_bishops
            else:
                self.piece_position = b_pieces.b_bishops
        if piece_type == "queen":
            self.directions = [-11, -13, 11, 13, 1, -1, 12, -12]
            if self.white:
                self.piece_position = w_pieces.w_queen
            else:
                self.piece_position = b_pieces.b_queen

    def create_moves(self):
        moves_dict = {}
        # loop through the list with all pieces
        for i in self.piece_position:
            list_of_moves = []
            # loop through possible directions
            for x in self.directions:
                next_square = i
                # while not end of the board or a piece on the square, continue
                while True:
                    next_square += x
                    on_board = board.square_on_board(self, next_square)
                    if next_square in self.enemy_occup:
                        enemy_piece_on_square = True
                    else:
                        enemy_piece_on_square = False
                    if on_board and (next_square not in self.friendly_occup):
                        list_of_moves.append(next_square)
                        if enemy_piece_on_square:
                            break
                    else:
                        break
            moves_dict[i] = list_of_moves
        return moves_dict


class Knights(Board):
    def __init__(self, side_to_move):
        Board.__init__(self)
        self.w_occupation = occupation.get_occupation("w")
        self.b_occupation = occupation.get_occupation("b")
        if side_to_move == "white":
            self.friendly_occup = self.w_occupation
            self.enemy_occup = self.b_occupation
            self.piece_position = w_pieces.w_knights
        else:
            self.friendly_occup = self.b_occupation
            self.enemy_occup = self.w_occupation
            self.piece_position = b_pieces.b_knights
        self.directions = [25, -25, 23, -23, 14, -14, 10, -10]

    def create_moves(self):
        moves_dict = {}
        for i in self.piece_position:
            list_of_moves = []
            for x in self.directions:
                next_square = i + x
                on_board = board.square_on_board(self, next_square)
                if on_board and (next_square not in self.friendly_occup):
                    list_of_moves.append(next_square)
            moves_dict[i] = list_of_moves
        return moves_dict


class Pawns(Board):
    def __init__(self, side_to_move):
        Board.__init__(self)
        self.w_occupation = occupation.get_occupation("w")
        self.b_occupation = occupation.get_occupation("b")
        if side_to_move == "white":
            self.friendly_occup = self.w_occupation
            self.enemy_occup = self.b_occupation
            self.piece_position = w_pieces.w_pawns
            self.take_right = 13
            self.take_left = 11
            self.forward = 12
            self.double_move = 24
            self.first_row = [39, 40, 41, 42, 43, 44, 45, 46]
            self.take_enpassant = b_pieces.enpassant_can_be_taken_from
        else:
            self.friendly_occup = self.b_occupation
            self.enemy_occup = self.w_occupation
            self.piece_position = b_pieces.b_pawns
            self.take_right = -13
            self.take_left = -11
            self.forward = -12
            self.double_move = -24
            self.first_row = [99, 100, 101, 102, 103, 104, 105, 106]
            self.take_enpassant = w_pieces.enpassant_can_be_taken_from

    def create_basic_moves(self):
        moves_dict = {}
        list_of_moves = []
        # create moves forward for every pawn
        for i in self.piece_position:
            next_square = i + self.forward
            on_board = board.square_on_board(self, next_square)
            if on_board and (next_square not in self.friendly_occup and next_square not in self.enemy_occup):
                list_of_moves.append(next_square)
            # if pawns are on second row, append double moves
            if i in self.first_row and (i + self.double_move) not in self.friendly_occup and (
                    i + self.double_move) not in self.enemy_occup:
                list_of_moves.append(i + self.double_move)
            # append taking
            if i + self.take_right in self.enemy_occup or i + self.take_right in self.take_enpassant:
                list_of_moves.append(i + self.take_right)
            if i + self.take_left in self.enemy_occup or i + self.take_left in self.take_enpassant:
                list_of_moves.append(i + self.take_left)

            moves_dict[i] = list_of_moves
            list_of_moves = []
        return moves_dict


class King(Board):
    def __init__(self, side_to_move):
        Board.__init__(self)
        self.w_occupation = occupation.get_occupation("w")
        self.b_occupation = occupation.get_occupation("b")
        if side_to_move == "white":
            self.friendly_occup = self.w_occupation
            self.enemy_occup = self.b_occupation
            self.piece_position = w_pieces.w_king
            self.short_castling_allowed = w_pieces.w_short_castling
            self.long_castling_allowed = w_pieces.w_long_castling
            self.short_castling_squares = [32, 33]
            self.short_castling_check_squares = [31, 32, 33]
            self.long_castling_squares = [30, 29, 28]
            self.long_castling_check_squares = [31, 30, 29]
            self.white = True
        else:
            self.friendly_occup = self.b_occupation
            self.enemy_occup = self.w_occupation
            self.piece_position = b_pieces.b_king
            self.short_castling_allowed = b_pieces.b_short_castling
            self.long_castling_allowed = b_pieces.b_long_castling
            self.short_castling_squares = [116, 117]
            self.short_castling_check_squares = [115, 116, 117]
            self.long_castling_squares = [114, 113, 112]
            self.long_castling_check_squares = [115, 114, 113]
            self.white = False
        self.directions = [12, -12, 13, -13, 11, -11, 1, -1]
        self.moves_dict = {}

    def create_moves(self):
        for i in self.piece_position:
            list_of_moves = []
            for x in self.directions:
                next_square = i + x
                on_board = board.square_on_board(self, next_square)
                if on_board and (next_square not in self.friendly_occup):
                    list_of_moves.append(next_square)
            self.moves_dict[i] = list_of_moves
        return self.moves_dict

    def create_castling(self, long_or_short):
        if long_or_short == "short":
            castling_allowed = self.short_castling_allowed
            castling_squares = self.short_castling_squares
            castling_check_squares = self.short_castling_check_squares

        else:
            castling_allowed = self.long_castling_allowed
            castling_squares = self.long_castling_squares
            castling_check_squares = self.long_castling_check_squares

        # if the player didn't move his rook or king
        if castling_allowed:
            # check if there are any pieces in the way
            for i in castling_squares:
                if i in self.friendly_occup or i in self.enemy_occup:
                    return
                else:
                    # check if castling squares are attacked by enemy pieces
                    if self.white:
                        b_attacks = b_pieces.create_moves_dict("trial")
                        for p in b_attacks.values():
                            for x in p:
                                if x in castling_check_squares:
                                    return
                    else:
                        w_attacks = w_pieces.create_moves_dict("trial")
                        for p in w_attacks.values():
                            for x in p:
                                if x in castling_check_squares:
                                    return


            self.moves_dict[castling_check_squares[0]].append(
                castling_check_squares[-1])


# while True:
#     w_pieces.create_moves_dict("create")
#     w_pieces.delete_move_if_check()
#     select_piece = int(input("select a piece: "))
#     select_next_square = int(input("select a square: "))
#     send_this_move = [select_piece, select_next_square]
#     w_pieces.move_a_piece(send_this_move, "the_function_does_not_care")
#     w_pieces.delete_taken_pieces()
#
#     b_pieces.create_moves_dict("create")
#     b_pieces.delete_move_if_check()
#     select_piece = int(input("select a piece: "))
#     select_next_square = int(input("select a square: "))
#     send_this_move = [select_piece, select_next_square]
#     b_pieces.move_a_piece(send_this_move, "I_cannot_think_of_a_name")
#     b_pieces.delete_taken_pieces()

