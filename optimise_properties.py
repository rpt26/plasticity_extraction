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
from matplotlib import pyplot as plt

def calc_r_squared(exp, model):
    '''Return the coefficient of determination to characterise
    the likelihood that a model is adequately explaining some data'''
    exp_average = np.mean(exp)
    top = np.sum((exp - model)**2)
    bottom = np.sum((exp-exp_average)**2)
    r_squared = 1 - top / bottom
    
    return r_squared

def calc_sum_of_squares(material_variables, exp_disp_load):
    '''Use FEM to generate a data saet from some material properties 
       to be compared with experiment. Calculate the sum of the square 
       of the residuals, i.e. a quantity to be minimised to increase 
       the agreement between model and experiment.'''
    # experimental displacement
    exp_load = exp_disp_load[:,1]
    exp_disp = exp_disp_load[:,0]
    try:
        modelled_load = run_simulation(material_variables)[:,1]
    except:
        modelled_load = np.ones_like(exp_load)
        print('Abaqus run failed! Attempting to continue...')
    
    try:
        plt.clf()
        experimental_plot, = plt.plot(exp_disp, exp_load, 'g-', label='Exp')
        modelled_plot, = plt.plot(exp_disp, modelled_load, 'b.', label='Model')
        plt.legend(handles=[experimental_plot, modelled_plot])
        plt.xlabel('Displacement (Microns)')
        plt.ylabel('Load (N)')
        plt.title('Comparison of the latest modelled and the experimental load-displacement curves')
        plt.savefig('Load-Disp_comparison.pdf')
    except:
        pass
    
    #if len(modelled_load) != len(exp_load):
   #     modelled_load = np.zeros_like(exp_load)

        ## I've made the assumption that there are the same number of data points
        # at every load. If not a correction needs to be made here.
    
    sum_of_squares = np.sum((exp_load - modelled_load) ** 2)
    r_squared = calc_r_squared(exp_load, modelled_load)
        
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

exp_filename = inputs.exp_filename
material_variables = inputs.material_variables
model = inputs.model


raw_load_disp_data = np.genfromtxt(exp_filename, delimiter=',')
load = raw_load_disp_data[:,0]
displacement = raw_load_disp_data[:,1]

max_displacement = np.amax(displacement)
interpolated_disp = np.linspace(0, max_displacement, num=51)
interpolated_load = np.interp(interpolated_disp, displacement, load)
scaled_displacement = interpolated_disp / (inputs.indenter_radius)
scaled_load = interpolated_load / (inputs.indenter_radius**2)



exp_disp_load = np.array((scaled_displacement, scaled_load)).T

hist_file = open('./results/history.txt', 'wt')
hist_file.write('sum of squares of residuals, yeild_stress, K, n\n')
hist_file.close()

algorithm = 'Nelder-Mead'


optimisation_result = optimize.minimize(calc_sum_of_squares, material_variables, args=(exp_disp_load,), tol=0.005, method=algorithm)
optimised_material_properties = optimisation_result.x
best_S = optimisation_result.fun

np.savetxt('./results/optimised_material_properties.csv', np.array([optimised_material_properties]), delimiter=',')






















































