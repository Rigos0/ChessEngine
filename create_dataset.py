from New_Board import *
import numpy as np
import os.path



# path = 'C:\\Users\\Rigos\\Documents\\GitHub\\ChessEngine\\datasets\\'
# file_15 = open(path + "file_15.txt","a")
# file_14 = open(path + "file_14.txt","a")
# file_13 = open(path + "file_13.txt","a")
# file_12 = open(path + "file_12.txt","a")
# file_11 = open(path + "file_11.txt","a")
# file_10 = open(path + "file_10.txt","a")
# file_9 = open(path + "file_9.txt","a")
# file_8 = open(path + "file_8.txt","a")
# file_7 = open(path + "file_7.txt","a")
# file_6 = open(path + "file_6.txt","a")
# file_5 = open(path + "file_5.txt","a")
# file_4 = open(path + "file_4.txt","a")
# file_3 = open(path + "file_3.txt","a")
# file_2 = open(path + "file_2.txt","a")
# file_1_5 = open(path + "file_1_5.txt","a")
# file_1 = open(path + "file_1.txt","a")
# file_0_75= open(path + "file_0_75.txt","a")
# file_0_5 = open(path + "file_0_5.txt","a")
# file_0_25 = open(path + "file_0_25.txt","a")
# file0 = open(path + "file0.txt","a")
# file15 = open(path + "file15.txt","a")
# file14 = open(path + "file14.txt","a")
# file13 = open(path + "file13.txt","a")
# file12 = open(path + "file12.txt","a")
# file11 = open(path + "file11.txt","a")
# file10 = open(path + "file10.txt","a")
# file9 = open(path + "file9.txt","a")
# file8 = open(path + "file8.txt","a")
# file7 = open(path + "file7.txt","a")
# file6 = open(path + "file6.txt","a")
# file5 = open(path + "file5.txt","a")
# file4 = open(path + "file4.txt","a")
# file3 = open(path + "file3.txt","a")
# file2 = open(path + "file2.txt","a")
# file1_5 = open(path + "file1_5.txt","a")
# file1 = open(path + "file1.txt","a")
# file0_75= open(path + "file0_75.txt","a")
# file0_5 = open(path + "file0_5.txt","a")
# file0_25 = open(path + "file0_25.txt","a")
# This file will create a dataset containing 8*8*12 files and an evaluation

