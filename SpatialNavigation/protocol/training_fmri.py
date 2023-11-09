# -*- coding: utf-8 -*-

# ----------------------------------------------------------
# SLT_DCM - fMRI TRAINING
# 
# Preamble
#
#
# ----------------------------------------------------------	

# --------
# Librarys
# --------

from __future__ import division
import viz
import vizact
import vizinput
import vizshape
import vizdlg
import viztask
import random
import vizjoy
import os
import datetime

import math
import sys

sys.path.insert(0,os.path.realpath('.\py'))

# load vizproximity library with removeSensor() hotfix
import myVizproximity as vizproximity

## user librarys

# load VE and objects and graphic effects
from loadRessources import * 
from defineOptions import options, view, optionsDict
from flipImage import *

# load text class
from displayInfo import *

# load timer class
from myTimer import *

# load joystick movement and wait conditions
from joystickConditions import waitJoy
from myMovement import joystick, updateMovement

# load instruction strings
from instructions import introText, procedualText

# convertAngles from Vizard to mathematical convention and vice versa
import convertAngles

# File I/O
from csv_io import write_to_csv as writeToFile

# -----------------
# Globals & Statics
# -----------------

## timer classes
logTime = myTimer(timeFormat = '%S')			# timer for log file, displays second.microseconds since the experiment started
genTime = myTimer()								# init timer instance for general timing (file name, etc)
movementTime = myTimer(timeFormat = '%S')		# timer to check if movement has halted during practice phase

## define waitCondition for user input, depending on the desired inputDevice
if options.movementInput == 'joystick':
	waitButton = waitJoy(joystick,'button',options.joyButton)				# button used for user input
	waitButtonText = waitJoy(joystick,'button',options.joyButton)			# if text is displayed on the screen and the subject makes a button press, it should disapper (avoid duplicate text on screen)
elif options.movementInput == 'keyboard':	
	waitButton = viztask.waitKeyDown(options.buttonMap['enter'])			# button used for user input
	waitButtonText = viztask.waitKeyDown(options.buttonMap['enter'])		# if text is displayed on the screen and the subject makes a button press, it should disapper (avoid duplicate text on screen)

## init input variables
sNr = [] 
sInitials = []
sGender = []
sAge = []

## movement
# for familiarisation phase
move_all = vizact.ontimer(0,updateMovement,inputDevice = options.movementInput, buttonMap = options.buttonMap)				# rotation + translation function
move_all.setEnabled(0)

# for practice and test phase
move_rot = vizact.ontimer(0,updateMovement,inputDevice = options.movementInput, trans = 0, buttonMap = options.buttonMap) 	# only rotational movement
move_rot.setEnabled(0)

## signals and bool variables
timerExpired = viztask.Signal()		# signal that is used to indicate that the timer expired during exploration phase
allSensorsFound = False				# variable to indicate that all sensor have beend identified during exploration phase

## other
globalTrialNr = 1					# used for experimental log file, trial Nr should start with 1 here
allSpheresFound = viztask.Signal()	# signal to indicate that all spheres have been found during fam phase
sphereCount = 0						# how many spheres have been found?
stoodStill = viztask.Signal()		# signal to indicate that participant has stood still during tutorial of practice phase

# -----------------
# Text & images
# -----------------

blackTheme = viz.getTheme()
blackTheme.backColor = (.5,.5,.5,1)
blackTheme.lightBackColor = (0.6,0.6,0.6,1)
blackTheme.darkBackColor = (0.2,0.2,0.2,1)
blackTheme.highBackColor = (0.2,0.2,0.2,1)
blackTheme.textColor = (viz.BLACK)
	
# counter in top left corner for sphere count in familiarisation
sphereCounter_panel = vizdlg.Panel(theme = blackTheme, border = False)
sphereCounter_text = sphereCounter_panel.addItem(viz.addText('Vous avez pris ' + str(sphereCount) +' des 8 boules.'),align=vizdlg.ALIGN_CENTER, fontSize = 24)
viz.link(viz.CenterCenter,sphereCounter_panel,offset=(-925,500,0))
sphereCounter_panel.visible(0)

