#
# arch.py
#
# This script implements three Python classes for three different artificial
# neural network architectures: no hidden layer, one hidden layer, and two
# hidden layers. Note that this script requires the installation of the
# PyTorch (torch) Python package.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# PLACE ANY COMMENTS, INCLUDING ACKNOWLEDGMENTS, HERE.
# ALSO, PROVIDE ANSWERS TO THE FOLLOWING TWO QUESTIONS.
# Ran 10 tests, data provided here: https://docs.google.com/spreadsheets/d/1PkmaOANj3zX_0_INEotoRZZqC-U1kwOi3ZnDDy-l8dY/edit?usp=sharing

# Which network architecture achieves the lowest training set error?
# Two Hidden Layer/AnnTwoHid which yielded a 0.05059 Average and a Lowest of 0.032

# Which network architecture tends to exhibit the best testing set accuracy?
# One Hidden Layer/AnnOneHid which yielded a 0.9634 Average. Extremely close to Two Hidden Layer/AnnTwoHid which in my tests yielded a 0.96 Average.
# These functions were always the same except for one test (test 7) which AnnOneHid had a better average than AnnTwoHid 

# PLACE YOUR NAME AND THE DATE HERE
# JEFFREY PENG 12-15-23

# PyTorch - Deep Learning Models
import torch.nn as nn
import torch.nn.functional as F


# Number of input features ...
input_size = 4
# Number of output classes ...
output_size = 3

# Given sample lines:
# self.my_layer = nn.Linear(in_features = 6, out_features = 9)
# my_layer_net = self.my_layer
# my_layer_act = F.relu(self.my_layer(x))
class AnnLinear(nn.Module):
    """Class describing a linear artificial neural network, with no hidden
    layers, with inputs directly projecting to outputs."""
    # A network with no hidden layer, connecting a 4-element input vector to a
    # 3-element linear output layer.

    def __init__(self):
        super().__init__()
        # PLACE NETWORK ARCHITECTURE CODE HERE
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x):
        # PLACE YOUR FORWARD PASS CODE HEREpip install numpy
        y_hat = self.linear(x)
        return y_hat


class AnnOneHid(nn.Module):
    """Class describing an artificial neural network with one hidden layer,
    using the rectified linear (ReLU) activation function."""
    # A network with a single hidden layer of 20 processing units, mediating the
    # production of a 3-element output vector from a 4-element input vector
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(input_size, 20)
        self.hiddenLayer1 = nn.Linear(20, output_size)

    def forward(self, x):
        # PLACE YOUR FORWARD PASS CODE HERE
        x = F.relu(self.linear(x))
        y_hat = self.hiddenLayer1(x)
        return y_hat


class AnnTwoHid(nn.Module):
    """Class describing an artificial neural network with two hidden layers,
    using the rectified linear (ReLU) activation function."""
    # A network with two successive hidden layers between a 4-element input and a
    # 3-element output, with the first hidden layer having 16 processing units
    # and the second one having 12 processing units
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(input_size, 16)
        self.hiddenLayer1 = nn.Linear(16,12)
        self.hiddenLayer2 = nn.Linear(12,output_size)

    def forward(self, x):
        x = F.relu(self.linear(x))
        x = F.relu(self.hiddenLayer1(x))
        y_hat = self.hiddenLayer2(x)
        return y_hat
