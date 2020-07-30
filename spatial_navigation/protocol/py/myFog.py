from __future__ import division
import viz
import vizact
import viztask
import os
import sys

class myFog:
	
	def __init__(self,startDist = 10,endDist = 100,fadeOutDist = 1000,fadeTime = 2, fogColor = [1,1,1]):
		
		# keep these values for reference
		self.fadeOutDist = fadeOutDist	
		self.startDist = startDist
		self.endDist = endDist
		
		# start and end distances, for init they are equal to faded out distance
		self.start = fadeOutDist	# start of fog when faded in
		self.end = fadeOutDist + 10	# end of fog when faded in, add 10 meters, otherwise flickering issue occurs (if both start and end values are the same, the screen will be completely gray one frame)
		
		# calculate iterations needed to reach specified time for fading animation
		fps = 60
		self.iterations = round(fps * fadeTime)
		self.fadeTime = fadeTime	# create self. variable to access it from outside the class directly (e.g. fog.fadeTime gives the fading time)
		
		# calculate fog fading steps
		self.stepsStart = (fadeOutDist - startDist)/self.iterations
		self.stepsEnd = (fadeOutDist + 10 - endDist)/self.iterations	# add 10 meters, otherwise flickering issue occurs (if both start and end values are the same, the screen will be completely gray one frame)
		
		self.color = fogColor
		
		# switch variables
		self.wasFadedIn = False
		self.doneFading = viztask.Signal()
		
		print('myFog module: Inititialized fog:\tIterations: ' + str(self.iterations) + '\t Start,end distances: ' + str(startDist) + ',' + str(endDist)
		+ '\tStart steps: ' + str(self.stepsStart) + '\tSteps end: ' + str(self.stepsEnd) + '\tFade time: ' + str(fadeTime))

	def fadeIn(self):
		
		viz.fogcolor(self.color)	# set fog color
		print('myFog module: Fading fog in...')
		
		def executeFadeIn():
			viz.fog(self.start,self.end)
			self.start = self.start - self.stepsStart
			self.end = self.end - self.stepsEnd
			
			# send a signal once the fog is completely faded in
			if round(self.start) <= round(self.startDist):
				self.doneFading.send()
		
		vizact.ontimer2(0,self.iterations-1,executeFadeIn) # execute fading animation
		
		self.wasFadedIn = True
	
	def fadeOut(self):
		
		viz.fogcolor(self.color)
		print('myFog module: Fading fog out...')
		
		def executeFadeOut():
			viz.fog(self.start,self.end)
			self.start = self.start + self.stepsStart
			self.end = self.end + self.stepsEnd
			
			# send a signal once the fog is completely faded out
			if round(self.start) >= round(self.fadeOutDist):
				self.doneFading.send()
		
		vizact.ontimer2(0,self.iterations-1,executeFadeOut) # execute fading animation
		self.wasFadedIn = False	# reset fog switch
	
	def off(self):
		viz.fog(0,0)
		print('myFog module: Fog turned off.')
		self.wasFadedIn = False
	
	def on(self):
		viz.fogcolor(self.color)	# set fog color
		viz.fog(self.startDist,self.endDist)
		self.start = self.startDist
		self.end = self.endDist
		print('myFog module: Fog turned on.')
		self.wasFadedIn = True