introScreenText = displayInfo(mode = 'fullscreen',fontSize = options.fontS_introScreen * options.reduceScreenSize[0], textAlignment = viz.ALIGN_LEFT_BOTTOM)	# fullscreen text for introduction text
introScreenText_continue = displayInfo(mode = 'fit', fontSize = options.fontS_introScreen_continue * options.reduceScreenSize[0],border = False,background = False,textAlignment = viz.ALIGN_CENTER_BOTTOM) 	# continue with button text on bottom of intro page
viz.link(viz.CenterCenter,introScreenText_continue.panel,offset = (options.offset_intro_continue[0]* options.reduceScreenSize[0],options.offset_intro_continue[1]* options.reduceScreenSize[1],0)) 

fullscreenText_bg = displayInfo(mode = 'fullscreen',fontSize = options.fontS_fullscreen * options.reduceScreenSize[0],background = True, border = False)	# fullscreen text with background

# text for additional information during practice
practiceText = displayInfo(mode = 'fit', fontSize = options.fontS_introScreen * options.reduceScreenSize[0],border = False,background = True, textAlignment = viz.ALIGN_CENTER_BOTTOM) 
practiceText.setTextColor(viz.BLACK)
practiceText.setFontsize(40)
viz.link(viz.CenterCenter,practiceText.panel,offset = (0,-200,0)) 

## image placeholders
imageC = displayInfo(mode = 'fullscreen',border = True, background = False)
imageC.positionPanel([options.imagePosition_cue[0], options.imagePosition_cue[1],0])

intro_imageL = displayInfo(mode = 'fullscreen',border = False)
intro_imageL.positionPanel([options.imagePosition_introL[0]*options.reduceScreenSize[0],options.imagePosition_introL[1]*options.reduceScreenSize[1],0])
intro_imageC = displayInfo(mode = 'fullscreen',border = False)
intro_imageC.positionPanel([options.imagePosition_introC[0]*options.reduceScreenSize[0],options.imagePosition_introC[1]*options.reduceScreenSize[1],0])
# during piloting, now right image -> center image is in position of right image!
intro_imageR = displayInfo(mode = 'fullscreen',border = False)
intro_imageR.positionPanel([options.imagePosition_introR[0]*options.reduceScreenSize[0],options.imagePosition_introR[1]*options.reduceScreenSize[1],0])

intro_imageL_text = displayInfo(mode = 'fit', fontSize = options.fontS_introImage * options.reduceScreenSize[0],border = False,background = False,textAlignment = viz.ALIGN_CENTER_BOTTOM)
intro_imageL_text.positionPanel([options.imagePosition_introL[0]*options.reduceScreenSize[0],options.imagePosition_introL[1]*options.reduceScreenSize[1]-220,0]) 
intro_imageC_text = displayInfo(mode = 'fit', fontSize = options.fontS_introImage * options.reduceScreenSize[0],border = False,background = False,textAlignment = viz.ALIGN_CENTER_BOTTOM) 
intro_imageC_text.positionPanel([options.imagePosition_introC[0]*options.reduceScreenSize[0],options.imagePosition_introC[1]*options.reduceScreenSize[1]-220,0]) 
# during piloting, now right image -> center image is in position of right image!
intro_imageR_text = displayInfo(mode = 'fit', fontSize = options.fontS_introImage * options.reduceScreenSize[0],border = False,background = False,textAlignment = viz.ALIGN_CENTER_BOTTOM) 
intro_imageR_text.positionPanel([options.imagePosition_introR[0]*options.reduceScreenSize[0],options.imagePosition_introR[1]*options.reduceScreenSize[1]-235,0]) 

# --------------
# Input & Output
# --------------

# input subject related data
if options.debug == 0:
	while type(sNr) != int:
		sNr = viz.input(' Subject number')

#	sInitials = viz.input('Subject initials')

#	while sGender not in range(1,3):
#		sGender = viz.input('Subject gender (1:f/2:m)')
	
#	while type(sAge) != int:
#		sAge = viz.input('Subject age')

fileTime = genTime.time()
fileDate = genTime.date().replace('.','')

# prompt for a directory to save log files in
path = os.getcwd()
logFilePath = os.path.join(path, 'logs')
if not os.path.exists(logFilePath):
	os.mkdir(logFilePath)
#logFilePath = vizinput.directory(prompt='Select a folder to save the log files.')

if options.debug == 0:
	logFileName =  logFilePath + '/Subject_'+ str(sNr) + '_' + fileDate + '_' + fileTime + '_training.csv'	# file name for general log file (saves every information)
	optionsFileName =  logFilePath + '/Subject_'+ str(sNr) + '_' + fileDate + '_' + fileTime + '_training_options' +  '.csv'	# file name for options file (saves only options)
