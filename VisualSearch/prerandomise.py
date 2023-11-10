"""
Module for pre-randomising trial and stimuli sequences for
Python/Expyriment implemetation of the protocol for visual 
and working memory search (protocol.py).

December 2020
Himanshu Aggarwal
himanshu.aggarwal@inria.fr
"""

import numpy as np
from numpy.random import default_rng
import time
import pandas as pd
import os


def generate_durations(save_to, runs, trial_num):

	"""
	Generates three types of randomised durations - Onset (500-1000ms), 
	ISI (4000-8000) and ITI (3500-7500) and saves them as a .txt file

	Paramenters
	-----------

	save_to: str
		location for saving the randomised durations

	runs: int
		total number of runs in the experiment

	trial_num: int
		number of trails in each run

	Returns
	-------

	save_as : str
		the filename for the saved randomised durations
	"""

	# filename to be saved as with current time appended to avoid overwriting previously saved files
	save_as = os.path.join(save_to, 'durations_runs_{}_trials_{}_{}.txt'.format(runs,trial_num,time.time()))

	# assign a random number generator
	rng = default_rng()
	# make an empty array
	a = np.empty((trial_num,3,runs))
	
	# open a file in which the durations would be saved
	with open(save_as,'w') as outfile:
		# header tp describe the content of the file
		outfile.write('# {} Runs (slices), {} Trials (rows) in each run and 3 randomised durations - onset, delay and ITI (in columns).\n'.format(runs, trial_num))
		# create randomised durations in each run
		for run in range(runs):
			# for better visualisations of separate runs
			outfile.write('\n# Run {} (slice {})\n'.format(run+1,run+1))
			# random intergers based on min-max values for each type of durations
			a[:,:,run] = rng.integers([500,4000,3500],[1000,8000,7500],size=(trial_num,3))
			# save the array to the text file
			np.savetxt(outfile, a[:,:,run], fmt='%-7.0f')
	return save_as

def generate_arrangements(empty_row, pics, arr_size, response):
	"""
	Generates randomised array arrangements and randomly selects display images.

	Parameters
	-----------
	
	empty_row: np 1d object array
		empty row of an array to hold the randomised arrangements

	pics: list of str
		a list containing names of the files for the images as strings

	arr_size: str
		number of images to be displayed in the array 

	response: str
		tells whether or not the array would contain the display image


	Returns
	-------

	empty_row : np 1d object array
		1d object array containing the randomised arrangements corresponding 
		to a trial
			
	"""

	rng = default_rng()

	# check array size and convert to integer
	if arr_size.split('_')[0] == 'two':
		size = 2
	else:
		size = 4

	# check the ideal response and if present select n=size and if absent n=size+1 stimuli images to be processed further
	if response == 'present':
		empty_row[0] = list(rng.choice(pics,size, replace = False))
	else:
		empty_row[0] = list(rng.choice(pics,size+1, replace = False))

	# select one out of the n=size or n=size+1 images. This image would be displayed.
	empty_row[1] = rng.choice(empty_row[0])

	# if the displayed image should be present in the array simply shuffle the positions of n=size images in the array
	# if the displayed image should not be present in the array remove it from the n=size+1 selected images and then 
	# shuffle the positions of the rest of images in the array
	if response == 'present':
		empty_row[2] = list(rng.permutation(empty_row[0]))
	else:
		empty_row[2] =list(rng.permutation(np.setdiff1d(empty_row[0],empty_row[1])))

	return empty_row


