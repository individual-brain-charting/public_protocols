# -*- coding: utf-8 -*-

# ----------------------------------------------------------
# SLT_DCM - fMRI MAIN
# 
# Preamble
#
#
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
import csv
from csv_io import write_to_csv as writeToFile

# Record buttonz
vizact.onkeydown('k', viz.window.startRecording, 'video_annotations.avi')
vizact.onkeydown('l', viz.window.stopRecording)

viz.setOption('viz.AVIRecorder.maxWidth', '1920')
viz.setOption('viz.AVIRecorder.maxHeight', '1080')

# ------------
# Start window
# ------------

if options.debug == 1:
	viz.window.setFullscreenMonitor(options.fullscreenMonitor)	# display only on first (1) monitor
	viz.go(viz.FULLSCREEN)
	viz.mouse.setScale(8, 1) 		# mouse speed
	sensorManager.setDebug(viz.ON) 		# show sensor areas
	
	screenSize = viz.window.getMonitorList()[options.fullscreenMonitor].size
	aspectRatio = screenSize[0]/screenSize[1]	# aspect ratio
	viz.fov(options.fov, aspectRatio)					# set field of view 
	
else:
	viz.mouse.setOverride(viz.ON)
	viz.mouse.setVisible(viz.OFF)
	
	if len(viz.window.getMonitorList()) > 1:
		viz.window.setFullscreenMonitor(options.fullscreenMonitor + 1)	# display only on first (1) monitor
		screenSize = viz.window.getMonitorList()[options.fullscreenMonitor].size
	else:
		viz.window.setFullscreenMonitor(1)
		screenSize = viz.window.getMonitorList()[0].size
	if options.fullscreen == True:
		
		# add subwindow -> in 3T MRI not the whole screen is visible
		aspectRatio = screenSize[0]/screenSize[1]				# aspect ratio
		viz.fov(60, aspectRatio)								# set field of view 
		view = viz.MainView
		
		xcorr = ((1 - options.subWindowSize)/2) * screenSize[0]	# value that needs to be applied to all text field in order to center them to the middle of the screen again
		ycorr = ((1 - options.subWindowSize)/2) * screenSize[1]	# value that needs to be applied to all text field in order to center them to the middle of the screen again
		
		subWindow = viz.addWindow()
		##Position the sub-window.
		subWindow.setSize([options.subWindowSize, options.subWindowSize])
		subWindow.setPosition([options.subWindowPosition[0], options.subWindowPosition[1]])
		subWindow.fov(options.fov, aspectRatio)
		subWindow.setView(view)
		covermainQuad = viz.addTexQuad(parent=viz.ORTHO, scale=[2000.0]*3,color=viz.BLACK, alpha=1)
		
		#covermainQuad.color(viz.BLACK)
		#covermainQuad.setParent(view)
		#covermainQuad.visible(True)
		covermainQuad.alignment(viz.ALIGN_LEFT_BOTTOM)
		#covermainQuad.drawOrder(9)
		viz.link(viz.MainWindow.WindowSize, covermainQuad)
		
		viz.go(viz.FULLSCREEN)
		
	elif options.fullscreen == False:
		viz.window.setFullscreenRectangle([options.windowPosition[0],options.windowPosition[1],options.windowSize[0],options.windowSize[1]])
		viz.go(viz.FULLSCREEN)
	sensorManager.setDebug(viz.OFF) 		# hide sensor areas
	
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
	waitButton = viztask.waitKeyDown(options.buttonMap_buttonBox['enter'])			# button used for user input
	waitButtonText = viztask.waitKeyDown(options.buttonMap_buttonBox['enter'])		# if text is displayed on the screen and the subject makes a button press, it should disapper (avoid duplicate text on screen)

## init input variables
sNr = [] 
sInitials = []
sGender = []
sAge = []
runstart = []

## movement
# for practice and test phase
move_rot = vizact.ontimer(0,updateMovement,inputDevice = options.movementInput, buttonMap = options.buttonMap_buttonBox, trans = 0) 	# only rotational movement
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

introScreenText = displayInfo(window = subWindow, mode = 'fullscreen',fontSize = options.fontS_introScreen * options.reduceScreenSize[0], textAlignment = viz.ALIGN_LEFT_BOTTOM)	# fullscreen text for introduction text
introScreenText_continue = displayInfo(subWindow, mode = 'fit', fontSize = options.fontS_introScreen_continue * options.reduceScreenSize[0],border = False,background = False, textAlignment = viz.ALIGN_CENTER_BOTTOM) 	# continue with button text on bottom of intro page
introScreenText_continue.positionPanel([-xcorr,options.offset_intro_continue[1] - ycorr,0])