else:
	logFileName =  logFilePath + '/debug_' + fileDate + '_' + fileTime + '.csv'	# file name for log file
	optionsFileName =  logFilePath + '/debug_' + fileDate + '_' + fileTime + '_options' +  '.csv'	# file name for options file

# save options into csv file
for option in sorted(optionsDict):
	
	if option != 'optionsDict':
		writeToFile([option, optionsDict[option]],optionsFileName)

if options.debug == 0:
	# write subject information to log file
	writeToFile(['Number',sNr],logFileName)
#	writeToFile(['Initials',sInitials],logFileName)
#	writeToFile(['Gender',sGender],logFileName)
#	writeToFile(['Age',sAge],logFileName)

# write header for following rows
writeToFile(['Data type','Time','sPos (x)','sPos (y)',' sPos(z)','View Angle','jPos (x)', 'jPos (z)'],logFileName)

# -------------------
# Procedual functions
# -------------------


def main():
	
	# init stuff
	logTime.start()			# start the time stamp for log file

	# start position logging
	if options.fs == -1:
		logTimer = vizact.ontimer(viz.getFrameElapsed(),posLogger)	# start the logging of position and view angle at maximum frequency (= framerate)
	else:
		logTimer = vizact.ontimer(1/fs,posLogger)					# start the logging of position and view angle at frequency specified by fs
	
	yield viztask.waitTime(.2)										# wait for split second to give position logging time to initiate
	
	toggleVE('on')		# enable virtual environment
	
	yield familiarisation()
	
	# hide street spheres from familiarisation phase
	for cBall in streetSpheres:
		cBall.visible(0)
	
	viz.collision(viz.OFF)		# disable collision for further partspracticeMastered = False	# variable to decided if experiment should continue with 
	
	fullscreenText_bg.message(' ',fade = options.textFadeTime)
	yield viztask.waitTime(1)
	
	practiceMastered = False	# variable to decided if experiment should continue with 
	
	while practiceMastered == False:

		yield practice()		# practice phase
		
		nextPhase = vizinput.ask('Done?')
		
		if nextPhase == 0:
			practiceMastered = False
			writeLog(['User input -> re-entering practice phase'],logFileName)
		else:	
			practiceMastered = True
			writeLog(['User input -> Practice phase accomplished'],logFileName)

	# end experiment
	logTimer.setEnabled(0)
	
	fullscreenText_bg.message(procedualText['partEnded'],fade = options.textFadeTime)
	
	yield viztask.waitTime(3)
	
	viz.quit()
	
def familiarisation():
	
	writeLog('Familiarisation started')
	
	# intro screen
	yield displayIntroScreen('fam')
	# hide intro screen text
	introScreenText.hide(options.textFadeTime)
	introScreenText_continue.hide(options.textFadeTime)
	
	writeLog('Setting viewpoint location and view direction to start value')
	view.setEuler(options.initialViewingDirection,0,0)				# set view direction to initial start position
	view.collision(viz.OFF)											# disable collision so that viewport can be moved
	
	view.setPosition(options.startx,options.eyeLvl,options.startz)	# set viewport position to initial start position
	
	view.collision(viz.ON)											# re-enable collision
	
	sensorMonitor = viztask.schedule(monitorSensors())				# start monitoring state of sphere sensors
	
	writeLog('Movement enabled')
	move_all.setEnabled(1)				# enable movement

	sphereCounter_panel.visible(1)		# add counter to show how many balls have been found
	
	yield allSpheresFound.wait()		# wait for signal to indicate subject has found all spheres

	writeLog('All sensors found')
	sphereCounter_panel.remove()		# remove counter
	
	sensorMonitor.kill()				# kill sensor monitor
	writeLog('Movement disabled')
	move_all.setEnabled(0)				# disable movement
	writeLog('Familiarisation ended')

