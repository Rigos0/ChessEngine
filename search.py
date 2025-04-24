from move_generator import *
import math
import keras
from keras.models import load_model

# We don't want to learn anymore.
keras.backend.set_learning_phase(0)

# load the neural network keras model
model = load_model('evaluation_regression2')


# a single Node in the tree
class Node:
    def __init__(self, probability, parent_node_index, move, colour, visits, wins, current_pos=None):
        self.parent_node_index = parent_node_index # pointer to its parent node
        self.probability = probability # or evaluation
        self.move = move # move in the form [original_square, next_square]
        self.visits = visits # how many times has been the node visited
        self.wins = wins # wins found starting from this node
        self.child_nodes_indices = [] # pointers to children nodes
        self.colour = colour # either white or black
        self.current_pos = current_pos # dictionary holding information about current chess position

    # self-explanatory functions for accessing information of the Node
    def get_parent_node(self):
        return self.parent_node_index

    def get_visits(self):
        return self.visits

    def get_wins(self):
        return self.wins

    def get_probability(self):
        return self.probability

    def get_children(self):
        return self.child_nodes_indices

    def get_parent(self):
        return self.parent_node_index

    def get_colour(self):
        return self.colour

    def get_move(self):
        return self.move

    def get_node_eval(self):
        evaluation = self.visits
        return evaluation

    # add a single child to the node
    def add_child(self, child):
        self.child_nodes_indices.append(child)

    # increase number of wins of the node
    def add_wins(self, wins):
        self.wins += wins

    # add number of visits to the Node
    def add_visits(self, visits):
        self.visits += visits


class Tree:
    def __init__(self):
        # holds all nodes
        self.tree = []
        # for the Monte Carlo search
        # increase it to explore less promising branches quicker
        self.tradeoff_parameter = 2**0.5

    # add a single node to the tree
    def add_node(self, node):
        self.tree.append(node)

    # get children of a node from a pointer to the parent node
    def get_children(self, index):
        return self.tree[index].get_children()

    # get data type Node from a pointer
    def get_node(self, index):
        return self.tree[index]

    # delete the tree
    def clear(self):
        self.tree.clear()

    # Monte Carlo search
    # get the next node to explore from a list of indices
    def get_best_upper_confidence_bound(self, indices_to_compare):
        list_of_UCB = []
        for node_index in indices_to_compare:
            wins = self.tree[node_index].get_wins()
            visits = self.tree[node_index].get_visits()
            probability = self.tree[node_index].get_probability()
            parent = self.tree[node_index].get_parent()
            parent_visits = self.tree[parent].get_visits()
            visits_parameter = (math.log(parent_visits) / (1 + visits))
            upper_confidence_bound = wins/visits + self.tradeoff_parameter * probability*(visits_parameter ** 0.5)
            list_of_UCB.append(upper_confidence_bound)
        best_UCB_index = list_of_UCB.index(max(list_of_UCB))
        return indices_to_compare[best_UCB_index]

    # how many nodes are in the tree
    def get_number_of_nodes(self):
        return len(self.tree)

    def get_most_promising_move(self, nodes_indices):
        evals = []
        for node_index in nodes_indices:
            node = self.get_node(node_index)
            node_eval = node.get_visits()
            evals.append(node_eval)
        max_eval_index = evals.index(max(evals))

        best_node = self.get_node(nodes_indices[max_eval_index])
        return best_node.get_move()

    # get probabilities in a list of playing each move from raw NN model predictions
    @staticmethod
    def get_probabilities(predictions, leaf_node_colour):
        if leaf_node_colour == "white":
            predictions_list = []
            for i in predictions:
                predictions_list.append(1/i)
            predictions = np.asarray(predictions_list)

        array_sum = np.sum(predictions)
        probabilities = []
        for evaluation in predictions:
            probability = evaluation/array_sum
            probabilities.append(float(probability))
        return probabilities