fullscreenText_bg = displayInfo(window = subWindow, mode = 'fullscreen',fontSize = options.fontS_fullscreen * options.reduceScreenSize[0],background = True, border = False)	# fullscreen text with background
fullscreenText_bg.positionPanel([-xcorr,-ycorr,0])

# text for additional information during practice
practiceText = displayInfo(window = subWindow, mode = 'fit', fontSize = options.fontS_introScreen * options.reduceScreenSize[0],border = False,background = True,  textAlignment = viz.ALIGN_LEFT_BOTTOM) 
practiceText.setTextColor(viz.BLACK)
practiceText.setFontsize(36)
viz.link(viz.CenterCenter,practiceText.panel,offset = (-xcorr,-200 - ycorr/2,0)) 

## image placeholders
imageC = displayInfo(window = subWindow,mode = 'fullscreen',border = True, background = False)
imageC.positionPanel([options.imagePosition_cue[0] - xcorr, options.imagePosition_cue[1] - ycorr/2 ,0])

intro_imageL = displayInfo(window = subWindow,mode = 'fullscreen',border = False)
intro_imageL.positionPanel([options.imagePosition_introL[0]*options.reduceScreenSize[0] - xcorr + 80,options.imagePosition_introL[1]*options.reduceScreenSize[1] - ycorr,0])

intro_imageC = displayInfo(window = subWindow,mode = 'fullscreen',border = False)
intro_imageC.positionPanel([options.imagePosition_introC[0]*options.reduceScreenSize[0] - xcorr,options.imagePosition_introC[1]*options.reduceScreenSize[1] - ycorr,0])

intro_imageR = displayInfo(window = subWindow,mode = 'fullscreen',border = False)
intro_imageR.positionPanel([options.imagePosition_introR[0]*options.reduceScreenSize[0] - xcorr - 80,options.imagePosition_introR[1]*options.reduceScreenSize[1] - ycorr,0])

intro_imageL_text = displayInfo(window = subWindow,mode = 'fit', fontSize = options.fontS_introImage * options.reduceScreenSize[0],border = False,background = False,textAlignment = viz.ALIGN_CENTER_BOTTOM)
intro_imageL_text.positionPanel([options.imagePosition_introL[0]*options.reduceScreenSize[0] - xcorr + 80,options.imagePosition_introL[1]*options.reduceScreenSize[1]-220 - ycorr,0]) 

intro_imageC_text = displayInfo(window = subWindow,mode = 'fit', fontSize = options.fontS_introImage * options.reduceScreenSize[0],border = False,background = False,textAlignment = viz.ALIGN_CENTER_BOTTOM) 
intro_imageC_text.positionPanel([options.imagePosition_introC[0]*options.reduceScreenSize[0] - xcorr,options.imagePosition_introC[1]*options.reduceScreenSize[1]-220 - ycorr,0]) 

intro_imageR_text = displayInfo(window = subWindow,mode = 'fit', fontSize = options.fontS_introImage * options.reduceScreenSize[0],border = False,background = False,textAlignment = viz.ALIGN_CENTER_BOTTOM) 
intro_imageR_text.positionPanel([options.imagePosition_introR[0]*options.reduceScreenSize[0] - xcorr - 80,options.imagePosition_introR[1]*options.reduceScreenSize[1]-235 - ycorr,0]) 

# --------------
# Input & Output
# --------------

# input subject related data
if options.debug == 0:
	while type(sNr) != int:
		sNr = viz.input(' Subject number')
		
# input desired start run
run_n = len(sequence_exp + sequence_ctrl) // (options.numExpTrials + options.numCtrlTrials) # Get number of runs using the total number of trials and len of the conditions
print(run_n)
if options.debug == 0:
	while (type(runstart) != int) & (runstart not in range(run_n)): # Make sure the input is an int an also within the accepted number of runs
		runstart = viz.input(' Desired starting run')
		
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
	
seqFilePath = os.path.join(path, 'sequences')
if not os.path.exists(seqFilePath):
	os.mkdir(seqFilePath)
#logFilePath = vizinput.directory(prompt='Select a folder to save the log files.')

log_sNr = "{:02d}".format(sNr)

