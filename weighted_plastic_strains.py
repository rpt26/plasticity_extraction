from odbAccess import *
import numpy as np 

def stresses(file_name):
    # Open the ODB and logfile.
    odb = openOdb(path=file_name + ".odb")

    # Find all the frames.
    frame_list = []
    for step_name in odb.steps.keys():
        for frame in odb.steps[step_name].frames:
            frame_list.append(frame)

    number_frame = len(frame_list)
    number_elements = len(odb.rootAssembly.instances['SPECIMEN-1'].elements)
    print(number_elements)
    print(number_frame)
    allstresses = np.zeros((number_elements, number_frame))

    # loop through instances
    for instance_name, instance in odb.rootAssembly.instances.items():
        if instance_name =='SPECIMEN-1':

            # Find all the elements in this instance
            element_db = {}
            for element in instance.elements:
                element_db[element.label] = []

            # loop through each frame.
            for j, frame in enumerate(frame_list):
                # load the fields that we are interested in.
                field = frame.fieldOutputs["S"]

                # Loop through all the instance elements.
                for elementSet_name, elementSet in instance.elementSets.items():
                    subfield = field.getSubset(region=elementSet, position=INTEGRATION_POINT,
                                                                  elementType="CAX3H")
                    
                    stresslist = np.zeros((number_elements, 1))
                    for i, stress in enumerate(subfield.values):
                        # stess.data = [s11, s22, s33, s12]
                        element_db[stress.elementLabel].append(list(stress.data))
                        von_mises = (0.5*((stress.data[0]-stress.data[1])**2 + (stress.data[1]-stress.data[2])**2 + (stress.data[0]-stress.data[2])**2 + 6*(stress.data[3])**2))**0.5
                        stresslist[i] = von_mises
                        allstresses[i,j] = stresslist[i]
                                    
            np.savetxt('./Stresses{:4g}.csv'.format(np.random.randint(99999)), allstresses, delimiter=',')    

            return allstresses
                    
def strains(file_name):
    # Open the ODB and logfile.
    odb = openOdb(path=file_name + ".odb")

    # Find all the frames.
    frame_list = []
    for step_name in odb.steps.keys():
        for frame in odb.steps[step_name].frames:
            frame_list.append(frame)

    number_frame = len(frame_list)
    number_elements = len(odb.rootAssembly.instances['SPECIMEN-1'].elements)
    print(number_elements)
    print(number_frame)
    allstrains = np.zeros((number_elements, number_frame))

    # loop through instances
    for instance_name, instance in odb.rootAssembly.instances.items():
        if instance_name =='SPECIMEN-1':

            # Find all the elements in this instance
            element_db = {}
            for element in instance.elements:
                element_db[element.label] = []

            # loop through each frame.
            for j, frame in enumerate(frame_list):
                # load the fields that we are interested in.
                field = frame.fieldOutputs["PE"]

                # Loop through all the instance elements.
                for elementSet_name, elementSet in instance.elementSets.items():
                    subfield = field.getSubset(region=elementSet, position=INTEGRATION_POINT,
                                                                  elementType="CAX3H")
                    
                    strainlist = np.zeros((number_elements, 1))
                    for i, strain in enumerate(subfield.values):
                        # stess.data = [s11, s22, s33, s12]
                        element_db[strain.elementLabel].append(list(strain.data))
                        eqstrain = (4/3*0.5*((strain.data[0] 
                                                            - (1/3)*(strain.data[0]+strain.data[1]+strain.data[2]))**2 
                                                            + (strain.data[1] 
                                                            - (1/3)*(strain.data[0]+strain.data[1]+strain.data[2]))**2 
                                                            + (strain.data[2] 
                                                            - (1/3)*(strain.data[0]+strain.data[1]+strain.data[2]))**2 
                                                            + 2*(strain.data[3])**2))**0.5
                        strainlist[i] = eqstrain
                        allstrains[i,j] = strainlist[i]
                                    
            np.savetxt('./Strains{:4g}.csv'.format(np.random.randint(99999)), allstrains, delimiter=',')
            
            return allstrains
            
