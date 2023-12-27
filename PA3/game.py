#
# game.py
#
# This Python script file provides the infrastructure needed to play
# the Guardian Game. In particular, a Game class is provided which captures
# both the parameters of a whole game (e.g., who goes first, who won) and
# the current state of play (e.g., player locations, current motion action).
# The Guardian is in location zero, the West player has a negative valued
# location, and the East player has a positive valued location. The West
# play is always the computer player, and the East player is the human
# opponent. The player who gets the first turn is specified upon creation
# or during initialization of the game.
#
# The computer player's action choices are determined by calls to the
# function "minimax_action", which is implemented elsewhere. Games are
# initiated by the "play" method.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# David Noelle - Thu Nov  2 17:30:31 PDT 2023
#


import random
from parameters import *
from minimax import minimax_action


class Game:
    """An instance of the Guardian Game, including the current state of
    play, which is taken to be fully observable."""

    def __init__(self, west_first=True):
        # player that takes the fist turn ...
        if west_first:
            self.goes_first = Player.west
        else:
            self.goes_first = Player.east
        # the locations of the two players, West and East ...
        self.w_loc = -board_size
        self.e_loc = board_size
        # player whose turn it is ...
        self.current_turn = self.goes_first
        # number of steps to move ...
        self.action = None
        # number of time steps before the Guardian turns ...
        self.time_remaining = None
        # the winner ...
        self.winner = None

    def __repr__(self):
        """Return a textual description of the current state of
        game play."""
        if self.current_turn is Player.west:
            turn = 'W'
        else:
            turn = 'E'
        if self.winner is not None:
            if self.winner is Player.west:
                turn = 'W'
            else:
                turn = 'E'
            rep = "<GG W={}, E={}, {} wins>".format(self.w_loc,
                                                    self.e_loc,
                                                    turn)
        elif self.need_action():
            rep = "<GG W={}, E={}, {} choosing>". format(self.w_loc,
                                                         self.e_loc,
                                                         turn)
        else:
            rep = "<GG W={}, E={}, {} moving {} steps>".format(self.w_loc,
                                                               self.e_loc,
                                                               turn,
                                                               self.action)
        return rep

    def initialize_state(self, west_first=True):
        """Initialize the state of game play in preparation of starting a
        game session. This includes seeding the pseudo-random number
        generator used to select random Guardian delay times."""
        if west_first:
            self.goes_first = Player.west
        else:
            self.goes_first = Player.east
        self.w_loc = -board_size
        self.e_loc = board_size
        self.current_turn = self.goes_first
        self.action = None
        self.time_remaining = None
        self.winner = None
        # seed the pseudo-random number generator ...
        random.seed()

    def guardian_reached(self):
        """Return true iff one of the players has reached the
        location of the Guardian."""
        return (self.w_loc == 0) or (self.e_loc == 0)

    def check_for_winner(self):
        """If game termination conditions hold, record the winner
        in the current state of play."""
        if self.w_loc == 0:
            self.winner = Player.west
        elif self.e_loc == 0:
            self.winner = Player.east
        elif self.action is not None and \
                self.time_remaining is not None and \
                (self.action >= 0) and \
                (self.time_remaining == 0):
            # the Guardian has caught the current player in motion ...
            if self.current_turn is Player.west:
                self.winner = Player.east
            elif self.current_turn is Player.east:
                self.winner = Player.west
            else:
                self.winner = None
        else:
            self.winner = None

    def terminal_state(self):
        """Return true iff a winner has been established."""
        return self.winner is not None

    def payoff(self):
        """Return the maximum payoff value if the West player has
        won, and the additive inverse of the maximum payoff value if
        the East player has one. If this is not a terminal state,
        then return zero."""
        if self.terminal_state():
            if self.winner is Player.west:
                return max_payoff
            elif self.winner is Player.east:
                return -max_payoff
            else:
                return 0.0
        else:
            return 0.0

    def turn_is_done(self):
        """Return true iff the current player has successfully
        completed its move without being caught in motion by
        the Guardian."""
        return (self.action == 0) and (self.time_remaining > 0)

    def need_action(self):
        """Return true iff an action needs to be selected by
        the current player."""
        return self.action is None

    def need_time(self):
        """Return true iff the delay time of the Guardian needs
         to be randomly selected."""
        return self.time_remaining is None

    def toggle_current_player(self):
        """Pass the turn to the next player, noting that an
        action now needs to be selected by that player."""
        self.action = None
        self.time_remaining = None
        if self.current_turn is Player.west:
            self.current_turn = Player.east
        else:
            self.current_turn = Player.west

    def select_time_remaining(self):
        """Randomly select the delay time of the Guardian for
        the current turn. This time is two more than the
        number of heads in three coin flips."""
        self.time_remaining = 2
        self.time_remaining += random.randint(0, 1)
        self.time_remaining += random.randint(0, 1)
        self.time_remaining += random.randint(0, 1)

    def clock_tick(self):
        """Advance the current player toward the Guardian by a
        single step, up to the number of steps specified. When
        appropriate, pass the turn to the next player. Do not
        do anything if this is a terminal state or if a move action
        still needs to be selected by the current player."""
        # assumes check_for_winner has been called since last tick ...
        if not self.terminal_state() and not self.need_action():
            if self.turn_is_done():
                # the current player successfully completed their
                # move without being caught ...
                self.toggle_current_player()
            else:
                # decrement that number of steps to take and the
                # time remaining before the Guardian turns ...
                self.action += -1
                self.time_remaining += -1
                # move the current player closer to zero ...
                if self.current_turn is Player.west:
                    self.w_loc += 1
                elif self.current_turn is Player.east:
                    self.e_loc += -1
                else:
                    raise Exception("Invalid moving player.")

    def complete_turn(self):
        """Given a specified action and a delay time for the
        Guardian, update the state of play to reflect the result
        of the current player making their move. This could result
        in a terminal state, either due to arriving at the zero
        location or due to being caught by the Guardian, or it
        could result in the successful completion of a move without
        being caught by the Guardian. Do not do anything if the
        current state of play is terminal or if the current player
        is at the end of their turn."""
        if not self.terminal_state() and not self.turn_is_done():
            if self.current_turn is Player.west:
                steps_left = -self.w_loc
            elif self.current_turn is Player.east:
                steps_left = self.e_loc
            else:
                raise Exception("Invalid turn completion player.")
            # time until the turn is done ...
            ticks = min(self.action, self.time_remaining, steps_left)
            self.action = self.action - ticks
            self.time_remaining = self.time_remaining - ticks
            # advance the current player toward the zero ...
            if self.current_turn is Player.west:
                self.w_loc = self.w_loc + ticks
            elif self.current_turn is Player.east:
                self.e_loc = self.e_loc - ticks
            else:
                raise Exception("Invalid turn completion player.")

    def get_computer_action(self):
        """Perform a look-ahead search in order to select an action
        expected to lead to the highest payoff."""
        self.action = minimax_action(self)

    def get_opponent_action(self):
        """Prompt the human opponent for a selected action."""
        self.action = int(input('Enter number of steps to take [1-4]: '))

    def get_action(self):
        """Determine the action to be taken by the current player."""
        if self.current_turn is Player.west:
            self.get_computer_action()
        elif self.current_turn is Player.east:
            self.get_opponent_action()
        else:
            raise Exception("Invalid current player.")
        # check to make sure that the action is valid ...
        if (self.action < min_act_steps) or (self.action > max_act_steps):
            raise Exception("Action not between " + str(min_act_steps) +
                            " and " + str(max_act_steps) + ".")

    def play(self):
        """Play a round of the Guardian Game."""
        print("The Guardian Game")
        # select who goes first at random ...
        self.initialize_state(random.randint(0, 1) == 0)
        # announce who goes first ...
        if self.goes_first is Player.west:
            print("West goes first.")
        else:
            print("East goes first.")
        # iterate over turns until the game is over ...
        while not self.terminal_state():
            print(self)
            self.get_action()
            self.select_time_remaining()
            # iterate over clock ticks until the turn is done ...
            while not self.terminal_state() and not self.need_action():
                print(self)
                self.clock_tick()
                self.check_for_winner()
        if self.winner is Player.west:
            winner_name = "West"
        elif self.winner is Player.east:
            winner_name = "East"
        else:
            raise Exception("Invalid winning player.")
        # announce if the current player was caught ...
        if not self.guardian_reached():
            print("Guardian catches player in motion!")
        print(self)
        # announce the winner ...
        print(winner_name + " wins the game!")
