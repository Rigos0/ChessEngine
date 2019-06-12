import random


class Board:
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
        Board.w_occupation = {}
        Board.b_occupation = {}
        Board.w_attacks = []
        Board.b_attacks = []

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

    def WhiteOccupation(self):
        white_pieces = Board.w_pawns + Board.w_bishops + Board.w_knights + Board.w_rooks + Board.w_king + Board.w_queen
        square_counter = 27
        while square_counter < 119:
            if square_counter in white_pieces:
                Board.w_occupation[square_counter] = True
            else:
                Board.w_occupation[square_counter] = False
            square_counter += 1

    def BlackOccupation(self):
        black_pieces = Board.b_pawns + Board.b_bishops + Board.b_knights + Board.b_rooks + Board.b_king + Board.b_queen
        square_counter = 27
        while square_counter < 119:
            if square_counter in black_pieces:
                Board.b_occupation[square_counter] = True
            else:
                Board.b_occupation[square_counter] = False
            square_counter += 1


class Move(Board):
    def __init__(self):
        Board.__init__(self)
        Move.dots = []
        Move.b_dots = []

    def w_get_squares(self, selected_square):
        Move.dots = []
        move = selected_square
        w_lists = [Board.w_knights_moves, Board.w_pawns_moves, Board.w_queen_moves, Board.w_bishops_moves,
                   Board.w_rooks_moves, Board.w_king_moves, Board.w_taking]

        for x in w_lists:
            for i in x:
                try:
                    curr_square = i[0] + i[1]
                    if curr_square == move:
                        next_square = i[3] + i[4]
                        Move.dots.append(next_square)
                except IndexError:
                    pass

    def b_get_squares(self, selected_square):
        Move.dots = []
        move = selected_square
        b_lists = [Board.b_knights_moves, Board.b_pawns_moves, Board.b_queen_moves, Board.b_bishops_moves,
                   Board.b_rooks_moves, Board.b_king_moves, Board.b_taking]
        for x in b_lists:
            for i in x:
                try:
                    curr_square = i[0] + i[1]
                    if curr_square == move:
                        next_square = i[3] + i[4]
                        Move.dots.append(next_square)

                except IndexError:
                    pass

    def w_make_move(self, square_to_go):
        move = square_to_go
        sel_piece = move[0] + move[1]
        key_list = list(Board.squares.keys())
        val_list = list(Board.squares.values())
        piece = (key_list[val_list.index(sel_piece)])
        sel_square = move[3] + move[4]
        new_pos = (key_list[val_list.index(sel_square)])

        if move in Board.w_bishops_moves:
            piece_position = Board.w_bishops.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])

            Board.w_bishops[piece_position] = new_pos

        if move in Board.w_rooks_moves:
            piece_position = Board.w_rooks.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])

            Board.w_rooks[piece_position] = new_pos

        if move in Board.w_knights_moves:
            piece_position = Board.w_knights.index(piece)
            Board.w_knights[piece_position] = new_pos
            Board.w_knights_moves = []

        if move in Board.w_king_moves:
            piece_position = Board.w_king.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])

            Board.w_king[piece_position] = new_pos

        if move in Board.w_queen_moves:
            piece_position = Board.w_queen.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])

            Board.w_queen[piece_position] = new_pos

        if move in Board.w_pawns_moves:
            piece_position = Board.w_pawns.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])

            Board.w_pawns[piece_position] = new_pos

        if move in Board.w_taking:
            b_lists = [Board.b_knights, Board.b_pawns, Board.b_queen, Board.b_bishops, Board.b_rooks, Board.b_taking]
            for x in b_lists:
                if new_pos in x:
                    piece_index = x.index(new_pos)
                    del x[piece_index]
            w_lists = [Board.w_knights, Board.w_pawns, Board.w_queen, Board.w_bishops, Board.w_rooks]
            for x in w_lists:
                if piece in x:
                    piece_position = x.index(piece)
                    sel_square = move[3] + move[4]
                    new_pos = (key_list[val_list.index(sel_square)])

                    x[piece_position] = new_pos


    def b_make_move(self, square_to_go):
        move = square_to_go
        # b_lists = Board.b_knights_moves+ Board.b_pawns_moves+ Board.b_queen_moves+ Board.b_bishops_moves+ Board.b_rooks_moves + Board.b_taking
        # random_number = random.randint(0, len(b_lists) -1)
        # move = b_lists[random_number]
        sel_piece = move[0] + move[1]
        key_list = list(Board.squares.keys())
        val_list = list(Board.squares.values())
        piece = (key_list[val_list.index(sel_piece)])
        sel_square = move[3] + move[4]
        new_pos = (key_list[val_list.index(sel_square)])

        if move in Board.b_bishops_moves:
            piece_position = Board.b_bishops.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_bishops[piece_position] = new_pos

        if move in Board.b_rooks_moves:
            piece_position = Board.b_rooks.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_rooks[piece_position] = new_pos

        if move in Board.b_knights_moves:
            piece_position = Board.b_knights.index(piece)
            Board.b_knights[piece_position] = new_pos

        if move in Board.b_king_moves:
            piece_position = Board.b_king.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_king[piece_position] = new_pos

        if move in Board.b_queen_moves:
            piece_position = Board.b_queen.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_queen[piece_position] = new_pos

        if move in Board.b_pawns_moves:
            piece_position = Board.b_pawns.index(piece)
            sel_square = move[3] + move[4]
            new_pos = (key_list[val_list.index(sel_square)])
            Board.b_pawns[piece_position] = new_pos

        if move in Board.b_taking:
            w_lists = [Board.w_knights, Board.w_pawns, Board.w_queen, Board.w_bishops, Board.w_rooks]
            for x in w_lists:
                if new_pos in x:
                    piece_index = x.index(new_pos)
                    del x[piece_index]
            b_lists = [Board.b_knights, Board.b_pawns, Board.b_queen, Board.b_bishops, Board.b_rooks]
            for x in b_lists:
                if piece in x:
                    piece_position = x.index(piece)
                    sel_square = move[3] + move[4]
                    new_pos = (key_list[val_list.index(sel_square)])

                    x[piece_position] = new_pos


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

    def w_take(self):
        w_lists = [Board.w_knights, Board.w_pawns, Board.w_queen, Board.w_bishops, Board.w_rooks, Board.w_king]
        for positions in w_lists:
            for i in positions:
                occupied = Board.w_occupation.get(i)
                if not occupied:
                    del positions[positions.index(i)]

    def b_take(self):
        b_lists = [Board.b_knights, Board.b_pawns, Board.b_queen, Board.b_bishops, Board.b_rooks, Board.b_king]
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
            for position in Board.w_knights:
                self.move = position + moves[i]
                w_occup = Board.w_occupation.get(self.move)
                normal_notation_next_square = (Board.squares.get(self.move))
                if w_occup:
                    pass
                else:
                    if normal_notation_next_square:
                        converted_move = (Board.squares.get(
                            position)) + "-" + normal_notation_next_square
                        if converted_move not in Board.w_knights_moves:
                            Board.w_knights_moves.append(converted_move)
                        if self.move not in Board.w_attacks:
                            Board.w_attacks.append(self.move)
                b_occup = Board.b_occupation.get(self.move)
                if b_occup:
                    converted_move = (Board.squares.get(position)) + "-" + normal_notation_next_square
                    if converted_move not in Board.w_taking:
                         Board.w_taking.append(converted_move)