def volume(file_name):
    odbName = 'Weighted_Strain.odb'
    odb = openOdb(odbName)
    lastFrame = odb.steps['Loading Step'].frames[-1]
    volumeField = lastFrame.fieldOutputs['EVOL']
    specimen = odb.rootAssembly.instances['SPECIMEN-1'].elementSets['Specimen Set']
    volumeSet = volumeField.getSubset(region=specimen, elementType='CAX3H')
    volumeFieldValues = volumeSet.values

    number_elements = len(odb.rootAssembly.instances['SPECIMEN-1'].elements)

    volume = np.zeros((number_elements))

    for i, vol in enumerate(volumeFieldValues):
        volume[i] = vol.data
    
    np.savetxt('./volume{:4g}.csv'.format(np.random.randint(99999)), volume, delimiter=',')
    
    return volume

def displacement_data(file_name):
    stepName = 'Loading Step'
    historyRegionName = 'Node Load Application-1.1'
    historyOutputName = 'U2'
    
    # open odb file
    odb = openOdb(path = file_name + '.odb')

    #
    # assign step object
    # print odb.steps.keys()
    step = odb.steps[stepName]
    #
    # assign historyRegion object
    # print step.historyRegions.keys()
    historyRegion = step.historyRegions[historyRegionName]
    #
    # assign historyOutput object
    # print historyRegion.historyOutputs.keys()
    data = np.array(historyRegion.historyOutputs[historyOutputName].data)
    
    data[:,1] = (data[0,1] - data[:,1]) * 1000

    return data

file_name = "Weighted_Strain1"
allstresses = stresses(file_name)
allstrains = strains(file_name)
volume = volume(file_name)
deltastrains = np.zeros_like(allstrains)

odb = openOdb(path=file_name + ".odb")

frame_list = []
for step_name in odb.steps.keys():
    for frame in odb.steps[step_name].frames:
        frame_list.append(frame)

number_frame = len(frame_list)
number_elements = len(odb.rootAssembly.instances['SPECIMEN-1'].elements)

for i in range(0,number_elements):
    for j in range(0,number_frame): 
      if j > 0 :
          deltastrains[i,j] = allstrains[i,j]-allstrains[i, j-1]
      else:
          deltastrains[i,j] = allstrains[i,j]
          
np.savetxt('./deltaStrains{:4g}.csv'.format(np.random.randint(99999)), deltastrains, delimiter=',')

wtotal = np.multiply(deltastrains, allstresses)

for i in range(0,number_elements):
    for j in range(0,number_frame): 
        wtotal[i,j] = wtotal[i,j]*volume[i]

np.savetxt('./strainsstressesvolume{:4g}.csv'.format(np.random.randint(99999)), wtotal, delimiter=',')

#wvalues = np.zeros((number_frame))
#for i in range (0,number_frame):
  #wvalues[i] = sum(wtotal[0:i])
wvalues = np.sum(wtotal, axis =0)  

wcumulative = np.zeros((number_frame))
wcumulative = np.cumsum(wvalues)  

strainframe = np.zeros((number_elements,number_frame))
for i in range(0,number_elements):
    for j in range(0,number_frame): 
      if j > 0:
        strainframe[i,j] = (allstrains[i,j]*wtotal[i,j]/wvalues[j])
      else:
        strainframe[i,j] = 0

np.savetxt('./strainframe{:4g}.csv'.format(np.random.randint(99999)), strainframe, delimiter=',')

totalstrainframe = 100*np.sum(strainframe, axis =0)  

totalstraintimeswork = np.zeros((number_frame))
for i in range (0,number_frame):
  totalstraintimeswork[i] = (totalstrainframe[i]*wvalues[i])
   
cumulativestraintimeswork = np.cumsum(totalstraintimeswork)

weightedstrain = np.zeros((number_frame))
for i in range(0,number_frame):
  if i > 0:
   weightedstrain[i] = cumulativestraintimeswork[i]/wcumulative[i]
  else:
   weightedstrain[i] = 0
   
# This assumes that the history output and field outputs have the same number of data points
displacement = displacement_data(file_name)
displacement_strain = np.column_stack((displacement.T[1], weightedstrain))
np.savetxt('./displacement_strain{:4g}.csv'.format(np.random.randint(99999)), displacement_strain, delimiter=',')

# Maximum plastic strains
maximum_strain = np.amax(allstrains, axis=0) 
displacement_maxstrain = np.column_stack((displacement.T[1], maximum_strain.T))
np.savetxt('./displacement_maxstrain{:4g}.csv'.format(np.random.randint(99999)), displacement_maxstrain, delimiter=',')