def generate_trials(save_to, path_to_pictures, runs, trial_num):

	"""
	Generates randomised trial sequence in factorial fashion based on search type 
	(visual/working-memory), array size (two/four) and ideal response (present/absent)
	along with the randomised image array arrangements for each trial.

	Parameters
	-----------

	save_to: str
		location for saving the randomised durations

	path_to_pictures: str
		location of the stimul files

	runs: int
		total number of runs in the experiment

	trial_num: int
		number of trails in each run

	Returns
	-------

	save_stimulus_as : str
		the filename for the saved randomised trial sequences

	save_arrangement_as: str
		filename for saved randomised array arrangements and display images

	"""

	# define filename to hold the trial sequences
	save_stimulus_as = os.path.join(save_to, 'trials_runs_{}_trials_{}_{}.txt'.format(runs,trial_num,time.time()))

	# factors involved
	search_type = ['vis','wm']
	array_size = ['two_ullr','two_urll','four']
	true_response = ['present','absent']

	# combine the events in a 2x2x2 factorial design
	factorial_df = pd.DataFrame([{'search_type':f1, 'array_size':f2, 'ideal_response':f3} for f1 in search_type for f2 in array_size for f3 in true_response])
	# right now the array size 2 is over-represented, doubling the array size 4 events
	factorial_df = factorial_df.append(factorial_df[factorial_df['array_size'] == 'four']).reset_index().drop(columns=['index'])
	# increase trial numbers to trial_num

	if trial_num%16 != 0:
		raise Exception('TRIAL_NUM should be in multiples of 16')

	scale = int(trial_num/16)
	factorial_df = pd.concat([factorial_df]*scale, ignore_index=True)

	trials_array = np.empty((trial_num,3,runs),dtype='object')

	# open the file for saving the trail sequences into
	with open(save_stimulus_as,'w') as outfile:
		# header for describing the contents of the file
		outfile.write('# {} Runs (slices), {} Trials (rows) in each run and 3 factors - search type, array size and ideal response (in columns).\n'.format(runs,trial_num))
		for run in range(runs):
			# separate the runs
			outfile.write('\n# Run {} (slice {})\n'.format(run+1,run+1))
			# shuffle the events and convert the pandas df to numpy array
			trials_array[:,:,run] = factorial_df.sample(frac=1).to_numpy()
			# save the array a .txt file
			np.savetxt(outfile, trials_array[:,:,run],delimiter=",",fmt="%s")

	# define filename to hold the arrangement of images in the arrays
	save_arrangement_as = os.path.join(save_to, 'arrangements_runs_{}_trials_{}_{}.txt'.format(runs,trial_num,time.time()))

	# create an empty array to hold the randomised arrangements
	arrangement_arr = np.empty((trial_num,3,runs),dtype='object')


	# get the image names
	pics = sorted(os.listdir(path_to_pictures))
	pics = [int(pic.split('.')[0]) for pic in pics]

	# open the file that would contain the arrangements
	with open(save_arrangement_as,'w') as outfile:
		# header to describe the contents
		outfile.write('# {} Runs (slices), {} Trials (rows) in each run and 3 levels random arrangements - random stimulus selection, random stimulus display and random arrangement in arrays (in columns).\n'.format(runs,trial_num))
		for run in range(runs):
			# separate the arrangements for each run
			outfile.write('\n# Run {} (slice {})\n'.format(run+1,run+1))
			# generate the array arrangement based upon trial type
			for i in range(trial_num):
				arrangement_arr[i,:,run] = generate_arrangements(arrangement_arr[i,:,run],pics
											,trials_array[i,1,run]
											,trials_array[i,2,run])
			# save the randomised array arrangements to a .txt file
			np.savetxt(outfile, arrangement_arr[:,:,run],delimiter=";",fmt="%s")

	return save_stimulus_as,save_arrangement_as

def load_prerand(file, runs, trial_num):
	"""
	Loads prerandomised conditions.

	Parameters
	-----------

	file: str
		path to the file to be loaded

	runs: str
		number of runs in the file

	trial_num: int
		number of trails in each run

	Returns
	-------
		
	loaded_data: 3-d numpy array
		array containing the prerandomised conditions
	"""

	# check the type of prerandoisation file
	if file.split(os.sep)[-1].split('_')[0] == 'trials':
		loaded_data = np.loadtxt(file,dtype=object,delimiter=',').reshape((runs,trial_num,3))
	elif file.split(os.sep)[-1].split('_')[0] == 'arrangements':
		loaded_data = np.loadtxt(file,dtype=object,delimiter=';').reshape((runs,trial_num,3))
	elif file.split(os.sep)[-1].split('_')[0] == 'durations':
		loaded_data = np.loadtxt(file).reshape((runs,trial_num,3))
	else:
		raise Exception('File type not recognised')

	return loaded_data
	
