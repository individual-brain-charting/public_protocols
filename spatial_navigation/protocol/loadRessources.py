from __future__ import division
import viz
import vizact
import vizmat
import vizshape
import os
import random
import itertools
import sys
import math
import cPickle

## user librarys
sys.path.insert(0,os.path.realpath('.\py'))
sys.path.insert(0,os.path.realpath('.\objects'))

from defineOptions import options
from myFog import *

# load vizproximity library with removeSensor() hotfix
import myVizproximity as vizproximity

# -------
# load VE
# -------

# add skybox 
env = viz.addEnvironmentMap('sky.jpg') 
sky = viz.add('skydome.dlc')
sky.texture(env)

# link the skybox to the position of the viewport, in order to render background to infinity
skylink = viz.link(viz.MainView, sky, mask = viz.LINK_POS)

# add fog 
fog = myFog(startDist = options.startDist,endDist = options.endDist,fadeOutDist = options.fadeOutDist,fadeTime = options.fogFadeTime, fogColor = options.fogColor) 
sky.color(fog.color)		# make the sky background color equal to fog color for fading animation
sky.visible(False)

# add ambient light
ambLight = viz.addLight()
ambLight.setEuler(0,90,0)
ambLight.intensity(1) 

# add city
city = viz.addChild(os.path.realpath('./objects/virtualtuebingen_baked.osgb'))
city.anisotropy(16)
city.visible(False)

groundDimension = 1000	# dimensions of ground in m in x and z direction
groundTilingSize = 20	# tiling of ground texture in m

grassTex = viz.addTexture('./images/grass.png',wrap = viz.REPEAT)

groundPlane = ()	# init tuple for ground planes

for x in range(-groundDimension,groundDimension,groundTilingSize):
	for z in range(-groundDimension,groundDimension,groundTilingSize):
		if (x*x + z*z < groundDimension*groundDimension):
			
			ground = viz.addTexQuad()
			ground.setScale([groundTilingSize,groundTilingSize,1])
			ground.setPosition([x, -2, z]) 
			ground.setEuler([0, 90, 0])
			ground.texture(grassTex, unit = 0)
	
			ground.anisotropy(16)
			ground.visible(False)
			groundPlane = groundPlane + (ground,)

# -----------
# ITI related
# -----------

ITI_bg = viz.addTexQuad(parent=viz.SCREEN, scale=[100.0]*3,color=options.ITI_bgColor, alpha=0)

# crosshair for ITI
cross =  viz.addTexQuad(parent=viz.SCREEN,texture=viz.addTexture(os.path.realpath('./images/cross.png')),scale = [options.ITI_crossSize[0],options.ITI_crossSize[1],1],align = viz.ALIGN_CENTER_CENTER)
cross.visible(False)


# ------------------------
# load targets & positions
# ------------------------

# small class that allows easy store of locations with their respective positions, names, etc...
class storeObject(object):
	
	def __init__(self):
		pass

'''
experimental condition (2 targets, name and position as specified in defineOptions.py)
for experimental targets, their images will be used as objects to store all necessary information about the current target
'''

targets_exp = ()

for k in range(len(options.targetNames_exp)):
	
	image = viz.addTexQuad(parent=viz.SCREEN,texture=viz.addTexture('./images/' + options.targetNames_exp[k] + '.tif'),scale = [options.scale_centerImage[0]*options.reduceScreenSize[0],
	options.scale_centerImage[1]*options.reduceScreenSize[1],1],align = viz.ALIGN_CENTER_CENTER)
	
	image.name = options.targetNames_exp[k]
	image.position = options.targetPositions_exp[k]
	
	image.visible(False)
	
	targets_exp = targets_exp + (image,)

'''	
control condition (2 targets per direction at each intersection: left and right)
for control targets, each house is a seperate target, this way, the run.py script can be written with minimum redundancy
'''

targets_ctrl = ()

for inters in range(4):
	
	for house in range(4):
		
		houseHandle = city.getChild('i' + str(inters) + 'h' + str(house))
		
		houseHandle.name = (str(inters) + str(house))
		
		houseHandle.color([1,1,1])
		# get center of object by grapping the handle to a small sphere that is positioned in the center of each object, depending on current direction and target
		centerHandle = city.getChild('pos_house_' + str(inters) + '_' + str(house) + '-GEODE')
		[ox,oy,oz] = centerHandle.getPosition(viz.ABS_GLOBAL)
		houseHandle.position = [ox,oz]
		
		targets_ctrl = targets_ctrl + (houseHandle,)

'''	
intersections are stored as objects, each intersection has its center position and four start positions
'''

intersections = ()

