#
# main.py
#
# This script provides a top-level driver to exercise some artificial
# neural network code, focusing on learning the Iris classification
# task (which is pretty easy).
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# David Noelle - Thu Nov 30 17:49:12 PST 2023
#

from arch import AnnLinear
from arch import AnnOneHid
from arch import AnnTwoHid
from ann import load_iris_data
from ann import train_model
from ann import test_model
import sys


def main():
    # Load the data set ...
    print("DOWNLOADING THE IRIS DATA SET")
    train_in, test_in, train_targ, test_targ = load_iris_data()

    # Create a linear model ...
    model_0hid = AnnLinear()
    # Train the linear model ...
    print("\nTRAINING LINEAR MODEL")
    train_model(model_0hid, train_in, train_targ)
    # Report test set accuracy ...
    test_accuracy = test_model(model_0hid, test_in, test_targ)
    print(f'Test Set Accuracy = {test_accuracy}')

    # Create a model with one hidden layer ...
    model_1hid = AnnOneHid()
    # Train the linear model ...
    print("\nTRAINING MODEL WITH ONE HIDDEN LAYER")
    train_model(model_1hid, train_in, train_targ)
    # Report test set accuracy ...
    test_accuracy = test_model(model_1hid, test_in, test_targ)
    print(f'Test Set Accuracy = {test_accuracy}')

    # Create a model with two hidden layers ...
    model_2hid = AnnTwoHid()
    # Train the linear model ...
    print("\nTRAINING MODEL WITH TWO HIDDEN LAYERS")
    train_model(model_2hid, train_in, train_targ)
    # Report test set accuracy ...
    test_accuracy = test_model(model_2hid, test_in, test_targ)
    print(f'Test Set Accuracy = {test_accuracy}')

    sys.exit(0)


# In PyCharm, press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
