# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:43:44 2015

@author: stdm
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import pandas as pd


###############################################################################
###   Hyper-parameters for training
###############################################################################
LEARNING_RATE = 0.1
CONVERGENCE_DELTA = 0.001


###############################################################################
###   M A I N   
###############################################################################
def main():
    # 1. Load train- and generate test data
    df = pd.read_excel("hydrocarbons.xlsx")
    X_train = df['nr_molecules']
    Y_train = df['heat_release']
    X_test = [7, 9, 2]
        
    # 2. Preprocess data using z transform (zero mean, unit variance)
    std_scale_x = preprocessing.StandardScaler().fit(X_train)
    std_scale_y = preprocessing.StandardScaler().fit(Y_train)
    X_train = std_scale_x.transform(X_train)
    Y_train = std_scale_y.transform(Y_train)
    X_test = std_scale_x.transform(X_test)
    
    # 3. Train model
    #   h_lr: the linear regression hypothesis function
    #   J_se: the squared error loss function
    #   batch_gradient_descent: the gradient descent optimization function
    theta_optimized = train_model(h_lr, J_se, batch_gradient_descent, (X_train, Y_train))
    print 'Optimized Parameters (ztrans domain): ', theta_optimized
    
    # 4. Apply the trained model
    Y_test = apply_model(h_lr, theta_optimized, X_test)
    X_test = std_scale_x.inverse_transform(X_test) #bring the results back to the original scale
    Y_test = std_scale_y.inverse_transform(Y_test)
    print 'Results: ', zip(X_test, Y_test)
    
    raw_input('Press any key to exit...')


###############################################################################
###   high level functions controlling learning & application of the model
###############################################################################
def train_model(hypothesis_function, cost_function, optimization_function, training_examples):
    theta_initial = (0, 0)
    learning_rate = LEARNING_RATE
    optimized_theta = optimization_function(theta_initial, learning_rate, cost_function, hypothesis_function, training_examples)

    #simple check if optimization took place (or the initial values where 
    #already perfect...)    
    nothing_happened = True
    for i in range(len(optimized_theta)):
        if theta_initial[i] != optimized_theta[i]:
            nothing_happened = False
            break
    if nothing_happened:
        print "No optimization took place. Program will exit now."
        exit()
    
    return optimized_theta

def apply_model(hypothesis_function, trained_parameters, data):
    results = []
    for x in data:
        y = hypothesis_function(x, trained_parameters)
        results.append(y)
    return results


###############################################################################
###   linear regression
###############################################################################
def h_lr(x, theta, derivative=False, derivative_dimension=0):
    '''
    The linear regression hypthesis function, receiving a single data point x 
    and parameter vector theta, returning y as in y = theta_0 + theta_1*x.
    Theta is a tuple containg theta_0 and theta_1.
    If derivative != 0, the value of the partial derivative of h_lr(x) with 
    respect to the derivative_dimension's parameter is returned, otherwise y as 
    in y = theta_0 + theta_1*x.
    '''
    #TODO
    
def J_se(h, theta, X, Y, derivative=False, derivative_dimension=0):
    '''
    The squared error cost function regarding a specific hypothesis function h,
    its parameterization theta and a set of training examples (X, Y). 
    The hypothesis function h has an interface like h_lr() above. X is a matrix 
    of training vectors and Y a matrix of corresponding ground truth.
    If derivative != 0, the value of the partial derivative of J_se(h, theta) 
    with respect to the derivative_dimension's parameter is returned, otherwise 
    the squared error as a float
    '''
    if not derivative:
        pass
        #TODO
    else: #partial derivatives of the cost function are expected as a result
        pass
        #TODO
        

###############################################################################
###   gradient descent
###############################################################################
def batch_gradient_descent(initial_theta, alpha, cost_function, hypothesis_function, training_examples):
    '''
    Performs batch (i.e. all training examples at once) gradient descent using 
    the given cost- and hypothesis functions with the given initial parameters
    theta and learning rate alpha.
    Returns the optimized parameters as a list.
    '''
    optimized_theta = list(initial_theta[:])
    last_cost = current_cost = 999999.0 #something big to start off the loop
    X = training_examples[0]
    Y = training_examples[1]
    
    create_plot(cost_function, hypothesis_function, X, Y)
    while True:
        #TODO
        #.
        #.
        #.
        update_plot_lr(X, Y, optimized_theta, current_cost)
        if abs(last_cost-current_cost) < CONVERGENCE_DELTA:
            break;

    return optimized_theta


###############################################################################
###   visualization
###############################################################################
def create_plot(J, h, X, Y):
    '''
    Creates two subplots:
    Upper shows a scatter plot of the data.
    Lower shows the contour of the cost surface (range has to be set according 
    to expected parameter values).
    '''        
    plt.subplot(2, 1, 1)
    plt.axis([min(X), max(X), min(Y), max(Y)])
    plt.title('X vs Y')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.ion()
    plt.plot(X, Y,'*') #plot the data points

    plt.subplot(2, 1, 2)
    theta_0 = np.linspace(-2.0, 2.0, 100)
    theta_1 = np.linspace(-2.0, 2.0, 100)
    cost = np.zeros(shape=(theta_0.size, theta_1.size))
    for i, t0 in enumerate(theta_0):
        for j, t1 in enumerate(theta_1):
            cost[j][i] = J(h, (t0, t1), X, Y)
    plt.contour(theta_0, theta_1, cost, np.logspace(-2, 3, 15))
    plt.title('Cost contour')    
    plt.xlabel('theta_0')
    plt.ylabel('theta_1')

    plt.show(block=False)

def update_plot_lr(X, Y, theta, cost):
    '''
    Updates the two subplots to show the learning progrss (to be called from 
    within the optimization loop).
    Upper shows regression straight superimposed on data scatter plot.
    Lower shows current position on cost surface.
    '''
    plt.subplot(2, 1, 1)
    x_min, x_max = min(X), max(X)    
    y_hmin, y_hmax = h_lr(x_min, theta), h_lr(x_max, theta)
    plt.title('X vs. Y; cost: {:.5f}'.format(cost))
    plt.plot([x_min, x_max], [y_hmin, y_hmax], 'r')

    plt.subplot(2, 1, 2)
    plt.title('Cost contour; theta_0={:.2f}'.format(theta[0]) + ', theta_1={:.2f}'.format(theta[1]))
    plt.scatter(theta[0], theta[1])
    
    plt.pause(0.001)

    
# start the script if executed directly    
if __name__ == '__main__':
    main()
