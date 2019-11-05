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
# $Date: 2009/06/30 17:44:52 $
# 
#

from pylink import *
import pygame
from pygame import *
from pygame.locals import *
import time
import gc
import sys

import numpy as np

#if you need to save bitmap features and/or backdrop features set
#BITMAP_SAVE_BACK_DROP to  true. This will require numpy or Numeric modules. Also
#in some configurations calling array3d segfaults. 
BITMAP_SAVE_BACK_DROP = False
if BITMAP_SAVE_BACK_DROP:
	from pygame.surfarray import *


RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
DURATION = 40000

###### some SHOWMOVIE initialization stuff

import elbuffermovie as buffermovie

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
		fixationcolor = 0,
		fcchange = 0
	return fixationsize, fixationcolor, fcchange



def getrect(size, color):
	s = pygame.Surface(size,0,32)
	pygame.draw.rect(s, color, (0, 0, size[0], size[1]))
	# data = pygame.image.tostring(s, 'RGBA')
	return s

def draw(pos, size, data, dtype):
	glRasterPos2d(-pos[0], -pos[1])
	glDrawPixels(size[0], size[1], dtype , GL_UNSIGNED_BYTE , data)

def flipscreen():
	glFinish()
	pygame.display.flip()

# screen_size = surf.something
screen_size = np.array([800, 600])

center = screen_size / 2

blank_screen = getrect(screen_size, blankcolor)
#################### END SHOWMOVIE init#######################



	
	
def end_trial():
	'''Ends recording: adds 100 msec of data to catch final events'''
	
  	pylink.endRealTimeMode();  
  	pumpDelay(100);       
 	getEYELINK().stopRecording();
 	while getEYELINK().getkey() : 
 	 	pass;

