
import numpy as np
yield_stress=350
saturation_stress=400
characteristic_strain=0.5
max_displacement=250.0
coeff_of_friction=0.2
sample_modulus=117
sample_poisson=0.33
indenter_radius=1
strains = np.linspace(0, 2, num=500)
stresses = yield_stress + (saturation_stress)*(1-np.exp(-strains / characteristic_strain)) 
plasticity_table = np.empty((len(strains), 2))
plasticity_table[:,0] = stresses
plasticity_table[:,1] = strains
job_name="250_ID23199_Y350_K400_n0-5"
