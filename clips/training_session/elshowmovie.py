#!/usr/bin/env python2.1
#
# A visual stimuli presentation script (showmovie.py)
# (written for fMRI study)
#
# requires: pygame
#           pyOpenGL
#           buffermovie.py
#
# 1-9-2009: sn
#  HDD streaming movie presentation with some buffer
#

import sys
import time
import datetime
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os
import elbuffermovie as buffermovie

import pylink

# parameters for screen setting
#scsize = (1024,768)
scsize = (800,600)
fullscreen = 1  # 0 for debug, 1 for prod

### for movie
blankcolor = (140,140,140)

### for text
#blankcolor = (0,0,0)

# movie buffer size (frames)
buffersize = 300


###tfactor for quarter head scans
#tfactor = 0.996286

###tfactor for Thomas full head
#tfactor = 0.968788

###tfactor for quarter head scans in 3T
#tfactor = 0.999749

###tfactor for 7T, GE white coil, 1.2mm isotropic
tfactor = 0.999961


def getfixationinfo(fmode):
	if fmode==1:
		fixationsize = (4,4)
		fixationcolor = ((255,80,80), (80,255,80), (80,80,255))
		fcchange = 3
	elif fmode==2:
		fixationsize = (4,4)
		fixationcolor = ((255,255,255),(255,255,255))
		fcchange = 1
	else:
		fixationsize = 0
		fixationcolor = 0
		fcchange = 0
	return fixationsize, fixationcolor, fcchange



def getrect(size, color):
	s = pygame.Surface(size,0,32)
	pygame.draw.rect(s, color, (0, 0, size[0], size[1]))
	data = pygame.image.tostring(s, 'RGBA')
	return data

def draw(pos, size, data, dtype):
	glRasterPos2d(-pos[0], -pos[1])
	glDrawPixels(size[0], size[1], dtype , GL_UNSIGNED_BYTE , data)

def flipscreen():
	glFinish()
	pygame.display.flip()