def draw_movie(surf, movie, show_hz, fixation_mode=1, eyetracker_mode=0):
		
		top_left = tuple((screen_size - np.array(movie.imsize)) / 2)
		
		print screen_size
		print movie.imsize
		print top_left
		
		[fixationsize, fixationcolor, fcchange] = getfixationinfo(fixation_mode)
		print "fixation size %s color %s freqchange %s" % tuple(map(str, (fixationsize, fixationcolor, fcchange)))
		if fixationsize:
			fixation_points = list()
			for fc in fixationcolor:
				fixation_points.append(getrect(fixationsize, fc))
			fcnum = len(fixationcolor)
			fixationpos = (screen_size[0]/2-fixationsize[0]/2, screen_size[1]/2-fixationsize[1]/2)

		track_gaze = eyetracker_mode == 1
		
		start_time = currentTime()
		
		end_time = start_time + movie.numframes * (1000. / show_hz)
		
		current_frame = -1
		current_fixation_rect = -1
		
		mean_gazes_x = np.zeros([movie.numframes])
		mean_gazes_y = np.zeros([movie.numframes])
		mean_gaze_dists = np.zeros([movie.numframes])
		mse_gaze_dists = np.zeros([movie.numframes])
		
		
		
		####### EYETRACKER stuff
		cursorsize = (5, 5)
		srcrct = None
		oldv = None
		gazecursor = getrect(cursorsize, (192, 192, 0))
		eye_used = getEYELINK().eyeAvailable(); #determine which eye(s) are available 
		if eye_used == RIGHT_EYE:
			getEYELINK().sendMessage("EYE_USED 1 RIGHT");
		elif eye_used == LEFT_EYE or eye_used == BINOCULAR:
			getEYELINK().sendMessage("EYE_USED 0 LEFT");
			eye_used = LEFT_EYE;
		else:
			print "Error in getting the eye information!";
			return TRIAL_ERROR;
	
		getEYELINK().flushKeybuttons(0)
		buttons =(0, 0);
		#######
		
		
		
		while True:
		
			####### Eyetracker stuff
			
			error = getEYELINK().isRecording()  # First check if recording is aborted
			if error!=0:
				print "error %s" % str(error)
				end_trial();
				return error
			if(getEYELINK().breakPressed()):	# Checks for program termination or ALT-F4 or CTRL-C keys
				end_trial();
				print "Break pressed, exiting"
				return ABORT_EXPT
			elif(getEYELINK().escapePressed()): # Checks for local ESC key to abort trial (useful in debugging)
				end_trial();
				print "Escape Pressed, exiting"
				return SKIP_TRIAL
			
			buttons = getEYELINK().getLastButtonPress() # Checks for eye-tracker buttons pressed
			if(buttons[0] != 0):
				getEYELINK().sendMessage("ENDBUTTON %d"%(buttons[0]));
				print "Button pressed, breaking?"
				end_trial();
				break;		
			
			dt = getEYELINK().getNewestSample() # check for new sample update
			t = currentTime() - start_time
			frame_we_should_see = int(t / 1000 * show_hz)
			if frame_we_should_see >= movie.numframes:
				break;
				
			if t >= 100000:
				print "Break after 100 seconds. Remember to remove"
				break;
			
			for event in pygame.event.get():
				# if (event.type == pygame.locals.KEY_DOWN) and (event.key == pygame.locals.K_ESCAPE):
					# break;
				pass
			
				
			
			
			if frame_we_should_see != current_frame:
				if current_frame != -1:
					mean_gazes_x[current_frame] = mean_gaze_x
					mean_gazes_y[current_frame] = mean_gaze_y
					mean_gaze_dists[current_frame] = mean_gaze_dist
					mse_gaze_dists[current_frame] = mse_gaze
			
				stall_counter = 0
				mean_gaze_x = 0.
				mean_gaze_y = 0.
				mean_gaze_dist = 0.
				mse_gaze = 0.
				
				image, image_size = movie.getframe(frame_we_should_see)
				
				rectimg = surf.blit(image, top_left)
				#pygame.display.update([rectimg])
				current_frame = frame_we_should_see
				movie.fetch()
				if fixationsize:
					fixation_rect_we_should_see = int(t / 1000 * fcchange) % len(fixation_points)
					if current_fixation_rect != fixation_rect_we_should_see:
						fixation_rect = fixation_points[fixation_rect_we_should_see]
						current_fixation_rect = fixation_rect_we_should_see
					rect = surf.blit(fixation_rect, fixationpos)
				
				pygame.display.update([rectimg])
			# else:
				# stall_counter += 1
				
				
			if dt is not None:
				stall_counter += 1.
			
				if eye_used == RIGHT_EYE and dt.isRightSample():
					gaze_position = dt.getRightEye().getGaze()
				elif eye_used == LEFT_EYE and dt.isLeftSample():
					gaze_position = dt.getLeftEye().getGaze()

				# Determines the top-left corner of the update region and determines whether an update is necessarily or not
				region_topleft = (gaze_position[0]-cursorsize[0]/2, gaze_position[1]-cursorsize[1]/2)

				mean_gaze_x = ((mean_gaze_x * (stall_counter - 1) + (gaze_position[0])) / 
					stall_counter)
				mean_gaze_y = ((mean_gaze_y * (stall_counter - 1) + (gaze_position[1])) / 
					stall_counter)
				mean_gaze_dist = ((mean_gaze_dist * (stall_counter - 1) + np.sqrt(
					(gaze_position[0] - screen_size[0] / 2.) ** 2 + (gaze_position[0] - screen_size[0] / 2.) ** 2)) /
					stall_counter)
				mse_gaze = np.sqrt((mse_gaze ** 2 * (stall_counter - 1) + (
					(gaze_position[0] - screen_size[0] / 2.) ** 2 + (gaze_position[0] - screen_size[0] / 2.) ** 2)) / 
					stall_counter)
				
				
				if(oldv != None and oldv == region_topleft):
					pass
				else:
					if track_gaze:
						toupdate = []
						if oldv is not None:
							rold = surf.blit(image, top_left, Rect(oldv, cursorsize)) # remove old cursor
							toupdate.append(rold)
						rnew = surf.blit(gazecursor, region_topleft)
						toupdate.append(rnew)
						pygame.display.update(toupdate)
					
						oldv = region_topleft
					
		return mean_gazes_x, mean_gazes_y, mean_gaze_dists, mse_gaze_dists			