class BlackKnight(Board):
    def __init__(self):
        Board.__init__(self)

    def b_knight_move(self):
        moves = [25, -25, 23, -23, 14, -14, 10, -10]
        for i in range(8):
            for position in Board.b_knights:
                self.move = position + moves[i]
                b_occup = Board.b_occupation.get(self.move)
                convert = (Board.squares.get(self.move))
                if b_occup:
                    pass
                else:
                    if convert:
                        converted_move = (Board.squares.get(position)) + "-" + convert
                        if converted_move not in Board.w_knights_moves:
                            Board.b_knights_moves.append(converted_move)
                        if self.move not in Board.b_attacks:
                            Board.b_attacks.append(self.move)
                w_occup = Board.w_occupation.get(self.move)
                if w_occup:
                    converted_move = (Board.squares.get(position)) + "-" + convert
                    if converted_move not in Board.b_taking:
                         Board.b_taking.append(converted_move)


class WhiteKing(Board):
    def __init__(self):
        Board.__init__(self)

    def king_move(self):
        moves = [12, -12, 13, -13, 11, -11, 1, -1]
        for i in range(8):
            self.move = Board.w_king[0] + moves[i]
            if self.move in Board.b_attacks:
                continue
            w_occup = Board.w_occupation.get(self.move)
            convert = (Board.squares.get(self.move))
            if w_occup:
                pass
            else:
                if convert:
                    converted_move = (Board.squares.get(Board.w_king[0])) + "-" + convert
                    if converted_move not in Board.w_king_moves:
                        Board.w_king_moves.append(converted_move)
                    if self.move not in Board.w_attacks:
                        Board.w_attacks.append(self.move)
            b_occup = Board.b_occupation.get(self.move)
            if b_occup:
                converted_move = (Board.squares.get(Board.w_king[0])) + "-" + convert
                if converted_move not in Board.w_taking:
                   Board.w_taking.append(converted_move)
                if self.move not in Board.w_attacks:
                    Board.w_attacks.append(self.move)


