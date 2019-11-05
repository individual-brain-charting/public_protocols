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


from pylink import *
import pygame
import time
import gc
import sys
import gcwindow_trial
import os


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
getEYELINK().openDataFile(edfFileName)		
	
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
	
	

pylink.setCalibrationColors( (0, 0, 0),(255, 255, 255));  	#Sets the calibration target and background color
pylink.setTargetSize(int(surf.get_rect().w/70), int(surf.get_rect().w/300));	#select best size for calibration target
pylink.setCalibrationSounds("", "", "");
pylink.setDriftCorrectSounds("", "off", "off");

if(getEYELINK().isConnected() and not getEYELINK().breakPressed()):
	gcwindow_trial.run_trials(surf)

if getEYELINK() != None:
	# File transfer and cleanup!
	getEYELINK().setOfflineMode();                          
	msecDelay(500);                 

	#Close the file and transfer it to Display PC
	getEYELINK().closeDataFile()
	getEYELINK().receiveDataFile(edfFileName, edfFileName)
	getEYELINK().close();

#Close the experiment graphics	
pylink.closeGraphics()
pygame.display.quit()
