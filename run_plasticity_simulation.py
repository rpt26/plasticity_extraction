# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

import odbAccess
import numpy as np
import os
import math

import job_params

# material variables will be the quantities to be fitted wrt experimental data
# parameters will be fixed quantitities like load

try:
	os.mkdir('./temp/')
except:
	pass

os.chdir('./temp/')

plasticity_table = job_params.plasticity_table
load = job_params.load
job_name = job_params.job_name

model = mdb.Model(name=job_name)


mdb.models[job_name].ConstrainedSketch(name='__profile__', sheetSize=2.0)
mdb.models[job_name].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[job_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -1.0), point2=(0.0, 1.0))
mdb.models[job_name].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].ArcByCenterEnds(center=(0.0, 0.0)
    , direction=CLOCKWISE, point1=(1.0, 0.0), point2=(0.0, -1.0))
mdb.models[job_name].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].vertices[2], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].vertices[1], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].Line(point1=(0.0, -1.0), point2=(
    0.0, 0.0))
mdb.models[job_name].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[3], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    1.0, 0.0))
mdb.models[job_name].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[job_name].sketches['__profile__'].geometry[5])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[4], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[5])
mdb.models[job_name].Part(dimensionality=AXISYMMETRIC, name='Elastic Indenter'
    , type=DEFORMABLE_BODY)
mdb.models[job_name].parts['Elastic Indenter'].BaseShell(sketch=
    mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(name='__profile__', sheetSize=2.0)
mdb.models[job_name].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[job_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -1.0), point2=(0.0, 1.0))
mdb.models[job_name].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    1.0, 0.0))
mdb.models[job_name].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[job_name].sketches['__profile__'].geometry[3])
mdb.models[job_name].Part(dimensionality=AXISYMMETRIC, name=
    'Rigid Loading Part', type=ANALYTIC_RIGID_SURFACE)
mdb.models[job_name].parts['Rigid Loading Part'].AnalyticRigidSurf2DPlanar(
    sketch=mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].parts['Rigid Loading Part'].ReferencePoint(point=
    mdb.models[job_name].parts['Rigid Loading Part'].vertices[0])
mdb.models[job_name].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[job_name].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[job_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -5.0), point2=(0.0, 5.0))
mdb.models[job_name].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].rectangle(point1=(0.0, -1.0), 
    point2=(10.0, -11.0))
mdb.models[job_name].Part(dimensionality=AXISYMMETRIC, name='Specimen', type=
    DEFORMABLE_BODY)
mdb.models[job_name].parts['Specimen'].BaseShell(sketch=
    mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(gridSpacing=0.74, name='__profile__', 
    sheetSize=29.73, transform=
    mdb.models[job_name].parts['Specimen'].MakeSketchTransform(
    sketchPlane=mdb.models[job_name].parts['Specimen'].faces[0], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(5.0, -6.0, 0.0)))
mdb.models[job_name].parts['Specimen'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models[job_name].sketches['__profile__'])
mdb.models[job_name].sketches['__profile__'].rectangle(point1=(-5.0, 5.0), 
    point2=(-3.0, 3.0))
mdb.models[job_name].parts['Specimen'].PartitionFaceBySketch(faces=
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#1 ]', 
    ), ), sketch=mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].Material(name='Tungsten Carbide')
mdb.models[job_name].materials['Tungsten Carbide'].Elastic(table=((650000.0, 
    0.21), ))
mdb.models[job_name].Material(name='Specimen')
mdb.models[job_name].materials['Specimen'].Elastic(table=((117000.0, 0.33), ))
mdb.models[job_name].materials['Specimen'].Plastic(table=(plasticity_table))
mdb.models[job_name].HomogeneousSolidSection(material='Tungsten Carbide', 
    name='Tunsgten Carbide', thickness=None)
mdb.models[job_name].HomogeneousSolidSection(material='Specimen', name=
    'Specimen', thickness=None)
mdb.models[job_name].parts['Specimen'].Set(faces=
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#3 ]', 
    ), ), name='Set-1')
mdb.models[job_name].parts['Specimen'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models[job_name].parts['Specimen'].sets['Set-1'], sectionName=
    'Specimen', thicknessAssignment=FROM_SECTION)
mdb.models[job_name].parts['Elastic Indenter'].Set(faces=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#1 ]', ), ), name='Indenter Set')
mdb.models[job_name].parts['Elastic Indenter'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models[job_name].parts['Elastic Indenter'].sets['Indenter Set'], 
    sectionName='Tunsgten Carbide', thicknessAssignment=FROM_SECTION)
mdb.models[job_name].rootAssembly.DatumCsysByThreePoints(coordSysType=
    CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 
    0.0, -1.0))
