#
# astar.py
#
# This file provides a function implementing A* search for a route finding
# problem. Various search utilities from "route.py" are used in this function,
# including the classes RouteProblem, Node, and Frontier. Also, this function
# uses heuristic function objects defined in the "heuristic.py" file.
# Didn't include any other params for the intitalization of node and TA Mariel corrected that and assisted me in that.
# YOUR COMMENTS INCLUDING CITATIONS
# copied from greedy.py with slight changes
# YOUR NAME - THE DATE
# Jeffrey Peng 10/20/23


from route import Node
from route import Frontier


def a_star_search(problem, h, repeat_check=False):
    """Perform A-Star search to solve the given route finding problem,
    returning a solution node in the search tree, corresponding to the goal
    location, if a solution is found. Only perform repeated state checking if
    the provided boolean argument is true."""

    # PLACE YOUR CODE HERE
    initialState = Node(problem.start, h_eval = h.h_cost(problem.start), h_fun = h)
    if problem.is_goal(initialState.loc):
        return initialState
    queue = Frontier(initialState, sort_by="f") #used f as it states in PA1spec
    reachedSet = set()
    reachedSet.add(initialState)
    while not queue.is_empty():
        temp = queue.pop()
        if problem.is_goal(temp.loc):
            return temp
        temp2 = temp.expand(problem)
        for node in temp2:
            if repeat_check == True:
                #referred to psuedocode from PA1 Spec
                if node in reachedSet:
                    if queue.contains(node) and (queue[node] > node.value("f")):
                        queue.__delitem__(node)
                        queue.add(node)
                else:
                    queue.add(node)
                    reachedSet.add(node)
            else:
                queue.add(node)
    return None