def practice():
	
	yield fadeFog('on')						# turn on fog for whole practice phase
	
	writeLog('Practice started')
	
	yield displayIntroScreen('prac')		# intro screen
	
	for i,trial in enumerate(options.sequence_practice_training):		# for loop that iterates over all of the trial in the practice sequence
		
		writeLog(['Starting trial',trial])
		
		if i < options.tutorialTrials:
			writeLog(['This is a tutorial trial'],logFileName)
	
		# get current trial properties and write them into vars (intersection, starting point, target)
		inters = trial[0]
		sP = trial[1]
		targetNr = trial[2]
		
		# get current target and write it into var
		if trial[3] == 'exp':
			target = targets_exp[trial[2]]
		elif trial[3] == 'ctrl':
			for house in targets_ctrl:
				if house.name == (str(trial[0]) + str(trial[2])):
					target = house
					target.color(options.ctrlHouseColor)	# color target house for control trials
					break
		
		## travel phase ------------
		# move to start position and rotate to view the intersection center
		writeLog(['Setting viewpoint position to', str(intersections[inters].startPoints[sP])])
		view.setPosition([intersections[inters].startPoints[sP][0],options.eyeLvl + intersections[inters].startPoints[sP][1] ,intersections[inters].startPoints[sP][2]])	
		writeLog('Rotating to intersection center')
		yield viztask.addAction(view, vizact.spinTo(point = [intersections[inters].position[0], options.eyeLvl + intersections[inters].position[1] , intersections[inters].position[2]] ,time = .01,interpolate = vizact.linear))
	
		# display once additional text after tutorial trials end
		if i == options.tutorialTrials:
			fullscreenText_bg.message(procedualText['tutorialOver'])
			yield viztask.waitTime(options.readTime)
			fullscreenText_bg.hide(fade = options.textFadeTime/2)
			
		yield displayCue(target,trial[3],'on')	# show according cue		
		
		# for the first 6 trials, display additional cues
		if i < options.tutorialTrials:
			practiceText.message(procedualText['tutorialMoveForward'])
			yield viztask.waitTime(options.readTime)
			practiceText.hide(fade = options.textFadeTime)
		
		# move subject to the middle of the intersection
		writeLog(['Moving subject to center of intersection',str(intersections[inters].position)])
		yield viztask.addAction(view, vizact.moveTo(pos = [intersections[inters].position[0], options.eyeLvl + intersections[inters].position[1] , intersections[inters].position[2]], time = options.travelTime_intersection))
		writeLog('Movement ended')
		
		## pointing phase ------------
		# short jittered wait phase
		sT = round(random.uniform(.5,1.5),3)
		writeLog(['Short wait time started', str(sT)])
		yield viztask.waitTime(sT)
		writeLog(['Short wait time ended'])
		
		# enable movement, only rotation
		move_rot.setEnabled(1)
		writeLog('Movement enabled')
		
		# start pointing phase
		crosshairImage.visible(True)
		writeLog('Crosshair displayed')
		
		# for the first 6 trials, display additional cues and wait for subject to stay still for some time
		if i < options.tutorialTrials:
			practiceText.message(procedualText['tutorialRotate'])
			arrowL.visible(True), arrowR.visible(True)				# show left and right arrow
			
			yield viztask.waitTime(options.readTime)
			
			movementMonitor = viztask.schedule(monitorMovement())	# start the function that monitors movement and sends a signal as soon as subject has stood still for certain amount of time
			yield stoodStill.wait()									# wait for subject to stand still
			movementMonitor.kill()									# kill monitor function as soon as signal was send
			arrowL.visible(False), arrowR.visible(False)			# hide arrows
			practiceText.message(procedualText['tutorialDecide'])
		
		# wait for subject to make response
		yield viztask.waitAny([waitButton])
		writeLog('Subject pressed button to indicate goal location')
		
		yield displayCue(target,trial[3],'off')		# hide according cue
		
		practiceText.hide()							# hide additional text
		crosshairImage.visible(False)				# hide crosshair
		writeLog('Crosshair hidden')
		
		# disable movement
		move_rot.setEnabled(0)
		writeLog('Movement disabled')
		
		calcAngleError(target,intersections[inters].position[0], intersections[inters].position[2])	# calculate error for indicated target location
		
		if trial[3] == 'ctrl':
			target.color([1,1,1])	# re-color target house 
		
		yield displayITI()			# display ITIs
	
	fullscreenText_bg.message(procedualText['partEnded'],fade = options.textFadeTime)
	yield viztask.waitTime(3)
	writeLog('Practice ended')

