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

    def square_on_board(self, square):
        none_true = self.squares.get(square)
        return none_true


class WhitePieces(Board):
    def __init__(self):
        self.w_bishops = [29, 32]
        self.w_rooks = [27, 34]
        self.w_knights = [28, 33]
        self.w_king = [31]
        self.w_queen = [30]
        self.w_pawns = [39, 40, 41, 42, 43, 44, 45, 46]

    def move_a_piece(self, selected_square):
        w_lists = [self.w_knights, self.w_pawns, self.w_queen, self.w_bishops, self.w_rooks]
        for x in w_lists:
            counter = 0
            for z in x:
                if z == selected_square:
                    x[counter] = int(input("insert a new move: "))
                counter += 1


class BlackPieces(Board):
    def __init__(self):
        self.b_bishops = [113, 116]
        self.b_rooks = [111, 118]
        self.b_knights = [112, 117]
        self.b_king = [115]
        self.b_queen = [114]
        self.b_pawns = [99, 100, 101, 102, 103, 104, 105, 106]

    def move_a_piece(self, selected_square):
        b_lists = [self.b_knights, self.b_pawns, self.b_queen, self.b_bishops, self.b_rooks]
        for x in b_lists:
            counter = 0
            for z in x:
                if z == selected_square:
                    x[counter] = int(input("insert a new move: "))
                counter += 1


class Occupation(WhitePieces, BlackPieces):
    def __init__(self):
        WhitePieces.__init__(self)
        BlackPieces.__init__(self)
        self.positions = []

    def get_occupation(self, white_or_black):
        if white_or_black == "w":
            self.positions = self.w_bishops + self.w_rooks + self.w_knights + self.w_king + self.w_queen + self.w_pawns
        if white_or_black == "b":
            self.positions = self.b_bishops + self.b_rooks + self.b_knights + self.b_king + self.b_queen + self.b_pawns
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


class LongRangePieces(Board):
    def __init__(self, piece_type, side_to_move):
        Board.__init__(self)
        self.w_occupation = occupation.get_occupation("w")
        self.b_occupation = occupation.get_occupation("b")
        if side_to_move == "white":
            self.friendly_occup = self.w_occupation
            self.enemy_occup = self.b_occupation
            self.white = True
        else:
            self.friendly_occup = self.b_occupation
            self.enemy_occup = self.w_occupation
            self.black = True
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
        board = Board
        for i in self.piece_position:
            list_of_moves = []
            for x in self.directions:
                next_square = i
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
            self.white = True
        else:
            self.friendly_occup = self.b_occupation
            self.enemy_occup = self.w_occupation
            self.piece_position = b_pieces.b_knights
            self.black = True
        self.directions = [25, -25, 23, -23, 14, -14, 10, -10]

    def create_moves(self):
        moves_dict = {}
        board = Board
        for i in self.piece_position:
            list_of_moves = []
            for x in self.directions:
                next_square = i + x
                on_board = board.square_on_board(self, next_square)
                if on_board and (next_square not in self.friendly_occup):
                    list_of_moves.append(next_square)
            moves_dict[i] = list_of_moves
        return moves_dict



while True:
    w_knight = Knights("white")
    w_rook = LongRangePieces("rook", "white")
    w_bishop = LongRangePieces("bishop", "white")
    w_queen = LongRangePieces("queen", "white")
    w_knights_moves = w_knight.create_moves()
    w_rooks_moves = w_rook.create_moves()
    w_bishops_moves = w_bishop.create_moves()
    w_queen_moves = w_queen.create_moves()
    w_moves = {**w_bishops_moves, **w_rooks_moves, **w_queen_moves, **w_knights_moves}
    print(w_moves)
    selected_square = int(input("make a move: "))
    w_pieces.move_a_piece(selected_square)
