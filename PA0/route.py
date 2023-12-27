#
# route.py
#
# This script defines several utility classes that can be used in the
# implementation of route-finding search algorithms. In particular, the
# file defines the following classes:
#   * RoadMap - encodes a graph containing locations and road segments
#   * RouteProblem - a formal search problem
#   * Node - a search tree node
#   * Frontier - the fringe of a search tree, implemented as either a
#                queue or a stack
# Each class includes relevant methods for the given objects.
#
# The script also uses a global node expansion counter and a search
# depth limit, with the latter parameter used to stop infinite loops.
#
# The contents of this file are based on code assembled for the book
# "Artificial Intelligence: A Modern Approach" by Stuart Russell and
# Peter Norvig.
#
# David Noelle - Mon Sep 19 21:25:10 PDT 2022
#


from collections import deque
import vars


# Search depth limit, to avoid infinite loops ...
depth_limit = 20


class RoadMap:
    """A road map contains locations on a Cartesian plane and directed
    connections between locations, called road segments, each with a
    cost. Road segments also can have names."""

    def __init__(self, connection_dict=None, road_dict=None, loc_dict=None):
        # road segment costs indexed by start and end locations
        self.connection_dict = connection_dict or {}
        # mapping from location and road segment to resulting location
        self.road_dict = road_dict or {}
        # Cartesian coordinates of locations
        self.loc_dict = loc_dict or {}

    def add_location(self, loc, longitude, latitude):
        """Add a location with the given y and x coordinates."""
        self.loc_dict[loc] = (longitude, latitude)

    def add_road(self, start, end, name=None, cost=1.0):
        """Add a road from start to end with the given cost."""
        self.connection_dict.setdefault(start, {})[end] = cost
        if name is not None:
            self.road_dict.setdefault(start, {})[name] = end

    def get(self, start, end=None):
        """Return the road cost from start to end. If end is not given,
        return a dict containing {end location: cost} entries."""
        successors = self.connection_dict.setdefault(start, {})
        if end is None:
            return successors
        else:
            return successors.get(end)

    def get_result(self, start, road=None):
        """Return the resulting location name when starting in the given
        location and taking the given road segment. If the road is not
        specified, return a dict with {road name: location} entries."""
        successors = self.road_dict.setdefault(start, {})
        if road is None:
            return successors
        else:
            return successors.get(road)


class RouteProblem:
    """A description of a route finding problem on a given map."""

    def __init__(self, roadmap, start, goal=None):
        self.map = roadmap
        self.start = start
        self.goal = goal

    def actions(self, loc):
        """Return the road segment names leading from the given location."""
        return self.map.get_result(loc).keys()

    def result(self, loc, road):
        """Return the location at the end of the given road, starting at
        the given location."""
        return self.map.get_result(loc, road)

    def is_goal(self, loc):
        """Return True if the given location is the goal location."""
        return loc == self.goal

    def action_cost(self, start, end):
        """Return the cost of taking the road segment from start to end."""
        return self.map.get(start, end)


class Node:
    """A node in the search tree for a route finding problem."""

    def __init__(self, loc, parent=None, road=None, path_cost=0):
        """Create a search tree Node, derived from a parent and a specified
        road segment (action)."""
        self.loc = loc
        self.parent = parent
        self.road = road
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.loc)

    def __lt__(self, node):
        return self.loc < node.loc

    def child_node(self, problem, road):
        """Return a node which is a child of the current node (self) via
        the given road segment."""
        child_loc = problem.result(self.loc, road)
        child_cost = self.path_cost + problem.action_cost(self.loc, child_loc)
        end_node = Node(child_loc, self, road, child_cost)
        return end_node

    def expand(self, problem):
        """Return a list of the nodes reachable via a single road segment
        from this node."""
        vars.nodes_expanded_count += 1
        if self.depth >= depth_limit:
            # Return no children if at the depth limit ...
            return []
        else:
            return [self.child_node(problem, road)
                    for road in problem.actions(self.loc)]

    def path(self):
        """Return a list of nodes forming the path from the search tree root
        to this node."""
        this_node = self
        backwards_path = []
        while this_node:
            backwards_path.append(this_node)
            this_node = this_node.parent
        return list(reversed(backwards_path))

    def solution(self):
        """Return the sequence of road segments from the root of the search
        tree to this node."""
        return [node.road for node in self.path()[1:]]

    def solution_with_roads(self):
        """Return a list of tuples, each consisting of a road name and the
        resulting location name, corresponding to the path from the search
        tree root to this node."""
        this_node = self
        backwards_path = []
        while this_node:
            backwards_path.append((this_node.road, this_node.loc))
            this_node = this_node.parent
        return list(reversed(backwards_path))

    def solution_locations(self):
        """Return a list of location names corresponding to the path from 
        the search tree root to this node."""
        this_node = self
        backwards_path = []
        while this_node:
            backwards_path.append(this_node.loc)
            this_node = this_node.parent
        return list(reversed(backwards_path))

    def __eq__(self, other):
        # For the purposes of checking if a node is in a list, nodes are
        # considered equal if they have the same location.
        return isinstance(other, Node) and self.loc == other.loc

    def __hash__(self):
        # For the purposes of comparing nodes in a hash table, the hash
        # code for the corresponding location should be used.
        return hash(self.loc)


class Frontier:
    """A list of the nodes in the fringe of a search tree, implemented
    as a queue or a stack."""

    def __init__(self, root_node, stack=False):
        """Create a frontier which is a FIFO queue, by default, or a LIFO
        list (a stack) if specified by the argument boolean. The frontier
        is initialized to contain the given root node of a search tree."""
        self.lifo = stack
        if stack:
            self.nodes = [root_node]
        else:
            # Python provides the "deque" object to make pushes and pops
            # more efficient than simply using a list.
            self.nodes = deque([root_node])

    def is_empty(self):
        return len(self.nodes) == 0

    def contains(self, query_node):
        """Return True if and only if there is a node in the frontier with
        the same location as the query node."""
        return query_node in self.nodes

    def add(self, new_nodes):
        """Add the given node (or nodes) to the frontier."""
        if isinstance(new_nodes, list):
            # Add the nodes in "new_nodes" to the end of the "nodes" list.
            self.nodes.extend(new_nodes)
        else:
            # Add the given single node to the end of the "nodes" list.
            self.nodes.append(new_nodes)

    def pop(self):
        """Remove the next node from the frontier, returning it."""
        if self.lifo:
            # Remove and return the "last in" node.
            return self.nodes.pop()
        else:
            # Remove and return the "first in" node.
            return self.nodes.popleft()
