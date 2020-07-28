from __future__ import division
import viz
import vizjoy
import math
import sys
import os
import vizact
import viztask

sys.path.insert(0,os.path.realpath('..'))

from defineOptions import *

# joystick movement
joystick = vizjoy.add() # add joystick variable

if debug == 1:
	
	dot = viz.addTexture('dot.tif')
	up = viz.addTexture('button_up.tif')
	down = viz.addTexture('button_down.tif')
	
	# Add the texture quad for the joystick position
	joyTexture = viz.addTexQuad(viz.SCREEN)
	joyTexture.setScale([0.1,0.1,0.1])
	#Set the joystick texture to the dot
	joyTexture.texture(dot)

	# Create a border for the joystick position
	JOY_CENTER_X = 0.85
	JOY_CENTER_Y = 0.88
	JOY_SCALE =  10.0
	viz.startLayer(viz.LINE_LOOP)
	viz.vertexColor(viz.BLACK)
	viz.vertex([(JOY_CENTER_X-(1.1/JOY_SCALE)),(JOY_CENTER_Y+(1.1/JOY_SCALE)),0])
	viz.vertex([(JOY_CENTER_X+(1.1/JOY_SCALE)),(JOY_CENTER_Y+(1.1/JOY_SCALE)),0])
	viz.vertex([(JOY_CENTER_X+(1.1/JOY_SCALE)),(JOY_CENTER_Y-(1.1/JOY_SCALE)),0])
	viz.vertex([(JOY_CENTER_X-(1.1/JOY_SCALE)),(JOY_CENTER_Y-(1.1/JOY_SCALE)),0])
	viz.endLayer(viz.SCREEN)
	
	joyPositionText = viz.addText('',pos=[0.74, 0.975, 0],color = viz.BLACK,parent=viz.SCREEN,scale = [0.2,0.2,0.2])
	viewPositionText = viz.addText('',pos=[0.5, 0.975, 0],color = viz.BLACK,parent=viz.SCREEN,scale = [0.2,0.2,0.2])
	
