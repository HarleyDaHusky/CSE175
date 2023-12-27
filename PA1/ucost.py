#
# ucost.py
#
# This file provides a function implementing uniform cost search for a
# route finding problem. Various search utilities from "route.py" are
# used in this function, including the classes RouteProblem, Node, and
# Frontier.
#
# YOUR COMMENTS INCLUDING CITATIONS
# Folloed given psuedocode with slight changes
# YOUR NAME - THE DATE
# Jeffrey Peng 10/18/23


from route import Node
from route import Frontier


def uniform_cost_search(problem, repeat_check=False):
    """Perform uniform cost search to solve the given route finding
    problem, returning a solution node in the search tree, corresponding
    to the goal location, if a solution is found. Only perform repeated
    state checking if the provided boolean argument is true."""

    # PLACE YOUR CODE HERE

    initialState = Node(problem.start)

    if problem.is_goal(initialState.loc):
        return initialState

    queue = Frontier(initialState, sort_by='g') #used g as it states in PA1spec
    reachedSet = set()
    reachedSet.add(initialState)
    while not queue.is_empty():
        temp = queue.pop()
        if problem.is_goal(temp.loc):
            return temp
        temp2 = temp.expand(problem)
        for node in temp2:
            if repeat_check:
                #copy and pasted BDS until this point
                #referred to psuedocode from PA1 Spec
                if node in reachedSet:
                    if queue.contains(node) and (queue[node] > node.value(sort_by="g")):
                        queue.__delitem__(node)
                        queue.add(node)
                else:
                    queue.add(node)
                    reachedSet.add(node)
            else:
                queue.add(node)
    return None