if options.debug == 0:
	logFileName = logFilePath + '/Subject_'+ log_sNr + '_start_run_' + str(runstart) + '_main.csv'	# file name for general log file (saves every information)
	optionsFileName = logFilePath + '/Subject_'+ log_sNr + '_start_run_' + str(runstart) + '_main_options.csv'	# file name for options file (saves only options)
	expFileName = logFilePath + '/Subject_'+ log_sNr + '_start_run_' + str(runstart) + '_main_experimentalData.csv'	# file name for log file (saves extra data during experimental phase)
	expSeqFileName = seqFilePath + '/Subject_'+ log_sNr + '_exp_sequence.csv'
	ctrlSeqFileName = seqFilePath + '/Subject_'+ log_sNr + '_ctrl_sequence.csv'
else:
	logFileName = logFilePath + '/debug_' + fileDate + '_' + fileTime + '.csv'	# file name for log file
	optionsFileName = logFilePath + '/debug_' + fileDate + '_' + fileTime + '_options' +  '.csv'	# file name for options file
	expFileName = logFilePath + '/debug_'+ log_sNr + '_' + fileDate + '_' + fileTime + '_experimentalData.csv'	# file name for log file (saves extra data during experimental phase)

# save options into csv file
for option in sorted(optionsDict):
	
	if option != 'optionsDict':
		writeToFile([option, optionsDict[option]],optionsFileName)
		
# store or load trial sequence:
if not os.path.exists(expSeqFileName):
	with open(expSeqFileName, 'w') as file:
		wr = csv.writer(file, dialect='excel')
		wr.writerows(sequence_exp)
	with open(ctrlSeqFileName, 'w') as file:
		wr = csv.writer(file, dialect='excel')
		wr.writerows(sequence_ctrl)
else:
	with open(expSeqFileName, 'r') as file:
		sequence_exp = [list(map(int, rec)) for rec in csv.reader(file, delimiter=',')]
	with open(ctrlSeqFileName, 'r') as file:
		sequence_ctrl = [list(map(int, rec)) for rec in csv.reader(file, delimiter=',')]	

if options.debug == 0:
	# write subject information to log file
	writeToFile(['Number',sNr],logFileName)
	writeToFile(['Initials',sInitials],logFileName)
	writeToFile(['Gender',sGender],logFileName)
	writeToFile(['Age',sAge],logFileName)

# write header for following rows
writeToFile(['Data type','Time','sPos (x)','sPos (y)',' sPos(z)','View Angle','jPos (x)', 'jPos (z)'],logFileName)

# write header for experimental log file
writeToFile(['Trial','Condition', 'Location', 'Direction', 'Target', 'Response_Angle', 'Right_Angle', 'Error_Angle', 'Accuracy', 'Travel_Onset', 'Crosshair_Onset', 'Response_Time', 'RT', 'ITI_Onset', 'ITI_Duration'], expFileName)


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
	
	# hide street spheres from familiarisation phase
	for cBall in streetSpheres:
		cBall.visible(0)
	
	viz.collision(viz.OFF)		# disable collision for further parts
	
	yield practice()		# practice phase

	yield test()			# test phase

	# end experiment
	logTimer.setEnabled(0)
	
	fullscreenText_bg.message(procedualText['expEnd'],fade = options.textFadeTime)
	
	yield viztask.waitTime(10)
	 
	viz.quit()
	
def practice():
	global runstart
	if runstart == 0:
		yield fadeFog('on')						# turn on fog for whole practice phase
		
		writeLog('Practice started')
		
		yield displayIntroScreen('prac')		# intro screen
		
		for i,trial in enumerate(options.sequence_practice_main):		# for loop that iterates over all of the trial in the practice sequence
			
			writeLog(['Starting trial',trial])
			
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
			
			yield displayCue(target,trial[3],'on')	# show according cue		
			
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
			
			# wait for subject to make response or time out
			waitCond = yield viztask.waitAny([waitButton,viztask.waitTime(options.pointingTime)])
			
			writeLog('Subject pressed button to indicate goal location')
			
			yield displayCue(target,trial[3],'off')		# hide according cue
			
			practiceText.hide()							# hide additional text
			crosshairImage.visible(False)				# hide crosshair
			writeLog('Crosshair hidden')
			
			# disable movement
			move_rot.setEnabled(0)
			writeLog('Movement disabled')
			
			# subject pressed button during pointing time
			if hasattr(waitCond.data, 'key'):
				writeLog('Subject pressed button to indicate goal location')
			else: 
				writeLog('Missing response from subject')
				responseTime = 'None'
				fullscreenText_bg.message(procedualText['missedPointing'])
				yield viztask.waitTime(options.textDisplayTime)
			
				fullscreenText_bg.removeText()
			
			calcAngleError(target,intersections[inters].position[0], intersections[inters].position[2])	# calculate error for indicated target location
			
			if trial[3] == 'ctrl':
				target.color([1,1,1])	# re-color target house 
			
			yield displayITI()			# display ITIs
		
		fullscreenText_bg.message(procedualText['partEnded'],fade = options.textFadeTime)
		yield viztask.waitTime(3)
		writeLog('Practice ended')
	else:
		pass
	
