
import numpy as np
yield_stress=332.5
K=413.33333333333337
n=0.5166666666666666
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
job_name="250_ID78313_Y332-5_K413-333_n0-516667"
