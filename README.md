# Abaqus

## R.P.Thompson and J. Campbell
## University of Camridge
### 2017
Extracting material properties from indentation data by fitting an FEM model using the abaqus package.

The script is designed to be simple to use. The script requires a system with abaqus installed and expects to find in its working directory:
* csv files containing experimental time-displacement data (as columns in that order) with filenames of the form _load_.csv where _load_ is in newtons.
* a script for fitting the relevant properties, e.g. creep.py. Currently included are a script for plasticity and creep.

The script is then run with the command "`python optimise_<property>.py`" assuming that a suitable python installation and abaqus installation are discoverable from your system's path. The simplest option on a windows machine is to install Anaconda and Abaqus and this should work.

Final material properties are then output in a newly created "results" directory.

Any published results generated with this script should cite this paper: [TO BE PUBLISHED]. The project is licensed under GPLv3, please get in touch if you're interested in an alternative commercial license. 
