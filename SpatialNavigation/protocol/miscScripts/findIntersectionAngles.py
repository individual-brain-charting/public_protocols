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
sys.path.insert(0,os.path.realpath('..\py'))
sys.path.insert(0,os.path.realpath('..\objects'))
# File I/O
from csv_io import write_to_csv as writeToFile

fileName = 'output.csv'

city = viz.addChild(os.path.realpath('../objects/virtualtuebingen_baked.osgb'))


for k in range(4):
	
	# create intersection object
	intersection = city.getChild('pos_inters_' + str(k) + '-GEODE')
	
	print('Intersection {}'.format(k))
	
	# get intersection center position
	intersection.position = [round(n,3) for n in intersection.getPosition(viz.ABS_GLOBAL)]

	# get intersection start points
	intersection.startPoints = []
	for i in range(4):
		sP = city.getChild('pos_sP_' + str(k) + '_' + str(i) + '-GEODE')
		sP.visible(False)
		
		print('Startpoint {}: {:0.3f}'.format(i, vizmat.AngleToPoint([intersection.position[0],intersection.position[2]],[sP.getPosition(viz.ABS_GLOBAL)[0], sP.getPosition(viz.ABS_GLOBAL)[2]]) ) )
		intersection.startPoints.append([round(n,3) for n in sP.getPosition(viz.ABS_GLOBAL)])
	
	
	
