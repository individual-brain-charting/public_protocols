"""
Python/Expyriment implemetation of the protocol for visual 
search and working memory. Imports prerandomise.py.

Himanshu Aggarwal 
himanshu.aggarwal@inria.fr 
December 2020
"""

#========== Visual stimulus display setup ====================

ang_ecc=2.58			# array eccentricity in degrees
ang_ele=2				# array elevation in degrees
ang_stim=1.80			# stimulus size in degrees

screen_width=0.6		# BOLD screen width in metres
screen_height=0.45		# BOLD screen height in metres
# BOLD screen aspect ratio should be 1.333 (width/height)

screen_res_x=1280		# screen resolution in pixels along x-axis
screen_res_y=960		# screen resolution in pixels along y-axis
# Screen resolution aspect ratio should be 1.333 (width/height)

distance=0.89			# distance between the subject and screen in metres
#==============================================================

import expyriment
from expyriment import design, control, stimuli, misc, io
import prerandomise as pr
import os
import ast
import math

# function for creating a search/memory array based...
# on prerandomised arrangements and array type
def setup_array(array_type,ecc,ele,stim_x,stim_y,pics):
	# set an empty canvas for inserting pictures
	array = stimuli.Canvas(size=(screen_res_x, screen_res_y))

	# set coordinates for pictures based on array type
	if array_type == 'two_urll':
		coords = [(ecc,ele),(-ecc,-ele)]
	elif array_type == 'two_ullr':
		coords = [(-ecc,ele),(ecc,-ele)]
	else:
		coords = [(ecc,ele),(-ecc,ele),(-ecc,-ele)
				,(ecc,-ele)]

	# plot pictures on the empty canvas based...
	# on prerandomised arrangements and array type
	for pic,coord in zip(pics,coords):
		item = stimuli.Picture('{}{}{}.png'.format(pics_path
								,os.sep,pic)
								,coord)
		item.scale((stim_x/170,stim_y/170))
		item.plot(array)

	# plot a cross in the middle
	cross = stimuli.FixCross(size=(30, 30)
							,line_width=3
							,colour=(255, 255, 255)
							).plot(array)
	return array


# function for loading stimuli in the trials based on trial...
# type from prerandomised trial sequences and stimuli..
# arrangements
def setup_run(trial_seq, arrangements, ecc, ele,
				stim_x, stim_y):

	# create a block (synonymous to run in this case) object 
	#for holding trials based on prerandomised trial types
	run = design.Block(name='Run - {}'.format(RUN))

	# loop over the prerandomised trial sequence
	for t,trial in enumerate(trial_seq):

		trial_ = design.Trial()

		# cue for the onset of the task
		onset = stimuli.TextLine("*", position=(0,-24)
								,text_size=100
								,text_colour=(255,255,255))
		trial_.add_stimulus(onset)

		trial_.set_factor('search_type', trial[0])
		trial_.set_factor('array_size', trial[1])
		trial_.set_factor('condition', trial[2])


		# if the trial is visual search type... 
		if trial[0] == 'vis':

			# load a sample picture based on the...
			# prerandomised arrangement
			sample_item = stimuli.Picture('{}{}{}.png'.format(
							pics_path,os.sep
							,int(arrangements[t][1])))
			sample_item.scale((stim_x/170,stim_y/170))
			trial_.add_stimulus(sample_item)

			# then load and delay cross
			delay_cross = stimuli.FixCross(size=(30, 30)
										,line_width=3
										,colour=(255, 255, 255))
			trial_.add_stimulus(delay_cross)

			# then load an array of 2 or 4 pictures which...
			# might or might not have the sample picture...
			# based on prerandomised arrangements
			search_array = setup_array(trial[1]
						,ecc,ele,stim_x,stim_y
						,ast.literal_eval(arrangements[t][2]))
			trial_.add_stimulus(search_array)


		# if the trial is working-memory search type... 
		if trial[0] == 'wm':

			# then load an array of 2 or 4 pictures which..
			# might or might not have the probe picture based.. 
			# on prerandomised arrangements
			memory_array = setup_array(trial[1]
									,ecc,ele,stim_x,stim_y
									,ast.literal_eval(arrangements[t][2]))
			trial_.add_stimulus(memory_array)

			# then load and delay cross
			delay_cross = stimuli.FixCross(size=(30, 30)
										,line_width=3
										,colour=(255, 255, 255))
			trial_.add_stimulus(delay_cross)

			# load a sample picture based on the prerandomised..
			# arrangement
			probe_item = stimuli.Picture('{}{}{}.png'.format(
							pics_path,os.sep
							,int(arrangements[t][1])))
			probe_item.scale((stim_x/170,stim_y/170))
			trial_.add_stimulus(probe_item)

		# then load an inter-trial blank screen
		iti_blank = expyriment.stimuli.BlankScreen()
		trial_.add_stimulus(iti_blank)

		trial_.preload_stimuli()

		
		run.add_trial(trial_)

	return run