# Implementation of the Minimax search algorithm
class ModifiedMinimax:
    def __init__(self):
        # the Keras model
        self.eval_model = model
        # search this many plies ahead
        self.max_depth = 2
        self.current_depth = 0
        # holds all leaf nodes
        self.leaf_nodes = []
        # holds all positions of the leaf nodes
        self.leaf_positions = []
        # Holds nodes after which one side is checkmated
        self.checkmate_nodes = []
        # Holds children of the root node.
        # The point of a chess engine is to find the most promising node
        # from these.
        self.root_node_children = []

    # Create the tree
    def build_tree(self, side_to_move, parent_node, depth):
        moves = create_moves(side_to_move) # find legal moves using the generator
        # if checkmate or stalemate occurs
        if not moves:
            return True
        for move in moves:
            # save current position, so we can return to this position after doing the search
            current_position = deepcopy(generator.return_current_position())
            # make current move on the board
            generator.make_a_move(move)
            # create a Node holding the parent node index, current move and side to move
            node = Node(None, parent_node, move, side_to_move, None, None)
            number_of_nodes = tree.get_number_of_nodes()
            # add the node to the tree
            tree.tree.append(node)
            # if this is the first iteration, add pointer to the node to root_node_children
            if depth == 1:
                self.root_node_children.append(number_of_nodes)

            if depth != self.max_depth:  # if max depth not reached
                # call itself again recursively
                # arguments: enemy side to move, pointer to current node (because
                # it will become a parent node for next nodes), and increase the depth by 1
                checkmate = self.build_tree(enemy_colour(side_to_move), number_of_nodes, depth + 1)
                # if we run into a checkmate, save current node, giving it high evaluation, to checkmate nodes
                if checkmate:
                    if side_to_move == "white":
                        mate_value = 1000
                    else:
                        mate_value = -1000
                    node = Node(mate_value, parent_node, move, side_to_move, None, None)
                    tree.tree[number_of_nodes] = node
                    self.checkmate_nodes.append(node)
            # maximum depth reached
            else:
                # add current node to leaf nodes
                self.leaf_nodes.append(node)
                # get matrix representation of the position
                position_matrix = convert_to_matrix(side_to_move)
                # add it to leaf nodes positions
                # append the matrix representation to a list, so we can later evaluate all next states at once
                self.leaf_positions.append(position_matrix)
            # return the move
            generator.go_back_to_previous_position(current_position, side_to_move)

    # propagate values back
    # Pass True to the function if we need to propagate back from
    # the leaf nodes.
    def backpropagate(self, first):
        new_leaf_nodes = []
        # if leaf layer of nodes
        if first:
            # fetch predictions of all leaf nodes from the NN model
            leaf_positions_array = np.asarray(self.leaf_positions)
            predictions = self.eval_model.predict(leaf_positions_array)
        # for every leaf node
        for index, leaf_node in enumerate(self.leaf_nodes):
            # get evaluation of the node
            if first:
                leaf_node_eval = predictions[index]
            else:
                leaf_node_eval = leaf_node.probability
            # if we reach the root node, there is nowhere to propagate to
            if leaf_node.get_parent() == 0:
                return True
            # get node to which we want to propagate the evaluation
            parent_node_index = leaf_node.get_parent()
            parent_node = tree.get_node(parent_node_index)
            # get parent node evaluation
            parent_node_eval = parent_node.probability
            # if parent node has not been given an evaluation
            if not parent_node_eval:
                # propagate the eval
                parent_node.probability = leaf_node_eval
            # If it has an evaluation.
            # This is where the logic of the Minimax search comes in place
            # We need to if current evaluation is better than the evaluation of the parent node
            # Like this, we will propagate back the most promising
            # children evaluation to the parent node
            else:
                parent_colour = parent_node.get_colour()
                if parent_colour == "white":
                    # we are looking for the lowest eval
                    # MINIMIZE
                    if leaf_node_eval < parent_node_eval:
                        parent_node.probability = leaf_node_eval
                else:
                    # MAXIMIZE
                    if leaf_node_eval > parent_node_eval:
                        parent_node.probability = leaf_node_eval
            # Add the parent node the list of leaf nodes because in the next iteration
            # we will propagate the value further towards the root node.
            if parent_node not in new_leaf_nodes:
                new_leaf_nodes.append(parent_node)
        # The layer closer to the root node now becomes the leaf layer
        self.leaf_nodes = new_leaf_nodes
        return False

    # Find the most promising move.
    def search(self):
        # Add root node to the tree.
        root = Node(None, None, None, None, None, None)
        tree.tree.append(root)
        # Build the tree
        # This implementation can find the best move for both sides
        # but the user interface currently supports playing only with white pieces
        # against the AI.
        self.build_tree("black", 0, 1)
        # propagate from the leaf layer of nodes
        self.backpropagate(True)

        # While not root node reached, propagate back
        # each iteration propagates from one layer of nodes.
        stop = False
        while not stop:
            stop = self.backpropagate(False)

        # Now, the tree is completely built. We only have to find
        # what is the most promising move to play.

        # Get evaluations of root node children
        evals = []
        for node_index in self.root_node_children:
            node = tree.get_node(node_index)
            eval = node.probability
            evals.append(eval)

        # Find the most promising move.
        min_eval_index = evals.index(min(evals))
        best_node_index = self.root_node_children[min_eval_index]
        best_move = tree.get_node(best_node_index).move

        # The search is finished. Delete the tree and reset.
        tree.clear()
        self.current_depth = 0
        self.leaf_nodes = []
        self.leaf_positions = []
        self.checkmate_nodes = []
        self.root_node_children = []
        generator.set_up_attributes("black")

        # Return the best move
        return best_move


