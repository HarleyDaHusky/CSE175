#
# bfs.py
#
# This file provides a function implementing breadth-first search for a
# route-finding problem. Various search utilities from "route.py" are
# used in this function, including the classes RouteProblem, Node, and
# Frontier.
#
# YOUR COMMENTS INCLUDING CITATIONS AND ACKNOWLEDGMENTS
# Textbook: Artificial Intelligence: A Modern Approach for PseudoCode
# Textbook states BFS is FIFO (First in First Out)
# Generic Search Psuedo in PA0spec
# https://www.w3schools.com/python/python_sets.asp - used for sets (line 32)
# "Goal is to populate the Frontier node" -Rebecca
# Emailed Rebecca, she mentioned that "You'll also want to start your repeat check before adding the child to your fringe"
# she also said, "You will want to expand your nodes," which clarified my misunderstanding of where the 'child nodes' mentioned in the documentation came from
# YOUR NAME - THE DATE
# Jeffrey Peng - 09/26/23


from route import Node
from route import Frontier


def BFS(problem, repeat_check=False):
    """Perform breadth-first search to solve the given route finding
    problem, returning a solution node in the search tree, corresponding
    to the goal location, if a solution is found. Only perform repeated
    state checking if the provided boolean argument is true."""

    # PLACE YOUR CODE HERE

    initialState = Node(problem.start)
    if problem.is_goal(initialState.loc):
        return initialState
    FIFO_queue = Frontier(initialState) #default initiator sets stack=False, stack=False because FIFO
    explored = set()
    while not FIFO_queue.is_empty():
        temp = FIFO_queue.pop()
        explored.add(initialState)
        if problem.is_goal(temp.loc):
            return temp
        temp2 = temp.expand(problem) #makes temp2 child nodes
        for node in temp2: #for node in child
            if repeat_check == True: #repeat check before adding node to frontier in accordance with the textbook.
                if node not in explored: #if the node is not in reached set, add to reached set and Frontier
                    explored.add(node)
                    FIFO_queue.add(node)
            else:
                FIFO_queue.add(node) #add child to Frontier if not repeated check
    return None
