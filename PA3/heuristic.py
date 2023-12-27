#
# heuristic.py
#
# This Python script file provides two functions in support of minimax search
# using the expected value of game states. First, the file provides the
# function "expected_value_over_delays". This function takes as an argument
# a state of game play in which the current player has just selected an
# action. The function calculates the expected value of the state over all
# possible random results determining the amount of time before the
# Guardian changes gaze direction. This function calculates this value
# regardless of whose turn it is. The value of game states that result from
# different random outcomes is determined by calling "value". Second, the
# file provides a heuristic evaluation function for non-terminal game states.
# The heuristic value returned is between "max_payoff" (best for the
# computer player) and negative one times that value (best for the opponent).
# The heuristic function may be applied to any state of play. It uses
# features of the game state to predict the game payoff without performing
# any look-ahead search.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# PLACE ANY COMMENTS, INCLUDING ACKNOWLEDGMENTS, HERE
#
# PLACE YOUR NAME AND THE DATE HERE
# Jeffrey Peng 11-29-23


from parameters import *
from minimax import probability_of_time
from minimax import value


def expected_value_over_delays(state, ply):
    """Calculate the expected utility over all possible randomly selected
    Guardian delay times. Return this expected utility value."""
    val = 0.0

    # PLACE YOUR CODE HERE
    # Note that the value of "ply" must be passed along, without
    # modification, to any function calls that calculate the value 
    # of a state.

    # This function is to return the expected value of the state over all possible random delays.

    # min_time_steps, max_time_steps == 2, 5 --- for guardian game.
    # steps can only be 2 -> (to) 5 so for loop must be at least 2 -> 5

    # 
    for i in range(2,6):
        state.time_remaining = i
        #line 46 logic was from the Decision Theory Equation from 10-31 slide 24
        val += probability_of_time(i) * value(state, ply)

    return val


def heuristic_value(state):
    """Return an estimate of the expected payoff for the given state of
    game play without performing any look-ahead search. This value must
    be between the maximum payoff value and the additive inverse of the
    maximum payoff."""
    val = 0.0
    # PLACE YOUR CODE HERE
    # this function must quickly estimate the value of the given state of play, encoded by a Game object.
    # Computer is always West
    # Human is always East
    
    # set the computer and human value in accordance to the board size and west/east starting locations.
    # specifically: west is -board_size --- east is board_size
    # from parameters.py, payoff is -100 to 100
    valComputer = abs(board_size) - abs(state.w_loc)
    valHuman = abs(board_size) - abs(state.e_loc)
    #if the value of human and computer are the same, then don't take any risks
    if valHuman == valComputer:
        if state.current_turn is Player.west: #if the turn is west (Computer)
            val = -25 #1
        else: #state.current_turn is Player.east: #if the turn is east (Human)
            val = 25 #1
    # Regardless, always at least take 2 steps and max 4
    # if the human is ahead, computer will be riskier but otherwise will be safer
    elif valHuman > valComputer:
        if state.current_turn is Player.west:
            val = -100 #4
        else: #state.current_turn is Player.east:
            val = -50 #2
    # if the computer is ahead, the computer will be safer but otherwise will be riskier
    elif valHuman < valComputer:  
        if state.current_turn is Player.west:
            val = 100 #4
        else: #state.current_turn is Player.east:
            val = 50 #2
    
    return val