mdb.models[job_name].rootAssembly.Instance(dependent=ON, name=
    'Elastic Indenter-1', part=mdb.models[job_name].parts['Elastic Indenter'])
mdb.models[job_name].rootAssembly.Instance(dependent=ON, name=
    'Rigid Loading Part-1', part=
    mdb.models[job_name].parts['Rigid Loading Part'])
mdb.models[job_name].rootAssembly.Instance(dependent=ON, name='Specimen-1', 
    part=mdb.models[job_name].parts['Specimen'])
mdb.models[job_name].StaticStep(initialInc=0.001, matrixSolver=DIRECT, 
    matrixStorage=UNSYMMETRIC, maxNumInc=1000, minInc=1e-08, name=
    'Loading Step', nlgeom=ON, previous='Initial')
del mdb.models[job_name].fieldOutputRequests['F-Output-1']
mdb.models[job_name].parts['Rigid Loading Part'].Set(name=
    'Reference Point Set', referencePoints=(
    mdb.models[job_name].parts['Rigid Loading Part'].referencePoints[2], ))
mdb.models[job_name].rootAssembly.regenerate()
del mdb.models[job_name].historyOutputRequests['H-Output-1']
mdb.models[job_name].HistoryOutputRequest(createStepName='Loading Step', name=
    'Indenter Load', rebar=EXCLUDE, region=
    mdb.models[job_name].rootAssembly.allInstances['Rigid Loading Part-1'].sets['Reference Point Set']
    , sectionPoints=DEFAULT, timeInterval=0.01, variables=('U2', 'RF2'))
mdb.models[job_name].FieldOutputRequest(createStepName='Loading Step', name=
    'F-Output-1', timeInterval=0.2, variables=('MISES', 'PEEQ', 'U'))
mdb.models[job_name].ContactProperty('Friction Coefficient')
mdb.models[job_name].interactionProperties['Friction Coefficient'].TangentialBehavior(
    dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
    formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
    pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
    table=((0.2, ), ), temperatureDependency=OFF)
mdb.models[job_name].rootAssembly.Surface(name='Indenter Master Surface', 
    side1Edges=
    mdb.models[job_name].rootAssembly.instances['Elastic Indenter-1'].edges.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models[job_name].rootAssembly.Surface(name='s_Surf-1', side1Edges=
    mdb.models[job_name].rootAssembly.instances['Specimen-1'].edges.getSequenceFromMask(
    ('[#60 ]', ), ))
mdb.models[job_name].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    clearanceRegion=None, createStepName='Loading Step', datumAxis=None, 
    initialClearance=OMIT, interactionProperty='Friction Coefficient', master=
    mdb.models[job_name].rootAssembly.surfaces['Indenter Master Surface'], 
    name='Indenter-Specimen', slave=
    mdb.models[job_name].rootAssembly.surfaces['s_Surf-1'], sliding=FINITE, 
    thickness=ON)
mdb.models[job_name].interactions['Indenter-Specimen'].move('Loading Step', 
    'Initial')