def monitorSensors():
	
	global allSpheresFound, sphereCount
	
	exploredSensors = []
	
	while True:
		enteredSensor = yield vizproximity.waitEnter(streetSensors)
		
		if enteredSensor.sensor.identified == False:	# check if sensor is activated the first time
			sphereCount += 1
			cBall = enteredSensor.sensor.getSource()
			
			writeLog(['User entered sensor at position',str(cBall._node.getPosition())])
			
			exploredSensors.append(enteredSensor.sensor)	# append the current sensor to the list of all activated sensors			
			enteredSensor.sensor.identified = True			# prevent a second activation of the sensor
			
			cBall._node.visible(viz.OFF)					# let the ball disappear 
			
			sphereCounter_text.message('Vous avez pris '+ str(sphereCount) + ' des 8 boules.')
			# check if all sensors have been activated, if so, send signal
			if len(exploredSensors) == len(streetSensors):
				writeLog('All sensors have been found')
				allSpheresFound.send()

def monitorMovement():
	
	global movementTime
	
	movementTime.start()
	eulerBefore = view.getEuler()[0]
	
	while True:
		eulerNow = view.getEuler()[0]
		
		if abs(eulerBefore - eulerNow) > .1:
			movementTime.start()
		elif float(movementTime.delta()) > options.stillTime:
			stoodStill.send()
		else:
			pass
		
		yield viztask.waitTime(.01)
		eulerBefore = eulerNow

def calcAngleError(target, ix, iz):
	
	results = []
	'''
	function calculates error between current position and target position. output error angle is between [-180,180] degree
	if the viewport is right to the target, the error is negative and vice versa
	'''
	
	# get current view angle
	curAng = vizmat.NormAngle(view.getEuler()[0])
	writeLog(['Current view angle', str(curAng)])
	
	results.append(curAng)
	
	[tx,tz] = [target.position[0], target.position[1]]	# get target location
	
	# get right angle
	rightAng = vizmat.AngleToPoint([ix,iz],[tx,tz])
	writeLog(['Right view angle',str(rightAng)])
	
	results.append(rightAng)
	
	## calculate difference and correct angle to be in the interval of [-180, 180]
	wrongAng = vizmat.AngleDiff(curAng,rightAng)
	
	writeLog(['Error in view angle',str(wrongAng)])
	
	results.append(wrongAng)
	
	# write out right or missed decision in control conditions based on error tolerance
	if target.name not in options.targetNames_exp:
		if -options.errorTolerance <= wrongAng <= options.errorTolerance:
			writeLog('Right control decision')
			results.append(1)
		else:
			writeLog('Missed control decision')
			results.append(0)
	
	return results

def displayCue(target, phase = [], state = 'off'):
	
	if state == 'on':
		ITI_bg.addAction(vizact.fadeTo(0))	# hide ITI from previous trial
		# hide text from intro screen (before first trial)
		introScreenText.hide()
		introScreenText_continue.hide()
		fullscreenText_bg.hide()	# if there is a background presented, hide it
		
		if phase == 'exp':
			
			writeLog(['Displaying experimental cue to target',target.name])
			target.visible(True)
			imageC.addImage(target)
			
			yield viztask.waitTime(options.cueTime)
			
		elif phase == 'ctrl':
			
			writeLog(['Displaying control cue to target',target.name])
			ctrlCueImage.visible(True)
			imageC.addImage(ctrlCueImage)
			
			yield viztask.waitTime(options.cueTime)
		
	else:
		if phase == 'exp':
			target.visible(False)
			writeLog(['Hiding experimental cue to target',target.name])	
			imageC.removeItems()
			imageC.hide()
		elif phase == 'ctrl':
			writeLog('Displaying control cue')
			ctrlCueImage.visible(False)
			writeLog(['Hiding control cue to target',target.name])	
			imageC.removeItems()
			imageC.hide()


	
def displayITI():
	
	# display ITI
	xPos = random.uniform(options.ITI_rx[0],options.ITI_rx[1])
	yPos = random.uniform(options.ITI_ry[0],options.ITI_ry[1])
	
	waitTime =  random.uniform(options.ITI_meanDisplayTime - options.ITI_minMaxDisplayTime,options.ITI_meanDisplayTime + options.ITI_minMaxDisplayTime)
	
	cross.setPosition(xPos,yPos)
	
	ITI_bg.addAction(vizact.fadeTo(1))
	fullscreenText_bg.hide()	# remove fullscreen text if present
	
	writeLog(['Displaying ITI at position',xPos,yPos,'time',waitTime])
	cross.visible(True)
	
	yield viztask.waitTime(waitTime)
	
	cross.visible(False)

