__author__ = 'Conor'

import logging
import main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GLOBAL_COUNTER = 0

class Algorithm(object):
    def __init__(self):
        self.heuristic_weighting = {}
        # TODO - Add multiple heuristics with possibility for weightings
        # Example: {(heuristic_1: .6), (heuristic_2: .25), (heuristic_3:.15)}

    def run(self):
        t = StateTree(main.Game(), None)
        t.generate_decision_tree()
        print "---- ::: Done ::: ----"
        num = t.count_nodes_below()
        print str(num)



class StateTree(object):
    # Initialize the algorithm
    def __init__(self, game_state, parent, depth = 0):
        self.game_state = game_state
        self.parent = parent
        self.depth = depth
        self.children = []

    # Generate one level of a decision tree from every possible move from this state
    def generate_decision_tree(self):

        all_possible_moves = self.game_state.get_all_possible_moves()
        all_possible_game_states = []
        for original_space in all_possible_moves.keys():
            for possible_move in all_possible_moves[original_space]:
                all_possible_game_states.append(self.new_game_state(original_space, possible_move, self.game_state))

        # print [str(item) for item in all_possible_game_states]
        for state in all_possible_game_states:
            self.children.append(StateTree(state, self, self.depth+1))

        # print "test"
        # print [str(x.game_state) for x in self.children]

        if self.depth < 2:
            for child in self.children:
                child.generate_decision_tree()  # Recur

    def count_nodes_below(self):
        result = 1
        for child in self.children:
            result += child.count_nodes_below()

        return result

    def new_game_state(self, original_space, possible_move, root_state):
        new_game_state = self.make_new_hypothetical_state(original_space, possible_move)
        return new_game_state

    def make_new_hypothetical_state(self, original_space, new_move):
        # board = str(self.game_state.state.split(' ')[0].split('/'))
        # print board
        # TODO - Actually change the board based on the original piece moving to the new space (& replacing if nec.)
        return main.Game(str(self.game_state))

    def __str__(self):
        parent_string = self.parent.game_state if self.parent is not None else "None"
        return "State: {0} | Parent: {1} | Number of Children: {2}".format(str(self.game_state), parent_string,
                                                                                    self.children.__sizeof__())
        # TODO - What if the parent doesn't have a state ie: this is the root node - need to be safer


if __name__ == '__main__':
    a = Algorithm()
    a.run()
