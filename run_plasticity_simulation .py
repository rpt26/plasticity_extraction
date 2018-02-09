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
coeff_of_friction = job_params.coeff_of_friction

sample_modulus = job_params.sample_modulus * 1000 # change from GPa to MPa
sample_poisson = job_params.sample_poisson # unitless



model = mdb.Model(name=job_name)


mdb.models[job_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[job_name].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[job_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -100.0), point2=(0.0, 100.0))
mdb.models[job_name].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(10.0, -10.0))
mdb.models[job_name].Part(dimensionality=AXISYMMETRIC, name='Specimen', type=
    DEFORMABLE_BODY)
mdb.models[job_name].parts['Specimen'].BaseShell(sketch=
    mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(gridSpacing=0.7, name='__profile__', 
    sheetSize=28.28, transform=
    mdb.models[job_name].parts['Specimen'].MakeSketchTransform(
    sketchPlane=mdb.models[job_name].parts['Specimen'].faces[0], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(5.0, -5.0, 0.0)))
mdb.models[job_name].parts['Specimen'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models[job_name].sketches['__profile__'])
mdb.models[job_name].sketches['__profile__'].rectangle(point1=(-5.0, 5.0), 
    point2=(-4.0, 4.0))
mdb.models[job_name].sketches['__profile__'].dragEntity(entity=
    mdb.models[job_name].sketches['__profile__'].vertices[5], points=((-4.0, 
    4.0), (-4.025, 4.025), (-3.85, 3.85), (-3.85, 3.85), (-3.85, 3.675), (
    -3.675, 3.675), (-3.58704471588135, 3.58860778808594), (-3.5, 3.5), (-3.5, 
    3.5), (-3.5, 3.325), (-3.5, 3.15), (-3.5, 3.15), (-3.325, 2.975), (-3.325, 
    2.975), (-3.15, 2.975), (-2.975, 2.975), (-2.975, 2.975)))
mdb.models[job_name].parts['Specimen'].PartitionFaceBySketch(faces=
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#1 ]', 
    ), ), sketch=mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[job_name].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[job_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -100.0), point2=(0.0, 100.0))
mdb.models[job_name].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].ArcByCenterEnds(center=(0.0, 1.0)
    , direction=COUNTERCLOCKWISE, point1=(0.0, 0.0), point2=(0.0, 2.0))
mdb.models[job_name].sketches['__profile__'].Line(point1=(0.0, 2.0), point2=(
    0.0, 0.0))
mdb.models[job_name].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[3], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].Part(dimensionality=AXISYMMETRIC, name='Elastic Indenter'
    , type=DEFORMABLE_BODY)
mdb.models[job_name].parts['Elastic Indenter'].BaseShell(sketch=
    mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(gridSpacing=0.11, name='__profile__', 
    sheetSize=4.46, transform=
    mdb.models[job_name].parts['Elastic Indenter'].MakeSketchTransform(
    sketchPlane=mdb.models[job_name].parts['Elastic Indenter'].faces[0], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.424413, 1.0, 
    0.0)))
mdb.models[job_name].parts['Elastic Indenter'].projectReferencesOntoSketch(
    filter=COPLANAR_EDGES, sketch=
    mdb.models[job_name].sketches['__profile__'])
mdb.models[job_name].sketches['__profile__'].Line(point1=(-0.424413, 
    0.499746680259705), point2=(0.441758608678356, 0.499746680259705))
mdb.models[job_name].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[job_name].sketches['__profile__'].geometry[5])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[2], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[5])
mdb.models[job_name].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].vertices[3], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].vertices[4], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[3])
mdb.models[job_name].parts['Elastic Indenter'].PartitionFaceBySketch(faces=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#1 ]', ), ), sketch=mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(gridSpacing=0.11, name='__profile__', 
    sheetSize=4.47, transform=
    mdb.models[job_name].parts['Elastic Indenter'].MakeSketchTransform(
    sketchPlane=mdb.models[job_name].parts['Elastic Indenter'].faces[0], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.445122, 0.828557, 
    0.0)))
mdb.models[job_name].parts['Elastic Indenter'].projectReferencesOntoSketch(
    filter=COPLANAR_EDGES, sketch=
    mdb.models[job_name].sketches['__profile__'])
mdb.models[job_name].sketches['__profile__'].Line(point1=(-0.445122, 
    -0.333830401737213), point2=(0.417837320826948, -0.333830401737213))
