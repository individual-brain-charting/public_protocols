from __future__ import division
import viz
import vizact
import vizjoy
import datetime
import viztask
import vizinput
import math
import sys
import os 

sys.path.insert(0,os.path.realpath('.\py'))
	
# --------------------------------------------------------------------------------------------------------
# Familiarisation options
# --------------------------------------------------------------------------------------------------------	
sensorPositions = [[-61.8,-31.8],[-23,-50.6],[41.5,-43.5],[57,-15.6],[54.3,39.6],[34.8,82.8],[-44,46.5],[-53,23.5]]	# position of the sensors at each street ending that detect whether this street has been explored or notsensorRadius = 1.2		# radius of the sensor surrounding the spheres
sphereRadius = 1		# radius of the spheresphereHeight = 1.5		# height of the spheres

# positioning
[startx,startz] = [-54,-32]		# start position
initialViewingDirection = 90	# initial viewing direction; 0=north, -90=west, 90=east, (-)180=south

# --------------------------------------------------------------------------------------------------------
# Practice options
# --------------------------------------------------------------------------------------------------------

'''
sequence used, encoded as follows: (intersection, direction,goal,'exp') for experimental trials; (intersection,direction,house,'ctrl') for control trials. 
house numbers are encoded in clockwise direction, starting with the lower left one (see overview.png for reference) 
note: you can add as many trials as you want in this list, the practice phase will change according to this
'''
sequence_practice_training = ((0,3,1,'exp'),(2,2,0,'exp'),(0,2,1,'ctrl'),(1,0,0,'exp'),(3,1,1,'exp'),(2,0,0,'ctrl'),(0,2,0,'exp'),(2,1,1,'exp'),(3,1,2,'ctrl'),(1,3,1,'exp'),(3,0,0,'exp'),(1,3,1,'ctrl'))  # practice sequence displayed outside of scanner; for fMRI as 3rd & 6th trial:(0,2,1,'ctrl'),/,(2,0,0,'ctrl')#sequence_practice_training = ((0,3,1,'exp'),(2,2,0,'exp'))  # practice sequence displayed outside of scannersequence_practice_main = ((0,3,1,'exp'),(2,2,0,'exp'),(0,2,1,'ctrl'),(1,0,0,'exp'),(3,1,1,'exp'),(2,0,0,'ctrl'))  # practice sequence displayed inside scanner; for fMRI as 3rd & 6th trial:(0,2,1,'ctrl'),/,(2,0,0,'ctrl')#sequence_practice_main = ((0,3,1,'exp'),(2,2,0,'exp'))  # practice sequence displayed inside scanner
interTrialTime = 2				# time that the script waits after a finished trialtutorialTrials = 6				# how many trials in practice phase with additional help?readTime = 4					# time in seconds the participant has to read small instructions during tutorial of practicestillTime = 2					# time in seconds the participant has to stay still until new text appears in first phase of practice trials

# --------------------------------------------------------------------------------------------------------
# Test options
# --------------------------------------------------------------------------------------------------------
# -----------------
# Positions & paths
# -----------------

# targets experimental
targetNames_exp = ['townHall','church']				# names of the target, must be identical to image names in ./images folder
targetPositions_exp = [[37.5,108],[-112.6,-34.876]]	# location of targets in m (x,y), corresponds to order in targetNames

'''
position of the streets, houses as well as intersections and their start points are loaded through loadRessources.py
'''
# feedback
# street paths for feedback [cw, ccw]
t0 = [['s7','i1','s6','-s6','i1','s5','i2','s4','-s4','i2','s3','-s3','i2','-s2','i3','s1','-s1','i3','-s0','s0','i3','-s11','i0','-s10','s10','i0','-s9','s9','i0','s8','i1','-s7'],
['s7','i1','-s8','i0','-s9','s9','i0','-s10','s10','i0','s11','i3','-s0','s0','i3','s1','-s1','i3','s2','i2','s3','-s3','i2','s4','-s4','i2','-s5','i1','s6','-s6','i1','-s7']]
t1 = [['s0','i3','-s11','i0','-s10','s10','i0','-s9','s9','i0','s8','i1','-s7','s7','i1','s6','-s6','i1','s5','i2','s4','-s4','i2','s3','-s3','i2','-s2','i3','s1','-s1','i3','-s0'],
['s0','i3','s1','-s1','i3','s2','i2','s3','-s3','i2','s4','-s4','i2','-s5','i1','s6','-s6','i1','-s7','s7','i1','-s8','i0','-s9','s9','i0','-s10','s10','i0','s11','i3','-s0']]
targetPaths = [t0, t1]
'''
sequence used in feedback mode 2 (travelling through the whole VR); first value is the target from which the movement starts
second value is the direction (cw - clockwise, ccw - counter-clockwise)
'''
fbSequence = [[0,'cw'],[1,'ccw'],[0,'ccw'],[1,'cw'],[0,'cw'],[1,'ccw'],[0,'ccw'],[1,'cw']]	additionalRandomisation = False		# should the directions be split in two halfs for the target?
# --------------------
# Experiment control
# --------------------

