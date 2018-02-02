import odbAccess
import numpy as np
import job_params

def extract_odb(path_to_odb):
    stepName = 'Loading Step'
    historyRegionName = 'Node Rigid Loading Part-1.1'
    historyOutputName = 'RF2'
    
    # open odb file
    ODBFile = odbAccess.openOdb(path = path_to_odb)

    #
    # assign step object
    # print ODBFile.steps.keys()
    step = ODBFile.steps[stepName]
    #
    # assign historyRegion object
    # print step.historyRegions.keys()
    historyRegion = step.historyRegions[historyRegionName]
    #
    # assign historyOutput object
    # print historyRegion.historyOutputs.keys()
    data = np.array(historyRegion.historyOutputs[historyOutputName].data)
    
    data[:,1] = (data[0,1] - data[:,1]) * 1

    return data

data = extract_odb('./temp/'+job_params.job_name+'.odb')
np.savetxt('./results/' + job_params.job_name + '.csv', data, delimiter=',')