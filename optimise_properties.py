from __future__ import division, print_function, with_statement
import subprocess
import numpy as np
from scipy import optimize
import os
import glob
import math
import time
import simulate
import inputs

def calc_g(exp, data):
    top = np.sum((exp - data) **2)
    average = np.mean(exp)
    bottom = np.sum((data - average)**2)

    if bottom > 1E-6:
        g =1-((top)/(bottom))**(0.5)
    else: 
        g = 2
    return g

def calc_r_squared(exp, model):
    '''Return the coefficient of determination to characterise
    the likelihood that a model is adequately explaining some data'''
    exp_average = np.mean(exp)
    top = np.sum((exp - model)**2)
    bottom = np.sum((exp-exp_average)**2)
    r_squared = 1 - top / bottom
    
    return r_squared

def calc_scaled_sum_of_squares(exp, data):
    '''Calculate the sum of squares of the residuals between some
       experimental data and some data that has been generated to fit it.'''
    residuals_squared = (exp*((exp - data)** 2))
    scaled_sum_of_squares = residuals_squared.sum()
    return scaled_sum_of_squares


def calc_combined_sum_of_squares(material_variables, model_params, exp_file, model):
    
    yield_stress = material_variables[0]
    K = material_variables[1]
    n = material_variables[2]    
    
    try:
        modelled_disp = run_simulation(material_variables, load)[:,1]
    except:
        modelled_disp = np.ones_like(exp_disp)
        print('Abaqus run failed!')
    experimental_filename = exp_files[i]
    expCsv = np.genfromtxt(experimental_filename, delimiter=",")
    exp_disp = expCsv[:,1]
    
    if len(modelled_disp) != len(exp_disp):
        modelled_disp = np.zeros_like(exp_disp)

        ## I've made the assumption that there are the same number of data points
        # at every load. If not a correction needs to be made here.
    
    sum_of_square = np.sum((exp_disp - modelled_disp) ** 2)
    r_squared = calc_r_squared(exp_disp, modelled_disp)
        
    rhist_file = open('./results/r_sq-history.txt', 'at')
    # save r_squared,  average, log10_C, n, m
    rhist_file.write('{},{},{},{}\n'.format(np.mean(r_squared), *material_variables))
    rhist_file.close()
    
    hist_file = open('./results/history.txt', 'at')
    # save sum of squares, yield stress, K, n
    hist_file.write('{},{},{},{}\n'.format(sum_of_squares, *material_variables))
    hist_file.close()
    
    return sum_of_squares

try:
    os.mkdir('./results/')
except:
    pass
try:
    os.mkdir('./temp/')
except:
    pass



# grab some stuff from the inputs file:
run_simulation = simulate.models[inputs.model)
model_params = inputs.model_params
exp_file = inputs.exp_file
material_variables = inputs.init_material_properties
model = inputs.model




hist_file = open('./results/history.txt', 'wt')
hist_file.write('sum of squares of residuals, yeild_stress, K, n\n')
hist_file.close()

optimisation_result = optimize.fmin(calc_combined_sum_of_squares, material_variables, args=(loads, exp_files, model), xtol=0.005)
optimised_material_properties = optimisation_result.x
best_S = optimisation_result.fun

np.savetxt('./results/optimised_material_properties.csv', np.array([optimised_material_properties]), delimiter=',')






















































