#
# minimax.py
#
# This Python script file provides functions for implementing minimax search
# using the expected value of game states. The top-level function is called
# "minimax_action", which assumes that it is the computer player's turn.
# This search depends on the initialization of the probability distribution
# over Guardian delay times, calculated using "calculate_time_distribution".
# The function "value" returns the estimated value of a state of play, using
# minimax to back-up values based on player choices and using a calculation
# of the expected utility of a state over random Guardian delay times. The
# game tree is implicit in the recursive calls to "value". At a maximum ply
# of the search, the minimax process is replaced by a value determined by
# a heuristic evaluation function applied to the current state of play.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# David Noelle - Thu Nov  2 17:31:48 PDT 2023
#


import copy
from game import *


# a dictionary containing the probability distribution of delay times ...
time_prob = {}


def calculate_time_distribution():
    """Initialize the dictionary containing the probability distribution
    of delay times. The delay is assumed to result by adding two to the
    number of heads in three random coin flips."""
    # a dictionary containing the number of ways to randomly produce a
    # given delay amount ...
    counts = {}
    # initialize counts to zero ...
    for total in range(0, 3+1):
        counts[total] = 0
    # iterate over all possible coin flips ...
    for coin1 in range(0, 1+1):
        for coin2 in range(0, 1+1):
            for coin3 in range(0, 1+1):
                coin_sum = coin1 + coin2 + coin3
                # increment the count of the number of ways to randomly
                # produce this sum ...
                counts[coin_sum] += 1
    # convert counts into probabilities by dividing by the total number
    # of possible outcomes (2^3 = 8), with outcomes from 2 to 5 ...
    for total in range(2, 5+1):
        time_prob[total] = float(counts[total-2]) / 8.0


def probability_of_time(total):
    """Return the probability of randomly selecting the given total
    amount of Guardian delay time, ranging from 2 to 5 steps."""
    return time_prob[total]


def minimax_action(parent_state):
    """Use the minimax algorithm to estimate the minimax values of
    the states of play resulting from all of the possible actions.
    Return the action with the highest minimax value."""
    best_action = None
    # initialize the best value to something truly awful ...
    best_value = -max_payoff - 1.0
    # copy the state of play so modifications to it don't affect
    # the Game object provided as an argument to this function ...
    state = copy.copy(parent_state)
    # iterate over all possible actions ...
    for act in range(min_act_steps, max_act_steps+1):
        state.action = act
        # calculate the value of the state of play resulting from
        # taking this action ...
        this_act_value = value(state, 0)
        # print("minimax: action = " + str(act) + "; value = " + str(this_act_value))
        # record the action corresponding to the highest value ...
        if this_act_value > best_value:
            best_value = this_act_value
            best_action = act
    return best_action


def value(parent_state, ply):
    """Return the value of the given state of play. The second argument
    specifies the current ply of the look-ahead search, allowing the
    value to be determined by a heuristic evaluation function once the
    ply limit is reached."""
    # copy the state of play so modifications to it don't affect
    # the Game object provided as an argument to this function ...
    state = copy.copy(parent_state)
    state.check_for_winner()
    if state.terminal_state():
        # the value of terminal states are their payoff ...
        return state.payoff()
    elif ply >= max_ply:
        # the ply limit has been reached, so use the heuristic ...
        return heuristic_value(state)
    elif state.time_remaining is not None and state.time_remaining > 0:
        # the current state of play is in the midst of a move action,
        # so the state needs to be updated to the end of the turn and
        # the value of the resulting state is returned ...
        return expected_value_after_move(state, ply)
    elif state.need_action():
        # calculate the minimax value for this state of play, which is
        # the start of one of the player's turns ...
        return minimax_value_over_actions(state, ply)
    else:
        # calculate the expected utility over all possible randomly
        # selected delay times of the current state of play ...
        return expected_value_over_delays(state, ply)


def expected_value_after_move(state, ply):
    """Play out the current turn, given the selected action and the
    randomly selected Guardian delay time. Return the value of the
    state of play that arises when the turn is passed to the next
    player."""
    state.complete_turn()
    state.check_for_winner()
    if state.terminal_state():
        return state.payoff()
    else:
        state.toggle_current_player()
        return value(state, ply)


def minimax_value_over_actions(state, ply):
    """Return the minimax value of the current state of play. If
    the current player is the computer player (a MAX node), then
    identify the maximum value over possible actions. If the
    current player is the opponent (a MIN node), then identify
    the minimum value over possible actions."""
    if state.current_turn is Player.west:
        return max_value_over_actions(state, ply)
    elif state.current_turn is Player.east:
        return min_value_over_actions(state, ply)
    else:
        raise Exception("Invalid minimax over actions player.")


def max_value_over_actions(state, ply):
    """Return the minimax value for the current state of play,
    in which the computer player is selecting an action."""
    # if the computer player went first, then this is the time
    # to increment the ply of the look-ahead search ...
    if state.goes_first is Player.west:
        new_ply = ply + 1
    elif state.goes_first is Player.east:
        new_ply = ply
    else:
        raise Exception("Invalid max over actions initial player.")
    # initialize the best value to something awful for the
    # computer player ...
    best_value = -max_payoff - 1.0
    # iterate over possible actions ...
    for act in range(min_act_steps, max_act_steps+1):
        state.action = act
        # calculate the value of the state of play resulting from
        # taking this action ...
        this_act_value = value(state, new_ply)
        # record the maximum value over actions ...
        if this_act_value > best_value:
            best_value = this_act_value
    return best_value


def min_value_over_actions(state, ply):
    """Return the minimax value for the current state of play,
    in which the opponent player is selecting an action."""
    # if the opponent player went first, then this is the time
    # to increment the ply of the look-ahead search ...
    if state.goes_first is Player.west:
        new_ply = ply
    elif state.goes_first is Player.east:
        new_ply = ply + 1
    else:
        raise Exception("Invalid min over actions initial player.")
    # initialize the best value to something awful for the
    # opponent player ...
    best_value = max_payoff + 1.0
    # iterate over possible actions ...
    for act in range(min_act_steps, max_act_steps+1):
        state.action = act
        # calculate the value of the state of play resulting from
        # taking this action ...
        this_act_value = value(state, new_ply)
        # record the minimum value over actions ...
        if this_act_value < best_value:
            best_value = this_act_value
    return best_value


# Usually, import statements are placed at the beginning of a
# file. These appear at the end to avoid circular dependencies
# while keeping the assignment solution in its own file,
# namely "heuristic.py".
from heuristic import expected_value_over_delays
from heuristic import heuristic_value