# general task related options
numExpTrials = 8				# number of experimental trials before switching to control trials
numCtrlTrials = 4				# number of control trials before switching to experimental trialspauseTrials = [12,24,36,48,     # number of trials (exp + ctrl) before a pause is introduced			   60,72,84,96]		
cueTime = 1						# number of seconds the cue is displayed
travelTime_intersection = 4		# time the viewpoint travels from starting position to center of intersection
pointingTime = 12				# time in seconds the subject has to point to target during pointing phase
ctrlCondition = True			# choose if control condition during test phase is enabled or not
# experimental condition specific
feedbackHeight = 20				# height in m of the viewpoint during feedback phase
travelTime_feedback = 5			# time in seconds for feedback phase duration
rotationSpeed_feedback = 40		# rotation speed in degrees/s during street path mode (1) of feedback phase
travelSpeed_feedback = 5 		# travel speed in m/s during street path mode of feedback phase
waitTime_feedbackTarget = 1.5	# time in seconds the subjects looks at the target after feedback phase
# control condition specific
ctrlHouseColor = [.168,.41,.74]	# color of house during control condition
errorTolerance = 25				# tolerance in pointing angle during control condition (positive and negative)

# --------------------------------------------------------------------------------------------------------
# General Options
# --------------------------------------------------------------------------------------------------------

debug = 0					# debug mode, 0 - disabled, 1- enable
fs = -1						# sampling rate in Hz for position, view angle & joystick logging. If fs = -1, fs will be identical to current framerate
pauseKey = 'p'				# key to pause the experiment
playKey = 'c'				# key to continue experiment

# MR-compatibility
pulseKey = 't'					# key that is passed from scanner to indicate MR pulse
prePulses = 0					# e.g. prePulses = 2 means: start at pulse 3, ignore the first 2, should not be needed at the PRISMA, which has 2 dummy scans without trigger

# --------------------------------------------------------------------------------------------------------
# Visual options
# --------------------------------------------------------------------------------------------------------
# ITI
ITI_meanDisplayTime = 3		# mean time in seconds the cross is displayed
ITI_minMaxDisplayTime = 2	# min and max deviation from mean display time if ITI (e.g. mean of 4 and min max of 1 -> 4s +- 1s)
ITI_crossSize = [1,1.2]		# arbitrary value of cross size (width, heigth)
ITI_bgColor = viz.GRAY		# color of background during ITIs
ITI_rx = [.5,.5]			# range of x-axis (vertical) in which position of cross is randomly positioned (in % of screen size)
ITI_ry = [.5,.5]			# range of y-axis (horizontal) in which position of cross is randomly positioned (in % of screen size)