class CreateDataset():
    def __init__(self):
        self.hash_table = []
        self.list_of_numpy_arrays = []
        self.list_of_evaluation = []
        self.lines_in_dataset = 0

    def create_dataset(self):
        raw_data = open("evaluation_data.txt")
        for line in raw_data:
            if self.lines_in_dataset > 300_000:
                write_to_file(self.list_of_numpy_arrays, self.list_of_evaluation)
                break
            word_list = []
            line = line.split()
            for word in line:
                word_list.append(word)

            move_index = 1
            eval_index = 4

            while move_index < len(word_list):
                if (eval_index - 4) % 12 == 0:
                    w_b = "white"
                    pieces = w_pieces
                else:
                    w_b = "black"
                    pieces = b_pieces
                move = convert_next_move(word_list[move_index], w_b)
                if move == "error":
                    break

                pieces.move_a_piece(move, "not_trial")
                pieces.delete_taken_pieces()

                board_representation = convert_position_to_np_array()
                # we don't need the same position more than once in the dataset
                string = ""
                lists = w_pieces.w_pawns+ w_pieces.w_knights+ w_pieces.w_bishops+ w_pieces.w_rooks+ w_pieces.w_queen+\
                                w_pieces.w_king+b_pieces.b_pawns+ b_pieces.b_knights+ b_pieces.b_bishops+\
                        b_pieces.b_rooks+  b_pieces.b_queen+b_pieces.b_king
                for x in lists:
                    x = str(x)
                    string = string + x
                position_number = int(string)
                hashed = hash(position_number)

                if hashed in self.hash_table:
                    move_index += 6
                    eval_index += 6
                    continue
                else:
                    self.hash_table.append(hashed)

                #get rid of the bracket behind evaluation
                evaluation = word_list[eval_index]
                evaluation = evaluation[:-1]
                if evaluation.startswith("#"):
                    evaluation = evaluation[1:]

               # normalize evaluation to one of our 10 options
                options = [-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1.5,-1,-0.75,-0.5,-0.25,0,0.25,
                           0.5,1,1.5,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                evaluation = float(evaluation)
                evaluation = min(options, key=lambda x: abs(x - evaluation))
                index = options.index(evaluation)
                # files = [file_15,file_14,file_13,file_12,file_11,file_10,file_9,file_8,file_7,file_6,file_5,
                #          file_4,file_3,file_2,file_1_5,file_1,file_0_75,file_0_5,file_0_25,
                #          file0, file0_25, file0_5, file0_75, file1,file1_5, file2, file3, file4, file5, file6,
                #          file7, file8, file9, file10, file11, file12, file13, file14, file15]
                for listitem in board_representation:
                    files[index].write('%s\n' % listitem)
                #labels = [1, 2, 3, 4, 5, 6,7, 8, 9, 10, 11]
                #self.list_of_evaluation.append(labels[index])
                # self.list_of_numpy_arrays.append(board_representation)
                self.lines_in_dataset += 1
                move_index += 6
                eval_index += 6

            reset_board()


def write_to_file(arrays, evals):
    arrays = np.asarray(arrays)
    evals = np.asarray(evals)
    arrays.dump("board_vectors.npy")
    evals.dump("evaluation.npy")




# this function takes next move in human like notation e.g. Be3 and converts it to a notation that our move generator
# understands
def convert_next_move(next_move, white_black):
    squares_to_go = []
    select_from_this_pieces = []
    if white_black == "white":
        w_pieces.create_moves_dict("not_trial")
        nested_list = w_pieces.delete_move_if_check("list")
        short_castle = [31, 33]
        long_castle = [31, 29]
        bishop = w_pieces.w_bishops
        rook = w_pieces.w_rooks
        knight = w_pieces.w_knights
        queen = w_pieces.w_queen
        pawn = w_pieces.w_pawns
        king = w_pieces.w_king

    else:
        b_pieces.create_moves_dict("not_trial")
        nested_list = b_pieces.delete_move_if_check("list")
        short_castle = [115, 117]
        long_castle = [115, 113]
        bishop = b_pieces.b_bishops
        rook = b_pieces.b_rooks
        knight = b_pieces.b_knights
        queen = b_pieces.b_queen
        pawn = b_pieces.b_pawns
        king = b_pieces.b_king
    if next_move.startswith("O-O"):
        return short_castle
    if next_move.startswith("O-O-O"):
        return long_castle

    if next_move.startswith("B"):
        piece = bishop
    elif next_move.startswith("R"):
        piece = rook
    elif next_move.startswith("N"):
        piece = knight
    elif next_move.startswith("Q"):
        piece = queen
    elif next_move.startswith("K"):
        piece = king
    elif next_move.startswith("R"):
        piece = rook

    else:
        piece = pawn
        next_move = "P" + next_move

    for i in range(2):
        if next_move.endswith("!"):
            next_move = next_move[:-1]
        if next_move.endswith("?"):
            next_move = next_move[:-1]
    # get rid of "+" if the string ends with +
    if next_move.endswith("+"):
        next_move = next_move[:-1]

    # get next square in the form 27-118 from human notation
    square_to_go = next_move[-2] + next_move[-1]
    convert_square_to_go = from_human_notation_to_27_118(square_to_go)

    for i in nested_list:
        if i[-1] == convert_square_to_go:
            squares_to_go.append(i)

    # if there are two pieces that can go to the same position
    if len(squares_to_go) == 1:
        return squares_to_go[0]
    else:
        for position in piece:
            for move in squares_to_go:
                if position == move[0]:
                    buffer = [move[0], convert_square_to_go]
                    select_from_this_pieces.append(buffer)

    if not select_from_this_pieces:
        return "error"
    if len(select_from_this_pieces) == 1:
        return select_from_this_pieces[0]
    else:
        rank_files = return_ranks_and_files_squares(next_move[1])
        if rank_files == "error":
            return "error"
        for u in select_from_this_pieces:
            if u[0] in rank_files:
                return [u[0], convert_square_to_go]
    return "error"


def from_human_notation_to_27_118(square):
    squares = {"a1": 27, "b1": 28, "c1": 29, "d1": 30, "e1": 31, "f1": 32, "g1": 33,
                "h1": 34, "a2": 39, "b2": 40, "c2": 41,"d2": 42,"e2": 43,"f2": 44,"g2": 45,
                "h2": 46,"a3": 51,"b3": 52,"c3": 53,"d3": 54,"e3": 55,"f3": 56,
                "g3": 57,"h3": 58,"a4": 63,"b4": 64,"c4": 65,"d4": 66,"e4": 67,"f4": 68,"g4": 69,"h4": 70,
                "a5": 75,"b5": 76,"c5": 77,"d5": 78,"e5": 79,"f5": 80,"g5": 81,"h5": 82,"a6": 87,"b6": 88,
                "c6": 89,"d6": 90,"e6": 91,"f6": 92,"g6": 93,"h6": 94,"a7": 99,"b7": 100,"c7": 101,"d7": 102,"e7":
                103, "f7": 104,"g7": 105,"h7": 106,"a8": 111,"b8": 112,"c8": 113,"d8": 114,
                   "e8": 115,"f8": 116,"g8": 117,"h8": 118}
    return squares.get(square)


def return_ranks_and_files_squares(letter):
    letter = str(letter)
    files_ranks = ["a", "b", "c", "d", "e", "f", "g", "h", "1", "2", "3", "4", "5", "6", "7", "8"]
    squares = [[27, 39, 51, 63, 75, 87, 99, 111], [28, 40, 52, 64, 76, 88, 100, 112],
               [29, 41, 53, 65, 77, 89, 101, 113], [30, 42, 54, 66, 78, 90, 102, 114],
               [31, 43, 55, 67, 79, 91, 103, 115], [32, 44, 56, 68, 80, 92, 104, 116],
               [33, 45, 57, 69, 81, 93, 105, 117], [34, 46, 58, 70, 82, 94, 106, 118],
               [27, 28, 29, 30, 31, 32, 33, 34], [39, 40, 41, 42, 43, 44, 45, 46],
               [51, 52, 53, 54, 55, 56, 57, 58], [63, 64, 65, 66, 67, 68, 69, 70],
               [75, 76, 77, 78, 79, 80, 81, 82], [87, 88, 89, 90, 91, 92, 93, 94],
               [99, 100, 101, 102, 103, 104, 105, 106], [111, 112, 113, 114, 115, 116, 117, 118]]
    if letter not in files_ranks:
        return "error"
    letter_index = files_ranks.index(letter)
    return squares[letter_index]


def convert_position(lists):
    list_768 = []
    squares = [27, 28, 29, 30, 31, 32, 33, 34, 39, 40, 41, 42, 43, 44, 45, 46,
               51, 52, 53, 54, 55, 56, 57, 58, 63, 64, 65, 66, 67, 68, 69, 70,
               75, 76, 77, 78, 79, 80, 81, 82, 87, 88, 89, 90, 91, 92, 93, 94,
               99, 100, 101, 102, 103, 104, 105, 106, 111, 112, 113, 114, 115, 116, 117, 118]
    # empty =        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # white_pawn =   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # white_knight = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # white_bishop = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # white_rook =   [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    # white_queen =  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    # white_king =   [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    # black_pawn =   [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    # black_knight = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    # black_bishop = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    # black_rook =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    # black_queen =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    # black_king =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    empty = [0]
    white_pawn = [1]
    white_knight = [3.12]
    white_bishop = [3.16]
    white_rook = [5]
    white_queen = [9]
    white_king = [50]
    black_pawn = [-1]
    black_knight = [-3.12]
    black_bishop = [-3.16]
    black_rook = [-5]
    black_queen = [-9]
    black_king = [-50]
    representational_list = [white_pawn, white_knight, white_bishop, white_rook,white_queen,white_king,black_pawn,
        black_knight, black_bishop, black_rook,black_queen, black_king]

    for i in squares:
        found = False
        for piece_pos in lists:
            if i in piece_pos:
                found = True
                index = lists.index(piece_pos)
                for u in representational_list[index]:
                    list_768.append(u)
                break
        if not found:
            for t in empty:
                list_768.append(t)

    return list_768


def convert_position_to_np_array():
    square_list = []
    board_list = []
    ranks = []
    ranks_list = [[111, 112, 113, 114, 115, 116, 117, 118],
               [99, 100, 101, 102, 103, 104, 105, 106],
               [87, 88, 89, 90, 91, 92, 93, 94],
               [75, 76, 77, 78, 79, 80, 81, 82],
               [63, 64, 65, 66, 67, 68, 69, 70],
               [51, 52, 53, 54, 55, 56, 57, 58],
               [39, 40, 41, 42, 43, 44, 45, 46],
               [27, 28, 29, 30, 31, 32, 33, 34]]
    white_pieces = [w_pieces.w_pawns, w_pieces.w_knights, w_pieces.w_bishops, w_pieces.w_rooks, w_pieces.w_queen,
                    w_pieces.w_king]
    black_pieces = [b_pieces.b_pawns, b_pieces.b_knights, b_pieces.b_bishops, b_pieces.b_rooks, b_pieces.b_queen,
                    b_pieces.b_king]
    # *8
    for rank in ranks_list:
        # *8
        for square in rank:
            #*6
            for i in range(6):
                if square in white_pieces[i]:
                    square_list.append(1)
                if square in black_pieces[i]:
                    square_list.append(-1)
                else:
                    square_list.append(0)
            square_list_arrray = np.asarray(square_list)
            ranks.append(square_list_arrray)
            square_list = []
        ranks_array = np.asarray(ranks_list)
        board_list.append(ranks_array)
        ranks = []
    board_list = np.asarray(board_list)

    return board_list


# main = CreateDataset()
# main.create_dataset()