mdb.models[job_name].rootAssembly.Surface(name='m_Surf-3', side2Edges=
    mdb.models[job_name].rootAssembly.instances['Rigid Loading Part-1'].edges.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models[job_name].rootAssembly.Surface(name='s_Surf-3', side1Edges=
    mdb.models[job_name].rootAssembly.instances['Elastic Indenter-1'].edges.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models[job_name].Tie(adjust=ON, master=
    mdb.models[job_name].rootAssembly.surfaces['m_Surf-3'], name=
    'Constraint-1', positionToleranceMethod=COMPUTED, slave=
    mdb.models[job_name].rootAssembly.surfaces['s_Surf-3'], thickness=ON, 
    tieRotations=ON)
mdb.models[job_name].rootAssembly.Set(edges=
    mdb.models[job_name].rootAssembly.instances['Specimen-1'].edges.getSequenceFromMask(
    ('[#8 ]', ), ), name='Set-1')
mdb.models[job_name].EncastreBC(createStepName='Loading Step', localCsys=None, 
    name='Fixed Bottom Surface', region=
    mdb.models[job_name].rootAssembly.sets['Set-1'])
mdb.models[job_name].boundaryConditions['Fixed Bottom Surface'].move(
    'Loading Step', 'Initial')
mdb.models[job_name].rootAssembly.Set(edges=
    mdb.models[job_name].rootAssembly.instances['Specimen-1'].edges.getSequenceFromMask(
    ('[#84 ]', ), ), name='Indenter Centre Line')
mdb.models[job_name].XsymmBC(createStepName='Loading Step', localCsys=None, 
    name='Symmetry Condition', region=
    mdb.models[job_name].rootAssembly.sets['Indenter Centre Line'])
mdb.models[job_name].boundaryConditions['Symmetry Condition'].move(
    'Loading Step', 'Initial')
mdb.models[job_name].rootAssembly.Set(edges=
    mdb.models[job_name].rootAssembly.instances['Elastic Indenter-1'].edges.getSequenceFromMask(
    ('[#1 ]', ), ), name='Set-3')
mdb.models[job_name].DisplacementBC(amplitude=UNSET, createStepName=
    'Loading Step', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    localCsys=None, name='Fixed Indenter Displacement', region=
    mdb.models[job_name].rootAssembly.sets['Set-3'], u1=0.0, u2=UNSET, ur3=
    UNSET)
mdb.models[job_name].boundaryConditions['Fixed Indenter Displacement'].move(
    'Loading Step', 'Initial')
mdb.models[job_name].rootAssembly.Set(edges=
    mdb.models[job_name].rootAssembly.instances['Elastic Indenter-1'].edges.getSequenceFromMask(
    ('[#1 ]', ), ), name='Set-4')
mdb.models[job_name].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'Displacement Condition', region=
    mdb.models[job_name].rootAssembly.sets['Set-4'], u1=UNSET, u2=SET, ur3=
    UNSET)
mdb.models[job_name].TabularAmplitude(data=((0.0, 0.0), (1.0, -1*load/1000)), name=
    'Displacement History', smooth=SOLVER_DEFAULT, timeSpan=STEP)
mdb.models[job_name].boundaryConditions['Displacement Condition'].setValuesInStep(
    amplitude='Displacement History', stepName='Loading Step', u2=1.0)
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#42 ]', ), ), number=180, ratio=1.0)
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#81 ]', ), ), number=90, ratio=1.0)
mdb.models[job_name].parts['Specimen'].setMeshControls(elemShape=TRI, regions=
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#1 ]', 
    ), ))
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask(('[#4 ]', 
    ), ), number=30, ratio=3.0)
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#20 ]', ), ), number=30, ratio=3.0)
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#18 ]', ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#18 ]', ), ), number=20, ratio=1.0)
mdb.models[job_name].parts['Specimen'].setElementType(elemTypes=(ElemType(
    elemCode=CAX4RH, elemLibrary=STANDARD, hourglassControl=DEFAULT), ElemType(
    elemCode=CAX3, elemLibrary=STANDARD)), regions=(
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#2 ]', 
    ), ), ))
mdb.models[job_name].parts['Specimen'].setElementType(elemTypes=(ElemType(
    elemCode=CAX4R, elemLibrary=STANDARD), ElemType(elemCode=CAX3H, 
    elemLibrary=STANDARD)), regions=(
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#1 ]', 
    ), ), ))
mdb.models[job_name].rootAssembly.regenerate()
mdb.models[job_name].parts['Specimen'].generateMesh()
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#4 ]', ), ), number=50, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#4 ]', ), ), number=50, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#2 ]', ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#2 ]', ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#1 ]', ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#1 ]', ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].setMeshControls(elemShape=TRI, 
    regions=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#1 ]', ), ))
mdb.models[job_name].parts['Elastic Indenter'].setElementType(elemTypes=(
    ElemType(elemCode=CAX4R, elemLibrary=STANDARD), ElemType(elemCode=CAX3H, 
    elemLibrary=STANDARD)), regions=(
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#1 ]', ), ), ))
mdb.models[job_name].parts['Elastic Indenter'].generateMesh()
mdb.models[job_name].rootAssembly.regenerate()
mdb.models[job_name].parts['Elastic Indenter'].deleteMesh(regions=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#1 ]', ), ))
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#4 ]', ), ), number=75, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].generateMesh()
mdb.models[job_name].rootAssembly.regenerate()
mdb.models[job_name].parts['Elastic Indenter'].deleteMesh(regions=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#1 ]', ), ))
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#2 ]', ), ), number=40, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].generateMesh()
mdb.models[job_name].rootAssembly.regenerate()
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model=job_name, modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=job_name, nodalOutputPrecision=SINGLE, 
    numCpus=8, numDomains=8, numGPUs=0, queue=None, resultsFormat=ODB, scratch=
    '', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs[job_name].submit(consistencyChecking=OFF)
mdb.jobs[job_name].waitForCompletion()

os.chdir('./../')