def test():
	
	global runstart
	writeLog('Test started')
	
	yield displayIntroScreen('test')		# intro screen
	len_exp = options.numExpTrials
	len_ctrl = options.numCtrlTrials
	len_block = len_exp + len_ctrl
	
	if options.ctrlCondition:
		# write sequences to log file
		writeLog(['Experimental sequence loaded', str(sequence_exp)])
		writeLog(['Control sequence loaded', str(sequence_ctrl)])
		
		# counters
		totalCount = 0 + (len_block * runstart)			# to keep track of total (overall) progression of the experiment
		expCount = 0 + (len_exp * runstart)			    # to keep track of experimental trials
		ctrlCount = 0 + (len_ctrl * runstart)			# to keep track of control trials
		
		expCount_block = 0		# to keep track of each block of experimental trials
		ctrlCount_block = 0		# to keep track of each block of control trials
		
		if runstart != 0:       # when starting from middle runs, fill the block to start from feedback phase
			expCount_block += len_exp
			ctrlCount_block += len_ctrl
			
		fdbck_idx = 0 + runstart  # to keep track of feedback nr.
		
		while totalCount < len(sequence_exp + sequence_ctrl):
			
			# start experimental trials
			while expCount_block < options.numExpTrials:
				
				yield experimentalTrial(expCount)	# jump into experimental trial
				
				expCount += 1
				expCount_block += 1
			
			# start control trials
			while ctrlCount_block < options.numCtrlTrials:
				
				yield controlTrial(ctrlCount)		# jump into control trial
				
				ctrlCount += 1
				ctrlCount_block += 1 
				
			# add trials at the end of the block, except if started from middle block
			if runstart == 0: # when runstart is not 0, we already added the numbers corresponding to the last block
				totalCount += options.numExpTrials + options.numCtrlTrials
			
			# if pause is wanted, introduce a short pause
			if (totalCount in options.pauseTrials) & (runstart == 0): # to avoid starting with a pause when starting from middle runs
				
				fullscreenText_bg.message(procedualText['pauseText'])
				
				yield viztask.waitTime(3)			# prevent accidental button press, force pause to 3 seconds
				
				print('Waiting for button c to continue...')
				yield viztask.waitKeyDown('c')
				
				print('Waiting for MR trigger...')
				yield viztask.waitKeyDown(options.pulseKey)
				writeLog(['Onset'])
			
			## feedback phase ------------
			if totalCount < len(sequence_exp + sequence_ctrl):
				fb_target = options.fbSequence[fdbck_idx][0]
				fb_direction = options.fbSequence[fdbck_idx][1]
				
				# get the right path that is to be travelled
				if fb_direction == 'cw':
					travelPath = getTravelPath(target = options.fbSequence[fdbck_idx][0], targetPath = options.targetPaths[fb_target][0], direction = options.fbSequence[fdbck_idx][1])	
				else:
					travelPath = getTravelPath(target = options.fbSequence[fdbck_idx][0], targetPath = options.targetPaths[fb_target][1], direction = options.fbSequence[fdbck_idx][1])
				
				writeLog(['Feedback phase','path',str(travelPath)],logFileName)
				
				fullscreenText_bg.message(' ')
				ITI_bg.addAction(vizact.fadeTo(0))	# hide ITI from previous trial
				
				writeLog(['Setting position to start of feedback path'],logFileName)
				view.setPosition((travelPath[0][0][0], options.eyeLvl + travelPath[0][0][1], travelPath[0][0][2]))	# move subject to start point of travel path
				
				writeLog(['Spin to first point of feedback path'],logFileName)
				yield viztask.addAction(view, vizact.spinTo(point = [targets_exp[fb_target].position[0], options.eyeLvl, targets_exp[fb_target].position[1]], time = .001))	# rotate to target
				
				yield viztask.waitTime(2)
				
				fullscreenText_bg.hide(fade = options.textFadeTime)
				
				yield fadeFog('out')
				
				writeLog('Moving subject through city')
				
				yield moveThroughVR(travelPath,fb_direction)
				
				yield viztask.waitTime(options.waitTime_feedbackTarget)		# let subject look at target after feedback phase
				
				writeLog('Movement along path ended')
				
				fullscreenText_bg.message(' ') 
				
				fdbck_idx += 1

			expCount_block, ctrlCount_block = 0,0	# reset block counters
			runstart = 0                            # reset normal behavior
	
	
	writeLog('Test ended')
	
