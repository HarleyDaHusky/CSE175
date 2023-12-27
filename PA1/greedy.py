#
# greedy.py
#
# This file provides a function implementing greedy best-first search for
# a route finding problem. Various search utilities from "route.py" are
# used in this function, including the classes RouteProblem, Node, and
# Frontier. Also, this function uses heuristic function objects defined
# in the "heuristic.py" file.
#
# YOUR COMMENTS INCLUDING CITATIONS
# Copy and editted from ucost.py
# initally ran, however output didn't match and looked unoptimized
# Node initializer was originally empty but copied the params from a*
# YOUR NAME - THE DATE
# Jeffrey Peng 10/20/23


from route import Node
from route import Frontier


def greedy_search(problem, h, repeat_check=False):
    """Perform greedy best-first search to solve the given route finding
    problem, returning a solution node in the search tree, corresponding
    to the goal location, if a solution is found. Only perform repeated
    state checking if the provided boolean argument is true."""

    # PLACE YOUR CODE HERE
    initialState = Node(problem.start, h_eval = h.h_cost(problem.start), h_fun = h)

    if problem.is_goal(initialState.loc):
        return initialState

    queue = Frontier(initialState, sort_by = 'h') #used h as it states in PA1spec
    reachedSet = set()
    reachedSet.add(initialState)

    while not queue.is_empty():
        tmpNode = queue.pop()
        if problem.is_goal(tmpNode.loc):
            return tmpNode
        tmpNodeList = tmpNode.expand(problem)
        for node in tmpNodeList:
            if repeat_check == True:
                if node not in reachedSet:
                    reachedSet.add(node)
                    queue.add(node)
            else:   
                queue.add(node)
    return None

