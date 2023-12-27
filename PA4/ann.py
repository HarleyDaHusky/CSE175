#
# ann.py
#
# This script implements an artificial neural network model for the
# Iris classification task (which is pretty easy).
#
# Note that this script requires the installation of the following Python
# packages: PyTorch (torch), Pandas (pandas), and Scikit-learn (scikit-learn).
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# David Noelle - Thu Nov 30 17:48:40 PST 2023
#

# PyTorch - Deep Learning Models
import torch
import torch.nn as nn
# Pandas - Data Loading and Manipulation
import pandas as pd
# Scikit-learn - Tools for Generating Training and Testing Sets
from sklearn.model_selection import train_test_split


def load_iris_data(test_fraction=0.2):
    """Load the Iris data set from the UC Irvine Machine Learning Repository,
    returning the data set as four PyTorch tensors: training set input features,
    testing set input features, training set targets, and testing set targets.
    The optional 'test_fraction' argument specifies how much of the data set
    is to be used as testing set examples."""
    # See "https://archive.ics.uci.edu/ml/datasets/iris".

    # URL of data set as "comma separated values" ...
    iris_csv_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    # labels for the input and output features ...
    column_labels = ['Sepal_Length',
                     'Sepal_Width',
                     'Petal_Length',
                     'Petal_Width',
                     'Class']
    # Use Pandas to read the data set from the UCI repository ...
    iris = pd.read_csv(iris_csv_url, names=column_labels)
    # Replace class names with integer target labels ...
    class_index = {'Iris-setosa': 0,
                   'Iris-versicolor': 1,
                   'Iris-virginica': 2}
    iris['Class'] = iris['Class'].apply(lambda x: class_index[x])
    # Use Scikit to split the data set into a training set and testing set, with
    # X being the input features and y being the targets ...
    X = iris.drop('Class', axis=1).values
    y = iris['Class'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_fraction)
    # Convert these into tensors for use in PyTorch ...
    X_train_tensor = torch.FloatTensor(X_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_train_tensor = torch.LongTensor(y_train)
    y_test_tensor = torch.LongTensor(y_test)
    return X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor


def train_model(model, X, y, lrate=0.01, epochs=100, report_epoch=10):
    """Train the given model on the given data set, using the specified
    learning rate, for the given number of epochs. Print a progress report
    every 'report_epoch' epochs."""
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lrate)
    # Iterate over training epochs ...
    for i in range(epochs):
        # Calculate network outputs ...
        y_hat = model.forward(X)
        # Calculate loss (error) value ...
        loss = criterion(y_hat, y)
        # Periodically report the training set error ...
        if i % report_epoch == 0:
            print(f'Epoch {i} Loss = {loss}')
        # Zero out previous error gradient values ...
        optimizer.zero_grad()
        # Calculate gradient values ...
        loss.backward()
        # Update network parameters ...
        optimizer.step()


def test_model(model, X, y):
    """Return the accuracy of the given trained model on the given data set,
    specified as input features (X) and output targets (y)."""
    predictions = []
    # Don't calculate gradient values during testing ...
    with torch.no_grad():
        # Iterate over input patterns ...
        for x in X:
            # Calculate the network output ...
            y_hat = model.forward(x)
            # Find the output element with the maximum activation, and use
            # its index as the predicted class, recording the prediction ...
            predictions.append(y_hat.argmax().item())
    # Use Pandas to make a table (DataFrame) of data set examples, listing the
    # target class, the predicted class, and a binary label indicating if the
    # prediction was correct (1) or not (0) ...
    examples = pd.DataFrame({'Y': y, 'YHat': predictions})
    examples['Correct'] = [1 if targ == pred else 0
                           for targ, pred in zip(examples['Y'], examples['YHat'])]
    accuracy = examples['Correct'].sum() / len(examples)
    return accuracy
