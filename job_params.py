
import numpy as np
yield_stress=300.0
K=300.0
n=0.5
load=3000
strains = np.linspace(0, 2, num=500)
stresses = yield_stress + K * (strains ** n) 
plasticity_table = np.empty((len(strains), 2))
plasticity_table[:,0] = stresses
plasticity_table[:,1] = strains
job_name="3000_ID26175_Y300_K300_n0-5"
