import random
from New_Board import *

global node_count


class Search(WhitePieces, BlackPieces):
    def __init__(self):
        WhitePieces.__init__(self)
        BlackPieces.__init__(self)
        self.hash_table = {}
        self.depth = 0
        self.node_count = 0
        self.ply = 0
        self.ply_depth = 1
        self.tree_node = 0

    def static_evaluation(self):
        w_material = len(w_pieces.w_pawns) + len(w_pieces.w_queen) * 9 + len(w_pieces.w_rooks) * 5 \
                     + len(w_pieces.w_bishops) * 3.16 + len(w_pieces.w_knights) * 3.16 + len(w_pieces.w_king) * 200
        b_material = len(b_pieces.b_pawns) + len(b_pieces.b_queen) * 9 + len(b_pieces.b_rooks) * 5 \
                     + len(b_pieces.b_bishops) * 3.16 + len(b_pieces.b_knights) * 3.16 + len(b_pieces.b_king) * 200

        w_pieces.create_moves_dict("trial")
        nested_list = w_pieces.delete_move_if_check("list")
        w_mobility = len(nested_list) * 0.1
        static_evaluation = w_material - b_material + w_mobility

        rounded = 1 + 100 * round(static_evaluation, 2)

        return rounded

    def search(self, side_to_move, last):
        if side_to_move == "white":
            # try to make the move and generate black's threats, if one of the black's pieces attacks our king, then delete
            # the move from the list of possible moves
            w_pieces.create_moves_dict("trial")
            nested_list = w_pieces.delete_move_if_check("list")
            evaluation_dictionary = {}
            counter_of_same_evals = 1
            self.ply += 1
            for move in nested_list:
                self.tree_node += 1
                w_pieces.move_a_piece(move, "trial")
                deleted_piece = w_pieces.delete_taken_pieces()
                # to avoid evaluating the same position again and again
                current_position_hash = hash_current_position()
                if current_position_hash not in self.hash_table:
                    current_evaluation = self.static_evaluation()
                    self.hash_table[current_position_hash] = current_evaluation
                else:
                    current_evaluation = self.hash_table[current_position_hash]

                rounded_eval = 1000 * round(current_evaluation, 2)
                self.node_count += 1

                if rounded_eval in evaluation_dictionary:
                    rounded_eval += counter_of_same_evals
                    counter_of_same_evals += 1
                    evaluation_dictionary[rounded_eval] = move
                else:
                    evaluation_dictionary[rounded_eval] = move

                if self.ply < self.ply_depth:

                    black_eval = self.search("black", "not")
                else:
                    black_eval = self.search("black", "last")

                # try:
                #     mini = min(black_eval.keys())
                #     evaluation_dictionary[mini] = evaluation_dictionary.pop(rounded_eval)
                #
                # except ValueError:
                #     pass

                tree = {self.tree_node: evaluation_dictionary,
                           self.tree_node: black_eval}
                print(tree)



                if deleted_piece:
                    w_pieces.b_lists[deleted_piece[0]].append(deleted_piece[1])
                reverse_move = [move[1], move[0]]
                w_pieces.move_a_piece(reverse_move, "trial")
            # it is not possible to delete an item directly in the process because it would mess up the 'for' loop
            return evaluation_dictionary

        else:
            b_pieces.create_moves_dict("trial")
            nested_list = b_pieces.delete_move_if_check("list")
            evaluation_dictionary = {}
            counter_of_same_evals = 1
            for move in nested_list:
                b_pieces.move_a_piece(move, "trial")
                deleted_piece = b_pieces.delete_taken_pieces()
                # to avoid evaluating the same position again and again
                current_position_hash = hash_current_position()
                if current_position_hash not in self.hash_table:
                    current_evaluation = self.static_evaluation()
                    self.hash_table[current_position_hash] = current_evaluation
                else:
                    current_evaluation = self.hash_table[current_position_hash]

                rounded_eval = 1000 * round(current_evaluation, 2)
                self.node_count += 1
                #print(self.node_count)

                if rounded_eval in evaluation_dictionary:
                    rounded_eval += counter_of_same_evals
                    counter_of_same_evals += 1
                    evaluation_dictionary[rounded_eval] = move
                else:
                    evaluation_dictionary[rounded_eval] = move

                if last != "last":
                    white_eval = self.search("white", "not_last")
                    try:
                        mini = max(white_eval.keys())
                        evaluation_dictionary[mini] = evaluation_dictionary.pop(rounded_eval)
                    except ValueError:
                        pass
                else:
                    pass



                if deleted_piece:
                    b_pieces.w_lists[deleted_piece[0]].append(deleted_piece[1])
                reverse_move = [move[1], move[0]]
                b_pieces.move_a_piece(reverse_move, "trial")
            # it is not possible to delete an item directly in the process because it would mess up the 'for' loop
            return evaluation_dictionary


def hash_current_position():
        list_of_tuples = []
        for i in w_pieces.w_lists:
            list_of_tuples.append(tuple(i))
        converted = tuple(list_of_tuples)
        return hash(converted)







def select_random_move(nested_list):
    random_number = random.randint(0, len(nested_list) -1)
    return nested_list[random_number]



def choose_the_best_move(eval_dict):
    max_value = max(eval_dict.keys())
    best_move = eval_dict[max_value]

    return best_move