for k in range(4):
	
	# create intersection object
	intersection = city.getChild('pos_inters_' + str(k) + '-GEODE')
	intersection.visible(False)	# hide the position node
	intersection.nr = k
	# get intersection center position
	intersection.position = [round(n,3) for n in intersection.getPosition(viz.ABS_GLOBAL)]
	
	intersection.closedIn = False	# bool to determine if participant has moved close to this intersection during feedback
	
	# get intersection start points
	intersection.startPoints = []
	for i in range(4):
		sP = city.getChild('pos_sP_' + str(k) + '_' + str(i) + '-GEODE')
		sP.visible(False)
		
		intersection.startPoints.append([round(n,3) for n in sP.getPosition(viz.ABS_GLOBAL)])
	
	intersections = intersections + (intersection,)

'''	
streets are stored as objects, each street has subnodes with their own positions
'''

streets = ()
nodeNames = city.getNodeNames()	# get the names of all the nodes in city model (needed for street subnodes)

for k in range(12):
	
	# find out how many sub nodes the current street has
	streetnodes = [item for item in nodeNames if ('pos_street_' + str(k) + '_') in item and '-GEODE' in item]
	
	# create street object
	street = storeObject()	
	street.nr = k
	
	# get positions of subnodes and store them in list
	street.subNodes = []
	for subNode in streetnodes:
		subNodeHandle = city.getChild(subNode)
		subNodeHandle.visible(False)
		street.subNodes.append([round(n,3) for n in subNodeHandle.getPosition(viz.ABS_GLOBAL)])
	
	streets = streets + (street,)
	
# -----------------
# load other images
# -----------------

crosshairImage = viz.addTexQuad(parent=viz.SCREEN,texture=viz.addTexture('./images/crosshair.png'),scale = [options.scale_crosshairImage[0]*options.reduceScreenSize[0],options.scale_crosshairImage[1]*options.reduceScreenSize[1]
,1],align = viz.ALIGN_CENTER_CENTER)
crosshairImage.setPosition([options.imagePosition_crosshair[0],options.imagePosition_crosshair[1],1])
crosshairImage.visible(False)

ctrlCueImage = viz.addTexQuad(parent=viz.SCREEN,texture=viz.addTexture('./images/ctrlCue.tif'),scale = [options.scale_centerImage[0]*options.reduceScreenSize[0],
	options.scale_centerImage[1]*options.reduceScreenSize[1],1],align = viz.ALIGN_CENTER_CENTER)
ctrlCueImage.visible(False)

arrowR = viz.addTexQuad(parent=viz.SCREEN,texture=viz.addTexture('./images/arrow.png'),scale = [options.scale_crosshairImage[0]*options.reduceScreenSize[0],options.scale_crosshairImage[1]*options.reduceScreenSize[1]
,1],align = viz.ALIGN_CENTER_CENTER)
arrowR.setPosition([options.imagePosition_crosshair[0] + 0.2 ,options.imagePosition_crosshair[1],1])
arrowR.setEuler([0,0,-90],viz.ABS_LOCAL)
arrowR.visible(False)

arrowL = viz.addTexQuad(parent=viz.SCREEN,texture=viz.addTexture('./images/arrow.png'),scale = [options.scale_crosshairImage[0]*options.reduceScreenSize[0],options.scale_crosshairImage[1]*options.reduceScreenSize[1]
,1],align = viz.ALIGN_CENTER_CENTER)
arrowL.setPosition([options.imagePosition_crosshair[0] - 0.2,options.imagePosition_crosshair[1],1])
arrowL.setEuler([0,0,90],viz.ABS_LOCAL)
arrowL.visible(False)

# ------------
# load sensors
# ------------

sensorManager = vizproximity.Manager() # create proximity manager

# add main viewpoint as proximity target
sensorTarget = vizproximity.Target(viz.MainView)
sensorManager.addTarget(sensorTarget)

# add spheres and sensors to the street endings

streetSensors = []
streetSpheres = ()

for sPos in options.sensorPositions:
	
	cBall = vizshape.addSphere(radius = options.sphereRadius)
	cBall.color(viz.RED) 
	cBall.disable(viz.INTERSECTION)
	cBall.setPosition([sPos[0],options.sphereHeight,sPos[1]])
	cBall.visible(False)
	
	ballSensor = vizproximity.Sensor(vizproximity.CircleArea(options.sensorRadius),source=cBall)
	ballSensor.identified = False	# variable to check if sensor has been identified
	sensorManager.addSensor(ballSensor)
	cBall.sensor = ballSensor
	
	streetSensors.append(ballSensor)
	streetSpheres = streetSpheres + (cBall,)
	
# ------------------
# load sequences
# ------------------

''' 
Sequences will be generated as lists, containing all possible combinations of 
experimental: intersections (4), directions (4) and targets (2) 
control: intersections (4), directions (4) + houses
The sequences are encoded as follows: (intersection, direction (starting point), target (house))
see defineOptions and overview.png in ./images/ folder for the corresponding positions of each number
'''

print 'Start generating experimental sequence...'

seqFound = False
	
