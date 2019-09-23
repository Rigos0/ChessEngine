import random
from New_Board import *


def select_random_move(nested_list):
    random_number = random.randint(0, len(nested_list) -1)
    return nested_list[random_number]


def play_the_best_move(evaluation_dict):
    max_value = max(evaluation_dict, key=int)
    best_move = evaluation_dict[max_value]
    return best_move


def static_evaluation():
    w_material = len(w_pieces.w_pawns) + len(w_pieces.w_queen)*9 + len(w_pieces.w_rooks)*5 \
                 + len(w_pieces.w_bishops)*3.16 + len(w_pieces.w_knights)*3.16 + len(w_pieces.w_king) * 200
    b_material = len(b_pieces.b_pawns) + len(b_pieces.b_queen)*9 + len(b_pieces.b_rooks)*5 \
                 +len(b_pieces.b_bishops)*3.16 + len(b_pieces.b_knights)*3.16 + len(b_pieces.b_king) * 200

    w_number_of_moves = len(dictionary_to_nested_list(w_pieces.create_moves_dict("trial")))
    w_mobility = w_number_of_moves * 0.2
    static_evaluation = w_material - b_material + w_mobility


    return static_evaluation


def white_search(nested_list):
    evaluation_list = []
    evaluation_dictionary = {}
    for move in nested_list:
        w_pieces.move_a_piece(move, "trial")
        # try to delete a piece if we take one, this variable stores information about the piece so we can return it
        # afterwards
        deleted_piece = w_pieces.delete_taken_pieces()

        static_eval = static_evaluation()
        round_static_eval = int(100*round(static_eval, 2))
        evaluation_list.append(round_static_eval)

        b_pieces.create_moves_dict("create")
        b_nested_list = b_pieces.delete_move_if_check()
        black_search(b_nested_list)

        if deleted_piece:
            w_pieces.b_lists[deleted_piece[0]].append(deleted_piece[1])
        # we tried to execute the move to check if our king would be hanging, therefore we have to take the move
        # back
        reverse_move = [move[1], move[0]]
        w_pieces.move_a_piece(reverse_move, "trial")
    # it is not possible to delete an item directly in the process because it would mess up the 'for' loop

    print(evaluation_list)
    counter = 0
    counter_of_the_same_values = -1
    for i in evaluation_list:
        # it won't happen often when the static evaluation function gets more complicated, but we need to check
        # if there are two moves with the exact same eval
        if i in evaluation_dictionary:
            evaluation_dictionary[i+counter_of_the_same_values] = nested_list[counter]
            counter_of_the_same_values -= 1
            counter += 1
            continue
        evaluation_dictionary[i] = nested_list[counter]
        counter += 1
    print(evaluation_dictionary)
    return evaluation_dictionary


def black_search(nested_list):
    evaluation_list = []
    evaluation_dictionary = {}
    for move in nested_list:
        w_pieces.move_a_piece(move, "trial")
        # try to delete a piece if we take one, this variable stores information about the piece so we can return it
        # afterwards
        deleted_piece = w_pieces.delete_taken_pieces()

        static_eval = static_evaluation()
        round_static_eval = int(100 * round(static_eval, 2))
        evaluation_list.append(round_static_eval)

        w_pieces.create_moves_dict("create")
        w_nested_list = w_pieces.delete_move_if_check()
        white_search(w_nested_list)

        if deleted_piece:
            w_pieces.b_lists[deleted_piece[0]].append(deleted_piece[1])
        # we tried to execute the move to check if our king would be hanging, therefore we have to take the move
        # back
        reverse_move = [move[1], move[0]]
        w_pieces.move_a_piece(reverse_move, "trial")
    # it is not possible to delete an item directly in the process because it would mess up the 'for' loop

    print(evaluation_list)
    counter = 0
    counter_of_the_same_values = -1
    for i in evaluation_list:
        # it won't happen often when the static evaluation function gets more complicated, but we need to check
        # if there are two moves with the exact same eval
        if i in evaluation_dictionary:
            evaluation_dictionary[i + counter_of_the_same_values] = nested_list[counter]
            counter_of_the_same_values -= 1
            counter += 1
            continue
        evaluation_dictionary[i] = nested_list[counter]
        counter += 1
    print(evaluation_dictionary)
    return evaluation_dictionary

