# !/usr/bin/python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-
#
# An OpenGL movie class with buffer (buffermovie.py)
#
# 01-09-2009: sn
#   A movie class with buffer
#

import sys
from string import *
import pygame
from pygame.locals import *



class buffermovie:
	"""
	A class to load and store movie (a sequence of image files)
	"""
	def __init__(self, imagedir, indexfile, buffersize, flip=0):
		self.imagedir  = imagedir
		self.indexfile = indexfile
		self.filenames = self.loadindexfile(indexfile)
		self.numframes = len(self.filenames)
		self.flip = flip
	
		self.buffersize = buffersize
		self.imbuffer = list()
		self.frame_shown = -1
		self.frame_loaded = -1
		
		# Load a image to know the size
		im, imsize = self.load(0)
		self.imsize = imsize
		
		# Pre-fill the buffer
		for ii in range(buffersize):
			self.fetch()
	
	def __del__(self):
		pass
	
	def fetch(self, framenum=-1):
		if (self.frame_loaded+1 >= self.frame_shown+self.buffersize) or (self.frame_loaded+1>=self.numframes):
			return
		if framenum>0:
			data, imsize = self.load(framenum)
			self.frame_loaded = framenum
		else:
			self.frame_loaded = self.frame_loaded + 1
			data, imsize = self.load(self.frame_loaded)
	
		if self.frame_loaded < self.buffersize:
			self.imbuffer.append(data)
		else:
			self.imbuffer[self.frame_loaded%self.buffersize] = data
		
	def getframe(self, framenum):
		if framenum > self.frame_loaded:
			print 'Buffer run out!'
			self.fetch(framenum)
		im = self.imbuffer[framenum%self.buffersize]
		self.frame_shown = framenum
		return im, self.imsize
	
	def load(self, framenum):
		thedata = pygame.image.load(self.imagedir+self.filenames[framenum])
		if self.flip:
			thedata = pygame.transform.flip(thedata, 1, 1)
		thesize = thedata.get_rect()
		thedata = pygame.image.tostring(thedata, 'RGBA', True)
		return thedata, thesize[2:]
	
	def loadindexfile(self, indexfile):
		"""
		Load an index file (text file containing one image file name per line)
		"""
		a = open(indexfile).read()
		t = a.split('\n')
		if len(t[-1])<=1: # just EOF?
			t=t[:-1]
		return t