# screen size and view properties
fullscreen = True			# display full screen image? (always disabled in debug)
windowSize = [1920,1080]	# base resolution for the window (i.e. native resolution of the screen)
reduceScreenSize = [1,1]	# initial option to reduce screen width and height to a certain % of the base resolution (minimum 0.1), NOTICE: if the values are not the same, the image will be cut off left and right to maintain aspect ratio
fov = 60					# vertical field of view of viewport
eyeLvl = 1.8				# height of viewport in m
fullscreenMonitor = 1		# which monitor is used to display fullscreen window? keep in mind: 0 = 1; 1 = 2!
screenPositionKeyMap = {'up':'i','down':'k','left':'j','right':'l'}	# key map to change screen position
mirrorImage = False			# mirror image along horizontal ('horizontal') or vertical ('vertical') axis, specify (False) if no mirroring is desired
# subWindow properties (if used, necessary e.g. for MRI, as not the whole screen is visible)subWindowSize = 1subWindowPosition = [(1 - subWindowSize)/2, 1]
# text display
textFadeTime = 0.5			# fade time between messages in s 
textDisplayTime = 3			# how long are misc. notifications displayed
# image scales
scale_centerImage = [2,2]			# image scale for images that are displayed in the center (cue images)
scale_crosshairImage = [1.5,1.8]	# image scale of crosshair, arbitrary value, depends on the size of the original image (to maintain aspect ration, the image must be of the same aspect ratio as screen size)
scale_introImages = [3,3]			# image scale for images in the introduction screens (e.g. practice phase)

# image positions
imagePosition_center = [.5,.5]			# relative x,y position of the center image (i.e. [.5,.5] is directly at the center)
imagePosition_crosshair = [.5,.5]		# relative x,y position of crosshair (i.e. [.5,.5] is directly at the center)
imagePosition_introL = [-550,150]			# offset from center in px for intro image
imagePosition_introC = [0,150]			# offset from center in px for intro image
imagePosition_introR = [550,150]			# offset from center in px for intro image		
imagePosition_cue = [0,-380]

# font sizes
fontS_fullscreen = 48				# font size for fullscreen messages, will be scaled by reduceScreenSize Factor 
fontS_fullscreen_goal = 60			# font size for fullscreen goal messages, will be scaled by reduceScreenSize Factor 
fontS_center = 36  					# font size for center messages, will be scaled by reduceScreenSize Factor 
fontS_introScreen = 34 				# font size for intro screen messages, will be scaled by reduceScreenSize Factor 
fontS_introScreen_continue = 38 	# font size for intro screen continue messages, will be scaled by reduceScreenSize Factor 
fontS_introImage = 38 				# font size for letter that appears on the lower left corner of the screen

textPadding = 10						# padding around text objects in px

# offsets
offset_center_score = [0,-75]		# x,y offset of center text in px, scaled by reduceScreenSize
offset_fullscreen_goal = [0,-100]	# x,y offset of fullscreen goal in px, scaled by reduceScreenSize
offset_intro_continue = [0,-300]	# x,y offset of intro continue in px, scaled by reduceScreenSize
offset_letter = [-400,-300]			# x,y offset of letter text, scaled by reduceScreenSize			
offset_introImages = [250,-30,0]	# x,y offset of images shown in intro screen, +- of x values are used accordingly, scaled by reduceScreenSize


## fog settings
fogColor = [.5,.5,.5]		# color of fog
startDist = 6				# start distance of linear increase
endDist = 15				# end distance, at which fog has reached maximum alpha
fadeOutDist = 150			# from which distance is the fog faded in
fogFadeTime = .8			# time it takes fog to fade in seconds


## viewport settings
view = viz.MainView					# variable for main view
viz.setMultiSample(8)				# FSAA 8x
view.collision(viz.ON)				# collision on
view.stepsize(0.3) 					# maximum allowed distance that the viewport may go up to step over object
view.collisionBuffer(1.0)			# minimum distance between objects and the viewport in m
viz.clip(0.1,1500)					# set minimum and maximum clipping distance in m (to avoid looking 'through' objects)
viz.vsync(1)						# enable vsync (syncs frame rate to refresh rate of monitor, avoids tearing)

# --------------------------------------------------------------------------------------------------------
# Movement options
# --------------------------------------------------------------------------------------------------------
movementInput = 'keyboard'		# 'joystick' or 'keyboard' are possible
buttonMap = {'left': '65361', 'right': '65363', 'forward': '65362', 'backward':'65364', 'enter': ' '}	# button map for keyboard input#buttonMap_buttonBox = {'left': '65361', 'right': '65363', 'enter': ' '}	# button map for keyboard inputbuttonMap_buttonBox =  {'left': 'y', 'right': 'g', 'enter': 'b'}	# button map for input when the response box from the scanner is used
joyButton = 1						# button of joystick that is to be used during trial
joyMode = 1							# 1 - rotation and forward/backward motion simultaneously, 2 - rotation and forward/backward motion separately	
keyboardMode = 1					# 1 - rotation and forward/backward motion simultaneously, 2 - rotation and forward/backward motion separately	
joyTranslationMode = 'dependent'	# decide, whether joystick translation (moving back/forward) is at a fixed speed ('fixed') or joystick position dependent ('dependent')
joyRotationMode = 'dependent'		# same as translation, only for rotation
invertRotation = False			# invert joystick axis for rotation (left/right) (for keyboard inverse movement, please change the wind map)
invertTranslation = False		# invert joystick axis for translation (forward/backward) (for keyboard inverse movement, please change the button map)