# -----------------------------------------
# Resource Functions & Classes
# -----------------------------------------

def experimentalTrial(seqPos):
	
	global globalTrialNr
	
	yield fadeFog('on')	# turn on fog for travel and pointing phase
	
	# get current trial (intersection, starting point, target)
	trial = sequence_exp[seqPos]	
	inters = trial[0]
	sP = trial[1]
	targetNr = trial[2]
	
	target = targets_exp[trial[2]]	# additionally get object of current target
	
	writeLog(['Starting experimental trial',str(trial)])
	
	## travel phase ------------
	# move to start position and rotate to view the intersection center
	writeLog(['Setting viewpoint position to', str(intersections[inters].startPoints[sP])])
	view.setPosition([intersections[inters].startPoints[sP][0],options. eyeLvl + intersections[inters].startPoints[sP][1] ,intersections[inters].startPoints[sP][2]])	
	writeLog('Rotating to intersection center')
	yield viztask.addAction(view, vizact.spinTo(point = [intersections[inters].position[0], options.eyeLvl + intersections[inters].position[1] , intersections[inters].position[2]] ,time = .01,interpolate = vizact.linear))
	
	yield displayCue(target,'exp','on')	# show according cue				
	
	# move subject to the middle of the intersection
	writeLog(['Moving subject to center of intersection',str(intersections[inters].position)])
	moveOnset = logTime.delta()
	yield viztask.addAction(view, vizact.moveTo(pos = [intersections[inters].position[0], options.eyeLvl + intersections[inters].position[1] , intersections[inters].position[2]], time = options.travelTime_intersection))
	writeLog('Movement ended')
	
	# short jittered wait phase
	sT = round(random.uniform(.5,1.5),3)
	writeLog(['Short wait time', str(sT)])
	yield viztask.waitTime(sT)
	writeLog(['Short wait time ended'])
	
	## pointing phase ------------
	# enable movement
	move_rot.setEnabled(1)
	writeLog('Movement enabled')
	
	# start pointing phase
	crosshairImage.visible(True)
	writeLog('Crosshair displayed')
	eventTime = logTime.delta()

	# wait for subject to make response or time out
	waitCond = yield viztask.waitAny([waitButton,viztask.waitTime(options.pointingTime)])
	
	responseTime = logTime.delta()
	
	yield displayCue(target,'exp','off')	# hide according cue		

	crosshairImage.visible(False)
	writeLog('Crosshair hidden')
	
	# disable movement
	move_rot.setEnabled(0)
	writeLog('Movement disabled')

	# subject pressed button during pointing time
	if hasattr(waitCond.data, 'key'):
		writeLog('Subject pressed button to indicate goal location')
	else: 
		writeLog('Missing response from subject')
		responseTime = 'None'
		fullscreenText_bg.message(procedualText['missedPointing'])
		yield viztask.waitTime(options.textDisplayTime)
		
		fullscreenText_bg.removeText()
	
	# calculate error for indicated target location
	pointingResult = calcAngleError(target,intersections[inters].position[0], intersections[inters].position[2])	

	# write trial information into seperate file
	
	if responseTime != 'None':
		eventResponseDiff = '{:.6f}'.format(float(responseTime) - float(eventTime))
	else:
		eventResponseDiff = 'None'

	# display ITI (here displayITI function is not used so that the entry into the experimental log file is easier)
	xPos = random.uniform(options.ITI_rx[0],options.ITI_rx[1])
	yPos = random.uniform(options.ITI_ry[0],options.ITI_ry[1])
	
	waitTime =  random.uniform(options.ITI_meanDisplayTime - options.ITI_minMaxDisplayTime,options.ITI_meanDisplayTime + options.ITI_minMaxDisplayTime)
	
	cross.setPosition(xPos,yPos)
	
	ITI_bg.addAction(vizact.fadeTo(1))
	fullscreenText_bg.hide()	# remove fullscreen text if present
	
	writeLog(['Displaying ITI at position',xPos,yPos,'time',waitTime])
	cross.visible(True)
	
	ITI_onset = logTime.delta()
	yield viztask.waitTime(waitTime)
	
	cross.visible(False)
	
	
	# write information about trial into log file
	writeToFile([str(globalTrialNr), '1', str(trial[0]), str(trial[1]), str(trial[2]), str(round(pointingResult[0],3)), str(round(pointingResult[1],3)), str(round(pointingResult[2],3)), 'None', moveOnset, eventTime, responseTime, eventResponseDiff, ITI_onset, '{:.6f}'.format(waitTime)],expFileName)
	
	globalTrialNr += 1
	