mdb.models[job_name].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[job_name].sketches['__profile__'].geometry[9])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[3], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[9])
mdb.models[job_name].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].vertices[5], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[3])
mdb.models[job_name].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].vertices[6], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].parts['Elastic Indenter'].PartitionFaceBySketch(faces=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#1 ]', ), ), sketch=mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[job_name].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[job_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -100.0), point2=(0.0, 100.0))
mdb.models[job_name].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].ArcByCenterEnds(center=(0.0, 0.0)
    , direction=CLOCKWISE, point1=(0.0, 1.0), point2=(1.0, 0.0))
mdb.models[job_name].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].vertices[2], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].Line(point1=(0.0, 1.0), point2=(
    0.0, 10.0))
mdb.models[job_name].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[3], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].sketches['__profile__'].Line(point1=(0.0, 10.0), point2=(
    10.0, 10.0))
mdb.models[job_name].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[job_name].sketches['__profile__'].geometry[5])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[4], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[5])
mdb.models[job_name].sketches['__profile__'].Line(point1=(10.0, 10.0), point2=
    (10.0, 0.0))
mdb.models[job_name].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[job_name].sketches['__profile__'].geometry[6])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[5], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[6])
mdb.models[job_name].sketches['__profile__'].Line(point1=(10.0, 0.0), point2=(
    1.0, 0.0))
mdb.models[job_name].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[job_name].sketches['__profile__'].geometry[7])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[6], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[7])
mdb.models[job_name].Part(dimensionality=AXISYMMETRIC, name='Steel', type=
    DEFORMABLE_BODY)
mdb.models[job_name].parts['Steel'].BaseShell(sketch=
    mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[job_name].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[job_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -100.0), point2=(0.0, 100.0))
mdb.models[job_name].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[job_name].sketches['__profile__'].geometry[2])
mdb.models[job_name].sketches['__profile__'].Line(point1=(0.0, 10.0), point2=(
    15.0, 10.0))
mdb.models[job_name].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[job_name].sketches['__profile__'].geometry[3])
mdb.models[job_name].sketches['__profile__'].Line(point1=(15.0, 10.0), point2=
    (15.0, 15.0))
mdb.models[job_name].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[job_name].sketches['__profile__'].geometry[3], entity2=
    mdb.models[job_name].sketches['__profile__'].geometry[4])
mdb.models[job_name].Part(dimensionality=AXISYMMETRIC, name=
    'Load Application Part', type=ANALYTIC_RIGID_SURFACE)
mdb.models[job_name].parts['Load Application Part'].AnalyticRigidSurf2DPlanar(
    sketch=mdb.models[job_name].sketches['__profile__'])
del mdb.models[job_name].sketches['__profile__']
mdb.models[job_name].parts['Load Application Part'].ReferencePoint(point=(0.0, 
    15.0, 0.0))
	
# Material Properties

mdb.models[job_name].Material(name='Specimen')
mdb.models[job_name].materials['Specimen'].Elastic(table=((117000.0, 0.33), ))
mdb.models[job_name].materials['Specimen'].Plastic(table=(plasticity_table))
mdb.models[job_name].Material(name='Tungsten Carbide')
mdb.models[job_name].materials['Tungsten Carbide'].Elastic(table=((650000.0, 
    0.21), ))
mdb.models[job_name].Material(name='Stainless Steel')
mdb.models[job_name].materials['Stainless Steel'].Elastic(table=((195000.0, 
    0.27), ))
mdb.models[job_name].HomogeneousSolidSection(material='Specimen', name=
    'Specimen', thickness=None)
mdb.models[job_name].HomogeneousSolidSection(material='Tungsten Carbide', 
    name='Tungsten Carbide', thickness=None)
mdb.models[job_name].HomogeneousSolidSection(material='Stainless Steel', name=
    'Stainless Steel', thickness=None)
mdb.models[job_name].parts['Specimen'].Set(faces=
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#3 ]', 
    ), ), name='Specimen')
mdb.models[job_name].parts['Specimen'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models[job_name].parts['Specimen'].sets['Specimen'], sectionName=
    'Specimen', thicknessAssignment=FROM_SECTION)
mdb.models[job_name].parts['Steel'].Set(faces=
    mdb.models[job_name].parts['Steel'].faces.getSequenceFromMask(('[#1 ]', ), 
    ), name='Stainless Steel')
