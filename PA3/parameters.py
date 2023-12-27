#
# parameters.py
#
# This Python script file gathers together parameters for the minimax
# solution to the Guardian Game.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# David Noelle - Thu Nov  2 17:32:10 PDT 2023
#


from enum import Enum


# player identity, West player or East player ...
Player = Enum('Player', 'west east')

# The number of steps each player starts from the Guardian ...
board_size = 13

# The minimum and maximum time steps before the Guardian turns ...
min_time_steps = 2
max_time_steps = 5

# The minimum and maximum action selection steps ...
min_act_steps = 1
max_act_steps = 4

# The maximum payoff value, symmetric around zero ...
max_payoff = 100.0

# maximum number of ply to search before applying heuristic ...
max_ply = 3
