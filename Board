class Board():
    def __init__(self, squares):
        self.squares = squares
        self.w_bishops = 
        self.w_rooks =
        self.w_knights = 
        self.w_king = 
        self.w_queen = 
        
        self.w_occupation = {
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
        self.b_occupation = {
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
        self.squares = {
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
            98: "h6",
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
        self.piece = 0

    def piece2(self):
        self.piece = 1

    def piece3(self):
        self.piece = 2

    def piece4(self):
        self.piece = 3

    def piece5(self):
        self.piece = 4

    def piece6(self):
        self.piece = 5

    def piece7(self):
        self.piece = 6

    def piece8(self):
        self.piece = 7





class Knight(Board):
    def __init__(self, squares):
        Board.__init__(self, squares)
        self.position = 33
        self.possible_moves = []

    def move(self):
        move = self.position + 23
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass

        move = self.position + 25
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.w_occupation[self.position] = False
            self.w_occupation[move] = True
            self.possible_moves.append(move)
        else:
            pass
        move = self.position + 10
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.w_occupation[self.position] = False
            self.w_occupation[move] = True
            self.possible_moves.append(move)
        else:
            pass
        move = self.position + 14
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.w_occupation[self.position] = False
            self.w_occupation[move] = True
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 14
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 10
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 23
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 25
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass

        print_moves(self)

    def b1_knight(self):
        self.position = 28


class King(Board):
    def __init__(self, squares):
        Board.__init__(self, squares)
        self.position = 31
        self.possible_moves = []

    def move(self):
        move = self.position + 1
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 1
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position + 11
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position + 12
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position + 13
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 11
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 12
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        move = self.position - 13
        occupated = self.w_occupation.get(move)
        if not occupated:
            self.possible_moves.append(move)
        else:
            pass
        print_moves(self)

        def b1_knight(self):
            self.position = 28


class Rook(Board):
    def __init__(self, squares):
        Board.__init__(self, squares)
        self.position = 27
        self.possible_moves = []

    def rook_move(self):
        move = self.position
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move += 1
                occupated = self.w_occupation.get(move)
                if not occupated:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break
        move = self.position
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move -= 1
                occupated = self.w_occupation.get(move)
                if not occupated:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break

        move = self.position
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move += 12
                occupated = self.w_occupation.get(move)
                if not occupated:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break

        move = self.position
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move -= 12
                occupated = self.w_occupation.get(move)
                if not occupated:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break

        print_moves(self)

    def h1_rook(self):
        self.position = 34


class Bishop(Board):
    def __init__(self, squares):
        Board.__init__(self, squares)
        self.position = [67, 66]
        self.possible_moves = []
        self.piece = 0

    def bishop_move(self):
        move = self.position[self.piece]
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move += 13
                occupated = self.w_occupation.get(move)
                if not occupated:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break
        move = self.position[self.piece]
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move += 11
                occupied = self.w_occupation.get(move)
                if not occupied:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break

        move = self.position[self.piece]
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move += -13
                occupated = self.w_occupation.get(move)
                if not occupated:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break

        move = self.position[self.piece]
        for i in range(8):
            out_of_board = self.squares.get(move)
            if out_of_board:
                move -= 11
                occupated = self.w_occupation.get(move)
                if not occupated:
                    self.possible_moves.append(move)
                else:
                    break
            else:
                break

    def print_moves(self):
        counter = 0
        for i in range(len(self.possible_moves)):
            move = (self.squares.get(self.possible_moves[counter]))
            counter += 1
            if move:
                print((self.squares.get(self.position[self.piece])), "-", (move), sep='')
        self.possible_moves.clear()


    def make_move(self):
        piece = input("select a piece: ")
        piece = int(piece,10)
        if piece == self.position[0]:
            new_pos = input("select a square: ")
            new_pos = int(new_pos, 10)
            self.w_occupation[piece] = False
            self.position[0] = new_pos
            self.w_occupation[new_pos] = True
            print("bishop pos is: ", (new_pos))
        if piece == self.position[1]:
            new_pos = input("select a square: ")
            new_pos = int(new_pos, 10)
            self.w_occupation[piece] = False
            self.position[1] = new_pos
            self.w_occupation[new_pos] = True
            print("bishop pos is: ",new_pos)
        else:
            pass


def print_moves(self):
    counter = 0
    for i in range(len(self.possible_moves)):
        move = (self.squares.get(self.possible_moves[counter]))
        counter += 1
        if move:
            print((self.squares.get(self.position)), "-", (move), sep='')
    self.possible_moves.clear()


class Queen(Bishop, Rook):
    def __init__(self, squares):
        Bishop.__init__(self, squares)
        self.position = 30
        self.possible_moves = []


class White_Pawn(Board):
    def __init__(self, squares):
        Board.__init__(self, squares)
        self.position = [39, 40, 41, 42, 43, 44, 45, 46]
        self.possible_moves = []

    def pawn_move(self):
        counter = 0
        for i in range(len(self.position)):
            move = self.position[counter] + 12
            self.possible_moves.append(move)
            convert = (self.squares.get(self.possible_moves[counter]))
            print((self.squares.get(self.position[counter])), "-", (convert), sep='')
            counter += 1
        self.possible_moves.clear()

    def double_move(self):
        starting = [39, 40, 41, 42, 43, 44, 45, 46]
        counter = 0
        counter2 = 0
        for i in self.position:
            if self.position[counter] in starting:
                move = self.position[counter] + 24
                self.possible_moves.append(move)
                convert = (self.squares.get(self.possible_moves[counter2]))
                print((self.squares.get(self.position[counter])), "-", (convert), sep='')
                counter2 += 1
            else:
                pass
            counter += 1

class Black_Pawn(Board):
    def __init__(self, squares):
        Board.__init__(self, squares)
        self.position = [99, 100, 101, 102, 103, 104, 105, 106]
        self.possible_moves = []

    def pawn_move(self):
        counter = 0
        for i in range(len(self.position)):
            move = self.position[counter] - 12
            self.possible_moves.append(move)
            convert = (self.squares.get(self.possible_moves[counter]))
            print((self.squares.get(self.position[counter])), "-", (convert), sep='')
            counter += 1
        self.possible_moves.clear()

    def double_move(self):
        starting = [99, 100, 101, 102, 103, 104, 105, 106]
        counter = 0
        counter2 = 0
        for i in self.position:
            if self.position[counter] in starting:
                move = self.position[counter] + 24
                self.possible_moves.append(move)
                convert = (self.squares.get(self.possible_moves[counter2]))
                print((self.squares.get(self.position[counter])), "-",convert, sep='')
                counter2 += 1
            else:
                pass
            counter += 1

#print("rook")
#rook = Rook(Board)
#rook.rook_move()
#rook.h1_rook()
#rook.rook_move()

#print("knight")
#knight = Knight(Board)
#knight.move()
#knight.b1_knight()
#knight.move()
bishop = Bishop(Board)
while True:
    print("bishop")

    bishop.bishop_move()
    bishop.print_moves()
    bishop.piece2()

    bishop.bishop_move()
    bishop.print_moves()
    bishop.make_move()
    bishop.piece1()



#print("queen")
#queen = Queen(Bishop)
#queen.bishop_move()
#queen = Queen(Rook)
#queen.rook_move()

#print("pawn")
#w_pawn = White_Pawn(Board)
#w_pawn.pawn_move()
#w_pawn.double_move()
