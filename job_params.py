
import numpy as np
yield_stress=207.56670160430144
K=431.088668050676
n=0.6112649891794524
max_displacement=250.0
coeff_of_friction=0.2
sample_modulus=117
sample_poisson=0.33
indenter_radius=1
strains = np.linspace(0, 2, num=500)
stresses = yield_stress + K * (1 - np.exp(-strains / n)) 
plasticity_table = np.empty((len(strains), 2))
plasticity_table[:,0] = stresses
plasticity_table[:,1] = strains
job_name="250_ID44190_Y207-567_K431-089_n0-611265"