# def drawgc(surf, bgbm,fgbm, startTime):
	# '''Does gaze-contingent drawing; uses the getNewestSample() to get latest update '''

	# cursorsize = (400,400)
	# srcrct = None
	# oldv = None
	# print "In DrawGC"
	# print currentTime()
	
  	# eye_used = getEYELINK().eyeAvailable(); #determine which eye(s) are available 
  	# if eye_used == RIGHT_EYE:
  		# getEYELINK().sendMessage("EYE_USED 1 RIGHT");
  	# elif eye_used == LEFT_EYE or eye_used == BINOCULAR:
  		# getEYELINK().sendMessage("EYE_USED 0 LEFT");
  		# eye_used = LEFT_EYE;
  	# else:
  		# print "Error in getting the eye information!";
  		# return TRIAL_ERROR;
	
	# getEYELINK().flushKeybuttons(0)
	# buttons =(0, 0);
	# blitcounter = 0
	# updatecounter = 0
	# gazepositions = []
	
	# display.flip()
	
	# while 1:
		# error = getEYELINK().isRecording()  # First check if recording is aborted 
		# if error!=0:
			# end_trial();
			# return error

		# if int(currentTime() -startTime) > int(DURATION):  #Writres out a time out message if no response is made
            # print "timeout"
			# getEYELINK().sendMessage("TIMEOUT");
			# end_trial();
			# buttons =(0, 0);
			# print "Exceeded DURATION %s, breaking loop" % str(DURATION)
			# break;
		
		# if(getEYELINK().breakPressed()):	# Checks for program termination or ALT-F4 or CTRL-C keys
			# end_trial();
			# print "Break pressed, exiting"
			# return ABORT_EXPT
		# elif(getEYELINK().escapePressed()): # Checks for local ESC key to abort trial (useful in debugging)
			# end_trial();
			# print "Escape Pressed, exiting"
			# return SKIP_TRIAL
			
		# buttons = getEYELINK().getLastButtonPress() # Checks for eye-tracker buttons pressed
		# if(buttons[0] != 0):
			# getEYELINK().sendMessage("ENDBUTTON %d"%(buttons[0]));
			# print "Button pressed, breaking?"
			# end_trial();
			# break;		
			
		# dt = getEYELINK().getNewestSample() # check for new sample update
		# if(dt != None):
			##Gets the gaze position of the latest sample,
			# if eye_used == RIGHT_EYE and dt.isRightSample():
				# gaze_position = dt.getRightEye().getGaze()
			# elif eye_used == LEFT_EYE and dt.isLeftSample():
				# gaze_position = dt.getLeftEye().getGaze()

			##Determines the top-left corner of the update region and determines whether an update is necessarily or not
			# region_topleft = (gaze_position[0]-cursorsize[0]/2, gaze_position[1]-cursorsize[1]/2)
			# updatecounter += 1
			# if(oldv != None and oldv == region_topleft):
				# continue
			# oldv = region_topleft
			# #gazepositions.append(gaze_position)
			# if(srcrct != None):	
                            # r1=surf.blit(bgbm, (srcrct.x, srcrct.y),(srcrct.x, srcrct.y, cursorsize[0], cursorsize[1]))
                            ##r1=surf.blit(fgbm, (srcrct.x, srcrct.y),(srcrct.x, srcrct.y, cursorsize[0], cursorsize[1]))
                            # srcrct.x = region_topleft[0]
                            # srcrct.y = region_topleft[1]
                            # r2=surf.blit(fgbm, (srcrct.x, srcrct.y),(srcrct.x, srcrct.y, cursorsize[0], cursorsize[1]))
                            ##r2=surf.blit(bgbm, (srcrct.x, srcrct.y),(srcrct.x, srcrct.y, cursorsize[0], cursorsize[1]))
                            # blitcounter += 1
                            # display.update([r1,r2])
                            ##display.flip()
			# else: # create a new backcursor and copy the new back cursor
                            # srcrct = Rect(0,0,cursorsize[0], cursorsize[1])

	# end_trial();	
	
	##The TRIAL_RESULT message defines the end of a trial for the EyeLink Data Viewer. 
	##This is different than the end of recording message END that is logged when the trial recording ends. 
	##Data viewer will not parse any messages, events, or samples that exist in the data file after this message. 
	# getEYELINK().sendMessage("TRIAL_RESULT %d"%(buttons[0]));
	
	# print "Last line of drawGC, blitcounter at %d, loop counter at %d" % (blitcounter, updatecounter)
	# print currentTime()
	##print gazepositions
	##np.save("gazepositions", np.array(gazepositions))
	# return getEYELINK().getRecordingStatus()
        
	
		
