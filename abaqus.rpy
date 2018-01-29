# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.14-1 replay file
# Internal Version: 2014_06_04-23.11.02 134264
# Run by gordon on Mon Jan 29 18:26:29 2018
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.34896, 1.35), width=198.567, 
    height=133.92)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('run_plasticity_ludwig_simulation.py', __main__.__dict__)
#: The model "3000_ID26175_Y300_K300_n0-5" has been created.
#: The interaction property "Steel-Indenter" has been created.
#: The interaction "Steel-Indenter" has been created.
#: The interaction property "Indenter-Specimen Friction" has been created.
#: The interaction "Indenter-Specimen" has been created.
