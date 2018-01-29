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

def calc_r_squared(exp, model):
    '''Return the coefficient of determination to characterise
    the likelihood that a model is adequately explaining some data'''
    exp_average = np.mean(exp)
    top = np.sum((exp - model)**2)
    bottom = np.sum((exp-exp_average)**2)
    r_squared = 1 - top / bottom
    
    return r_squared

def calc_sum_of_squares(material_variables, model_params, exp_file, model):
    '''Use FEM to generate a data saet from some material properties 
       to be compared with experiment. Calculate the sum of the square 
       of the residuals, i.e. a quantity to be minimised to increase 
       the agreement between model and experiment.'''
    experimental_filename = exp_file
    expCsv = np.genfromtxt(experimental_filename, delimiter=",")
    exp_disp = expCsv[:,1]

    try:
        modelled_disp = run_simulation(material_variables, model_params)[:,1]
    except:
        modelled_disp = np.ones_like(exp_disp)
        print('Abaqus run failed! Attempting to continue...')

    
    if len(modelled_disp) != len(exp_disp):
        modelled_disp = np.zeros_like(exp_disp)

        ## I've made the assumption that there are the same number of data points
        # at every load. If not a correction needs to be made here.
    
    sum_of_squares = np.sum((exp_disp - modelled_disp) ** 2)
    r_squared = calc_r_squared(exp_disp, modelled_disp)
        
    rhist_file = open('./results/r_sq-history.txt', 'at')
    # save r_squared,  material properties (currently 3 for all the laws used
    rhist_file.write('{},{},{},{}\n'.format(np.mean(r_squared), *material_variables))
    rhist_file.close()
    
    hist_file = open('./results/history.txt', 'at')
    # save sum of squares, and material properties
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
run_simulation = simulate.models[inputs.model]
model_params = inputs.model_params
exp_file = inputs.exp_file
material_variables = inputs.init_material_properties
model = inputs.model




hist_file = open('./results/history.txt', 'wt')
hist_file.write('sum of squares of residuals, yeild_stress, K, n\n')
hist_file.close()

optimisation_result = optimize.fmin(calc_sum_of_squares, material_variables, args=(model_params, exp_file, model), xtol=0.005)
optimised_material_properties = optimisation_result.x
best_S = optimisation_result.fun

np.savetxt('./results/optimised_material_properties.csv', np.array([optimised_material_properties]), delimiter=',')






















