# fgtext  = [
# "Buck did not read the newspapers, or he would have known that",
# "trouble was brewing, not alone for himself, but for every ",
# "tide-water dog, strong of muscle and with warm, long hair, from", 
# "Puget Sound to San Diego. Because men, groping in the Arctic ",
# "darkness, had found a yellow metal and because steamship and ",
# "transportation companies were booming the find, thousands of ",
# "men were rushing into the Northland. These men wanted dogs, ",
# "and the dogs they wanted were heavy dogs, with strong muscles ",
# "by which to toil, and furry coats to protect them from the frost.",
# "                                                                 ",
# "Buck lived at a big house in the sun-kissed Santa Clara ",
# "Valley. Judge Miller's place, it was called. It stood back ",
# "from the road, half hidden among the trees, through which ",
# "glimpses could be caught of the wide cool veranda that ran ",
# "around its four sides."
# ]

# bgtext  = [
# "Xxxx xxx xxx xxxx xxx xxxxxxxxxxx xx xx xxxxx xxxx xxxxx xxxx",
# "xxxxxxx xxx xxxxxxxx xxx xxxxx xxx xxxxxxxx xxx xxx xxxxx ",
# "xxxxxxxxxx xxxx xxxxxx xx xxxxxx xxx xxxx xxxxx xxxx xxxxx xxxx", 
# "Xxxxx Xxxxx xx Xxx Xxxxxx Xxxxxxx xxxx xxxxxxx xx xxx Xxxxxx ",
# "xxxxxxxxx xxx xxxxx x xxxxxx xxxxx xxx xxxxxxx xxxxxxxxx xxx ",
# "xxxxxxxxxxxxxx xxxxxxxxx xxxx xxxxxxx xxx xxxxx xxxxxxxxx xx ",
# "xxx xxxx xxxxxxx xxxx xxx Xxxxxxxxxx Xxxxx xxx xxxxxx xxxxx ",
# "xxx xxx xxxx xxxx xxxxxx xxxx xxxxx xxxxx xxxx xxxxxx xxxxxxx ",
# "xx xxxxx xx xxxx, xxx xxxxx xxxxx xx xxxxxxx xxxx xxxx xxx xxxxxx",
# "                                                                 ",
# "Xxxx xxxxx xx x xxx xxxxx xx xxx xxxxxxxxxx Xxxxx Xxxxx ",
# "Xxxxxxx Xxxxx Xxxxxxxx xxxxxx xx xxx xxxxxxx Xx xxxxx xxxx ",
# "xxxx xxx xxxxx xxxx xxxxxx xxxxx xxx xxxxxx xxxxxxx xxxxx ",
# "xxxxxxxx xxxxx xx xxxxxx xx xxx xxxx xxxx xxxxxxx xxxx xxx ",
# "xxxxxx xxx xxxx xxxxxx"
# ]



# def getTxtBitmap(text, dim):
	# ''' This function is used to create a page of text. '''

	# ''' return image object if successful; otherwise None '''

	# if(not font.get_init()):
		# font.init()
	# fnt = font.Font("cour.ttf",15)
	# fnt.set_bold(1)
	# sz = fnt.size(text[0])
	# bmp = Surface(dim)
	
	# bmp.fill((255,255,255,255))
	# for i in range(len(text)):
		# txt = fnt.render(text[i],1,(0,0,0,255), (255,255,255,255))
		# bmp.blit(txt, (0,sz[1]*i))
	
	# return bmp
	
	
# def getImageBitmap(pic):
	# ''' This function is used to load an image into a new surface. '''

	# ''' return image object if successful; otherwise None '''

	# if(pic == 1):
		# try:
			# bmp = image.load("sacrmeto.jpg", "jpg")
			# return bmp
		# except:
			# print "Cannot load image sacrmeto.jpg";
			# return None;
	# else:
		# try:
			# bmp = image.load("sac_blur.jpg", "jpg")
			# return bmp
		# except:
			# print "Cannot load image sac_blur.jpg";
			# return None;
	
	
	
# trial_condition = ["Image-Window", "Image-Mask", "Text-Window", "Text-Mask"];	
	
# def arrayToList(w,h,dt):
	# rv = []
	# for y in xrange(h):
		# line =[]
		# for x in xrange(w):
			# v = dt[x,y]
			# line.append((v[0],v[1],v[2]))
		# rv.append(line)
	# return rv