# Implementation of the U-search
class U_search:
    def __init__(self):
        self.model = model
        self.steps = 0
        # Steps are approximately proportional to the time this search takes
        # to finish. Increase max_steps to give the search more time and
        # to make the AI stronger.
        self.max_steps = 200

    # First layer of nodes. It is a simple algorithm, but seems to work well combined
    # with the neural value network.
    def assumption_search(self):
        next_positions = []
        variation_count = []
        # this search only plays from the black side, therefore start the search by creating all possible moves
        # for black
        moves = create_moves("black")
        # loop over possible moves
        for move in moves:
            # save current position, so we can return to this position after doing the search
            current_position = deepcopy(generator.return_current_position())
            # make current move on the board
            generator.make_a_move(move)

            # get matrix representation of current position. In this case, we do not flip the board, so the prediction
            # could be slightly of when predicting for the black side
            position_matrix = convert_to_matrix("black")
            # append the matrix representation to a list, so we can later evaluate all next states at once
            next_positions.append(position_matrix)
            # return the move
            generator.go_back_to_previous_position(current_position, "black")
        # evaluate all next states at once and save them in according order to "node_predictions"
        node_predictions = self.model.predict(np.asarray(next_positions))
        initial_position = deepcopy(generator.return_current_position())
        # while not the maximum amount of steps
        while self.steps < self.max_steps:
            # find current best move
            minimize_index = np.argmin(node_predictions)
            # save current position so we can go back afterwards
            current_position = deepcopy(generator.return_current_position())
            # play the best move and call the function that creates next nodes for white
            generator.make_a_move(moves[minimize_index])

            # increase the amount of steps taken
            self.steps += 1
            # expand the tree by searching next white moves
            # this is the first white node, so we need to pass an empty array because there are not any previous
            # nodes from the white side
            evaluation_of_this_branch = self.assumption_white(np.array([]), node_predictions)
            # if not evaluation_of_this_branch, it means that we haven't found any refutations of our line in given time
            if evaluation_of_this_branch:
                for key in evaluation_of_this_branch.keys():
                    node_predictions[minimize_index] = key
                    variation_count.append(tuple(moves[np.argmax(node_predictions)]))

            generator.go_back_to_previous_position(current_position, "black")

        generator.go_back_to_previous_position(initial_position, "black")
        minimize_index = np.argmin(node_predictions)
        # reset the steps
        self.steps = 0
        # return the most promising move for black
        return moves[minimize_index]

    # expand the search tree by exploring white nodes
    def assumption_white(self, previous_white_predictions, black_node_predictions):
        next_positions = []
        # create all possible moves for white
        moves = create_moves('white')
        # if there are no moves, white is in checkmate
        if not moves:
            return {np.float32(0): "black"}
        # loop over all possible moves
        for move in moves:
            # save current position
            current_position = deepcopy(generator.return_current_position())
            # make a move for white
            generator.make_a_move(move)

            # convert to matrix
            position_matrix = convert_to_matrix("white")
            # append the matrix to list of positions
            next_positions.append(position_matrix)
            # return the position
            generator.go_back_to_previous_position(current_position, "white")

        # predict all states at once
        white_node_predictions = self.model.predict(np.asarray(next_positions))
        while True:
            # find our best option among current moves
            current_max = np.amax(white_node_predictions)
            current_position = deepcopy(generator.return_current_position())
            # if there are any previous white nodes
            if previous_white_predictions.any():
                # if our current best option is not as good as our best option in previous white predictions,
                # then propagate back the current best option
                if current_max < np.amax(previous_white_predictions):
                    generator.go_back_to_previous_position(current_position, "white")
                    # propagate best option back
                    return {current_max: "white"}
            # play the best move and call black search
            max_index = np.argmax(white_node_predictions)
            # make current best move

            generator.make_a_move(moves[max_index])

            self.steps += 1
            # call next black node
            if self.steps > self.max_steps:
                generator.go_back_to_previous_position(current_position, "white")
                return {current_max: "white"}
            search_path_eval = self.assumption_black(black_node_predictions, white_node_predictions)
            for key, value in search_path_eval.items():
                # if we found worse position for black, propagate the evaluation back to black node
                if value == "black":
                    generator.go_back_to_previous_position(current_position, "white")
                    return {key: value}
                # if we found worse position for white, change the currently searched node eval to its lower value and
                # continue searching next node
                elif value == "white":
                    white_node_predictions[max_index] = key
                    generator.go_back_to_previous_position(current_position, "white")

    # Similar to assumption_white, but does everything for black instead.
    # See assumption_white for comments.
    def assumption_black(self, previous_node_predictions, white_nodes_predictions):
        next_positions = []
        moves = create_moves('black')
        if not moves:
            print("black in checkmate")
            return {np.float32(1): "white"}
        for move in moves:
            current_position = deepcopy(generator.return_current_position())
            generator.make_a_move(move)
            position = convert_to_matrix("black")
            next_positions.append(position)
            generator.go_back_to_previous_position(current_position, "black")

        predictions = self.model.predict(np.asarray(next_positions))
        # find current best move
        while True:
            current_min = np.amin(predictions)
            min_index = np.argmin(predictions)
            current_position = deepcopy(generator.return_current_position())

            # if our position got worse compared to previous node
            if current_min > np.amin(previous_node_predictions):
                return {current_min: "black"}
            # play our best move and call white node
            generator.make_a_move(moves[min_index])

            self.steps += 1
            if self.steps > self.max_steps:
                generator.go_back_to_previous_position(current_position, "black")
                return {current_min: "black"}
            search_path_eval = self.assumption_white(white_nodes_predictions, predictions)
            for key, value in search_path_eval.items():
                if value == "white":
                    generator.go_back_to_previous_position(current_position, "black")
                    return {key: value}
                elif value == "black":
                    predictions[min_index] = key
            generator.go_back_to_previous_position(current_position, "black")