mdb.models[job_name].parts['Steel'].SectionAssignment(offset=0.0, offsetField=
    '', offsetType=MIDDLE_SURFACE, region=
    mdb.models[job_name].parts['Steel'].sets['Stainless Steel'], sectionName=
    'Stainless Steel', thicknessAssignment=FROM_SECTION)
mdb.models[job_name].parts['Elastic Indenter'].Set(faces=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#7 ]', ), ), name='Set-1')
mdb.models[job_name].parts['Elastic Indenter'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models[job_name].parts['Elastic Indenter'].sets['Set-1'], sectionName=
    'Tungsten Carbide', thicknessAssignment=FROM_SECTION)
mdb.models[job_name].rootAssembly.DatumCsysByThreePoints(coordSysType=
    CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 
    0.0, -1.0))
mdb.models[job_name].rootAssembly.Instance(dependent=ON, name=
    'Elastic Indenter-1', part=mdb.models[job_name].parts['Elastic Indenter'])
mdb.models[job_name].rootAssembly.Instance(dependent=ON, name=
    'Load Application Part-1', part=
    mdb.models[job_name].parts['Load Application Part'])
mdb.models[job_name].rootAssembly.Instance(dependent=ON, name='Specimen-1', 
    part=mdb.models[job_name].parts['Specimen'])
mdb.models[job_name].rootAssembly.Instance(dependent=ON, name='Steel-1', part=
    mdb.models[job_name].parts['Steel'])
mdb.models[job_name].rootAssembly.translate(instanceList=(
    'Load Application Part-1', 'Steel-1'), vector=(0.0, 1.0, 0.0))
mdb.models[job_name].StaticStep(initialInc=1e-05, matrixSolver=DIRECT, 
    matrixStorage=UNSYMMETRIC, maxNumInc=10000, minInc=1e-08, name=
    'Loading Step', nlgeom=ON, previous='Initial')
mdb.models[job_name].parts['Load Application Part'].Set(name=
    'Reference Point Set', referencePoints=(
    mdb.models[job_name].parts['Load Application Part'].referencePoints[2], ))
mdb.models[job_name].rootAssembly.regenerate()
mdb.models[job_name].HistoryOutputRequest(createStepName='Loading Step', name=
    'Indenter Displacement', rebar=EXCLUDE, region=
    mdb.models[job_name].rootAssembly.allInstances['Load Application Part-1'].sets['Reference Point Set']
    , sectionPoints=DEFAULT, timeInterval=0.02, variables=('U2', ))
mdb.models[job_name].fieldOutputRequests['F-Output-1'].setValues(timeInterval=
    0.25, variables=('S', 'MISES', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'EVOL'))
mdb.models[job_name].rootAssembly.Surface(name='Load-Application Part', 
    side2Edges=
    mdb.models[job_name].rootAssembly.instances['Load Application Part-1'].edges.getSequenceFromMask(
    ('[#3 ]', ), ))
mdb.models[job_name].rootAssembly.Surface(name='Steel Top', side1Edges=
    mdb.models[job_name].rootAssembly.instances['Steel-1'].edges.getSequenceFromMask(
    ('[#10 ]', ), ))
mdb.models[job_name].Tie(adjust=ON, master=
    mdb.models[job_name].rootAssembly.surfaces['Load-Application Part'], name=
    'Constraint-1', positionToleranceMethod=COMPUTED, slave=
    mdb.models[job_name].rootAssembly.surfaces['Steel Top'], thickness=ON, 
    tieRotations=ON)
mdb.models[job_name].ContactProperty('Steel-Indenter')
mdb.models[job_name].rootAssembly.Surface(name='m_Surf-3', side1Edges=
    mdb.models[job_name].rootAssembly.instances['Steel-1'].edges.getSequenceFromMask(
    ('[#6 ]', ), ))
mdb.models[job_name].rootAssembly.Surface(name='s_Surf-3', side1Edges=
    mdb.models[job_name].rootAssembly.instances['Elastic Indenter-1'].edges.getSequenceFromMask(
    ('[#48 ]', ), ))