# function for calculating screen pixels from given visual angles
# ang_ecc, ang_ele, ang_stim are in degrees
# screen_xy (screen height and widht) and distance (bw subject and screen) are in metres
# res_xy is in pixels
# returns eccentricity, elevation and stimulus width and height in pixels
def visual_angles_to_pixels(ang_ecc=2.58, ang_ele=2, ang_stim=1.72,
							screen_xy=(0.6,0.45), res_xy=(1280,960),
							distance=0.89):

	pix_ecc = (math.tan((ang_ecc/2)*(math.pi/180))*distance*res_xy[0])/(screen_xy[0]/2)
	pix_ele = (math.tan((ang_ele/2)*(math.pi/180))*distance*res_xy[1])/(screen_xy[1]/2)
	pix_stim_x = (math.tan((ang_stim/2)*(math.pi/180))*distance*res_xy[0])/(screen_xy[0]/2)
	pix_stim_y = (math.tan((ang_stim/2)*(math.pi/180))*distance*res_xy[1])/(screen_xy[1]/2)

	return pix_ecc,pix_ele,pix_stim_x,pix_stim_y



#====== Global variables (CAUTION: do not change) ===========

TRIAL_NUM = 48      # number of trials in each run
					# should be 48

TOTAL_RUNS = 4		# Total number of runs
					# should be 4

path = os.getcwd()
prerand_path = os.path.join(path, 'stim','prerandomisations')
pics_path = os.path.join(path, 'stim','pictures')

#============================================================


# initialize the experiment
exp = design.Experiment(name="Visual Search and Working Memory")
# Set developer mode on/off
control.set_develop_mode(False)
control.initialize(exp)
exp.set_log_level(2)


#==========Asks user to specify RUN number===================
# this segment adapted from formisano_protocol.py

# Create text input box
ti = io.TextInput(message='Specify run number to start from:',
				message_text_size=24,
				message_colour=(153,50,204),
				user_text_colour=(230,101,0),
				ascii_filter=misc.constants.K_ALL_DIGITS,
				background_colour=(0, 0, 0),
				frame_colour=(70, 70, 70)
				)

# Load user's input
while True:
	sb = ti.get('0')
	# If string is empty
	if not sb:
		warning_message1 = stimuli.TextLine(
			"Please enter a number between 0 and {}".format(TOTAL_RUNS-1),
			text_size=24,
			text_colour=(204, 0, 0))
		warning_message1.present()
		exp.keyboard.wait(misc.constants.K_RETURN
			, duration=4000)
		continue
	# If run number introduced is higher than the number of runs preset
	elif int(sb) > TOTAL_RUNS-1 or int(sb) < 0:
		warning_message2 = stimuli.TextLine(
			"Please enter a number between 0 and {}".format(TOTAL_RUNS-1),
			text_size=24,
			text_colour=(204, 0, 0))
		warning_message2.present()
		exp.keyboard.wait(misc.constants.K_RETURN
			, duration=4000)
		continue
	else:
		RUN = int(sb)
		break
#============================================================

control.start(exp, skip_ready_screen=True)

