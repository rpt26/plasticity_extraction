### Input file for automated extraction of material properties from indentation data

# define the model: a string linked to a simulation model set up in the simulate module

model = 'ludwig' 
model_params = [3000]  # e.g. max load for plasticity model
exp_file = '3000.csv' # experiemntal data file as a string
init_material_properties = [300, 300, 0.5] # these have to match the model being used