def get_prerands(prerand_path, pics_path, prerand_type, runs, current_run, trial_num):
	
	"""
	Looks for previously available prerandomised conditions, if not, generates new conditions and then loads 
	conditions for the current run.

	Parameters
	-----------

	file: str
		path to the file to be loaded

	runs: str
		number of runs in the file
	
	trial_num: int
		number of trails in each run

	Returns
	-------
		
	loaded_data: 3-d numpy array
		array containing the prerandomised conditions
	"""

	# look for previously saved prerandomisations
	all_files = sorted(os.listdir(prerand_path))
	prerand_files = [file for file in all_files if file.split('_')[0] == prerand_type and file.split('_')[2] == str(runs) and file.split('_')[4] == str(trial_num)]

	if prerand_type == 'durations':
		# generate new prerandomisations is none are already available
		if len(prerand_files) == 0:
			print('Prerandomised durations not available. Generating new set of randomised durations...')
			prerand = generate_durations(prerand_path, runs, trial_num)
		# use previously available prerandomisation
		elif len(prerand_files) == 1:
			prerand = prerand_files[0]
		# use the latest of available prerandomisations if more than one exists
		else:
			prerand = prerand_files[-1]
		prerand = os.path.join(prerand_path, prerand)
		return load_prerand(prerand,runs, trial_num)[current_run,:,:]

	# trials are accompanied by the arrangements
	elif prerand_type == 'trials':
		# generate new prerandomisations is none are already available
		if len(prerand_files) == 0:
			print('Prerandomised trial sequences not available. Generating new set of randomised sequences...')
			prerand1, prerand2 = generate_trials(prerand_path, pics_path, runs, trial_num)
		# generate new prerandomisations is none are already available
		elif len(prerand_files) == 1:
			prerand1 = prerand_files[0]
			prerand2 = [file for file in all_files if file.split('_')[0] == 'arrangements' and file.split('_')[2] == str(runs) and file.split('_')[4] == str(trial_num)][0]
		# generate new prerandomisations is none are already available
		else:
			prerand1 = prerand_files[-1]
			prerand2 = [file for file in all_files if file.split('_')[0] == 'arrangements' and file.split('_')[2] == str(runs) and file.split('_')[4] == str(trial_num)][-1]
		prerand1 = os.path.join(prerand_path, prerand1)
		prerand2 = os.path.join(prerand_path, prerand2)
		return load_prerand(prerand1,runs, trial_num)[current_run,:,:], load_prerand(prerand2,runs, trial_num)[current_run,:,:]

	else:
		raise Exception('Select either "durations" or "trials" prerand_type')


def generate_practice_prerands(path_to_pictures):
	# generate random durations
	rng = default_rng()
	durations = np.empty((8,3))
	durations[:,:] = rng.integers([500,4000,3500],[1000,8000,7500],size=(8,3))

	# generate specific balanced trial sequence
	search_type = ['vis','wm']
	array_size = ['two_ullr','four']
	true_response = ['present','absent']
	factorial_df = pd.DataFrame([{'search_type':f1, 'array_size':f2, 'ideal_response':f3} for f1 in search_type for f2 in array_size for f3 in true_response])
	factorial_df['array_size'][1] = 'two_urll'
	factorial_df['array_size'][5] = 'two_urll'
	new_index = [0,5,3,6,4,1,2,7]
	factorial_df = factorial_df.reindex(new_index)
	trials_array = factorial_df.to_numpy()

	# generate random arrangements
	arrangement_arr = np.empty((8,3),dtype='object')
	pics = sorted(os.listdir(path_to_pictures))
	pics = [int(pic.split('.')[0]) for pic in pics]
	for i in range(8):
		arrangement_arr[i,:] = generate_arrangements(arrangement_arr[i,:],pics
										,trials_array[i,1]
										,trials_array[i,2])

	return durations, trials_array, arrangement_arr
	