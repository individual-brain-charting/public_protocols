import os
import viz
import vizjoy
import sys

sys.path.insert(0,os.path.realpath('..'))

from defineOptions import *

# ---------------------------
# Joystick & Movement related
# ---------------------------

# wait for specific joystick input before code proceeds
class waitJoy(viztask.Condition):
	
	def __init__(self,joy,conditionType,condition):			# if class is initialized, these variables are created
		
		self.joy = joy
		self.conditionType = conditionType
		self.condition = condition
		self.buttonWasDown = False							# trigger variable to let class return true only once (and not the whole time the button is pressed)
	
	def update(self):
		
		# a specific button needs to be pressed
		if self.conditionType == 'button':
		
			# button was not pressed before
			if self.buttonWasDown == False and self.joy.isButtonDown(self.condition) == True:
				self.buttonWasDown = True 					# exit this for loop -> true is not returned anymore
				return True
			elif self.buttonWasDown == True and self.joy.isButtonDown(self.condition) == False:
				self.buttonWasDown = False					# once button is depressed, reset trigger variable -> true can be returned again
	
		# a specific axis needs to be moved	
		if self.conditionType == 'axis':
			
			joyPos = joystick.getPosition()					# continously get joystick axis position	
			
			# find the 1 or -1 that has been passed by init of class
			try: 
				posIndex = self.condition.index(1)
			except ValueError:
				posIndex = [] 								# if 1 is not passed, assign empty list
			try:	
				negIndex = self.condition.index(-1)
			except ValueError:
				negIndex = []								# if -1 is not passed, assign empty list
			
			# depending on passed condition, return True
			if posIndex != []:					
				if joyPos[posIndex] > joyDeadzone:
					return True
			if negIndex != []:
				if joyPos[negIndex] < -joyDeadzone:
					return True
