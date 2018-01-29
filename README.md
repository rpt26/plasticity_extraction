# Plasticity Extraction

## R.P.Thompson and J. Campbell
## University of Camridge
### 2017
Extracting material properties from indentation data by fitting an FEM model using the abaqus package.

The script is designed to be simple to use. The script requires a system with abaqus installed and expects to find in its working directory:
* An input file called `inputs.py`, containing variables and parameters for the model and the filename of the experimental data.
* experimental data in a csv file as referred to in the inputs file.

The script is then run with the command "`python optimise_properties.py`" assuming that a suitable python installation and abaqus installation are discoverable from your system's path. The simplest option on a windows machine is to install Anaconda and Abaqus and this should work out of the box.

An example data file and input file are given for a 3000N load.

Final material properties are then output in a newly created "results" directory, along with a file detailing the history of the search, mostly to allow us to characterise the optimisation alghorithm and the "shape" of parameter space. A load of Abaqus related stuff gets left in the temp directory, but can usually be ignored and deleted.

Any published results generated with this script should cite this paper: [TO BE PUBLISHED]. The project is licensed under the Non-profit Open Software License 3.0, please get in touch if you're interested in an alternative commercial license. 
