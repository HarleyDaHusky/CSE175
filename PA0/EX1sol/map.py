#
# map.py
#
# This script defines a class that encodes a simple road map. Each
# object of the ReadMap class encodes a graph containing locations and
# road segments. The class includes relevant methods for the objects.
#
# David Noelle - Tue Sep  5 14:52:32 PDT 2023
#
# Acknowledgments: Solution "path_cost" method by David Noelle. The Python 
# Tutorial at "python.org" was referenced while preparing this solution. No
# other assistance was received.
#


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
        """Return the road segment cost from start to end. If end is
        not given return a dict containing {location: cost} entries."""
        successors = self.connection_dict.setdefault(start, {})
        if successors is None:
            return None
        if end is None:
            return successors
        else:
            return successors.get(end)

    def get_result(self, start, road=None):
        """Return the resulting location name when starting in the given
        location and taking the given road segment. If the road is not
        specified, return a dict with {road name: location} entries."""
        successors = self.road_dict.setdefault(start, {})
        if successors is None:
            return None
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
