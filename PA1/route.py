#
# route.py
#
# This script defines several utility classes that can be used in the
# implementation of route-finding heuristic search algorithms. In particular,
# the file defines the following classes:
#   * RoadMap - encodes a graph containing locations and road segments
#   * RouteProblem - a formal search problem
#   * Node - a search tree node
#   * Frontier - the fringe of a search tree, implemented as a priority
#                queue sorted by one of three common node metrics
# Each class includes relevant methods for the given objects.
#
# The script also uses a global node expansion counter and a search
# depth limit, with the latter parameter used to stop infinite loops.
#
# The contents of this file are based on code assembled for the book
# "Artificial Intelligence: A Modern Approach" by Stuart Russell and
# Peter Norvig.
#
# David Noelle - Tue Sep 26 13:14:29 PDT 2023
#


import heapq
import math
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

    def locations(self):
        """Return a list of all of the locations on the map."""
        return self.loc_dict.keys()

    def get(self, start, end=None):
        """Return the road cost from start to end. If end is not given,
        return a dict containing {location: cost} entries."""
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

    def path_cost(self, start, road_list):
        """For the given sequence of road segments, specified by name,
        return the total cost of the path starting in the specified
        location and continuing along the given sequence of roads."""
        # Zero should be returned if the given road sequence does not
        # form a valid path from the given starting location.
        total_cost = 0.0
        loc = start
        for road in road_list:
            next_loc = self.get_result(loc, road)
            if next_loc is None:
                # the path is not valid
                return 0.0
            # increment the total path cost
            total_cost += self.get(loc, next_loc)
            # move on to next road segment
            loc = next_loc
        # return the total cost
        return total_cost

    def location_coordinates(self, loc):
        """Return the coordinates of the given location in the map."""
        (x, y) = self.loc_dict.setdefault(loc, (0.0, 0.0))
        if x and y:
            return x, y
        else:
            raise Exception("Unknown location - " + loc)

    def euclidean_distance(self, loc0, loc1):
        (x0, y0) = self.location_coordinates(loc0)
        (x1, y1) = self.location_coordinates(loc1)
        return math.sqrt(((x0 - x1) * (x0 - x1)) + ((y0 - y1) * (y0 - y1)))


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

    def __init__(self, loc, parent=None, road=None, path_cost=0.0, h_eval=0.0, h_fun=None):
        """Create a search tree Node, derived from a parent and a specified
        road segment (action)."""
        self.loc = loc
        self.parent = parent
        self.road = road
        self.path_cost = path_cost
        self.h_eval = h_eval
        self.h_fun = h_fun
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.loc)

    def __lt__(self, node):
        return self.loc < node.loc

    def value(self, sort_by='g'):
        if sort_by == 'g':
            return self.path_cost
        elif sort_by == 'h':
            return self.h_eval
        elif sort_by == 'f':
            return self.path_cost + self.h_eval
        else:
            return 0.0

    def child_node(self, problem, road, h_fun=None):
        """Return a node which is a child of the current node (self) via
        the given road segment."""
        child_loc = problem.result(self.loc, road)
        child_cost = self.path_cost + problem.action_cost(self.loc, child_loc)
        # If a heuristic function is provided as an argument, then use it.
        # Otherwise, use the heuristic function of the parent.
        if h_fun is None:
            if self.h_fun is None:
                child_h_fun = None
            else:
                child_h_fun = self.h_fun
        else:
            child_h_fun = h_fun
        if child_h_fun is not None:
            child_eval = child_h_fun.h_cost(child_loc)
        else:
            child_eval = 0.0
        end_node = Node(child_loc, self, road, child_cost, child_eval, child_h_fun)
        return end_node

    def expand(self, problem):
        """Return a list of the nodes reachable via a single road segment
        from this node."""
        vars.node_expansion_count += 1
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
    as a priority queue using one of three common cost metrics."""

    def __init__(self, root_node, sort_by='g'):
        """Create a frontier which is a priority queue sorted by the
        specified cost metric (g, h, or f). The frontier is initialized to
        contain the given root node the search tree."""
        self.sort_by = sort_by
        self.fringe = [(root_node.value(sort_by), root_node)]
        heapq.heapify(self.fringe)

    def __len__(self):
        """Return the size of the priority queue."""
        return len(self.fringe)

    def __contains__(self, query):
        """Returns True if and only if there is a node in the priority
        queue that matches the given query node."""
        # This supports the use of the "in" operator. If "f" is a
        # Frontier and "n" is a Node, the conditional test "(n in f)"
        # will be True if and only if there is a Node in "f" with the
        # same location as "n".
        return any([n == query for _, n in self.fringe])

    def __getitem__(self, query):
        """Returns the cost metric value for a node in the priority queue
        that matches the given query node."""
        # This supports checking the value of a Node in a Frontier. If
        # "f" is a Frontier and "n" is a Node, then "f[n]" will be the
        # value of the first Node in "f" that has the same location as "n".
        for value, n in self.fringe:
            if n == query:
                return value
        raise KeyError(str(query) + " is not in the frontier.")

    def __delitem__(self, query):
        """Delete the first node in the priority queue that matches the
        given query node."""
        # This supports the use of the "del" operator to remove a Node
        # from a Frontier. If "f" is a Frontier and "n" is a Node, then the
        # command "del f[n]" will remove the first Node with a location that
        # matches "n" from "f".
        try:
            del self.fringe[[n == query for _, n in self.fringe].index(True)]
        except ValueError:
            raise KeyError(str(query) + " is not in the frontier.")
        heapq.heapify(self.fringe)

    def is_empty(self):
        return len(self.fringe) == 0

    def contains(self, query):
        """Return True if and only if there is a node in the frontier with
        the same location as the query node."""
        return query in self

    def add(self, nodes):
        """Add the given node (or nodes) to the frontier."""
        if isinstance(nodes, list):
            for n in nodes:
                heapq.heappush(self.fringe, (n.value(self.sort_by), n))
        else:
            heapq.heappush(self.fringe, (nodes.value(self.sort_by), nodes))

    def pop(self):
        """Remove the next node from the frontier, returning it."""
        if self.fringe:
            return heapq.heappop(self.fringe)[1]
        else:
            raise Exception("Trying to pop from an empty frontier.")
