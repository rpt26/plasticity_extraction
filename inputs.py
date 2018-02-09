### Input file for automated extraction of material properties from indentation data

# define the model: a string linked to a simulation model set up in the simulate module


sample_modulus = 210 # GPa
sample_poisson = 0.3 # unitless
indenter_radius = 1 # mm
exp_filename = 'example.csv' # experiemntal data filename as a string


# define the constitutive law as detailed in docs
model = 'ludwick' 
# first guess at material variables as defined by constitutive law
# e.g. Ludwick-holloman [yield_stress, K, n]
material_variables = [500, 500, 1]

# optional parameters, will take default values if not defineds
coeff_of_friction = 0.2