def controlTrial(seqPos):
	
	global globalTrialNr
	
	yield fadeFog('on')			# fade in fog for travel and pointing phase
	
	trial = sequence_ctrl[seqPos]	
	inters = trial[0]
	sP = trial[1]
	targetNr = trial[2]
	
	# get handle to the current target house of the current intersection (needed to change color of the correct house
	for house in targets_ctrl:
		if house.name == (str(trial[0]) + str(trial[2])):
			target = house
			target.color(options.ctrlHouseColor)	# color target house 
			break			
	
	writeLog(['Starting control trial',str(trial)])
	## travel phase ------------
	# move to start position and rotate to view the intersection center
	writeLog(['Setting viewpoint position to', str(intersections[inters].startPoints[sP])])
	view.setPosition([intersections[inters].startPoints[sP][0],options.eyeLvl + intersections[inters].startPoints[sP][1] ,intersections[inters].startPoints[sP][2]])	
	writeLog('Rotating to intersection center')
	yield viztask.addAction(view, vizact.spinTo(point = [intersections[inters].position[0], options.eyeLvl + intersections[inters].position[1] , intersections[inters].position[2]] ,time = .01,interpolate = vizact.linear))
	
	yield displayCue(target,'ctrl','on')	# show according cue
	
	# move subject to the middle of the intersection
	writeLog(['Moving subject to center of intersection',str(intersections[inters].position)])
	moveOnset = logTime.delta()
	yield viztask.addAction(view, vizact.moveTo(pos = [intersections[inters].position[0], options.eyeLvl + intersections[inters].position[1] , intersections[inters].position[2]], time = options.travelTime_intersection))
	writeLog('Movement ended')
	
	## pointing phase ------------
	
	# short jittered wait phase
	sT = round(random.uniform(.5,1.5),3)
	writeLog(['Short wait time', str(sT)])
	yield viztask.waitTime(sT)
	writeLog(['Short wait time ended'])
	
	# enable movement
	move_rot.setEnabled(1)
	writeLog('Movement enabled')
	
	# start pointing phase
	crosshairImage.visible(True)
	writeLog('Crosshair displayed')
	eventTime = logTime.delta()
	
	# wait for subject to make response or time out
	waitCond = yield viztask.waitAny([waitButton,viztask.waitTime(options.pointingTime)])
	
	yield displayCue(target,'ctrl','off')	# hide according cue	
	crosshairImage.visible(False)
	writeLog('Crosshair hidden')
	
	# disable movement
	move_rot.setEnabled(0)
	writeLog('Movement disabled')

	# subject pressed button during pointing time
	if hasattr(waitCond.data, 'key'):
		writeLog('Subject pressed button to indicate goal location')
		responseTime = logTime.delta()
	# pointing time ran out without button press
	else: 
		writeLog('Missing response from subject')
		responseTime = 'None'
		fullscreenText_bg.message(procedualText['missedPointing'])
		yield viztask.waitTime(options.textDisplayTime)
		fullscreenText_bg.hide()
	
	# calculate error for indicated target location
	pointingResult = calcAngleError(target,intersections[inters].position[0], intersections[inters].position[2])
	
	target.color([1,1,1])			# uncolor the target	
	
	if responseTime != 'None':
		eventResponseDiff = str(float(responseTime) - float(eventTime))
	else:
		eventResponseDiff = 'None'
	
	# f += 1

	# display ITI (here displayITI function is not used so that the entry into the experimental log file is easier)
	xPos = random.uniform(options.ITI_rx[0],options.ITI_rx[1])
	yPos = random.uniform(options.ITI_ry[0],options.ITI_ry[1])
	
	waitTime =  random.uniform(options.ITI_meanDisplayTime - options.ITI_minMaxDisplayTime,options.ITI_meanDisplayTime + options.ITI_minMaxDisplayTime)
	
	cross.setPosition(xPos,yPos)
	
	ITI_bg.addAction(vizact.fadeTo(1))
	fullscreenText_bg.hide()	# remove fullscreen text if present
	
	writeLog(['Displaying ITI at position',xPos,yPos,'time',waitTime])
	cross.visible(True)
	
	ITI_onset = logTime.delta()
	yield viztask.waitTime(waitTime)
	
	cross.visible(False)
	
	# write information about trial into log file
	writeToFile([str(globalTrialNr), '2', str(trial[0]), str(trial[1]), str(trial[2]), str(round(pointingResult[0],3)), str(round(pointingResult[1],3)), str(round(pointingResult[2],3)), str(pointingResult[3]), moveOnset, eventTime, responseTime, eventResponseDiff, ITI_onset, '{:.6f}'.format(waitTime)],expFileName)

