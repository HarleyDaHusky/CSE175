#
# main.py
#
# This script provides a top-level driver to exercise search algorithm
# functions. The script contains the parameters for a route-finding
# problem: a starting location, a goal location, and a road map. These
# parameters are assembled into a formal problem specification, and that
# object is used to run four tests of search functions. Breadth-first
# search is run with and without repeated state checking. Then, depth-first
# search is run with and without repeated state checking. Solutions
# are output to the console, along with search algorithm performance
# statistics.
#
# David Noelle - Mon Sep 19 21:56:25 PDT 2022
#


import sys
import vars
from route import RoadMap
from route import RouteProblem
import bfs
import dfs


start_location = 'home'
goal_location = 'bookstore'

test_map = RoadMap(dict(
        # road segment costs
        home=dict(corner_store=3.1,
                  fire_station=3.3,
                  coffee_shop=3.6,
                  bus_station=6.9),
        corner_store=dict(home=3.1,
                          school=4.2),
        fire_station=dict(home=3.3,
                          coffee_shop=5.1,
                          police_station=9.9),
        school=dict(corner_store=4.2,
                    bus_station=5.8,
                    stadium=18.1),
        coffee_shop=dict(home=3.6,
                         fire_station=5.1,
                         bus_station=4.9,
                         donut_shop=6.6),
        bus_station=dict(home=6.9,
                         school=5.8,
                         coffee_shop=4.9,
                         fast_food=4.2,
                         stadium=16.0),
        police_station=dict(fire_station=9.9,
                            grocery_store=3.9,
                            factory=6.3),
        donut_shop=dict(coffee_shop=6.6,
                        grocery_store=3.7),
        grocery_store=dict(police_station=3.9,
                           donut_shop=3.7,
                           gym=4.2),
        gym=dict(grocery_store=4.2,
                 factory=4.9,
                 car_dealer=13.0),
        factory=dict(police_station=6.3,
                     gym=4.9),
        car_dealer=dict(gym=13.0,
                        truck_stop=15.3,
                        fast_food=27.9),
        truck_stop=dict(car_dealer=15.3,
                        bookstore=1.4),
        fast_food=dict(bus_station=4.2,
                       bookstore=4.2,
                       car_dealer=27.9),
        bookstore=dict(fast_food=4.2,
                       truck_stop=1.4,
                       diner=14.4),
        stadium=dict(school=18.1,
                     bus_station=16.0,
                     ranch=15.4),
        ranch=dict(stadium=15.4,
                   diner=19.1,
                   park=35.5),
        diner=dict(ranch=19.1,
                   bookstore=14.4),
        park=dict(ranch=35.5)),
                   dict(
        # road segment names
        home=dict(path='corner_store',
                  sidewalk='fire_station',
                  hill_street='coffee_shop',
                  central='bus_station'),
        corner_store=dict(path='home',
                          north_street='school'),
        fire_station=dict(sidewalk='home',
                          narrows='coffee_shop',
                          back_street='police_station'),
        school=dict(north_street='corner_store',
                    elm_street='bus_station',
                    hill_pass='stadium'),
        coffee_shop=dict(hill_street='home',
                         narrows='fire_station',
                         the_avenue='bus_station',
                         side_street='donut_shop'),
        bus_station=dict(central='home',
                         elm_street='school',
                         the_avenue='coffee_shop',
                         highway_north='fast_food',
                         stadium_street='stadium'),
        police_station=dict(back_street='fire_station',
                            lower_main='grocery_store',
                            grimey_place='factory'),
        donut_shop=dict(side_street='coffee_shop',
                        upper_main='grocery_store'),
        grocery_store=dict(lower_main='police_station',
                           upper_main='donut_shop',
                           alley='gym'),
        gym=dict(alley='grocery_store',
                 damp_drive='factory',
                 long_drive='car_dealer'),
        factory=dict(grimey_place='police_station',
                     damp_drive='gym'),
        car_dealer=dict(long_drive='gym',
                        back_road='truck_stop',
                        overgrown_path='fast_food'),
        truck_stop=dict(back_road='car_dealer',
                        highway_south='bookstore'),
        fast_food=dict(highway_north='bus_station',
                       highway_east='bookstore',
                       overgrown_path='car_dealer'),
        bookstore=dict(highway_east='fast_food',
                       highway_south='truck_stop',
                       access_road='diner'),
        stadium=dict(hill_pass='school',
                     stadium_street='bus_station',
                     gravel_road='ranch'),
        ranch=dict(gravel_road='stadium',
                   old_highway='diner',
                   dirt_road='park'),
        diner=dict(old_highway='ranch',
                   access_road='bookstore'),
        park=dict(dirt_road='ranch')),
                   dict(
        # location coordinates
        home=(32.1, 54.4),
        corner_store=(37.9, 58.2),
        school=(42.0, 55.5),
        fire_station=(28.1, 50.3),
        coffee_shop=(36.6, 49.8),
        bus_station=(42.0, 50.0),
        stadium=(59.9, 49.1),
        ranch=(67.7, 44.0),
        park=(86.0, 42.0),
        donut_shop=(37.6, 41.9),
        police_station=(27.7, 36.5),
        grocery_store=(34.1, 39.9),
        fast_food=(48.0, 36.4),
        gym=(35.3, 32.3),
        diner=(69.0, 32.0),
        car_dealer=(47.7, 22.2),
        bookstore=(64.0, 24.2),
        truck_stop=(66.6, 18.1),
        factory=(31.9, 28.2)))