mdb.models[job_name].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    clearanceRegion=None, createStepName='Loading Step', datumAxis=None, 
    initialClearance=OMIT, interactionProperty='Steel-Indenter', master=
    mdb.models[job_name].rootAssembly.surfaces['m_Surf-3'], name=
    'Steel-Indenter', slave=
    mdb.models[job_name].rootAssembly.surfaces['s_Surf-3'], sliding=FINITE, 
    thickness=ON)
mdb.models[job_name].interactions['Steel-Indenter'].move('Loading Step', 
    'Initial')
mdb.models[job_name].ContactProperty('Indenter-Specimen Friction')
mdb.models[job_name].interactionProperties['Indenter-Specimen Friction'].TangentialBehavior(
    dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
    formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
    pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
    table=((coeff_of_friction, ), ), temperatureDependency=OFF)
mdb.models[job_name].rootAssembly.Surface(name='m_Surf-5', side1Edges=
    mdb.models[job_name].rootAssembly.instances['Elastic Indenter-1'].edges.getSequenceFromMask(
    ('[#c ]', ), ))
mdb.models[job_name].rootAssembly.Surface(name='s_Surf-5', side1Edges=
    mdb.models[job_name].rootAssembly.instances['Specimen-1'].edges.getSequenceFromMask(
    ('[#60 ]', ), ))
mdb.models[job_name].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    clearanceRegion=None, createStepName='Loading Step', datumAxis=None, 
    initialClearance=OMIT, interactionProperty='Indenter-Specimen Friction', 
    master=mdb.models[job_name].rootAssembly.surfaces['m_Surf-5'], name=
    'Indenter-Specimen', slave=
    mdb.models[job_name].rootAssembly.surfaces['s_Surf-5'], sliding=FINITE, 
    thickness=ON)
mdb.models[job_name].interactions['Indenter-Specimen'].move('Loading Step', 
    'Initial')
mdb.models[job_name].TabularAmplitude(data=((0.0, 0.0), (1.0, -1*load)), name=
    'Load History', smooth=SOLVER_DEFAULT, timeSpan=STEP)
mdb.models[job_name].rootAssembly.Set(name='Set-1', referencePoints=(
    mdb.models[job_name].rootAssembly.instances['Load Application Part-1'].referencePoints[2], 
    ))
mdb.models[job_name].ConcentratedForce(amplitude='Load History', cf2=1.0, 
    createStepName='Loading Step', distributionType=UNIFORM, field='', 
    localCsys=None, name='Load History', region=
    mdb.models[job_name].rootAssembly.sets['Set-1'])
mdb.models[job_name].loads['Load History'].suppress()
mdb.models[job_name].loads['Load History'].resume()
mdb.models[job_name].rootAssembly.Set(edges=
    mdb.models[job_name].rootAssembly.instances['Specimen-1'].edges.getSequenceFromMask(
    ('[#8 ]', ), ), name='Set-2')
mdb.models[job_name].EncastreBC(createStepName='Loading Step', localCsys=None, 
    name='Fixed Bottom', region=
    mdb.models[job_name].rootAssembly.sets['Set-2'])
mdb.models[job_name].boundaryConditions['Fixed Bottom'].move('Loading Step', 
    'Initial')
mdb.models[job_name].rootAssembly.Set(edges=
    mdb.models[job_name].rootAssembly.instances['Elastic Indenter-1'].edges.getSequenceFromMask(
    ('[#a2 ]', ), ), name='Set-3')
mdb.models[job_name].DisplacementBC(amplitude=UNSET, createStepName=
    'Loading Step', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    localCsys=None, name='Fixed Indenter Displacement', region=
    mdb.models[job_name].rootAssembly.sets['Set-3'], u1=0.0, u2=UNSET, ur3=
    UNSET)
mdb.models[job_name].boundaryConditions['Fixed Indenter Displacement'].move(
    'Loading Step', 'Initial')
mdb.models[job_name].rootAssembly.Set(edges=
    mdb.models[job_name].rootAssembly.instances['Specimen-1'].edges.getSequenceFromMask(
    ('[#84 ]', ), ), name='Set-4')
mdb.models[job_name].XsymmBC(createStepName='Initial', localCsys=None, name=
    'Symmetry Condition', region=
    mdb.models[job_name].rootAssembly.sets['Set-4'])