# return the enemy colour
def enemy_colour(side_to_move):
    if side_to_move == "white":
        return "black"
    else:
        return "white"


class Monte_Carlo_Search():
    def __init__(self):
        # loops to finish
        self.depth = 20
        self.policy_network = load_model("evaluation_regression2")
        self.value_network = load_model("classification1_win_draw_loss_1")

    def selection(self, parent_node_index):
        children_indices = tree.get_children(parent_node_index)
        if children_indices:
            best_node_index = tree.get_best_upper_confidence_bound(children_indices)
            node_to_explore = tree.get_node(best_node_index)
            node_move = node_to_explore.get_move()
            generator.make_a_move(node_move)
            unexplored_leaf_node = self.selection(best_node_index)
        else:
            return parent_node_index
        return unexplored_leaf_node

    # expand the tree from the leaf node
    def expansion(self, current_node_index, leaf_node_colour):
        enemy_side = enemy_colour(leaf_node_colour)
        current_node = tree.tree[current_node_index]
        moves = create_moves(enemy_side)
        # if we ran into a checkmate, return a win
        if not moves:
            return 1, 1

        # create pointers to future children nodes
        total_amount_of_nodes = tree.get_number_of_nodes()
        number_of_children = len(moves)
        for i in range(number_of_children):
            current_node.add_child(total_amount_of_nodes + i + 0)

        # evaluate the next node
        node_predictions, wins_list, visits_list = self.get_predictions(moves, leaf_node_colour)
        # get how good is the leaf node in percentages
        probabilities = tree.get_probabilities(node_predictions, leaf_node_colour)

        # expand the tree
        for index, probability in enumerate(probabilities):
            visits = visits_list[index]
            wins = wins_list[index]
            node = Node(probability, current_node_index, moves[index], enemy_side, visits, wins)
            tree.add_node(node)
        return sum(wins_list), sum(visits_list)

    def propagate_back(self, node_to_propagate_to_index, number_of_wins, number_of_visits):
        node_to_propagate_to = tree.get_node(node_to_propagate_to_index)
        node_to_propagate_to.add_visits(number_of_visits)
        node_to_propagate_to.add_wins(number_of_wins)
        next_node = node_to_propagate_to.get_parent()
        # if we reach root node
        if not next_node:
            return
        # our losses are enemy side wins
        other_side_wins = number_of_visits-number_of_wins
        self.propagate_back(next_node, other_side_wins, number_of_visits)

    def get_predictions(self, moves, leaf_node_colour):
        next_positions = []
        wins_list = []
        visits_list = []
        enemy_side = enemy_colour(leaf_node_colour)
        # loop over possible moves
        for move in moves:
            # save current position, so we can return to this position after doing the search
            current_position = deepcopy(generator.return_current_position())
            # make current move on the board
            generator.make_a_move(move)
            # get matrix representation of current position. In this case, we do not flip the board, so the prediction
            # could be slightly of when predicting for the black side
            position_matrix = convert_to_matrix(enemy_side)
            # append the matrix representation to a list, so we can later evaluate all next states at once
            next_positions.append(position_matrix)
            enemy_moves = create_moves(leaf_node_colour)
            if not enemy_moves:
                print("enemy_error")
            number_of_wins = self.get_fake_rollout_wins(enemy_moves, leaf_node_colour)
            visits_list.append(len(enemy_moves))
            wins_list.append(number_of_wins)
            # return the move
            generator.go_back_to_previous_position(current_position, enemy_side)
        # evaluate all next states at once and save them in according order to "node_predictions"
        predictions = self.policy_network.predict(np.asarray(next_positions))
        return predictions, wins_list, visits_list

    def get_fake_rollout_wins(self, moves, leaf_node_colour):
        matrices_to_be_evaluated = []
        for move in moves:
            # save current position, so we can return to this position after doing the search
            current_position = deepcopy(generator.return_current_position())
            # make current move on the board
            generator.make_a_move(move)
            # get matrix representation of current position. In this case, we do not flip the board, so the prediction
            # could be slightly of when predicting for the black side
            position_matrix = convert_to_matrix(leaf_node_colour)
            # append the matrix representation to a list, so we can later evaluate all next states at once
            matrices_to_be_evaluated.append(position_matrix)
            # return the move
            generator.go_back_to_previous_position(current_position, leaf_node_colour)
        predictions = self.value_network.predict(np.asarray(matrices_to_be_evaluated))

        # print("I am not sure in what form will this thing predict. Future me, please change the code underneath.")
        wins = 0
        if leaf_node_colour == "white":
            win_class = 0
        else:
            win_class = 1
        for prediction in predictions:
            wins += (prediction[win_class])

        return wins

    def search(self):
        # initiate the tree with a root node
        root_node = Node(0, None, None, "white", 0, 0)
        tree.add_node(root_node)

        # the main Monte Carlo Search loop
        for i in range(self.depth):
            # save current state of the board
            current_position = deepcopy(generator.return_current_position())
            # find index of next leaf node
            leaf_node_index = self.selection(0)
            # get the leaf node Object
            leaf_node = tree.tree[leaf_node_index]
            # get colour of the leaf node
            leaf_node_colour = leaf_node.get_colour()
            # expand the branch and get the evaluations
            wins, visits = self.expansion(leaf_node_index, leaf_node_colour)
            # propagate the new information about the branch towards the root note
            self.propagate_back(leaf_node_index, wins, visits)
            # go back to the original position
            generator.go_back_to_previous_position(current_position, "black")






        for i in root_node.get_children():
            node = tree.get_node(i)
            print(vars(node))
        print(root_node.get_children())
        for i in range(3):
           print("\n")

        children = root_node.get_children()
        best_move = tree.get_most_promising_move(children)

        tree.clear()
        ###########################################################

        # print(len(tree.tree))
        # print(tree.tree)
        ###########################################################
        # print(best_move)
        # leaf_node_index = self.selection(0)
        # leaf_node = tree.get_node(leaf_node_index)
        # # print(vars(leaf_node))
        # parent_index = leaf_node.get_parent()
        # parent = tree.get_node(parent_index)
        # while True:
        #     # print(vars(parent))
        #     parent_index = parent.get_parent()
        #     if not parent_index:
        #         break
        #     parent = tree.get_node(parent_index)
        return best_move