# def do_trial(trial, surf):
	# '''Does the simple trial'''

	## This supplies the title at the bottom of the eyetracker display
	# message ="record_status_message 'Trial %d %s'"%(trial+1, trial_condition[trial])
	# getEYELINK().sendCommand(message);	
	
	##Always send a TRIALID message before starting to record.
	##EyeLink Data Viewer defines the start of a trial by the TRIALID message.  
	##This message is different than the start of recording message START that is logged when the trial recording begins. 
	##The Data viewer will not parse any messages, events, or samples, that exist in the data file prior to this message.
	# msg = "TRIALID %s"%trial_condition[trial];
	# getEYELINK().sendMessage(msg);
	
	##Creates the bitmap images for the foreground and background images;
	# if(trial == 0):
		# fgbm = getImageBitmap(1)
		# bgbm = getImageBitmap(2) 
	# elif(trial == 1):
		# fgbm = getImageBitmap(2)
		# bgbm = getImageBitmap(1) 
	# elif(trial == 2):
		# fgbm = getTxtBitmap(fgtext, (surf.get_rect().w, surf.get_rect().h))
		# bgbm = getTxtBitmap(bgtext, (surf.get_rect().w, surf.get_rect().h))
	# elif(trial == 3):
		# bgbm = getTxtBitmap(fgtext, (surf.get_rect().w, surf.get_rect().h))
		# fgbm = getTxtBitmap(bgtext, (surf.get_rect().w, surf.get_rect().h))
	# else:
		# return SKIP_TRIAL ;
		
	# if (fgbm == None or bgbm == None):
		# print "Skipping trial ", trial+1, "because images cannot be loaded"
		# return SKIP_TRIAL ;
		
		
	##The following code is for the EyeLink Data Viewer integration purpose.   
	##See section "Protocol for EyeLink Data to Viewer Integration" of the EyeLink Data Viewer User Manual
	##The IMGLOAD command is used to show an overlay image in Data Viewer 
	# getEYELINK().sendMessage("!V IMGLOAD FILL  sacrmeto.jpg");
	
	##This TRIAL_VAR command specifies a trial variable and value for the given trial. 
	##Send one message for each pair of trial condition variable and its corresponding value.
 	# getEYELINK().sendMessage("!V TRIAL_VAR image  sacrmeto.jpg");
 	# getEYELINK().sendMessage("!V TRIAL_VAR type  gaze_contingent");
 	
	
	# if BITMAP_SAVE_BACK_DROP:
		##array3d(bgbm) crashes on some configurations. 
		# agc = arrayToList(bgbm.get_width(),bgbm.get_height(),array3d(bgbm))
		# bitmapSave(bgbm.get_width(),bgbm.get_height(),agc,0,0,bgbm.get_width(),bgbm.get_height(),"trial"+str(trial)+".bmp","trialimages", SV_NOREPLACE,)
		# getEYELINK().bitmapSaveAndBackdrop(bgbm.get_width(),bgbm.get_height(),agc,0,0,bgbm.get_width(),bgbm.get_height(),"trial"+str(trial)+".png","trialimages", SV_NOREPLACE,0,0,BX_MAXCONTRAST)
	
	

	
	##The following does drift correction at the begin of each trial
	# while 1:
		##Checks whether we are still connected to the tracker
		# if not getEYELINK().isConnected():
			# return ABORT_EXPT;			
		
		##Does drift correction and handles the re-do camera setup situations
		# try:
                        # print surf.get_rect().w/2,surf.get_rect().h/2
			# error = getEYELINK().doDriftCorrect(surf.get_rect().w/2,surf.get_rect().h/2,1,1)
			# if error != 27: 
				# break;
			# else:
				# getEYELINK().doTrackerSetup();
		# except:
			# break #getEYELINK().doTrackerSetup()		
	
	# error = getEYELINK().startRecording(1,1,1,1)
	# if error:	return error;
	# gc.disable();
	##begin the realtime mode
	# pylink.beginRealTimeMode(100)

	# if not getEYELINK().waitForBlockStart(1000, 1, 0):
		# end_trial();
		# print "ERROR: No link samples received!";
      		# return TRIAL_ERROR;
      	  
	##surf.fill((255,255,255,255))
	# surf.blit(bgbm,(0,0))
	# display.flip()
	# startTime = currentTime()
	
	# getEYELINK().sendMessage("SYNCTIME %d"%(currentTime()-startTime));
	# ret_value = drawgc(surf,bgbm, fgbm, startTime);
	# pylink.endRealTimeMode();
	# gc.enable();
	# return ret_value;
	
