import random
from New_Board import *


def select_random_move(nested_list):
    random_number = random.randint(0, len(nested_list) -1)
    return nested_list[random_number]


def static_evaluation():
    w_material = len(w_pieces.w_pawns) + len(w_pieces.w_queen)*9 + len(w_pieces.w_rooks)*5 \
                 + len(w_pieces.w_bishops)*3.16 + len(w_pieces.w_knights)*3.16
    b_material = len(b_pieces.b_pawns) + len(b_pieces.b_queen)*9 + len(b_pieces.b_rooks)*5 \
                 + len(b_pieces.b_bishops)*3.16 + len(b_pieces.b_knights)*3.16

    static_evaluation = w_material - b_material

    return static_evaluation

def search(nested_list):
 # try to make the move and generate black's threats, if one of the black's pieces attacks our king, then delete
        # the move from the list of possible moves
        for move in nested_list:
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
        moves_in_dict = nested_list_to_dictionary(nested_list_of_moves)
        return moves_in_dict