class BlackKing(Board):
    def __init__(self):
        Board.__init__(self)

    def king_move(self):
        moves = [12, -12, 13, -13, 11, -11, 1, -1]
        for i in range(8):
            self.move = Board.b_king[0] + moves[i]
            print(Board.w_attacks)
            if self.move in Board.w_attacks:
                continue
            b_occup = Board.b_occupation.get(self.move)
            convert = (Board.squares.get(self.move))
            if b_occup:
                pass
            else:
                if convert:
                    converted_move = (Board.squares.get(Board.b_king[0])) + "-" + convert
                    if converted_move not in Board.b_king_moves:
                        Board.b_king_moves.append(converted_move)
                    if self.move not in Board.b_attacks:
                        Board.b_attacks.append(self.move)
            w_occup = Board.w_occupation.get(self.move)
            if w_occup:
                converted_move = (Board.squares.get(Board.b_king[0])) + "-" + convert
                if converted_move not in Board.b_taking:
                    Board.b_taking.append(converted_move)
                if self.move not in Board.b_attacks:
                    Board.b_attacks.append(self.move)


class WhiteRook(Board):
    def __init__(self):
        Board.__init__(self)

    def rook_move(self):
        moves = [1, -1, 12, -12]
        for i in moves:
            for position in Board.w_rooks:
                next_square = position          # next_square is actually current square - for simplicity
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        w_occupied = Board.w_occupation.get(next_square)
                        if not w_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            b_occupied = Board.b_occupation.get(next_square)
                            if b_occupied:
                                if move not in Board.w_taking:
                                    Board.w_taking.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.w_rooks_moves:
                                    Board.w_rooks_moves.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
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
            for position in Board.b_rooks:
                next_square = position
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        b_occupied = Board.b_occupation.get(next_square)
                        if not b_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            w_occupied = Board.w_occupation.get(next_square)
                            if w_occupied:
                                if move not in Board.b_taking:
                                    Board.b_taking.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.b_rooks_moves:
                                    Board.b_rooks_moves.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
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
            for position in Board.w_bishops:
                next_square = position
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        w_occupied = Board.w_occupation.get(next_square)
                        if not w_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            b_occupied = Board.b_occupation.get(next_square)
                            if b_occupied:
                                if move not in Board.w_taking:
                                    Board.w_taking.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.w_bishops_moves:
                                    Board.w_bishops_moves.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
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
            for position in Board.b_bishops:
                next_square = position
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        b_occupied = Board.b_occupation.get(next_square)
                        if not b_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            w_occupied = Board.w_occupation.get(next_square)
                            if w_occupied:
                                if move not in Board.b_taking:
                                    Board.b_taking.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.b_bishops_moves:
                                    Board.b_bishops_moves.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
                        else:

                            break
                    else:
                        break


