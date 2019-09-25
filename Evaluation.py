import random
from New_Board import *


class Search(WhitePieces, BlackPieces):
    def __init__(self):
        WhitePieces.__init__(self)
        BlackPieces.__init__(self)
        self.hash_table = {}
        self.ply = 1

    def static_evaluation(self):
        w_material = len(w_pieces.w_pawns) + len(w_pieces.w_queen) * 9 + len(w_pieces.w_rooks) * 5 \
                     + len(w_pieces.w_bishops) * 3.16 + len(w_pieces.w_knights) * 3.16 + len(w_pieces.w_king) * 200
        b_material = len(b_pieces.b_pawns) + len(b_pieces.b_queen) * 9 + len(b_pieces.b_rooks) * 5 \
                     + len(b_pieces.b_bishops) * 3.16 + len(b_pieces.b_knights) * 3.16 + len(b_pieces.b_king) * 200

        # w_mobility = len(possible_moves) * 0.1
        static_evaluation = w_material - b_material  #w_mobility

        rounded = 1 + 100 * round(static_evaluation, 2)

        return rounded

    def search(self, side_to_move):
        evaluation_dictionary = {}
        if side_to_move == "white":
            # we don't need to worry about canceling castling or en passant stuff in the parent class (I hope),
            # therefore we won't use the parameter "trial"
            w_pieces.create_moves_dict("trial")
            # generate possible moves in current position
            possible_moves_list = w_pieces.delete_move_if_check("list")
            print("moves", possible_moves_list)
            exact_same_eval_counter = 1
            for move in possible_moves_list:
                # get evaluation after every possible move
                w_pieces.move_a_piece(move, "trial")
                deleted_piece = w_pieces.delete_taken_pieces()

                # to avoid evaluating the same position again and again
                # current_position_hash = self.hash_current_position()
                # if current_position_hash not in self.hash_table:
                evaluation = self.static_evaluation()
                #     self.hash_table[current_position_hash] = evaluation
                # else:
                #     evaluation = self.hash_table[current_position_hash]

                if evaluation not in evaluation_dictionary:
                    evaluation_dictionary[evaluation] = move
                else:
                    evaluation += exact_same_eval_counter
                    exact_same_eval_counter += 1
                    evaluation_dictionary[evaluation] = move
                print("evaluation", evaluation_dictionary)
                if self.ply > 0:
                    self.ply -= 1
                    black_eval = self.search("black")
                    try:
                        mini = min(black_eval.keys())
                        evaluation_dictionary[mini] = evaluation_dictionary.pop(evaluation)
                    except ValueError:
                        pass

                if deleted_piece:
                    w_pieces.b_lists[deleted_piece[0]].append(deleted_piece[1])
                reverse_move = [move[1], move[0]]
                w_pieces.move_a_piece(reverse_move, "trial")


        else:
            b_pieces.create_moves_dict("trial")
            # generate possible moves in current position
            possible_moves_list = b_pieces.delete_move_if_check("list")
            print("black", possible_moves_list)

            exact_same_eval_counter = 1
            for move in possible_moves_list:
                # get evaluation after every possible move
                b_pieces.move_a_piece(move, "trial")
                deleted_piece = b_pieces.delete_taken_pieces()

                # to avoid evaluating the same position again and again
                # current_position_hash = self.hash_current_position()
                # if current_position_hash not in self.hash_table:
                evaluation = self.static_evaluation()
                #     self.hash_table[current_position_hash] = evaluation
                # else:
                #     evaluation = self.hash_table[current_position_hash]

                if evaluation not in evaluation_dictionary:
                    evaluation_dictionary[evaluation] = move
                else:
                    evaluation += exact_same_eval_counter
                    exact_same_eval_counter += 1
                    evaluation_dictionary[evaluation] = move
                print("black evaluation", evaluation_dictionary)
                if self.ply > 0:
                    white_eval = self.search("white")
                    self.ply -= 1
                    try:
                        maxi = max(white_eval.keys())
                        evaluation_dictionary[maxi] = evaluation_dictionary.pop(evaluation)
                    except ValueError:
                        pass

                if deleted_piece:
                    b_pieces.w_lists[deleted_piece[0]].append(deleted_piece[1])
                reverse_move = [move[1], move[0]]
                b_pieces.move_a_piece(reverse_move, "trial")

        return evaluation_dictionary

    def hash_current_position(self):
        list_of_tuples = []
        for i in w_pieces.w_lists:
            list_of_tuples.append(tuple(i))
        converted = tuple(list_of_tuples)
        return hash(converted)







def select_random_move(nested_list):
    random_number = random.randint(0, len(nested_list) -1)
    return nested_list[random_number]




def white_search(last):
    # try to make the move and generate black's threats, if one of the black's pieces attacks our king, then delete
    # the move from the list of possible moves
    w_pieces.create_moves_dict("trial")
    moves_dict = w_pieces.delete_move_if_check()
    nested_list = dictionary_to_nested_list(moves_dict)
    evaluation_dictionary = {}
    counter_of_same_evals = 1
    for move in nested_list:
        w_pieces.move_a_piece(move, "trial")
        deleted_piece = w_pieces.delete_taken_pieces()

        current_evaluation = static_evaluation()
        rounded_eval = 1000 * round(current_evaluation, 2)
        global node_count
        node_count += 1


        if rounded_eval in evaluation_dictionary:
            rounded_eval += counter_of_same_evals
            counter_of_same_evals += 1
        evaluation_dictionary[rounded_eval] = move
        if last != "last":
            black_eval = black_search()
            try:
                mini = min(black_eval.keys())
                evaluation_dictionary[mini] = evaluation_dictionary.pop(rounded_eval)
            except ValueError:
                pass


        if deleted_piece:
            w_pieces.b_lists[deleted_piece[0]].append(deleted_piece[1])
        reverse_move = [move[1], move[0]]
        w_pieces.move_a_piece(reverse_move, "trial")
    # it is not possible to delete an item directly in the process because it would mess up the 'for' loop
    return evaluation_dictionary


def choose_the_best_move(eval_dict):
    max_value = max(eval_dict.keys())
    best_move = eval_dict[max_value]

    return best_move



def black_search():
    b_pieces.create_moves_dict("trial")
    moves_dict = b_pieces.delete_move_if_check()
    nested_list = dictionary_to_nested_list(moves_dict)
    evaluation_dictionary = {}
    counter_of_same_evals = 1
    for move in nested_list:
        b_pieces.move_a_piece(move, "trial")
        deleted_piece = b_pieces.delete_taken_pieces()

        current_evaluation = static_evaluation()
        rounded_eval = 1000 * round(current_evaluation, 2)
        global node_count
        node_count += 1

        if rounded_eval in evaluation_dictionary:
            rounded_eval += counter_of_same_evals
            counter_of_same_evals += 1
        evaluation_dictionary[rounded_eval] = move

        # white_eval = white_search("last")
        # try:
        #     mini = max(white_eval.keys())
        #     evaluation_dictionary[mini] = evaluation_dictionary.pop(rounded_eval)
        # except ValueError:
        #     pass

        if deleted_piece:
            b_pieces.w_lists[deleted_piece[0]].append(deleted_piece[1])
        reverse_move = [move[1], move[0]]
        b_pieces.move_a_piece(reverse_move, "trial")
    # it is not possible to delete an item directly in the process because it would mess up the 'for' loop
    return evaluation_dictionary


