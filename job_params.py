
import numpy as np
yield_stress=525.0
K=500.0
n=1.0
max_displacement=250.0
coeff_of_friction=0.2
sample_modulus=117
sample_poisson=0.33
indenter_radius=1
strains = np.linspace(0, 2, num=500)
stresses = yield_stress + K * (strains ** n) 
plasticity_table = np.empty((len(strains), 2))
plasticity_table[:,0] = stresses
plasticity_table[:,1] = strains
job_name="250_ID8075_Y525_K500_n1"