def waitForPulse():
	
	print('Waiting for MR trigger...')
	MRpulses = 0	# private count variable for pulses from the scanner

	# if prepulses are wanted, wait for according number
	if options.prePulses > 0:
		while MRpulses < options.prePulses + 1 :
			yield viztask.waitKeyDown(options.pulseKey)
			MRpulses += 1
	# if no prepulses are desired, continue without them
	else:
		yield viztask.waitKeyDown(options.pulseKey)
	
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

def monitorDistanceToIntersections():

	while True:
		
		for curInters in intersections:
			dist = vizmat.Distance(viz.MainView.getPosition(),curInters.getPosition(viz.ABS_GLOBAL))
			
			if dist <= 20 and curInters.closedIn == False:
				writeLog(['User closing in on intersection', str(curInters.nr)])
				curInters.closedIn = True
			elif dist > 20 and curInters.closedIn == True:
				curInters.closedIn = False
				writeLog(['User moved away from intersection', str(curInters.nr)])
		
		yield viztask.waitTime(viz.getFrameElapsed())
	
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
			
			sphereCounter_text.message('Sie haben '+ str(sphereCount) + ' von 8 Bällen gefunden.')
			# check if all sensors have been activated, if so, send signal
			if len(exploredSensors) == len(streetSensors):
				writeLog('All sensors have been found')
				allSpheresFound.send()
	
def explorationTimer(time):
	
	writeLog('Exploration timer started')

	yield viztask.waitTime(time)
	
	timerExpired.send('timeout')	

def getTravelPath(target = [], targetPath = [], direction = []):
	
	path = []
	
	
	# targetPath is a nested list, each nested list will contain the path until a dead end is arrived (here, subject will turn around and a new path will start)
	
	# go through travelPath and create sub-paths until a dead end is arrived
	subPath = []	# create subPath (for first sub-path until first dead-end)
	
	for i,pointOnPath in enumerate(targetPath):
		
		# next point is intersection
		if pointOnPath[0] == 'i':
			subPath.append(intersections[int(pointOnPath[1])].position)
		
		# if next point is street
		else:
			# if street is in reversed order, reverse list order
			if pointOnPath[0] == '-':
				streetNr = pointOnPath[2:]
				subNodeList = reversed(streets[int(pointOnPath[2:])].subNodes)
			else:
				streetNr = pointOnPath[1:]
				subNodeList = streets[int(pointOnPath[1:])].subNodes
			
			# add nodes of current street to subPath
			for subNode in subNodeList:
				subPath.append(subNode)	
			
			# if the next street is the same as the current one -> dead end -> append subPath and create a new one
			# also, check if the next point on path is not intersection with the same nr (3rd condition)
			if i < len(targetPath)-1 and streetNr in targetPath[i+1] and 'i' not in targetPath[i+1]:
				path.append(subPath)
				subPath = []
			# if the last subPath is reached, append it to path	
			elif i == len(targetPath)-1:
				path.append(subPath)

	return path