while seqFound == False:		
	sequence_exp = list(itertools.product(range(4),range(4),range(2))) * 2
	
	lenSeq = len(sequence_exp)		# var needed to zip in reverse order through the loop
	
	random.shuffle(sequence_exp)	
	duplFound = False
	
	# see documentation for constraints, forward direction
	for first, sec, third, fourth, fifth in zip(sequence_exp, sequence_exp[1:], sequence_exp[2:],sequence_exp[3:],sequence_exp[4:]):
		
	#  at least 4 trials between repetition of intersection/direction/target
		if first[0:3] == sec[0:3] or first [0:3] == third[0:3] or first[0:3] == fourth[0:3] or first[0:3] == fifth[0:3]:
			duplFound = True
			break
		
		# at least two trials before intersection/direction is repeated
		if first[:2] == sec[:2] or first[:2] == third[:2]:
			duplFound = True
			break
		
		# maximum of 4 repetitions of the same target
		if first[2] == sec[2] and first[2] == third[2] and first[2] == fourth[2] and first[2] == fifth[2]:
			duplFound = True
			break
	
	# no everything in reversed order for the last items (zip only iterates until the shortes list has reached its end - fifth element here)
	sequence_exp_rev = sequence_exp[::-1]
	
	for first, sec, third, fourth, fifth in zip(sequence_exp_rev, sequence_exp_rev[1:], sequence_exp_rev[2:],sequence_exp_rev[3:],sequence_exp_rev[4:]):
		
	#  at least 4 trials between repetition of intersection/direction/target
		if first[0:3] == sec[0:3] or first [0:3] == third[0:3] or first[0:3] == fourth[0:3] or first[0:3] == fifth[0:3]:
			duplFound = True
			break
		
		# at least two trials before intersection/direction is repeated
		if first[:2] == sec[:2] or first[:2] == third[:2]:
			duplFound = True
			break
		
		# maximum of 4 repetitions of the same target
		if first[2] == sec[2] and first[2] == third[2] and first[2] == fourth[2] and first[2] == fifth[2]:
			duplFound = True
			break
	
	# if no adjacent duplicates are found, exit while loop
	if duplFound == False:
		seqFound = True
	
print('done.')

print 'Start generating control sequence...'

houseList = range(4)

dirPos = [[-1,0],[0,1],[1,0],[0,-1]]					# normalized starting positions for directions

housePos = [[-1,-1],[-1,1],[1,1],[1,-1]]				# normalized house positions

seqFound = False

while seqFound == False:		
	sequence_ctrl = list(itertools.product(range(4),range(4))) * 2
	
	# add random blue house to sequence_ctrl
	tempHouseList = list(houseList)		
	for i in range(len(sequence_ctrl)):
		
		house = random.choice(tempHouseList)	# choose random house
		sequence_ctrl[i] = sequence_ctrl[i] + (house,)	# add to current trial
		
		tempHouseList.remove(house)
		
		if tempHouseList == []:
			tempHouseList = list(houseList)
	
	random.shuffle(sequence_ctrl)	
	
	duplFound = False
	
	# see documentation for constraints, blue house constraints is solved by calculating the angle between starting position and house position (saves a lot of code in the run.py file)
	for trials in zip(sequence_ctrl, sequence_ctrl[1:], sequence_ctrl[2:], sequence_ctrl[3:]):
		
		# get the normalized angle between the direction and their houses
		angles = []
		for trial in trials:
			angle = abs(vizmat.NormAngle(vizmat.AngleToPoint(dirPos[trial[1]],housePos[trial[2]])-vizmat.AngleToPoint([0,0],dirPos[trial[1]])))
			if 150 < angle < 270:
				angles.append('front')
			else:
				angles.append('back')
		
		# check if not more than the following three have the same angle + the additional constraint
		if (angles[0] == angles[1] and angles[0] == angles[2] and angles[0] == angles[3]) or (trials[0][:2] == trials[1][:2] or trials[0][:2] == trials[2][:2]):
			duplFound = True
			break
	
	# same in reversed direction
	sequence_ctrl_rev = sequence_ctrl[::-1]
	for trials in zip(sequence_ctrl_rev, sequence_ctrl_rev[1:], sequence_ctrl_rev[2:], sequence_ctrl_rev[3:]):
		
		# get the normalized angle between the direction and their houses
		angles = []
		for trial in trials:
			angle = abs(vizmat.NormAngle(vizmat.AngleToPoint(dirPos[trial[1]],housePos[trial[2]])-vizmat.AngleToPoint([0,0],dirPos[trial[1]])))
			if 150 < angle < 270:
				angles.append('front')
			else:
				angles.append('back')
		
		# check if not more than the following three have the same angle + the additional constraint
		if (angles[0] == angles[1] and angles[0] == angles[2] and angles[0] == angles[3]) or (trials[0][:2] == trials[1][:2] or trials[0][:2] == trials[2][:2]):
			duplFound = True
			break
	
	# now final check: each intersection/direction is presented twice, make sure that the have different target houses
	for item in sequence_ctrl:
		idx = [i for i, x in enumerate(sequence_ctrl) if x == item]
		
		if len(idx) > 1:
			duplFound = True
			break

	# if no adjacent duplicates are found, exit while loop
	if duplFound == False:
		seqFound = True

print('done.')
