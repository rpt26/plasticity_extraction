from __future__ import division, print_function, with_statement
import subprocess
import numpy as np
from scipy import optimize
import os
import glob
import math
import time

def simulate_plasticity_ludwig(material_properties, model_params):
    load = model_params[0]

    if len(material_properties) != 3:
        print('Wrong number of material properties provided!')
    if len(model_params) != 1:
        print('Wrong number of model parameters rpovided!')

    yield_stress = material_properties[0]
    K = material_properties[1]
    n = material_properties[2]

    job_name = '{:3g}_ID{:g}_Y{:4g}_K{:4g}_n{:4g}'.format(load, np.random.randint(99999), yield_stress, K, n)
    job_name = job_name.replace('.', '-')
    job_name = job_name.replace(' ', '')


    parameter_file_text = ('\n' +
                           'import numpy as np\n' +
                           'yield_stress={}\n'.format(yield_stress) +
                           'K={}\n'.format(K) +
                           'n={}\n'.format(n) +
                           'load={}\n'.format(load) +
                           'strains = np.linspace(0, 2, num=500)\n' +
                           'stresses = yield_stress + K * (strains ** n) \n' +
                           'plasticity_table = np.empty((len(strains), 2))\n' +
                           'plasticity_table[:,0] = stresses\n' +
                           'plasticity_table[:,1] = strains\n' +
                           'job_name="' + job_name + '"\n')


    with open('job_params.py', 'wt') as file:
        file.write(parameter_file_text)

    experimental_filename = str(int(load)) + '.csv'
    expCsv = np.genfromtxt(experimental_filename, delimiter=",")

    if yield_stress < 0:
        data = np.ones_like(expCsv)*yield_stress
    if K < 0:
        data = np.ones_like(expCsv)*K
    if n < 0:
        data = np.ones_like(expCsv)*n
    if n > 1:
        data = np.ones_like(expCsv)*1000*n

    try:
        data
    except NameError:
	    subprocess.run(['abaqus', 'cae', 'noGUI=run_plasticity_ludwig_simulation.py'], shell=True)
	    # wait for data to be written (seemed to not be finding the file so trying this)
	    time.sleep(1) 
	    subprocess.run(['abaqus', 'python', 'extract_data.py'], shell=True)
	    print('waiting')
	    time.sleep(1)
	    data = np.genfromtxt('./results/' + job_name + '.csv', delimiter=',')

    return data


def simulate_plasticity_voce(material_properties, model_params):
    load = model_params[0]

    if len(material_params) != 3:
        print('Wrong number of material properties provided!')
    if len(model_params) != 1:
        print('Wrong number of model parameters rpovided!')

    yield_stress = material_properties[0]
    saturation_stress = material_properties[1]
    characteristic_strain = material_properties[2]

    job_name = '{:3g}_ID{:g}_Y{:4g}_K{:4g}_n{:4g}'.format(load, np.random.randint(99999), yield_stress, K, n)
    job_name = job_name.replace('.', '-')
    job_name = job_name.replace(' ', '')


    parameter_file_text = ('\n' +
                           'import numpy as np\n' +
                           'yield_stress={}\n'.format(yield_stress) +
                           'saturation_stress={}\n'.format(saturation_stress) +
                           'characeristic_strain={}\n'.format(characteristic_strain) +
                           'load={}\n'.format(load) +
                           'coeff_of_friction={}'.format(coeff_of_friction) +
                           'strains = np.linspace(0, 2, num=500)\n' +
                           'stresses = saturation_stress - (saturation_stress - yield_stress) * np.exp(-strains / characteristic_strain) \n' +
                           'plasticity_table = np.empty((len(strains), 2))\n' +
                           'plasticity_table[:,0] = stresses\n' +
                           'plasticity_table[:,1] = strains\n' +
                           'job_name="' + job_name + '"\n')


    with open('job_params.py', 'wt') as file:
        file.write(parameter_file_text)

    experimental_filename = str(int(load)) + '.csv'
    expCsv = np.genfromtxt(experimental_filename, delimiter=",")

    if yield_stress < 0:
        data = np.ones_like(expCsv)*yield_stress
    if K < 0:
        data = np.ones_like(expCsv)*K
    if n < 0:
        data = np.ones_like(expCsv)*n
    if n > 1:
        data = np.ones_like(expCsv)*1000*n

    try:
        data
    except NameError:
	    subprocess.run(['abaqus', 'cae', 'noGUI=run_plasticity_ludwig_simulation.py'], shell=True)
	    # wait for data to be written (seemed to not be finding the file so trying this)
	    time.sleep(1) 
	    subprocess.run(['abaqus', 'python', 'extract_data.py'], shell=True)
	    print('waiting')
	    time.sleep(1)
	    data = np.genfromtxt('./results/' + job_name + '.csv', delimiter=',')

    return data

models = dict(ludwig=simulate_plasticity_ludwig,
              voce=simulate_plasticity_voce)





































