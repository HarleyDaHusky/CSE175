#
# heuristic.py
#
# This script defines a utility class that can be used as an implementation
# of a frontier state (location) evaluation function for use in route-finding
# heuristic search algorithms. When a HeuristicSearch object is created,
# initialization code can be executed to prepare for the use of the heuristic
# during search. In particular, a RouteProblem object is typically provided 
# when the HeuristicFunction is created, providing information potentially
# useful for initialization. The actual heuristic cost function, simply
# called "h_cost", takes a state (location) as an argument.
#
# YOUR COMMENTS INCLUDING CITATIONS
# We're lookg for proximity for HeuristicFunction, so the initializer needs to have the start and end locations, and a 'empty' (set to 0) speed value
# For finding the cost, we will need to use the euclidean distance otherwise known as pythagorean theorem
#
# Had a problem where my Greedy best-first search and A star weren't outputting the correct values
# TA Mariel helped me discover my issue was (see line 65 vs line 66)
# YOUR NAME - THE DATE
#Jeffrey Peng 10/20/23


import route


class HeuristicFunction:
    """A heuristic function object contains the information needed to
    evaluate a state (location) in terms of its proximity to an optimal
    goal state."""

    def __init__(self, problem=None):
        self.problem = problem
        # PLACE ANY INITIALIZATION CODE HERE
        self.start = problem.start #starting location
        self.goal = problem.goal #ending locaiton
        self.speed = 0.0 #speed

    def h_cost(self, loc=None):
        """An admissible heuristic function, estimating the cost from
        the specified location to the goal state of the problem."""
        # a heuristic value of zero is admissible but not informative
        value = 0.0
        if loc is None:
            return value
        else:
            # PLACE YOUR CODE FOR CALCULATING value OF loc HERE
            #To find euclidean distance, we need to find action cost
            
            #for each locations in problem's map so that all other routes are filtered out
            for location in self.problem.map.loc_dict: 
                #for each possible connection in said map
                for possibleRoute in self.problem.map.connection_dict:
                    # cost = the cost of location and possible connections as starts and ends
                    tempCost = self.problem.map.get(location,possibleRoute)
                    # so long as cost is not 0
                    if tempCost is not None:
                        #euclidean_distance is the pythagorean theorem
                        tempDistance = self.problem.map.euclidean_distance(location,possibleRoute)
                        # pythagorean theorem start and end
                        # we have distance, now we need to find speed
                        # speed = distance / time from physics
                        tempSpeed = tempDistance / tempCost 
                        if tempSpeed > self.speed: #keep whichever speed is faster, also prevents negative speeds
                            self.speed = tempSpeed
            #tempDistance2 = self.problem.map.euclidean_distance(location, sel.goal)
            tempDistance2 = self.problem.map.euclidean_distance(loc, self.goal)
            # with the distance now found, we still need to find the speed.
            # from Physics, we know speed = distance / time and we have a speed from the function init
            value = tempDistance2 / self.speed
            return value