def moveThroughVR(travelPath, direction = []):
	
	# in tour through city mode, travelPath is a nested list, each containing subPaths until a dead end is reached
	
	# rotate 45 degrees in cw or in ccw direction, depending on the current direction of the tour (cw - right, ccw - left)
	if direction == 'cw':
		yield viztask.addAction(view, vizact.spinTo(euler = view.getEuler()[0]+45, speed = options.rotationSpeed_feedback, interpolate = vizact.linear))
	elif direction == 'ccw':
		yield viztask.addAction(view, vizact.spinTo(euler = view.getEuler()[0]-45, speed = options.rotationSpeed_feedback, interpolate = vizact.linear))
	
	# start function that monitors distance to intersections
	distanceMonitor = viztask.schedule(monitorDistanceToIntersections())
	
	# rotate to first point on target pathyield viztask.addAction(view, vizact.spinTo(euler = view.getEuler()[0]-45, speed = options.rotationSpeed_feedback, interpolate = vizact.linear))
	yield viztask.addAction(view, vizact.spinTo(point = [travelPath[0][1][0],options.eyeLvl + travelPath[0][1][1], travelPath[0][2][2]], speed = options.rotationSpeed_feedback, interpolate = vizact.linear))
	
	for i,subPath in enumerate(travelPath):
		
		animationPath = viz.addAnimationPath()
		
		for nr, coord in enumerate(subPath):
			# do not rotate for first and interpolate in linear fashion
			if nr == 0 or nr == len(subPath)-1:
				cp = animationPath.addControlPoint(nr+1, pos = [coord[0],options.eyeLvl + coord[1], coord[2]])
				cp.setTranslateMode(viz.LINEAR)
			# for all other control points, rotate	
			else:
				cp = animationPath.addControlPoint(nr+1, pos = [coord[0],options.eyeLvl + coord[1], coord[2]], euler = vizmat.AngleToPoint([coord[0],coord[2]],[subPath[nr+1][0],subPath[nr+1][2]]) )
				cp.setTranslateMode(viz.LINEAR)
		
		animationPath.addEventAtEnd('end')
		animationPath.setConstantSpeed(viz.ON,options.travelSpeed_feedback)
		link = viz.link(animationPath,view)
		animationPath.play()
			
		yield viztask.waitPathEvent(animationPath, 'end')
		
		link.remove()
		
		# at the end of the subPath, rotate around to the next second position on the next subPath (the one leading out of the street)	
		if i < len(travelPath)-1:
			
			# rotate 45 degrees in cw or in ccw direction, depending on the current direction of the tour (cw - right, ccw - left)
			if direction == 'cw':
				yield viztask.addAction(view, vizact.spinTo(euler = view.getEuler()[0]+45, speed = options.rotationSpeed_feedback, interpolate = vizact.linear))
			elif direction == 'ccw':
				yield viztask.addAction(view, vizact.spinTo(euler = view.getEuler()[0]-45, speed = options.rotationSpeed_feedback, interpolate = vizact.linear))
			
			# rotate to next second position on next subPath
			yield viztask.addAction(view, vizact.spinTo(point = [travelPath[i+1][1][0],options.eyeLvl + travelPath[i+1][1][1], travelPath[i+1][1][2]], speed = options.rotationSpeed_feedback, interpolate = vizact.linear))

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
	introScreenText_continue.message(' ')
	
	writeLog('Start displaying intro screen')
	## #continue with button press' message
	if runstart == 0:
		introScreenText_continue.message(procedualText['introContinue'])
	
	# reposition panel to the middle of the screen and reapply settings for fontsize
	introScreenText.positionPanel([-xcorr,-ycorr,0])
	introScreenText.setFontsize(options.fontS_introScreen*options.reduceScreenSize[0])
	
	
	if phase == 'prac':
		
		introScreenText_continue.message(procedualText['introContinue'])
		
		### display first page
		introScreenText.message(introText[2])
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
#		introScreenText.message(introText[2])
#		yield viztask.waitAny([waitButton])
	
	elif phase == 'test':
		global runstart
		if runstart == 0:
			introScreenText_continue.message(' ')
			
			introScreenText.message(introText[3])
			
		else:
			yield controlTrial(0)
			fullscreenText_bg.message(procedualText['pauseText'])
			
		yield waitForPulse()
		writeLog(['Onset'])
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
			curPos = subWindow.getPosition()
			subWindow.setPosition(curPos[0] + 0.005, curPos[1])
		elif key ==	options.screenPositionKeyMap['left']:
			curPos = subWindow.getPosition()
			subWindow.setPosition(curPos[0] - 0.005, curPos[1])
		elif key ==	options.screenPositionKeyMap['up']:
			curPos = subWindow.getPosition()
			subWindow.setPosition(curPos[0], curPos[1] + 0.005)
		elif key ==	options.screenPositionKeyMap['down']:
			curPos = subWindow.getPosition()
			subWindow.setPosition(curPos[0], curPos[1] - 0.005)
		else:
			pass

viztask.schedule(main())		# jump into trial

flipImage(options.mirrorImage)

viz.callback(viz.KEYDOWN_EVENT,registerKey) # register button press
