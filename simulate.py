from __future__ import division, print_function, with_statement
import subprocess
import numpy as np
from scipy import optimize
import os
import glob
import math
import time
import inputs

exp_filename = inputs.exp_filename
raw_load_disp_data = np.genfromtxt(exp_filename, delimiter=',')
load = raw_load_disp_data[:,0]
displacement = raw_load_disp_data[:,1]
max_displacement = np.amax(displacement)

if inputs.coeff_of_friction:
    coeff_of_friction = inputs.coeff_of_friction
else:
    coeff_of_friction = 0.2

    
def simulate_plasticity_ludwick(material_variables):
    yield_stress = material_variables[0]
    K = material_variables[1]
    n = material_variables[2]
    
    job_name = '{:3g}_ID{:g}_Y{:4g}_K{:4g}_n{:4g}'.format(max_displacement, np.random.randint(99999), yield_stress, K, n)
    job_name = job_name.replace('.', '-')
    job_name = job_name.replace(' ', '')


    parameter_file_text = ('\n' +
                           'import numpy as np\n' +
                           'yield_stress={}\n'.format(yield_stress) +
                           'K={}\n'.format(K) +
                           'n={}\n'.format(n) +
                           'max_displacement={}\n'.format(max_displacement) +
                           'coeff_of_friction={}\n'.format(coeff_of_friction) +
                           'sample_modulus={}\n'.format(inputs.sample_modulus) +
                           'sample_poisson={}\n'.format(inputs.sample_poisson) +
                           'indenter_radius={}\n'.format(inputs.indenter_radius) +
                           'strains = np.linspace(0, 2, num=500)\n' +
                           'stresses = yield_stress + K * (strains ** n) \n' +
                           'plasticity_table = np.empty((len(strains), 2))\n' +
                           'plasticity_table[:,0] = stresses\n' +
                           'plasticity_table[:,1] = strains\n' +
                           'job_name="' + job_name + '"\n')


    with open('job_params.py', 'wt') as file:
        file.write(parameter_file_text)

    expCsv = np.genfromtxt(inputs.exp_filename, delimiter=",")


    subprocess.run(['abaqus', 'cae', 'noGUI=run_plasticity_simulation.py'], shell=True)
    # wait for data to be written (seemed to not be finding the file so trying this)
    time.sleep(1) 
    subprocess.run(['abaqus', 'python', 'extract_data.py'], shell=True)
    print('waiting')
    time.sleep(1)
    data = np.genfromtxt('./results/' + job_name + '.csv', delimiter=',')

    return data


def simulate_plasticity_voce(material_variables):

    yield_stress = inputs.material_variables[0]
    saturation_stress = inputs.material_variables[1]
    characteristic_strain = inputs.material_variables[2]
    
    
    job_name = '{:3g}_ID{:g}_Y{:4g}_K{:4g}_n{:4g}'.format(max_displacement, np.random.randint(99999), yield_stress, K, n)
    job_name = job_name.replace('.', '-')
    job_name = job_name.replace(' ', '')


    parameter_file_text = ('\n' +
                           'import numpy as np\n' +
                           'yield_stress={}\n'.format(yield_stress) +
                           'saturation_stress={}\n'.format(saturation_stress) +
                           'characeristic_strain={}\n'.format(characteristic_strain) +
                           'max_displacement={}\n'.format(max_displacement) +
                           'coeff_of_friction={}\n'.format(coeff_of_friction) +
                           'sample_modulus={}\n'.format(inputs.sample_modulus) +
                           'sample_poisson={}\n'.format(inputs.sample_poisson) +
                           'indenter_radius={}\n'.format(inputs.indenter_radius) +
                           'strains = np.linspace(0, 2, num=500)\n' +
                           'stresses = saturation_stress - (saturation_stress - yield_stress) * np.exp(-strains / characteristic_strain) \n' +
                           'plasticity_table = np.empty((len(strains), 2))\n' +
                           'plasticity_table[:,0] = stresses\n' +
                           'plasticity_table[:,1] = strains\n' +
                           'job_name="' + job_name + '"\n')


    with open('job_params.py', 'wt') as file:
        file.write(parameter_file_text)

    expCsv = np.genfromtxt(experimental_filename, delimiter=",")


    subprocess.run(['abaqus', 'cae', 'noGUI=run_plasticity_simulation.py'], shell=True)
    # wait for data to be written (seemed to not be finding the file so trying this) 
    subprocess.run(['abaqus', 'python', 'extract_data.py'], shell=True)
    print('waiting')
    data = np.genfromtxt('./results/' + job_name + '.csv', delimiter=',')

    return data

models = dict(ludwick=simulate_plasticity_ludwick,
              voce=simulate_plasticity_voce,
              Ludwick=simulate_plasticity_ludwick,
              Voce=simulate_plasticity_voce)





































