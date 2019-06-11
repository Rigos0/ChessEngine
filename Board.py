class Board():
    def __init__(self):
        Board.w_bishops = [29, 32]
        Board.w_rooks = [27, 34]
        Board.w_knights = [28, 33]
        Board.w_king = [31]
        Board.w_queen = [30]
        Board.w_pawns = [39, 40, 41, 42, 43, 44, 45, 46]
        Board.b_bishops = [113, 116]
        Board.b_rooks = [111, 118]
        Board.b_knights = [112, 117]
        Board.b_king = [115]
        Board.b_queen = [114]
        Board.b_pawns = [99, 100, 101, 102, 103, 104, 105, 106]
        Board.w_bishops_moves = []
        Board.w_rooks_moves = []
        Board.w_knights_moves = []
        Board.w_king_moves = []
        Board.w_queen_moves = []
        Board.w_pawns_moves = []
        Board.w_taking = []
        Board.b_bishops_moves = []
        Board.b_rooks_moves = []
        Board.b_knights_moves = []
        Board.b_king_moves = []
        Board.b_queen_moves = []
        Board.b_pawns_moves = []
        Board.b_taking = []
        Board.piece = 0

        Board.w_occupation = {
            27: True,
            28: True,
            29: True,
            30: True,
            31: True,
            32: True,
            33: True,
            34: True,
            39: True,
            40: True,
            41: True,
            42: True,
            43: True,
            44: True,
            45: True,
            46: True,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
            69: False,
            70: False,
            75: False,
            76: False,
            77: False,
            78: False,
            79: False,
            80: False,
            81: False,
            82: False,
            87: False,
            88: False,
            89: False,
            90: False,
            91: False,
            92: False,
            93: False,
            98: False,
            99: False,
            100: False,
            101: False,
            102: False,
            103: False,
            104: False,
            105: False,
            106: False,
            111: False,
            112: False,
            113: False,
            114: False,
            115: False,
            116: False,
            117: False,
            118: False,
        }
        Board.b_occupation = {
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            39: False,
            40: False,
            41: False,
            42: False,
            43: False,
            44: False,
            45: False,
            46: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
            69: False,
            70: False,
            75: False,
            76: False,
            77: False,
            78: False,
            79: False,
            80: False,
            81: False,
            82: False,
            87: False,
            88: False,
            89: False,
            90: False,
            91: False,
            92: False,
            93: False,
            98: False,
            99: True,
            100: True,
            101: True,
            102: True,
            103: True,
            104: True,
            105: True,
            106: True,
            111: True,
            112: True,
            113: True,
            114: True,
            115: True,
            116: True,
            117: True,
            118: True,
        }
        Board.squares = {
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
            118: "h8"
        }

    def piece1(self):
        Board.piece = 0

    def piece2(self):
        Board.piece = 1

    def piece3(self):
        Board.piece = 2

    def piece4(self):
        Board.piece = 3

    def piece5(self):
        Board.piece = 4

    def piece6(self):
        Board.piece = 5

    def piece7(self):
        Board.piece = 6

    def piece8(self):
        Board.piece = 7