def updateMovement(trans = 1, rot = 1,inputDevice = 'joystick', buttonMap = {'left': '65361', 'right': '65363', 'forward': '65362', 'backward':'65364', 'enter': ' '}):
	
	global joyMovSpeed
	
	# subject movement related
	[jx,jy,jz] = joystick.getPosition() # continously get joystick axis position
	[vx,vy,vz] = viz.MainView.getPosition()
	[vyaw,vpitch,vroll] = viz.MainView.getEuler()
	
	if debug == 1:
		joyTexture.setPosition(JOY_CENTER_X+(jx/10.0),JOY_CENTER_Y-(jy/10.0))
		joyPositionText.message('Joystick:\nx: ' + str(round(jx,3)) + ',y: ' + str(round(jy,3)))
		viewPositionText.message('View:\nx: ' + str(round(vx,3)) + ',y: ' + str(round(vz,3)) + ',yaw: ' + str(round(vyaw,3)))
		
	if inputDevice == 'joystick':
		
		try:
			# set variables for inverse movement
			if invertTranslation == True:
				it = -1
			elif invertRotation == False:
				it = 1
			if invertRotation == True:
				ir = -1
			elif invertRotation == False:
				ir = 1
		except NameError:
			it,ir = 1
		
		if joyMode == 1:
			
			if trans == 1:
				# translation in x
				if math.fabs(jy) > joyDeadzone: 
					
					if jy > 0:	# backward
						if joyTranslationMode == 'fixed':
							view.move(0,0,viz.getFrameElapsed()*-joyMovSpeed*it) 	# viz. elapsed() allows movement, as long as joystick axes are moved
						elif joyTranslationMode == 'dependent':
							view.move(0,0,viz.getFrameElapsed()*jy*-joyMovSpeed*it) 	# viz. elapsed() allows movement, as long as joystick axes are moved
					if jy < 0:	# forward
						if joyTranslationMode == 'fixed':
							view.move(0,0,viz.getFrameElapsed()*joyMovSpeed*it)
						elif joyTranslationMode == 'dependent':
							view.move(0,0,viz.getFrameElapsed()*-jy*joyMovSpeed*it)

			if rot == 1:
				# rotation with joystick dependent speed
				if  math.fabs(jx) > joyDeadzone:		# rotation
					
					if  jx < 0: 	# left
						if joyRotationMode == 'dependent':
							view.setEuler([joyRotSpeed*ir*jx*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
						elif joyRotationMode == 'fixed':
							view.setEuler([-joyRotSpeed*ir*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
					if  jx > 0:  	# right
						if joyRotationMode == 'dependent':
							view.setEuler([joyRotSpeed*ir*jx*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
						elif joyRotationMode == 'fixed':
							view.setEuler([joyRotSpeed*ir*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
		
		elif joyMode == 2:

			# calculate movement zones
				zoneX = (alphaTranslation/2)/45
				zoneY = (alphaRotation/2)/45
				
				# rotation and translation in x
				if trans and rot == 1:
					
					if math.fabs(jy) > joyDeadzone and -zoneX < jx < zoneX: 	# translation
						
						if jy > 0:	# backward
							if joyTranslationMode == 'fixed':
								view.move(0,0,viz.getFrameElapsed()*-joyMovSpeed*it) 	# viz. elapsed() allows movement, as long as joystick axes are moved
							elif joyTranslationMode == 'dependent':
								view.move(0,0,viz.getFrameElapsed()*jy*-joyMovSpeed*it) 	# viz. elapsed() allows movement, as long as joystick axes are moved
						if jy < 0:	# forward
							if joyTranslationMode == 'fixed':
								view.move(0,0,viz.getFrameElapsed()*joyMovSpeed*it)
							elif joyTranslationMode == 'dependent':
								view.move(0,0,viz.getFrameElapsed()*-jy*joyMovSpeed*it)
						
					elif math.fabs(jx) > joyDeadzone and -zoneY < jy < zoneY:	# rotation
						
						if  jx < 0: 	# left
							if joyRotationMode == 'dependent':
								view.setEuler([joyRotSpeed*ir*jx*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
							elif joyRotationMode == 'fixed':
								view.setEuler([-joyRotSpeed*ir*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
						if  jx > 0:  	# right
							if joyRotationMode == 'dependent':
								view.setEuler([joyRotSpeed*ir*jx*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
							elif joyRotationMode == 'fixed':
								view.setEuler([joyRotSpeed*ir*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
						
					else: 
						pass			# don't move
				
				if trans == 1 and rot == 0:
					
					if math.fabs(jy) > joyDeadzone and -zoneX < jx < zoneX: 	# translation
						
						if jy > 0:	# backward
							if joyTranslationMode == 'fixed':
								view.move(0,0,viz.getFrameElapsed()*-joyMovSpeed*it) 	# viz. elapsed() allows movement, as long as joystick axes are moved
							elif joyTranslationMode == 'dependent':
								view.move(0,0,viz.getFrameElapsed()*jy*-joyMovSpeed*it) 	# viz. elapsed() allows movement, as long as joystick axes are moved
						if jy < 0:	# forward
							if joyTranslationMode == 'fixed':
								view.move(0,0,viz.getFrameElapsed()*joyMovSpeed*it)
							elif joyTranslationMode == 'dependent':
								view.move(0,0,viz.getFrameElapsed()*-jy*joyMovSpeed*it)
						
					else: 
						pass			# don't move

				if rot == 1 and trans == 0:
					
					if math.fabs(jx) > joyDeadzone and -zoneY < jy < zoneY:	# rotation
						
						if  jx < 0: 	# left
							if joyRotationMode == 'dependent':
								view.setEuler([joyRotSpeed*ir*jx*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
							elif joyRotationMode == 'fixed':
								view.setEuler([-joyRotSpeed*ir*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
						if  jx > 0:  	# right
							if joyRotationMode == 'dependent':
								view.setEuler([joyRotSpeed*ir*jx*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
							elif joyRotationMode == 'fixed':
								view.setEuler([joyRotSpeed*ir*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
						
					else: 
						pass			# don't move

	if inputDevice == 'keyboard':
		
		if keyboardMode == 1:
			if trans and rot == 1:
				if viz.key.isDown(buttonMap['left']):
					view.setEuler([-joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
				if viz.key.isDown(buttonMap['right']):
					view.setEuler([joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
				if viz.key.isDown(buttonMap['forward']):
					view.move(0,0,viz.getFrameElapsed()*joyMovSpeed) 	
				if viz.key.isDown(buttonMap['backward']):
					view.move(0,0,viz.getFrameElapsed()*-joyMovSpeed)
			
			if trans == 1 and rot == 0:
				if viz.key.isDown(buttonMap['forward']):
					view.move(0,0,viz.getFrameElapsed()*joyMovSpeed) 	
				if viz.key.isDown(buttonMap['backward']):
					view.move(0,0,viz.getFrameElapsed()*-joyMovSpeed)
			
			if trans == 0 and rot == 1:
				if viz.key.isDown(buttonMap['left']):
					view.setEuler([-joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
				if viz.key.isDown(buttonMap['right']):
					view.setEuler([joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
					
		elif keyboardMode == 2:
			
			if trans and rot == 1:
				if viz.key.isDown(buttonMap['left']):
					view.setEuler([-joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
				elif viz.key.isDown(buttonMap['right']):
					view.setEuler([joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
				elif viz.key.isDown(buttonMap['forward']):
					view.move(0,0,viz.getFrameElapsed()*joyMovSpeed) 	
				elif viz.key.isDown(buttonMap['backward']):
					view.move(0,0,viz.getFrameElapsed()*-joyMovSpeed)
			
			if trans == 1 and rot == 0:
				if viz.key.isDown(buttonMap['forward']):
					view.move(0,0,viz.getFrameElapsed()*joyMovSpeed) 	
				elif viz.key.isDown(buttonMap['backward']):
					view.move(0,0,viz.getFrameElapsed()*-joyMovSpeed)
			
			if trans == 0 and rot == 1:
				if viz.key.isDown(buttonMap['left']):
					view.setEuler([-joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)
				elif viz.key.isDown(buttonMap['right']):
					view.setEuler([joyRotSpeed*viz.getFrameElapsed(),0,0],viz.HEAD_ORI,viz.REL_PARENT)