autoRotSpeed = 45				# rotation speed during automated turning in degrees/second
autoMovSpeed = 5				# movement speed in m/s for automated movement

joyMovSpeed = 5					# movement speed in m/s for manual movement, default 5
joyRotSpeed = 45				# rotation speed in degrees/second for manual movement

joyDeadzone = 0.35				# joystick deadzone in percent

# if joyMode = 2, different joystick positions, in which the movement in initiated, may be defined by specifying the according angles 
alphaTranslation = 80			# translation angle in degrees, is defined as +alphaTranslation/2 and -alphaTranslation/2 			
alphaRotation = 80				# rotation angle in degrees, is defined as +alphaRotation/2 and -alphaRotation/2 	

# --------------------------------------------------------------------------------------------------------
# Postprocessing
# --------------------------------------------------------------------------------------------------------
	
# define screen sizes and position

# get monitor props
monitors = viz.window.getMonitorList()	if len(viz.window.getMonitorList()) > 1:
	screenSize = monitors[fullscreenMonitor-1].sizeelse:	screenSize = monitors[0].size	
screenAspect = screenSize[0]/screenSize[1]

if fullscreen == False:
	windowSize[0],windowSize[1] = windowSize[0]*reduceScreenSize[0],windowSize[1]*reduceScreenSize[1]	# reduce window size if specified
	aspectRatio = windowSize[0]/windowSize[1]	# aspect ratio
	viz.fov(fov,aspectRatio)					# set field of view 
elif fullscreen == True:
	viz.fov(fov)

view.eyeheight(eyeLvl)							# height of viewport

if debug == 0 and fullscreen == False:	
	
	# ask user wether to input screen position or change it during experiment
	desiredScreenPosition = vizinput.choose('How do you want to define the position of the screen',['Center','Input coordinates','Use last used value'])

	if desiredScreenPosition == 0:
		screenFile = open('screenPosition.txt','w')
		windowPosition = [0 + screenSize[0]/2 - windowSize[0]/2, 0 + screenSize[1]/2 - windowSize[1]/2]
		screenFile.write(str(windowPosition[0]) + '\t' + str(windowPosition[1]))
		screenFile.close()
	elif desiredScreenPosition == 1:
		screenFile = open('screenPosition.txt','w')
		wx = int(viz.input('Please x position in px'))
		wy = int(viz.input('Please y position in px'))
		windowPosition = [wx,wy]
		screenFile.write(str(windowPosition[0]) + '\t' + str(windowPosition[1]))
		screenFile.close()
	elif desiredScreenPosition == 2:
		
		fileWindowPosition = []
		
		try:
			f = open('screenPosition.txt','r') # open file read only
		except:
			print('No screen size file found, please define first or use center!')
		
		for line in f:
			line = line.strip()
			fileWindowPosition.append(map(str, line.split('\t')))
		
		windowPosition = [float(fileWindowPosition[0][0]), float(fileWindowPosition[0][1])]

# summarize all local variables in an object
class storeOptions(object):
	
	def __init__(self):
		pass

options = storeOptions()	# create options object to store options 
optionsDict = {} 			# create options dictionary, to be able to write them into the header later
localVars = dict(locals())

# clean dictionary from imported modules and built-ins
for option in localVars:

	# exlude stuff starting with '_'
	if option[0] == '_':
		pass
	# options to keep
	elif isinstance(localVars[option],(int,list,str,float,bool,dict,tuple)):
		setattr(options,option,localVars[option])
		optionsDict[option] = localVars[option]
	# remaining stuff (e.g. loaded functions, imported modules)
	else:
		pass