def do_trial(surf, impath, indexfile, fixationcross=1, eyetrackercross=1):

	movie = buffermovie.buffermovie(impath, indexfile, 300, 0)
	# Do drift correction before every trial:
	
	try:
		error = getEYELINK().doDriftCorrect(surf.get_rect().w/2,surf.get_rect().h/2,1,1)
		
		if error != 27:
			pass
		else:
			getEYELINK().doTrackerSetup()
	except:
		pass
	
	error = getEYELINK().startRecording(1,1,1,1)
	if error:	return error;

	gc.disable()
	pylink.beginRealTimeMode(100)

	mgx, mgy, mgd, mge = draw_movie(surf, movie, show_hz, fixationcross, eyetrackercross)
	
	pylink.endRealTimeMode()
	gc.enable()

	return mgx, mgy, mgd, mge

def start_trials(impath, indexfile, surf, fixationcross=(0, 1, 1, 1),
											eyetrackercross=(1, 1, 0, 0)):
	
	measures = []
	
	getEYELINK().doTrackerSetup()
	for trial, (fc, ec) in enumerate(zip(fixationcross, eyetrackercross)):
		message ="record_status_message 'Trial %d %s'"%(trial + 1, 'movie')
		getEYELINK().sendCommand(message);	

		msg = "TRIALID %s"% ('movie_%d' % (trial + 1));
		getEYELINK().sendMessage(msg);

		start_time = currentTime()
		getEYELINK().sendMessage("SYNCTIME %d" % (currentTime() - start_time))
		# if (trial == 0 and fixationcross == 1) or (trial + 1 == num_trials and fixationcross == 0):
			# eyetrackercross = 1
		# else:
		#	eyetrackercross = 0
		mgx, mgy, mgd, mge = do_trial(surf, impath, indexfile, fixationcross=fc, eyetrackercross=ec)
		
		radius = 20
		score = naive_evaluate(mgd, radius)
		display_message(surf, "Temps passe dans un rayon de %d pixels: %1.2f%%" % (radius, score * 100))
		getkey()
		
		measures.append(dict(
			mgx=mgx, mgy=mgy, mgd=mgd, mge=mge))
	
	return measures

def display_message(surf, message):
	surf.blit(blank_screen, (0,0))
	font = pygame.font.SysFont("calibri", 40)
	
	text = font.render(str(message), True, (255, 128, 0))
	# print text.get_rect()
	# print "width: %d, height: %d" % (text.get_rect().width, text.get_rect().height)
	r = text.get_rect()
	h = r.height
	w = r.width
	surf.blit(text, (screen_size - np.array([w, h])) / 2)
	pygame.display.flip()

def getkey():
	while True:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				return event.key

def naive_evaluate(mgd, radius=30):
	return np.float64((mgd < radius).sum()) / len(mgd)


dtch = []
def load_all_measures():
		global dtch
		if dtch:
			return dtch
		else:
			f = np.load("measures.npz")
			for file in f.files:
				for data in f[file]:
					dtch.append(data['mgd'])
			return dtch

def compare_time_seq_to_all(seq):
	dtch = np.array(load_all_measures())
	ranks = (dtch >= seq).sum(0)
	
	rank_freq = (ranks[:, np.newaxis] == np.arange(len(dtch) + 1)[np.newaxis, :]).sum(0)
	
	
	
	
	
# NTRIALS = 1
# def run_trials(surface):
	# ''' This function is used to run individual trials and handles the trial return values. '''

	# ''' Returns a successful trial with 0, aborting experiment with ABORT_EXPT (3); It also handles
	# the case of re-running a trial. '''
	## Do the tracker setup at the beginning of the experiment.
	# getEYELINK().doTrackerSetup()

	# for trial in range(NTRIALS):
		# if(getEYELINK().isConnected() ==0 or getEYELINK().breakPressed()): break;

		# while 1:
			# ret_value = do_trial(trial, surface)
			# endRealTimeMode()
		
			# if (ret_value == TRIAL_OK):
				# getEYELINK().sendMessage("TRIAL OK");
				# break;
			# elif (ret_value == SKIP_TRIAL):
				# getEYELINK().sendMessage("TRIAL ABORTED");
				# break;			
			# elif (ret_value == ABORT_EXPT):
				# getEYELINK().sendMessage("EXPERIMENT ABORTED")
				# return ABORT_EXPT;
			# elif (ret_value == REPEAT_TRIAL):
				# getEYELINK().sendMessage("TRIAL REPEATED");
			# else: 
				# getEYELINK().sendMessage("TRIAL ERROR")
				# break;
				
	# return 0;
		