mdb.models[job_name].parts['Elastic Indenter'].setMeshControls(elemShape=TRI, 
    regions=
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#7 ]', ), ))
mdb.models[job_name].parts['Elastic Indenter'].setElementType(elemTypes=(
    ElemType(elemCode=CAX4R, elemLibrary=STANDARD), ElemType(elemCode=CAX3H, 
    elemLibrary=STANDARD)), regions=(
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#7 ]', ), ), ))
mdb.models[job_name].parts['Steel'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Steel'].edges.getSequenceFromMask(('[#2 ]', ), 
    ), number=30, ratio=1.0)
mdb.models[job_name].parts['Steel'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Steel'].edges.getSequenceFromMask(('[#5 ]', ), 
    ), number=40, ratio=10.0)
mdb.models[job_name].parts['Steel'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Steel'].edges.getSequenceFromMask(('[#1 ]', ), 
    ), number=40, ratio=10.0)
mdb.models[job_name].parts['Steel'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Steel'].edges.getSequenceFromMask(('[#18 ]', 
    ), ), number=20, ratio=1.0)
mdb.models[job_name].parts['Steel'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Steel'].edges.getSequenceFromMask(('[#18 ]', 
    ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Steel'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Steel'].edges.getSequenceFromMask(('[#18 ]', 
    ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Steel'].generateMesh()
mdb.models[job_name].parts['Steel'].deleteMesh(regions=
    mdb.models[job_name].parts['Steel'].faces.getSequenceFromMask(('[#1 ]', ), 
    ))
mdb.models[job_name].parts['Steel'].setMeshControls(elemShape=TRI, regions=
    mdb.models[job_name].parts['Steel'].faces.getSequenceFromMask(('[#1 ]', ), 
    ))
mdb.models[job_name].parts['Steel'].generateMesh()
mdb.models[job_name].parts['Steel'].setElementType(elemTypes=(ElemType(
    elemCode=CAX4R, elemLibrary=STANDARD), ElemType(elemCode=CAX3H, 
    elemLibrary=STANDARD)), regions=(
    mdb.models[job_name].parts['Steel'].faces.getSequenceFromMask(('[#1 ]', ), 
    ), ))
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#82 ]', ), ), number=20, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#44 ]', ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#8 ]', ), ), end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#20 ]', ), ), number=20, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#8 ]', ), ), end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#20 ]', ), ), number=20, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#11 ]', ), ), number=25, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].seedEdgeByBias(biasMethod=
    SINGLE, constraint=FINER, end2Edges=
    mdb.models[job_name].parts['Elastic Indenter'].edges.getSequenceFromMask((
    '[#11 ]', ), ), number=25, ratio=1.0)
mdb.models[job_name].parts['Elastic Indenter'].setElementType(elemTypes=(
    ElemType(elemCode=CAX4R, elemLibrary=STANDARD), ElemType(elemCode=CAX3H, 
    elemLibrary=STANDARD)), regions=(
    mdb.models[job_name].parts['Elastic Indenter'].faces.getSequenceFromMask((
    '[#7 ]', ), ), ))
mdb.models[job_name].parts['Elastic Indenter'].generateMesh()

mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#42 ]', ), ), number=150, ratio=1.0)
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#81 ]', ), ), number=75, ratio=1.0)
mdb.models[job_name].parts['Specimen'].setMeshControls(elemShape=TRI, regions=
    mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#1 ]', 
    ), ))
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask(('[#4 ]', 
    ), ), end2Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#20 ]', ), ), number=50, ratio=6.0)
mdb.models[job_name].parts['Specimen'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models[job_name].parts['Specimen'].edges.getSequenceFromMask((
    '[#18 ]', ), ), number=30, ratio=1.0)
mdb.models[job_name].parts['Specimen'].setElementType(elemTypes=(ElemType(
    elemCode=CAX4RH, elemLibrary=STANDARD, hourglassControl=DEFAULT), ElemType(
    elemCode=CAX3, elemLibrary=STANDARD)), regions=(mdb.models[job_name].parts['Specimen'].faces.getSequenceFromMask(('[#2 ]', 
    ), ), ))
mdb.models[job_name].parts['Specimen'].generateMesh()
mdb.models[job_name].rootAssembly.regenerate()

mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model=job_name, modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=job_name, nodalOutputPrecision=SINGLE, 
    numCpus=2, numDomains=2, numGPUs=0, queue=None, resultsFormat=ODB, scratch=
    '', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs[job_name].submit(consistencyChecking=OFF)
mdb.jobs[job_name].waitForCompletion()

os.chdir('./../')
