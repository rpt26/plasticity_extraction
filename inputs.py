### Input file for automated extraction of material properties from indentation data

# define the model: a string linked to a simulation model set up in the simulate module


sample_modulus = 117 # GPa
sample_poisson = 0.33 # unitless
indenter_radius = 1 # mm
exp_filename = 'AnnealedCopper.csv' # experiemntal data filename as a string


# define the constitutive law as detailed in docs
<<<<<<< HEAD
model = 'voce' 
# first guess at material variables as defined by constitutive law
# e.g. Ludwick-holloman [yield_stress, K, n]
material_variables = [47, 455.6, 0.534]
=======
model = 'Voce' 
# first guess at material variables as defined by constitutive law
# e.g. Ludwick-holloman [yield_stress, K, n]
material_variables = [400, 400, 0.5]
>>>>>>> origin/master

# optional parameters, will take default values if not defineds
coeff_of_friction = 0.2

# Mesh parameters
seeds = 80

# Number of cores for simulations, default num_cores = 1
num_cores = 1