tree = Tree()










# def play_best_moves(plies, side_to_move):
#     moves = create_moves()


# class Modified_U_search():
#     def __init__(self):
#         self.depth = 750
#         self.policy_network = load_model("evaluation_regression2")
#
#     def selection(self, parent_node_index, side_to_move):
#         children_indices = tree.get_children(parent_node_index)
#         enemy_side = enemy_colour(side_to_move)
#         if children_indices:
#             best_node_index = tree.select_node_to_explore(children_indices, side_to_move)
#             node_to_explore = tree.get_node(best_node_index)
#             node_move = node_to_explore.get_move()
#             generator.make_a_move(node_move)
#             unexplored_leaf_node = self.selection(best_node_index, enemy_side)
#         else:
#             return parent_node_index
#         return unexplored_leaf_node
#
#     def expansion(self, current_node_index, leaf_node_colour):
#         enemy_side = enemy_colour(leaf_node_colour)
#         current_node = tree.tree[current_node_index]
#         moves = create_moves(enemy_side)
#         # create pointers to future child nodes
#         total_amount_of_nodes = tree.get_number_of_nodes()
#         number_of_children = len(moves)
#         for i in range(number_of_children):
#             current_node.add_child(total_amount_of_nodes + i + 0)
#         node_predictions,current_positions = self.get_predictions(moves, leaf_node_colour)
#         predictions = np.ndarray.tolist(node_predictions)
#         # expand the tree
#         for index, prediction in enumerate(predictions):
#             node = Node(prediction, current_node_index, moves[index], enemy_side, visits=0, wins=0
#                         , current_pos=current_positions[index])
#             tree.add_node(node)
#         if leaf_node_colour == "white":
#             best_eval = min(predictions)
#         else:
#             best_eval = max(predictions)
#         return best_eval
#
#     def propagate_back(self, node_to_propagate_from_index, current_eval, colour):
#         node_to_propagate_to = tree.get_node(node_to_propagate_from_index)
#         node_to_propagate_to.probability = current_eval
#         previous_other_colour_node_index = node_to_propagate_to.get_parent()
#         previous_other_colour_node = tree.get_node(previous_other_colour_node_index)
#         if not previous_other_colour_node.get_parent():
#             return 0
#         previous_same_colour_node_index = previous_other_colour_node.get_parent()
#         previous_same_colour_node = tree.get_node(previous_same_colour_node_index)
#         if not previous_same_colour_node.get_parent():
#             return 0
#         previous_same_colour_node_score = previous_same_colour_node.get_probability()
#         if colour == "white":
#             if current_eval > previous_same_colour_node_score:
#                 starting_node_index = self.propagate_back(previous_same_colour_node_index, current_eval, colour)
#             else:
#                 return previous_same_colour_node.get_parent()
#         else:
#             if current_eval < previous_same_colour_node_score:
#                 starting_node_index = self.propagate_back(previous_same_colour_node_index, current_eval, colour)
#             else:
#                 return previous_same_colour_node.get_parent()
#         return starting_node_index
#
#
#
#     def get_predictions(self, moves, leaf_node_colour):
#         next_positions = []
#         current_positions = []
#         enemy_side = enemy_colour(leaf_node_colour)
#         # loop over possible moves
#         for move in moves:
#             # save current position, so we can return to this position after doing the search
#             current_position = deepcopy(generator.return_current_position())
#             current_positions.append(current_position)
#             # make current move on the board
#             generator.make_a_move(move)
#             # get matrix representation of current position. In this case, we do not flip the board, so the prediction
#             # could be slightly of when predicting for the black side
#             position_matrix = convert_to_matrix(enemy_side)
#             # append the matrix representation to a list, so we can later evaluate all next states at once
#             next_positions.append(position_matrix)
#             # return the move
#             generator.go_back_to_previous_position(current_position, enemy_side)
#         # evaluate all next states at once and save them in according order to "node_predictions"
#         predictions = self.policy_network.predict(np.asarray(next_positions))
#         return predictions, current_positions
#
#     def search(self):
#         current_position = deepcopy(generator.return_current_position())
#
#         root_node = Node(0, None, None, "white", 0, 0, current_pos=current_position)
#         tree.add_node(root_node)
#         starting_node_index = 0
#         next_loop_start_colour = "black"
#
#         for i in range(20):
#             position = tree.get_node(starting_node_index).current_pos
#             generator.go_back_to_previous_position(position, next_loop_start_colour)
#             leaf_node_index = self.selection(starting_node_index, next_loop_start_colour)
#             leaf_node = tree.get_node(leaf_node_index)
#             leaf_node_colour = leaf_node.get_colour()
#             current_eval = self.expansion(leaf_node_index, leaf_node_colour)
#             # print(vars(leaf_node))
#             leaf_node_parent_index = leaf_node.get_parent()
#
#             if not leaf_node_parent_index:
#                 next_loop_start_colour = enemy_colour(leaf_node_colour)
#                 continue
#             leaf_node_parent = tree.get_node(leaf_node_parent_index)
#             parent_eval = leaf_node_parent.get_probability()
#             # parent node has the other colour than the leaf node
#             if leaf_node_colour == "white":
#                 if current_eval > parent_eval:
#                     starting_node_index = self.propagate_back(leaf_node_parent_index, current_eval, leaf_node_colour)
#                 else:
#                     next_loop_start_colour = enemy_colour(leaf_node_colour)
#                     continue
#             else:
#                 if current_eval < parent_eval:
#                     starting_node_index = self.propagate_back(leaf_node_parent_index, current_eval, leaf_node_colour)
#                 else:
#                     next_loop_start_colour = enemy_colour(leaf_node_colour)
#                     continue
#             next_loop_start_colour = enemy_colour(leaf_node_colour)
#
#         children = root_node.get_children()
#         evals = []
#         for i in children:
#             node = tree.get_node(i)
#             evals.append(node.probability)
#         best_node_index= evals.index(min(evals))
#         best_node = tree.get_node(children[best_node_index])
#         best_move = best_node.get_move()
#         ###########################################################
#         for i in root_node.get_children():
#             node = tree.get_node(i)
#             print(vars(node))
#         ###########################################################
#
#         generator.set_up_attributes("black")
#         return best_move
#