def toggleVE(state):
	
	if state == 'on':
		city.visible(True)
		sky.visible(True)
		for ground in groundPlane:
			ground.visible(True)
		
		for cBall in streetSpheres:
			cBall.visible(True)
	
	elif state == ('off'):
		city.visible(False)
		sky.visible(False)
		for ground in groundPlane:
			ground.visible(False)
		
		for cBall in streetSpheres:
			cBall.visible(False)
def fadeFog(state):

	if state == 'in':
		if fog.wasFadedIn == False:
			writeLog('Fog starts to fade in')
		
			# fade sky in
			for x in [x * 0.05 for x in range(0, 21)]:
				sky.texblend(1-x)
				yield viztask.waitTime(viz.getFrameElapsed())
			
			fog.fadeIn()	# fade fog in

			yield fog.doneFading.wait()	# wait for fog to finish
			writeLog('Fog faded in completely')
	
	elif state == 'out':
		if fog.wasFadedIn == True:
			writeLog('Fog starts to fade out')
			
			def executeFadeOut():
				
				def fadeSkyIn():
					for x in [x * 0.05 for x in range(0, 21)]:
						sky.texblend(x)
						yield viztask.waitTime(viz.getFrameElapsed())
				
				viztask.schedule(fadeSkyIn())
				fog.fadeOut()
			
			executeFadeOut()
			
			yield fog.doneFading.wait()
			writeLog('Fog faded out completely')
			fog.off()
			sky.visible(viz.ON)
	
	elif state == 'on':
		sky.texblend(0)
		fog.on()

def displayIntroScreen(phase):
	
	fullscreenText_bg.hide() # hide any text that might still be displayed
	
	writeLog('Start displaying intro screen')
	## #continue with button press' message
	introScreenText_continue.message(procedualText['introContinue'])
	
	# reposition panel to the middle of the screen and reapply settings for fontsize
	introScreenText.positionPanel([0,0,0])
	introScreenText.setFontsize(options.fontS_introScreen*options.reduceScreenSize[0])
	
	## intro screen screens
	if phase == 'fam':
		for screenMessage in introText[0]:
			introScreenText.message(screenMessage)
			yield viztask.waitAny([waitButton])
			introScreenText.removeText()

	elif phase == 'prac':
		
		introScreenText_continue.message(procedualText['introContinue'])
		
		### display first page
		introScreenText.message(introText[1][0])
		yield viztask.waitAny([waitButton])
		introScreenText.removeText()
		
		### display second text with images
		# experimental images
		targets_exp[0].visible(True)
		targets_exp[0].setScale([options.scale_introImages[0]*options.reduceScreenSize[0],options.scale_introImages[1]*options.reduceScreenSize[1],1])
		targets_exp[1].visible(True)
		targets_exp[1].setScale([options.scale_introImages[0]*options.reduceScreenSize[0],options.scale_introImages[1]*options.reduceScreenSize[1],1])
		
		intro_imageL.addImage(targets_exp[0])
		intro_imageL_text.message(procedualText['targetText'][0][0])
		intro_imageC.addImage(targets_exp[1])
		intro_imageC_text.message(procedualText['targetText'][1][0])
		
		# control image
		ctrlCueImage.visible(True)
		ctrlCueImage.setScale([options.scale_introImages[0]*options.reduceScreenSize[0],options.scale_introImages[1]*options.reduceScreenSize[1],1])
		intro_imageR.addImage(ctrlCueImage)
		intro_imageR_text.message(procedualText['targetText'][2][0])
		
		yield viztask.waitAny([waitButton])
		
		# hide images and text
		targets_exp[0].visible(False)
		targets_exp[1].visible(False)
		ctrlCueImage.visible(False)
		
		intro_imageL.removeItems(), intro_imageL.hide()
		intro_imageC.removeItems(), intro_imageC.hide()
		intro_imageR.removeItems(), intro_imageR.hide()
		
		intro_imageL_text.hide()
		intro_imageC_text.hide()
		intro_imageR_text.hide()
		
		# rescale all the images
		targets_exp[0].setScale([options.scale_centerImage[0]*options.reduceScreenSize[0],options.scale_centerImage[1]*options.reduceScreenSize[1],1])
		targets_exp[1].setScale([options.scale_centerImage[0]*options.reduceScreenSize[0],options.scale_centerImage[1]*options.reduceScreenSize[1],1])
		ctrlCueImage.setScale([options.scale_centerImage[0]*options.reduceScreenSize[0],options.scale_centerImage[1]*options.reduceScreenSize[1],1])
		
		
		### display third text
		
		introScreenText.message(introText[1][1])
		yield viztask.waitAny([waitButton])
	
	elif phase == 'test':
		
		introScreenText.message(introText[3])
		yield viztask.waitAny([waitButton])
		introScreenText.removeText()

	writeLog('End displaying intro screen')

	