def movieshow(movie, show_hz, fixationmode = 0):

	# set up a screen
	pygame.init()
	pygame.mouse.set_visible(0)
	if fullscreen:
		flags = FULLSCREEN |  DOUBLEBUF | HWSURFACE | OPENGL
	else:
		flags = DOUBLEBUF | HWSURFACE | OPENGL
	screen = pygame.display.set_mode(scsize, flags)
	
	## Pylink initialization stuff
	# pylink.openGraphics()
	# edf_file_name = "TEST_ME.EDF"
	# e = pylink.EyeLink("100.1.1.1")
	# e.openDataFile(edf_file_name)
	# pylink.flushGetkeyQueue()
	# e.setOfflineMode()
	
	# surf = screen # pygame.display.get_surface()    # is this equal to screen? yes!
	
	# e.sendCommand("screen_pixel_coords = 0 0 %d %d" % (surf.get_rect().w, surf.get_rect().h))
	
	# if e.getTrackerVersion() == 2:
		# e.sendCommand("select_parser_configuration 0")
	# else:
		# e.sendCommand("saccade_velocity_threshold = 35")
		# e.sendCommand("saccade_acceleration_threshold = 9500")
	
	# e.setFileEventFilter("LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
	# e.setFileSampleFilter("LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")
	# e.setLinkEventFilter("LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
	# e.setLinkSampleFilter("LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")
	# e.sendCommand("button-function 5 'accept_target_fixation'")
	
	# pylink.setCalibrationColors((255, 255, 255), (0, 0, 0))
	# pylink.setTargetSize(int(surf.get_rect().w / 70.),
							# int(surf.get_rect().w / 300.))
							
	# pylink.setCalibrationSounds("", "", "")
	
	# e.doTrackerSetup()
	
	# End Calibration stuff
	
	sccenter = (scsize[0]/2, scsize[1]/2)
	glOrtho(0,-scsize[0],0,-scsize[1],0,1)
        impos = ((scsize[0]-movie.imsize[0])/2, (scsize[1]-movie.imsize[1])/2)

	

	# fixation spot
	[fixationsize, fixationcolor, fcchange] = getfixationinfo(fixationmode)
	if fixationsize:
		fixationstr = list()
		for fc in fixationcolor:
        	        fixationstr.append(getrect(fixationsize, fc))
        	fcnum = len(fixationcolor)
		fixationpos = (scsize[0]/2-fixationsize[0]/2, scsize[1]/2-fixationsize[1]/2)
		
	# blank screen
	blankstr = getrect(scsize, blankcolor)

	playstatus = 0

	kwait = 1
	while kwait:
		draw((0,0), scsize, blankstr, GL_RGBA)
		if fixationsize:
			draw(fixationpos, fixationsize, fixationstr[0], GL_RGBA)
		flipscreen()
		for event in pygame.event.get():
			if (event.type == KEYDOWN):
				if event.key == K_t or event.key == K_5:
					kwait = 0
				if event.key == K_ESCAPE:
					playstatus = 99
		if playstatus == 99:
			break
		
	lasttime = gettime()
	firsttime = lasttime
	finaltime = firsttime + movie.numframes/show_hz
	bufferlog = list([-1]*int(movie.numframes/show_hz))
	bufferlogtick = 0
	thisframe = 0
	while lasttime < finaltime:
		if playstatus == 99:
			break
		thisframe = int(1.0*show_hz*(lasttime-firsttime))
		if thisframe >= movie.numframes:
			thisframe = movie.numframes-1
		im, imsize = movie.getframe(thisframe)

		draw(impos, imsize, im, GL_RGBA)

		if fixationsize:
	                fn = int(lasttime*fcchange)%fcnum
	        	draw(fixationpos, fixationsize, fixationstr[fn], GL_RGBA)

		flipscreen()
		
		movie.fetch()
		
		lasttime = gettime()
		
		if lasttime-firsttime > bufferlogtick+1:
			bufferlog[bufferlogtick] = movie.frame_loaded-movie.frame_shown+1
			bufferlogtick = bufferlogtick+1
		

		while True:
			if playstatus==2:
				playstatus = 1
			for event in pygame.event.get():
				if (event.type == KEYDOWN):
					if event.key == K_ESCAPE:
						playstatus = 99
					#if event.key == K_t:
					#	kts.append(lasttime-firsttime)
						
			if playstatus == 0:
				break
			elif playstatus == 2:
				break
			elif playstatus == 99:
				break
		

	ted = gettime()
	td = lasttime-firsttime
	if td:
		print "%.2f sec for %d frames (%.2f frames/sec)" % ( td, thisframe+1, (thisframe+1)/td )
		print bufferlog
		logwrite(bufferlog)
	if playstatus == 99:
		print "Aborted by user."
	pygame.mouse.set_visible(1)
	pygame.display.quit()


def gettime():
        return time.time()/tfactor


def logwrite(bufferlog):
        d=datetime.datetime.today()
        fname=d.strftime('%Y%m%d_%H%M%S')
        
        fout=open('./log/bufferlog'+fname, 'w')
        for t in bufferlog:
                fout.write(str(t)+'\n')
        fout.close()


def show(impath, indexfile, show_hz = 15, flip = 0, fixationmode = 1):
        #impath = '/Users/sn/fmristim/stim200812_randomcut/color/trn002/'
        #indexfile = 'valseq01.index'

        # set up a movie buffer
        print "Pre-loading images...(buffering", buffersize, "frames)"
        movie = buffermovie.buffermovie(impath, indexfile, buffersize, flip)
        imsize = movie.imsize
        print "done.\n"

        print "Size:", imsize, 'pixels, ', movie.numframes, 'frames'
        print "Path:", impath
        print "Files:", movie.filenames[0], movie.filenames[1], '...', movie.filenames[-1]


        movieshow(movie, show_hz, fixationmode)