def main():
    print("UNINFORMED SEARCH ALGORITHM COMPARISON")
    problem = RouteProblem(test_map, start_location, goal_location)
    print("TESTING BFS WITHOUT REPEATED STATE CHECKING")
    vars.nodes_expanded_count = 0
    sol = bfs.BFS(problem, False)
    print("Solution:")
    if sol is None:
        print("No solution found.")
    else:
        print(f'Start at {start_location}.')
        for (r, d) in sol.solution_with_roads()[1:]:
            print(f'Take {r} to {d}.')
        print("Depth =", sol.depth)
        print("Path Cost =", sol.path_cost)
        print("Number of Node Expansions =", vars.nodes_expanded_count)
    print("TESTING BFS WITH REPEATED STATE CHECKING")
    vars.nodes_expanded_count = 0
    sol = bfs.BFS(problem, True)
    print("Solution:")
    if sol is None:
        print("No solution found.")
    else:
        print(f'Start at {start_location}.')
        for (r, d) in sol.solution_with_roads()[1:]:
            print(f'Take {r} to {d}.')
        print("Depth =", sol.depth)
        print("Path Cost =", sol.path_cost)
        print("Number of Node Expansions =", vars.nodes_expanded_count)
    print("TESTING DFS WITHOUT REPEATED STATE CHECKING")
    vars.nodes_expanded_count = 0
    sol = dfs.DFS(problem, False)
    print("Solution:")
    if sol is None:
        print("No solution found.")
    else:
        print(f'Start at {start_location}.')
        for (r, d) in sol.solution_with_roads()[1:]:
            print(f'Take {r} to {d}.')
        print("Depth =", sol.depth)
        print("Path Cost =", sol.path_cost)
        print("Number of Node Expansions =", vars.nodes_expanded_count)
    print("TESTING DFS WITH REPEATED STATE CHECKING")
    vars.nodes_expanded_count = 0
    sol = dfs.DFS(problem, True)
    print("Solution:")
    if sol is None:
        print("No solution found.")
    else:
        print(f'Start at {start_location}.')
        for (r, d) in sol.solution_with_roads()[1:]:
            print(f'Take {r} to {d}.')
        print("Depth =", sol.depth)
        print("Path Cost =", sol.path_cost)
        print("Number of Node Expansions =", vars.nodes_expanded_count)
    print("ALGORITHM COMPARISON COMPLETE")
    sys.exit(0)


# In PyCharm, press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
