#
# Copyright (c) 1996-2005, SR Research Ltd., All Rights Reserved
#
#
# For use by SR Research licencees only. Redistribution and use in source
# and binary forms, with or without modification, are NOT permitted.
#
#
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
#
# Neither name of SR Research Ltd nor the name of contributors may be used
# to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# $Date: 2007/08/29 18:48:21 $
# 
#

#########################################

# 2017-02-12 Michael Eickenberg:
# There was an issue with the pylink27 package as stored in path append below, namely
# that it was a 32 bit version, whereas the python environment (anaconda install) was
# 64 bit. This led to a dll error referring to the fact that "this dll is not a valid win32 app blabla"
# The solution was either to downgrade anaconda to 32 bits or to use a different pylink package:
# Note that the folder C:\\Users\\Public\\Documents\\EyeLink\\SampleExperiments contains many different
# pylink versions for many different python versions. We chose "python27-amd64" to make it work.
# ****CRUCIAL****: The pacakage contains absolute imports! The package thinks it is called "pylink", so you
# have to give it that name, otherwise internal imports will attempt to load something from somewhere else.
# While this is obviously poor programming style, we have to make do with this and work around it.
# The solution in place at the moment is a copy of pylink27-amd64 in the site-packages of anaconda.
# Upon anaconda reinstall this will have to be redone.
# Alternatively, the below commented code can be uncommented and then one has to make sure that the "pylink"
# folder contains the right version of the package (not the case by default, but is the case right now. 
# At eyelink reinstal this will have to be redone.)

## ad hoc addition of path to eyelink lib
## comment out if something doesnt work
## Michael Eickenberg 25/9/2015
#import sys
#sys.path.append(u'C:\\Users\\Public\\Documents\\EyeLink\\SampleExperiments\\Python')

#########################################

from pylink import *
#from eyelink import EyeLink   # I don't know why this was here. The class Eyelink is in pylink. (Michael 12/02/17)
import pygame
import time
import gc
import sys
import gcwindow_movie_trials
import os
import numpy as np


##### INITITALIZE VIDEO STUFF from PLAY.PY

cwd = os.path.abspath(os.path.split(__file__)[0])
#cwd = "C:\Data\agrilopi\movies\"

types = dict(val=("val%03d_3min", "valseq3minby10_%02d.index"), trn=("trn%03d", "trnseq.index"),
	eyetrack=("val%03d_3min", "val_1min.index"))
seq = [("trn", 1), ("val", 1), ("trn", 2), ("val", 2), ("trn", 3), ("val", 3), ("trn", 4), ("val",5), ("eyetrack", 3)]
### added ("val",5) for a 10 x 1-min repeatability test run
### 9/3/2012 SN

pname, session, run, subject = sys.argv

t, r = seq[int(run)-1]
impath, idxfile = types[t]
if t == "val":
	impath  = impath%int(session)
	idxfile = idxfile % r
elif t == "trn":
	impath  = impath%((int(session)-1)*4+r)
else:
	impath = impath % int(session)

impath = os.path.join(cwd, impath)+'/'
idxfile = os.path.join(cwd, idxfile)

print impath
print idxfile

gcwindow_movie_trials.fixationcolor = ((255, 80, 80), (80,255,80), (80, 80, 255), (255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80))
gcwindow_movie_trials.fcchange = 2
gcwindow_movie_trials.show_hz = 15
gcwindow_movie_trials.tfactor = 1.0000 #1.03365
# gcwindow_movie_trials.show(impath, idxfile)

############## END play INIT

## try showing the movie here, without eyetracker. This works, so it is commented

# pygame.init()
# surface = pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.RLEACCEL, 32)
surface = pygame.display.set_mode((800, 600), pygame.RLEACCEL, 32)

# gcwindow_movie_trials.do_trial(impath, idxfile, surface)

# sys.exit()
## end trying to show the movie

spath = os.path.dirname(sys.argv[0])
if len(spath) !=0: os.chdir(spath)


eyelinktracker = EyeLink()
#Here is the starting point of the experiment
#Initializes the graphics
pygame.init()
pygame.display.init()
# pygame.display.set_mode((800, 600), pygame.FULLSCREEN |pygame.DOUBLEBUF |pygame.RLEACCEL|pygame.HWSURFACE ,32)
pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.RLEACCEL, 32)
pylink.openGraphics()


#Opens the EDF file.
edfFileName = "TEST.EDF";

edfFileName = subject[:5] + '%03d.edf'
edffilepath = os.path.join(edfFileName)
filecounter = 0

while os.path.exists(edffilepath % filecounter):
	filecounter += 1

edffilepath = edffilepath % filecounter
print edffilepath
getEYELINK().openDataFile(edffilepath)		
	
pylink.flushGetkeyQueue(); 
getEYELINK().setOfflineMode();                          

#Gets the display surface and sends a mesage to EDF file;
surf = pygame.display.get_surface()
getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" %(surf.get_rect().w, surf.get_rect().h))
getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" %(surf.get_rect().w, surf.get_rect().h))

tracker_software_ver = 0
eyelink_ver = getEYELINK().getTrackerVersion()
if eyelink_ver == 3:
	tvstr = getEYELINK().getTrackerVersionString()
	vindex = tvstr.find("EYELINK CL")
	tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))
	

if eyelink_ver>=2:
	getEYELINK().sendCommand("select_parser_configuration 0")
	if eyelink_ver == 2: #turn off scenelink camera stuff
		getEYELINK().sendCommand("scene_camera_gazemap = NO")
else:
	getEYELINK().sendCommand("saccade_velocity_threshold = 35")
	getEYELINK().sendCommand("saccade_acceleration_threshold = 9500")
	
# set EDF file contents 
getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
if tracker_software_ver>=4:
	getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
else:
	getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")

# set link data (used for gaze cursor) 
getEYELINK().sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
if tracker_software_ver>=4:
	getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET")
else:
	getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")
	
	

# pylink.setCalibrationColors( (0, 0, 0),(255, 255, 255));  	#Sets the calibration target and background color
pylink.setCalibrationColors( (0, 0, 0),(140, 140, 140));  	#Sets the calibration target and background color
pylink.setTargetSize(int(surf.get_rect().w/70), int(surf.get_rect().w/300));	#select best size for calibration target
pylink.setCalibrationSounds("", "", "");
pylink.setDriftCorrectSounds("", "off", "off");

out_file = "measures.npz"

if(getEYELINK().isConnected() and not getEYELINK().breakPressed()):
	# gcwindow_movie_trials.run_trials(surf)
	measures = gcwindow_movie_trials.start_trials(impath, idxfile, surf,
		fixationcross=(0, 1, 1, 1), eyetrackercross=(1, 1, 1, 0))
	
	contents = {}
	if os.path.exists(out_file):
		f = np.load(out_file)
		for key in f.files:
			contents[key] = f[key]
	
	contents[edffilepath[:-4]] = measures
	
	np.savez(out_file, **contents)

if getEYELINK() != None:
	# File transfer and cleanup!
	getEYELINK().setOfflineMode();                          
	msecDelay(500);                 

	#Close the file and transfer it to Display PC
	getEYELINK().closeDataFile()
	getEYELINK().receiveDataFile(edffilepath, edffilepath)
	getEYELINK().close();

#Close the experiment graphics	
pylink.closeGraphics()
pygame.display.quit()