class Move(Board):
    def __init__(self):
        Board.__init__(self)
        Move.dots = []
        Move.b_dots = []

    def w_get_squares(self, selected_square):
        Move.dots = []
        inserted = selected_square
        w_lists = [Board.w_knights_moves, Board.w_pawns_moves, Board.w_queen_moves, Board.w_bishops_moves,
                   Board.w_rooks_moves, Board.w_king_moves, Board.w_taking]

        for x in w_lists:
            for i in x:
                try:
                    curr_square = i[0] + i[1]
                    if curr_square == inserted:
                        next_square = i[3] + i[4]
                        Move.dots.append(next_square)

                except IndexError:
                    pass

    def b_get_squares(self, b_selected_square):
        Move.b_dots = []
        inserted = b_selected_square
        b_lists = [Board.b_knights_moves, Board.b_pawns_moves, Board.b_queen_moves, Board.b_bishops_moves,
                   Board.b_rooks_moves, Board.b_king_moves]
        for x in b_lists:
            for i in x:
                try:
                    curr_square = i[0] + i[1]
                    if curr_square == inserted:
                        next_square = i[3] + i[4]
                        Move.b_dots.append(next_square)

                except IndexError:
                    pass

    def w_make_move(self, square_to_go):
        inserted = square_to_go
        sel_piece = inserted[0] + inserted[1]
        key_list = list(Board.squares.keys())
        val_list = list(Board.squares.values())
        piece = (key_list[val_list.index(sel_piece)])
        sel_square = inserted[3] + inserted[4]
        new_pos = (key_list[val_list.index(sel_square)])

        if inserted in Board.w_bishops_moves:
            piece_position = Board.w_bishops.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.w_occupation[piece] = False
            Board.w_bishops[piece_position] = new_pos
            Board.w_occupation[new_pos] = True

        if inserted in Board.w_rooks_moves:
            try:
                piece_position = Board.w_rooks.index(piece)
                sel_square = inserted[3] + inserted[4]
                new_pos = (key_list[val_list.index(sel_square)])
                Board.w_occupation[piece] = False
                Board.w_rooks[piece_position] = new_pos
                Board.w_occupation[new_pos] = True
            except ValueError:
                pass

        if inserted in Board.w_knights_moves:
            Board.w_occupation[piece] = False
            piece_position = Board.w_knights.index(piece)
            Board.w_knights[piece_position] = new_pos
            Board.w_occupation[new_pos] = True
            Board.w_knights_moves = []

        if inserted in Board.w_king_moves:
            piece_position = Board.w_king.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.w_occupation[piece] = False
            Board.w_king[piece_position] = new_pos
            Board.w_occupation[new_pos] = True

        if inserted in Board.w_queen_moves:
            piece_position = Board.w_queen.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.w_occupation[piece] = False
            Board.w_queen[piece_position] = new_pos
            Board.w_occupation[new_pos] = True

        if inserted in Board.w_pawns_moves:
            piece_position = Board.w_pawns.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.w_occupation[piece] = False
            Board.w_pawns[piece_position] = new_pos
            Board.w_occupation[new_pos] = True

        if inserted in Board.w_taking:
            b_lists = [Board.b_knights, Board.b_pawns, Board.b_queen, Board.b_bishops, Board.b_rooks]
            for x in b_lists:
                if new_pos in x:
                    piece_index = x.index(new_pos)
                    del x[piece_index]
                    Board.b_occupation[new_pos] = False
            w_lists = [Board.w_knights, Board.w_pawns, Board.w_queen, Board.w_bishops, Board.w_rooks]
            for x in w_lists:
                if piece in x:
                    piece_position = x.index(piece)
                    sel_square = inserted[3] + inserted[4]
                    new_pos = (key_list[val_list.index(sel_square)])
                    Board.w_occupation[piece] = False
                    x[piece_position] = new_pos
                    Board.w_occupation[new_pos] = True

    def b_make_move(self, b_square_to_go):
        inserted = b_square_to_go
        sel_piece = inserted[0] + inserted[1]
        key_list = list(Board.squares.keys())
        val_list = list(Board.squares.values())
        piece = (key_list[val_list.index(sel_piece)])
        sel_square = inserted[3] + inserted[4]
        new_pos = (key_list[val_list.index(sel_square)])

        if inserted in Board.b_bishops_moves:
            piece_position = Board.b_bishops.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_occupation[piece] = False
            Board.b_bishops[piece_position] = new_pos
            Board.b_occupation[new_pos] = True

        if inserted in Board.b_rooks_moves:
            piece_position = Board.b_rooks.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_occupation[piece] = False
            Board.b_rooks[piece_position] = new_pos
            Board.b_occupation[new_pos] = True

        if inserted in Board.b_knights_moves:
            Board.b_occupation[piece] = False
            piece_position = Board.b_knights.index(piece)
            Board.b_knights[piece_position] = new_pos
            Board.b_occupation[new_pos] = True

        if inserted in Board.b_king_moves:
            piece_position = Board.b_king.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_occupation[piece] = False
            Board.b_king[piece_position] = new_pos
            Board.b_occupation[new_pos] = True

        if inserted in Board.b_queen_moves:
            piece_position = Board.b_queen.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_occupation[piece] = False
            Board.b_queen[piece_position] = new_pos
            Board.b_occupation[new_pos] = True

        if inserted in Board.b_pawns_moves:
            piece_position = Board.b_pawns.index(piece)
            sel_square = inserted[3] + inserted[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_occupation[piece] = False
            Board.b_pawns[piece_position] = new_pos
            Board.b_occupation[new_pos] = True

        if inserted in Board.b_taking:
            w_lists = [Board.w_knights, Board.w_pawns, Board.w_queen, Board.w_bishops, Board.w_rooks]
            for x in w_lists:
                if new_pos in x:
                    piece_index = x.index(new_pos)
                    del x[piece_index]
                    Board.w_occupation[new_pos] = False
            b_lists = [Board.b_knights, Board.b_pawns, Board.b_queen, Board.b_bishops, Board.b_rooks]
            for x in b_lists:
                if piece in x:
                    piece_position = x.index(piece)
                    sel_square = inserted[3] + inserted[4]
                    new_pos = (key_list[val_list.index(sel_square)])
                    Board.b_occupation[piece] = False
                    x[piece_position] = new_pos
                    Board.b_occupation[new_pos] = True

    def print_w_moves(self):
        for i in range(len(Board.w_pawns_moves)):
            print(Board.w_pawns_moves[i])
        for i in range(len(Board.w_knights_moves)):
            print(Board.w_knights_moves[i])
        for i in range(len(Board.w_taking)):
            print(Board.w_taking[i])
        for i in range(len(Board.w_king_moves)):
            print(Board.w_king_moves[i])
        for i in range(len(Board.w_rooks_moves)):
            print(Board.w_rooks_moves[i])
        for i in range(len(Board.w_bishops_moves)):
            print(Board.w_bishops_moves[i])
        for i in range(len(Board.w_queen_moves)):
            print(Board.w_queen_moves[i])

    def print_b_moves(self):
        for i in range(len(Board.b_pawns_moves)):
            print(Board.b_pawns_moves[i])
        for i in range(len(Board.b_knights_moves)):
            print(Board.b_knights_moves[i])
        for i in range(len(Board.b_taking)):
            print(Board.b_taking[i])
        for i in range(len(Board.b_king_moves)):
            print(Board.b_king_moves[i])
        for i in range(len(Board.b_rooks_moves)):
            print(Board.b_rooks_moves[i])
        for i in range(len(Board.b_bishops_moves)):
            print(Board.b_bishops_moves[i])
        for i in range(len(Board.b_queen_moves)):
            print(Board.b_queen_moves[i])

    def clean_piece_moves(self):
        Board.w_pawns_moves = []
        Board.w_queen_moves = []
        Board.w_rooks_moves = []
        Board.b_rooks_moves = []
        Board.w_knights_moves = []
        Board.w_bishops_moves = []
        Board.b_pawns_moves = []
        Board.b_knights_moves = []
        Board.b_queen_moves = []
        Board.w_taking = []
        Board.b_taking = []
        Board.w_king_moves = []
        Board.b_king_moves = []
        Board.b_bishops_moves = []

    def delete_duplicates(self):
        Board.w_pawns_moves = set(Board.w_pawns_moves)
        Board.w_pawns_moves = list(Board.w_pawns_moves)
        Board.w_queen_moves = set(Board.w_queen_moves)
        Board.w_queen_moves = list(Board.w_queen_moves)
        Board.w_rooks_moves = set(Board.w_rooks_moves)
        Board.w_rooks_moves = list(Board.w_rooks_moves)
        Board.b_rooks_moves = set(Board.b_rooks_moves)
        Board.b_rooks_moves = list(Board.b_rooks_moves)
        Board.w_knights_moves = set(Board.w_knights_moves)
        Board.w_knights_moves = list(Board.w_knights_moves)
        Board.w_bishops_moves = set(Board.w_bishops_moves)
        Board.w_bishops_moves = list(Board.w_bishops_moves)
        Board.b_bishops_moves = set(Board.b_bishops_moves)
        Board.b_bishops_moves = list(Board.b_bishops_moves)
        Board.b_pawns_moves = set(Board.b_pawns_moves)
        Board.b_pawns_moves = list(Board.b_pawns_moves)
        Board.b_knights_moves = set(Board.b_knights_moves)
        Board.b_knights_moves = list(Board.b_knights_moves)
        Board.b_queen_moves = set(Board.b_queen_moves)
        Board.b_queen_moves = list(Board.b_queen_moves)
        Board.w_king_moves = set(Board.w_king_moves)
        Board.w_king_moves = list(Board.w_king_moves)
        Board.b_king_moves = set(Board.b_king_moves)
        Board.b_king_moves = list(Board.b_king_moves)
        Board.w_taking = set(Board.w_taking)
        Board.w_taking = list(Board.w_taking)
        Board.b_taking = set(Board.b_taking)
        Board.b_taking = list(Board.b_taking)

    def w_take(self):
        w_lists = [Board.w_knights, Board.w_pawns, Board.w_queen, Board.w_bishops, Board.w_rooks]
        for positions in w_lists:
            for i in positions:
                occupied = Board.w_occupation.get(i)
                if not occupied:
                    del positions[positions.index(i)]

    def b_take(self):
        b_lists = [Board.b_knights, Board.b_pawns, Board.b_queen, Board.b_bishops, Board.b_rooks]
        for positions in b_lists:
            for i in positions:
                occupied = Board.b_occupation.get(i)
                if not occupied:
                    del positions[positions.index(i)]


class WhiteKnight(Board):
    def __init__(self):
        Board.__init__(self)

    def w_knight_move(self):
        moves = [25, -25, 23, -23, 14, -14, 10, -10]
        for i in range(8):
            self.move = Board.w_knights[Board.piece] + moves[i]
            w_occup = Board.w_occupation.get(self.move)
            convert = (Board.squares.get(self.move))
            if w_occup:
                pass
            else:
                if convert:
                    converted_move = (Board.squares.get(Board.w_knights[Board.piece])) + "-" + convert
                    Board.w_knights_moves.append(converted_move)
                    self.move = int
            b_occup = Board.b_occupation.get(self.move)
            if b_occup:
                converted_move = (Board.squares.get(Board.w_knights[Board.piece])) + "-" + convert
                Board.w_taking.append(converted_move)


class BlackKnight(Board):
    def __init__(self):
        Board.__init__(self)

    def b_knight_move(self):
        moves = [25, -25, 23, -23, 14, -14, 10, -10]
        for i in range(8):
            self.move = Board.b_knights[Board.piece] + moves[i]
            b_occup = Board.b_occupation.get(self.move)
            convert = (Board.squares.get(self.move))
            if b_occup:
                pass
            else:
                if convert:
                    converted_move = (Board.squares.get(Board.b_knights[Board.piece])) + "-" + convert
                    Board.b_knights_moves.append(converted_move)
            w_occup = Board.w_occupation.get(self.move)
            if w_occup:
                converted_move = (Board.squares.get(Board.b_knights[Board.piece])) + "-" + convert
                Board.b_taking.append(converted_move)


class WhiteKing(Board):
    def __init__(self):
        Board.__init__(self)

    def king_move(self):
        moves = [12, -12, 13, -13, 11, -11, 1, -1]

        for i in range(8):
            self.move = Board.w_king[Board.piece] + moves[i]
            w_occup = Board.w_occupation.get(self.move)
            convert = (Board.squares.get(self.move))
            if w_occup:
                pass
            else:
                if convert:
                    converted_move = (Board.squares.get(Board.w_king[Board.piece])) + "-" + convert
                    Board.w_king_moves.append(converted_move)
                    self.move = int
            b_occup = Board.b_occupation.get(self.move)
            if b_occup:
                converted_move = (Board.squares.get(Board.w_king[Board.piece])) + "-" + convert
                Board.w_taking.append(converted_move)


class BlackKing(Board):
    def __init__(self):
        Board.__init__(self)

    def king_move(self):
        moves = [12, -12, 13, -13, 11, -11, 1, -1]
        for i in range(8):
            self.move = Board.b_knights[Board.piece] + moves[i]
            b_occup = Board.b_occupation.get(self.move)
            convert = (Board.squares.get(self.move))
            if b_occup:
                pass
            else:
                if convert:
                    converted_move = (Board.squares.get(Board.b_knights[Board.piece])) + "-" + convert
                    Board.b_knights_moves.append(converted_move)
            w_occup = Board.w_occupation.get(self.move)
            if w_occup:
                converted_move = (Board.squares.get(Board.b_knights[Board.piece])) + "-" + convert
                Board.b_taking.append(converted_move)


class WhiteRook(Board):
    def __init__(self):
        Board.__init__(self)

    def rook_move(self):
        moves = [1, -1, 12, -12]
        for i in moves:
            next_square = Board.w_rooks[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    w_occupied = Board.w_occupation.get(next_square)
                    if not w_occupied:
                        move = (Board.squares.get(Board.w_rooks[Board.piece])) + "-" + on_board
                        b_occupied = Board.b_occupation.get(next_square)
                        if b_occupied:
                            Board.w_taking.append(move)
                            break
                        else:
                            Board.w_rooks_moves.append(move)
                    else:
                        break
                else:
                    break


class BlackRook(Board):
    def __init__(self):
        Board.__init__(self)

    def rook_move(self):
        moves = [1, -1, 12, -12]
        for i in moves:
            next_square = Board.b_rooks[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    b_occupied = Board.b_occupation.get(next_square)
                    if not b_occupied:
                        move = (Board.squares.get(Board.b_rooks[Board.piece])) + "-" + on_board
                        w_occupied = Board.w_occupation.get(next_square)
                        if w_occupied:
                            Board.b_taking.append(move)
                            break
                        else:
                            Board.b_rooks_moves.append(move)
                    else:
                        break
                else:
                    break


class WhiteBishop(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []

    def bishop_move(self):
        moves = [13, -13, 11, -11]
        for i in moves:
            next_square = Board.w_bishops[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    w_occupied = Board.w_occupation.get(next_square)
                    if not w_occupied:
                        move = (Board.squares.get(Board.w_bishops[Board.piece])) + "-" + on_board
                        b_occupied = Board.b_occupation.get(next_square)
                        if b_occupied:
                            Board.w_taking.append(move)
                            break
                        else:
                            Board.w_bishops_moves.append(move)
                    else:
                        break
                else:
                    break


class BlackBishop(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []

    def bishop_move(self):
        moves = [13, -13, 11, -11]
        for i in moves:
            next_square = Board.b_bishops[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    b_occupied = Board.b_occupation.get(next_square)
                    if not b_occupied:
                        move = (Board.squares.get(Board.b_bishops[Board.piece])) + "-" + on_board
                        w_occupied = Board.w_occupation.get(next_square)
                        if w_occupied:
                            Board.b_taking.append(move)
                            break
                        else:
                            Board.b_bishops_moves.append(move)
                    else:

                        break
                else:
                    break


class WhiteQueen(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []

    def bishop_move(self):
        moves = [13, -13, 11, -11]
        for i in moves:
            next_square = Board.w_queen[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    w_occupied = Board.w_occupation.get(next_square)
                    if not w_occupied:
                        move = (Board.squares.get(Board.w_queen[Board.piece])) + "-" + on_board
                        b_occupied = Board.b_occupation.get(next_square)
                        if b_occupied:
                            Board.w_taking.append(move)
                            break
                        else:
                            Board.w_queen_moves.append(move)
                    else:
                        break
                else:
                    break

    def rook_move(self):
        moves = [1, -1, 12, -12]
        for i in moves:
            next_square = Board.w_queen[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    w_occupied = Board.w_occupation.get(next_square)
                    if not w_occupied:
                        move = (Board.squares.get(Board.w_queen[Board.piece])) + "-" + on_board
                        b_occupied = Board.b_occupation.get(next_square)
                        if b_occupied:
                            Board.w_taking.append(move)
                            break
                        else:
                            Board.w_queen_moves.append(move)
                    else:
                        break
                else:
                    break


class BlackQueen(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []

    def bishop_move(self):
        moves = [13, -13, 11, -11]
        for i in moves:
            next_square = Board.b_queen[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    b_occupied = Board.b_occupation.get(next_square)
                    if not b_occupied:
                        move = (Board.squares.get(Board.b_queen[Board.piece])) + "-" + on_board
                        w_occupied = Board.w_occupation.get(next_square)
                        if w_occupied:
                            Board.b_taking.append(move)
                            break
                        else:
                            Board.b_queen_moves.append(move)
                    else:

                        break
                else:
                    break

    def rook_move(self):
        moves = [1, -1, 12, -12]
        for i in moves:
            next_square = Board.b_queen[Board.piece]
            for x in range(8):
                next_square += i
                on_board = Board.squares.get(next_square)
                if on_board:
                    b_occupied = Board.b_occupation.get(next_square)
                    if not b_occupied:
                        move = (Board.squares.get(Board.b_queen[Board.piece])) + "-" + on_board
                        w_occupied = Board.w_occupation.get(next_square)
                        if w_occupied:
                            Board.b_taking.append(move)
                            break
                        else:
                            Board.b_queen_moves.append(move)
                    else:
                        break
                else:
                    break


class White_Pawn(Board):
    def __init__(self):
        Board.__init__(self)
        self.move = int

    def pawn_move(self):
        self.move = Board.w_pawns[Board.piece] + 12
        w_occup = Board.w_occupation.get(self.move)
        if w_occup:
            return
        b_occup = Board.b_occupation.get(self.move)
        if b_occup:
            return
        r_taking = Board.b_occupation.get((Board.w_pawns[Board.piece]) + 13)
        l_taking = Board.b_occupation.get((Board.w_pawns[Board.piece]) + 11)
        if r_taking:
            r_take_square = (Board.squares.get((Board.w_pawns[Board.piece]) + 13))
            converted_move = (Board.squares.get(Board.w_pawns[Board.piece])) + "-" + r_take_square
            Board.w_taking.append(converted_move)
        if l_taking:
            l_take_square = (Board.squares.get((Board.w_pawns[Board.piece]) + 11))
            converted_move = (Board.squares.get(Board.w_pawns[Board.piece])) + "-" + l_take_square
            Board.w_taking.append(converted_move)

        convert = (Board.squares.get(self.move))
        converted_move = (Board.squares.get(Board.w_pawns[Board.piece])) + "-" + convert
        Board.w_pawns_moves.append(converted_move)
        self.move = int

    def double_move(self):
        counter = 0
        starting = [39, 40, 41, 42, 43, 44, 45, 46]
        if Board.w_pawns[Board.piece] in starting:
            self.move = Board.w_pawns[Board.piece] + 24
            w_occup = Board.w_occupation.get(self.move)
            w_occup2 = Board.w_occupation.get((self.move - 12))
            if w_occup or w_occup2:
                return
            b_occup = Board.b_occupation.get(self.move)
            b_occup2 = Board.b_occupation.get((self.move - 12))
            if b_occup or b_occup2:
                return
            convert = (Board.squares.get(self.move))
            converted_move = (Board.squares.get(Board.w_pawns[Board.piece])) + "-" + convert
            Board.w_pawns_moves.append(converted_move)
        else:
            pass
        self.move = int


class Black_Pawn(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []
        self.move = int

    def pawn_move(self):
        self.move = Board.b_pawns[Board.piece] - 12
        w_occup = Board.w_occupation.get(self.move)
        if w_occup:
            return
        b_occup = Board.b_occupation.get(self.move)
        if b_occup:
            return
        r_taking = Board.w_occupation.get((Board.b_pawns[Board.piece]) - 13)
        l_taking = Board.w_occupation.get((Board.b_pawns[Board.piece]) - 11)
        if r_taking:
            r_take_square = (Board.squares.get((Board.b_pawns[Board.piece]) - 13))
            converted_move = (Board.squares.get(Board.b_pawns[Board.piece])) + "-" + r_take_square
            Board.b_taking.append(converted_move)
        if l_taking:
            l_take_square = (Board.squares.get((Board.b_pawns[Board.piece]) - 11))
            converted_move = (Board.squares.get(Board.b_pawns[Board.piece])) + "-" + l_take_square
            Board.b_taking.append(converted_move)

        convert = (Board.squares.get(self.move))
        converted_move = (Board.squares.get(Board.b_pawns[Board.piece])) + "-" + convert
        Board.b_pawns_moves.append(converted_move)
        self.move = int

    def double_move(self):
        counter = 0
        starting = [99, 100, 101, 102, 103, 104, 105, 106]
        if Board.b_pawns[Board.piece] in starting:
            self.move = Board.b_pawns[Board.piece] - 24
            w_occup = Board.w_occupation.get(self.move)
            w_occup2 = Board.w_occupation.get((self.move - 12))
            if w_occup or w_occup2:
                return
            b_occup = Board.b_occupation.get(self.move)
            b_occup2 = Board.b_occupation.get((self.move - 12))
            if b_occup or b_occup2:
                return
            convert = (Board.squares.get(self.move))
            converted_move = (Board.squares.get(Board.b_pawns[Board.piece])) + "-" + convert
            Board.b_pawns_moves.append(converted_move)
        else:
            pass
        self.move = int


w_rook = WhiteRook()
b_rook = BlackRook()
w_knight = WhiteKnight()
b_knight = BlackKnight()
w_bishop = WhiteBishop()
b_bishop = BlackBishop()
w_queen = WhiteQueen()
b_queen = BlackQueen()
w_pawn = White_Pawn()
b_pawn = Black_Pawn()
w_king = WhiteKing()
b_king = BlackKing()
move = Move()


def w_main():
    move.w_take()

    piece_count = len(Board.w_rooks)
    if piece_count >= 1:
        w_rook.piece1()
        w_rook.rook_move()
        if piece_count >= 2:
            w_rook.piece2()
            w_rook.rook_move()

            piece_count = len(Board.w_knights)
    if piece_count >= 1:
        w_knight.piece1()
        w_knight.w_knight_move()
        if piece_count >= 2:
            w_knight.piece2()
            w_knight.w_knight_move()

    piece_count = len(Board.w_bishops)
    if piece_count >= 1:
        w_bishop.piece1()
        w_bishop.bishop_move()
        if piece_count >= 2:
            w_bishop.piece2()
            w_bishop.bishop_move()

    w_queen.piece1()
    w_queen.bishop_move()
    w_queen.rook_move()

    w_king.piece1()
    w_king.king_move()

    piece_count = len(Board.w_pawns)
    if piece_count >= 1:
        w_pawn.piece1()
        w_pawn.pawn_move()
        w_pawn.double_move()
        if piece_count >= 2:
            w_pawn.piece2()
            w_pawn.pawn_move()
            w_pawn.double_move()
            if piece_count >= 3:
                w_pawn.piece3()
                w_pawn.pawn_move()
                w_pawn.double_move()
                if piece_count >= 4:
                    w_pawn.piece4()
                    w_pawn.pawn_move()
                    w_pawn.double_move()
                    if piece_count >= 5:
                        w_pawn.piece5()
                        w_pawn.pawn_move()
                        w_pawn.double_move()
                        if piece_count >= 6:
                            w_pawn.piece6()
                            w_pawn.pawn_move()
                            w_pawn.double_move()
                            if piece_count >= 7:
                                w_pawn.piece7()
                                w_pawn.pawn_move()
                                w_pawn.double_move()
                                if piece_count >= 8:
                                    w_pawn.piece8()
                                    w_pawn.pawn_move()
                                    w_pawn.double_move()

    move.delete_duplicates()


def get_squares(selected_square):
    move.w_get_squares(selected_square)

def main_w_move(square_to_go):
    move.w_make_move(square_to_go)
    move.clean_piece_moves()


def b_main(b_selected_square):
    move.b_take()

    piece_count = len(Board.b_rooks)
    if piece_count >= 1:
        b_rook.piece1()
        b_rook.rook_move()
        if piece_count >= 2:
            b_rook.piece2()
            b_rook.rook_move()

    piece_count = len(Board.b_knights)
    if piece_count >= 1:
        b_knight.piece1()
        b_knight.b_knight_move()
        if piece_count >= 2:
            b_knight.piece2()
            b_knight.b_knight_move()

    piece_count = len(Board.b_bishops)
    if piece_count >= 1:
        b_bishop.piece1()
        b_bishop.bishop_move()
        if piece_count >= 2:
            b_bishop.piece2()
            b_bishop.bishop_move()

    b_queen.piece1()
    b_queen.bishop_move()
    b_queen.rook_move()

    piece_count = len(Board.b_pawns)
    if piece_count >= 1:
        b_pawn.piece1()
        b_pawn.pawn_move()
        b_pawn.double_move()
        if piece_count >= 2:
            b_pawn.piece2()
            b_pawn.pawn_move()
            b_pawn.double_move()
            if piece_count >= 3:
                b_pawn.piece3()
                b_pawn.pawn_move()
                b_pawn.double_move()
                if piece_count >= 4:
                    b_pawn.piece4()
                    b_pawn.pawn_move()
                    b_pawn.double_move()
                    if piece_count >= 5:
                        b_pawn.piece5()
                        b_pawn.pawn_move()
                        b_pawn.double_move()
                        if piece_count >= 6:
                            b_pawn.piece6()
                            b_pawn.pawn_move()
                            b_pawn.double_move()
                            if piece_count >= 7:
                                b_pawn.piece7()
                                b_pawn.pawn_move()
                                b_pawn.double_move()
                                if piece_count >= 8:
                                    b_pawn.piece8()
                                    b_pawn.pawn_move()
                                    b_pawn.double_move()
    move.b_get_squares(b_selected_square)


def main_b_move(b_square_to_go):
    move.b_make_move(b_square_to_go)
    move.clean_piece_moves()