class WhiteQueen(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []

    def bishop_like_move(self):
        moves = [13, -13, 11, -11]
        for i in moves:
            for position in Board.w_queen:
                next_square = position
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        w_occupied = Board.w_occupation.get(next_square)
                        if not w_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            b_occupied = Board.b_occupation.get(next_square)
                            if b_occupied:
                                if move not in Board.w_taking:
                                    Board.w_taking.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.w_queen_moves:
                                    Board.w_queen_moves.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
                        else:
                            break
                    else:
                        break

    def rook_like_move(self):
        moves = [1, -1, 12, -12]
        for i in moves:
            for position in Board.w_queen:
                next_square = position
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        w_occupied = Board.w_occupation.get(next_square)
                        if not w_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            b_occupied = Board.b_occupation.get(next_square)
                            if b_occupied:
                                if move not in Board.w_taking:
                                    Board.w_taking.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.w_queen_moves:
                                    Board.w_queen_moves.append(move)
                                if next_square not in Board.w_attacks:
                                    Board.w_attacks.append(next_square)
                        else:
                            break
                    else:
                        break


class BlackQueen(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []

    def bishop_like_move(self):
        moves = [13, -13, 11, -11]
        for i in moves:
            for position in Board.b_queen:
                next_square = position
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        b_occupied = Board.b_occupation.get(next_square)
                        if not b_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            w_occupied = Board.w_occupation.get(next_square)
                            if w_occupied:
                                if move not in Board.b_taking:
                                    Board.b_taking.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.b_queen_moves:
                                    Board.b_queen_moves.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
                        else:

                            break
                    else:
                        break

    def rook_like_move(self):
        moves = [1, -1, 12, -12]
        for i in moves:
            for position in Board.b_queen:
                next_square = position
                for x in range(8):
                    next_square += i
                    on_board = Board.squares.get(next_square)
                    if on_board:
                        b_occupied = Board.b_occupation.get(next_square)
                        if not b_occupied:
                            move = (Board.squares.get(position)) + "-" + on_board
                            w_occupied = Board.w_occupation.get(next_square)
                            if w_occupied:
                                if move not in Board.b_taking:
                                    Board.b_taking.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
                                break
                            else:
                                if move not in Board.b_queen_moves:
                                    Board.b_queen_moves.append(move)
                                if next_square not in Board.b_attacks:
                                    Board.b_attacks.append(next_square)
                        else:
                            break
                    else:
                        break


class White_Pawn(Board):
    def __init__(self):
        Board.__init__(self)
        self.move = int

    def pawn_move(self):
        for position in Board.w_pawns:
            r_taking = Board.b_occupation.get(position + 13)
            l_taking = Board.b_occupation.get(position + 11)
            r_take_square = (Board.squares.get(position + 13))
            l_take_square = (Board.squares.get(position + 11))
            if (position + 13) not in Board.w_attacks:
                if r_take_square:
                    Board.w_attacks.append(position + 13)
            if (position + 11) not in Board.w_attacks:
                if l_take_square:
                    Board.w_attacks.append(position + 11)
            if r_taking:
                converted_move = (Board.squares.get(position)) + "-" + r_take_square
                if converted_move not in Board.w_taking:
                    Board.w_taking.append(converted_move)
            if l_taking:
                converted_move = (Board.squares.get(position)) + "-" + l_take_square
                if converted_move not in Board.w_taking:
                    Board.w_taking.append(converted_move)
            self.move = position + 12
            w_occup = Board.w_occupation.get(self.move)
            b_occup = Board.b_occupation.get(self.move)
            if not b_occup and not w_occup:
                convert = (Board.squares.get(self.move))
                if convert:  # check for 8th rank
                    converted_move = (Board.squares.get(position)) + "-" + convert
                    if converted_move not in Board.w_pawns_moves:
                        Board.w_pawns_moves.append(converted_move)

    def double_move(self):
        starting = [39, 40, 41, 42, 43, 44, 45, 46]
        for position in Board.w_pawns:
            if position in starting:
                self.move = position + 24
                w_occup = Board.w_occupation.get(self.move)
                w_occup2 = Board.w_occupation.get((self.move - 12))
                b_occup = Board.b_occupation.get(self.move)
                b_occup2 = Board.b_occupation.get((self.move - 12))
                if not(w_occup or w_occup2 or b_occup or b_occup2):
                    convert = (Board.squares.get(self.move))
                    converted_move = (Board.squares.get(position)) + "-" + convert
                    if converted_move not in Board.w_pawns_moves:
                        Board.w_pawns_moves.append(converted_move)
            else:
                pass


class Black_Pawn(Board):
    def __init__(self):
        Board.__init__(self)
        self.possible_moves = []
        self.move = int

    def pawn_move(self):
        for position in Board.b_pawns:
            self.move = position - 12
            r_taking = Board.w_occupation.get((position) - 13)
            l_taking = Board.w_occupation.get((position) - 11)
            r_take_square = (Board.squares.get(position - 13))
            l_take_square = (Board.squares.get(position - 11))
            if (position - 13) not in Board.b_attacks:
                if r_take_square:
                    Board.b_attacks.append(position - 13)
            if (position - 11) not in Board.b_attacks:
                if l_take_square:
                    Board.b_attacks.append(position - 11)
            if r_taking:
                converted_move = (Board.squares.get(position)) + "-" + r_take_square
                if converted_move not in Board.b_taking:
                    Board.b_taking.append(converted_move)
            if l_taking:
                converted_move = (Board.squares.get(position)) + "-" + l_take_square
                if converted_move not in Board.b_taking:
                    Board.b_taking.append(converted_move)
            w_occup = Board.w_occupation.get(self.move)
            b_occup = Board.b_occupation.get(self.move)
            if not w_occup and not b_occup:
                convert = (Board.squares.get(self.move))
                if convert:
                    converted_move = (Board.squares.get(position)) + "-" + convert
                    if converted_move not in Board.b_pawns_moves:
                        Board.b_pawns_moves.append(converted_move)

    def double_move(self):
        starting = [99, 100, 101, 102, 103, 104, 105, 106]
        for position in Board.b_pawns:
            if position in starting:
                self.move = position - 24
                w_occup = Board.w_occupation.get(self.move)
                w_occup2 = Board.w_occupation.get((self.move + 12))
                b_occup = Board.b_occupation.get(self.move)
                b_occup2 = Board.b_occupation.get((self.move + 12))
                if not (w_occup or w_occup2 or b_occup or b_occup2):
                    convert = (Board.squares.get(self.move))
                    converted_move = (Board.squares.get(position)) + "-" + convert
                    if converted_move not in Board.b_pawns_moves:
                        Board.b_pawns_moves.append(converted_move)
            else:
                pass


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
board = Board()


def w_main():
    move.w_take()

    w_rook.rook_move()
    w_knight.w_knight_move()

    w_bishop.bishop_move()

    w_queen.bishop_like_move()
    w_queen.rook_like_move()

    w_pawn.pawn_move()
    w_pawn.double_move()

    w_king.king_move()
    #Board.b_attacks = []



def w_get_squares(selected_square):
    move.w_get_squares(selected_square)


def main_w_move(square_to_go):

    move.w_make_move(square_to_go)
    move.clean_piece_moves()


def b_main():
    move.b_take()

    b_rook.rook_move()

    b_knight.b_knight_move()

    b_bishop.bishop_move()

    b_queen.bishop_like_move()
    b_queen.rook_like_move()

    b_pawn.pawn_move()
    b_pawn.double_move()

    b_king.king_move()
   # Board.w_attacks = []


def main_b_move(square_to_go):
    move.b_make_move(square_to_go)
    move.clean_piece_moves()


def b_get_squares(selected_square):
    move.b_get_squares(selected_square)


def create_occupation_lists():
    board.WhiteOccupation()
    board.BlackOccupation()