while RUN<TOTAL_RUNS:
	# End of run message
	end_block = stimuli.TextBox('Fin',
							(1000,1000), position=(0, -400),
							text_size=44)
	end_block.preload()

	# header for the data files
	exp.data_variable_names = ["Run", "Trial", "Time","Search_type"
							, "Array_size", "Ideal_Response"
							, "Sub_Response", "Check", "RT"
							, "Onset", "Stimulus_1","Delay"
							, "Stimulus_2", "Stimulus_2_End"
							, "Inter_trial"]

	# TTL cross
	fix_TTL = stimuli.FixCross(size=(40, 40)
							,line_width=6,
	                           colour=(255,0,0))
	fix_TTL.preload()

	# get the prerandomised onset, delay and ...
	# inter-trial durations
	durations = pr.get_prerands(prerand_path, pics_path
				, 'durations', TOTAL_RUNS, RUN, TRIAL_NUM)
	onset_dur = durations[:,0]
	delay_dur = durations[:,1]
	iti_dur = durations[:,2]
	stimuli_dur = 200
	response_dur = 2000

	ecc,ele,stim_x,stim_y = visual_angles_to_pixels(
			ang_ecc,		# array eccentricity in degrees
			ang_ele,		# array elevation in degrees
			ang_stim,		# stimulus size in degrees
			(screen_width,screen_height),# BOLD screen dimensions in metres
			(screen_res_x,screen_res_y),# screen resolution in pixels
			distance		# distance between the subject and screen in metres
			)

	# get the prerandomised trial sequences and picture arrangements
	trial_seq, arrangements = pr.get_prerands(prerand_path, pics_path
							, 'trials', TOTAL_RUNS, RUN, TRIAL_NUM)

	# set up the run and preload the stimuli based on...
	# prerandomised trial sequences and stimuli arrangements
	run = setup_run(trial_seq, arrangements, ecc, ele, stim_x, stim_y)


	# Wait for TTL
	fix_TTL.present()

	exp.keyboard.wait_char('t')
	# Start a clock with the onset of the run
	t0 = misc.Clock()

	trial_cnt = 1
	# Stimuli presentation loop
	for t, trial in enumerate(run.trials):

		# note the time of onset of each trial and present the
		# onset asterisk
		onset_time = t0.time
		trial.stimuli[0].present()
		exp.clock.wait(onset_dur[t],process_control_events=True)

		# display the first stimulus
		stim1_time = t0.time
		trial.stimuli[1].present()
		exp.clock.wait(stimuli_dur,process_control_events=True)

		# delay after the next stimulus
		delay_time = t0.time
		trial.stimuli[2].present()
		exp.clock.wait(delay_dur[t],process_control_events=True)

		# display second stimulus while registering response
		stim2_time = t0.time
		# Wait for parallel "Y" or "G" key press...
		# and register response
		key, rt = exp.keyboard.wait(keys=[misc.constants.K_y
									, misc.constants.K_g
									, misc.constants.K_b
									, misc.constants.K_r
									, misc.constants.K_m]
									,duration=stimuli_dur
									,callback_function=trial.stimuli[3].present()
									)
		# if repsonse is given before stimulus duration ends 
		# keep displaying stimulus for residual stimulus duration
		if key is not None:
			trial.stimuli[3].present()
			exp.clock.wait(stimuli_dur-rt)
		# else remove the stim 2 from the screen and
		# keep registering response for residual response duration
		else:
			exp.screen.clear()
			stim2_end_time = t0.time
			exp.screen.update()
			key, rt = exp.keyboard.wait(keys=[misc.constants.K_y
											, misc.constants.K_g
											, misc.constants.K_b
											, misc.constants.K_r
											, misc.constants.K_m]
									,duration=response_dur-stimuli_dur
									)
			# take stim duration into consideration for rt
			if type(rt) is int:
				rt = stimuli_dur+rt

		# response and inter trial period
		iti_time = t0.time
		trial.stimuli[4].present()

		# convert the key presses to appropriate response
		if key == 121:		# if key Y or index finger is pressed
			response = 'present'
		elif key == 103:	# if key G or middle finger is pressed
			response = 'absent'
		elif key == None:
			response = 'NA'
			rt = -1
		else:
			if key == 98:
				response = 'Other_{}'.format('B')
			elif key == 109:
				response  = 'Other_{}'.format('R')
			elif key == 114:
				response = 'Other_{}'.format('M') 

		# check whether or not subjects's response was correct
		if trial.get_factor('condition') == response:
			response_check = 'hit'
		else:
			response_check = 'miss'

		# append the collected data to the data file
		exp.data.add([RUN+1, trial_cnt, int(t0.time+iti_dur[t])
			, trial.get_factor('search_type')
			,trial.get_factor('array_size')
			,trial.get_factor('condition')
			,response, response_check, rt
			,onset_time, stim1_time, delay_time
			, stim2_time, stim2_end_time, iti_time])

		# the inter-trial period
		exp.clock.wait(iti_dur[t],process_control_events=True)

		trial_cnt += 1

	RUN = RUN + 1
	end_block.present()
	exp.clock.wait(4000,process_control_events=True)
	run.clear_factors()
	run.clear_trials()
	exp.keyboard.wait(keys=[misc.constants.K_RETURN])

control.end()
