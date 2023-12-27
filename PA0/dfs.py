#
# dfs.py
#
# This file provides a function implementing depth-first search for a
# route-finding problem. Various search utilities from "route.py" are
# used in this function, including the classes RouteProblem, Node, and
# Frontier.
# 
# YOUR COMMENTS INCLUDING CITATIONS AND ACKNOWLEDGMENTS
# Copied over from bfs.py
# Textbook states depth-first search is LIFO (Last in First Out)
# Lecture slides state that DFS is also stored in stack instead of queue.
# because of LIFO, stack should be used for Frontier
# https://www.spiceworks.com/tech/devops/articles/fifo-vs-lifo/#:~:text=LIFO%20elements%20are%20added%20to,more%20importance%20to%20data%20recency.
# Above link: to understand better FIFO vs LIFO in Stack/Queue
# YOUR NAME - THE DATE
# Jeffrey Peng - 09/26/23


from route import Node
from route import Frontier


def DFS(problem, repeat_check=False):
    """Perform depth-first search to solve the given route finding
    problem, returning a solution node in the search tree, corresponding
    to the goal location, if a solution is found. Only perform repeated
    state checking if the provided boolean argument is true."""

    # PLACE YOUR CODE HERE

    initialState = Node(problem.start)
    if problem.is_goal(initialState.loc):
        return initialState
    LIFO_queue = Frontier(initialState, stack=True) #set stack = True since LIFO
    explored = set()
    while not LIFO_queue.is_empty():
        temp = LIFO_queue.pop()
        explored.add(initialState)
        if problem.is_goal(temp.loc):
            return temp
        temp2 = temp.expand(problem) #makes temp2 child nodes
        for node in temp2: #for node in child
            if repeat_check == True:
                if node not in explored: #if the node is not in reached set, add to reached set and Frontier
                    explored.add(node)
                    LIFO_queue.add(node)
            else:
                LIFO_queue.add(node) #add node to Frontier if not repeated check
    return None