def posLogger():
	
	curPos = view.getPosition()
	curAngle_uncorr = view.getEuler()
	
	curAngle = convertAngles.toMath(curAngle_uncorr[0])
	
	curJoyPos = joystick.getPosition()
	
	writeToFile(['POSITION',logTime.delta(),'{:0.3f}'.format(curPos[0]),'{:0.3f}'.format(curPos[1]),'{:0.3f}'.format(curPos[2]),'{:0.3f}'.format(curAngle),
	'{:0.3f}'.format(curJoyPos[0]),'{:0.3f}'.format(-curJoyPos[1])],logFileName)

# write log events

def writeLog(text, fileName = logFileName):
	
	writeToFile(['EVENT',logTime.delta(),text],fileName)
	
	if options.debug == 1:
		print('EVENT\t' + logTime.delta() + '\t' +  str(text) )

def registerKey(key):
	
	if key == options.pauseKey:
		writeLog('Simulation paused')
		viz.pause()
		
	if key == options.playKey:
		writeLog('Simulation continued')
		viz.play()

	if options.debug == 0:
		
		if key == options.pulseKey:
			writeLog('MR pulse')
		elif key ==	options.screenPositionKeyMap['right']:
			windowPosition[0] += 50 
			viz.window.setFullscreenRectangle([windowPosition[0],windowPosition[1],windowSize[0],windowSize[1]])
			screenFile = open('screenPosition.txt','w')
			screenFile.write(str(windowPosition[0]) + '\t' + str(windowPosition[1]))
			screenFile.close()
		elif key ==	options.screenPositionKeyMap['left']:
			windowPosition[0] -= 50 
			viz.window.setFullscreenRectangle([windowPosition[0],windowPosition[1],windowSize[0],windowSize[1]])	
			screenFile = open('screenPosition.txt','w')
			screenFile.write(str(windowPosition[0]) + '\t' + str(windowPosition[1]))
			screenFile.close()
		elif key ==	options.screenPositionKeyMap['up']:
			windowPosition[1] -= 50 
			viz.window.setFullscreenRectangle([windowPosition[0],windowPosition[1],windowSize[0],windowSize[1]])
			screenFile = open('screenPosition.txt','w')
			screenFile.write(str(windowPosition[0]) + '\t' + str(windowPosition[1]))
			screenFile.close()
		elif key ==	options.screenPositionKeyMap['down']:
			windowPosition[1] += 50 
			viz.window.setFullscreenRectangle([windowPosition[0],windowPosition[1],windowSize[0],windowSize[1]])	
			screenFile = open('screenPosition.txt','w')
			screenFile.write(str(windowPosition[0]) + '\t' + str(windowPosition[1]))
			screenFile.close()
		else:
			pass

viztask.schedule(main())		# jump into trial

flipImage(options.mirrorImage)

viz.callback(viz.KEYDOWN_EVENT,registerKey) # register button press

# ------------
# Start window
# ------------

if options.debug == 1:
	viz.window.setFullscreenMonitor(options.fullscreenMonitor)	# display only on first (1) monitor
	viz.go(SCREEN)
	viz.mouse.setScale(8, 1) 		# mouse speed
	sensorManager.setDebug(viz.ON) 		# show sensor areas
else:
	viz.mouse.setOverride(viz.ON)
	viz.mouse.setVisible(viz.OFF)
	if len(viz.window.getMonitorList()) > 1:
		viz.window.setFullscreenMonitor(options.fullscreenMonitor)	# display only on first (1) monitor
	else:
		viz.window.setFullscreenMonitor(1)
		
	if options.fullscreen == True:
		viz.go(viz.FULLSCREEN)
	elif options.fullscreen == False:
		viz.window.setFullscreenRectangle([options.windowPosition[0],options.windowPosition[1],options.windowSize[0],options.windowSize[1]])
		viz.go(viz.FULLSCREEN)
	sensorManager.setDebug(viz.OFF) 		# hide sensor areas
