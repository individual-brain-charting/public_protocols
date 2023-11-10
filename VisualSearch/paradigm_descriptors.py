"""
Event extraction script for visual search and working memory.
Creates tsv files with relevant events.

Himanshu Aggarwal
himanshu.aggarwal@inria.fr
December 2020
"""

import numpy as np
import expyriment as ex
import pandas as pd
import os

while True:
    try:
        sub_num = int(input("Enter subject number: "))
    except ValueError:
        print("Invalid subject number. Expecting an integer.")
        #better try again... Return to the start of the loop
        continue
    else:
        #we're ready to exit the loop.
        break

path = os.getcwd()
data_dir = os.path.join(path, 'data')
data_files = sorted(os.listdir(data_dir))

out_dir = os.path.join(path, 'output_paradigm_descriptors')
try:
	os.mkdir(out_dir)
except OSError:
	pass

out_files = sorted(os.listdir(out_dir))

practice = [file for file in data_files if file.split('_')[0]=='practice' and int(file.split('_')[1])==sub_num]
main = [file for file in data_files if file.split('_')[0]=='protocol' and int(file.split('_')[1])==sub_num]

def create_df(_type,in_data):
	cols = list(in_data.columns)

	out_data = pd.DataFrame(columns=['onset','duration','trial_type'])

	if _type=='Response':
		out_data.onset = in_data['Stimulus_2'].astype('int32')/1000
		if 'Stimulus_2_End' in cols:
			out_data.duration = (in_data['RT'].astype('int32')-200
								-(in_data['Stimulus_2'].astype('int32')
								-in_data['Stimulus_2_End'].astype('int32')))/1000
		else:
			out_data.duration = in_data['RT'].astype('int32')/1000
		out_data.trial_type = np.where((in_data['RT'].astype('int32') > 0), 'response_' + in_data['Check'],
								 'no_response')

	else:
		out_data.onset = in_data[_type].astype('int32')/1000
		out_data.duration = -(in_data[_type].astype('int32')
							-in_data[cols[cols.index(_type)+1]].astype('int32')
							)/1000
		if _type=='Onset':
			out_data.trial_type = 'trial_onset'
		elif _type=='Stimulus_1':
			out_data.trial_type = np.where((in_data['Search_type'] == 'vis'), 'sample_item',
								 'memory_array_' + in_data['Array_size'].str.split('_', 1).str[0])
		elif _type=='Stimulus_2':
			out_data.trial_type = np.where((in_data['Search_type'] == 'vis'),
									 'search_array_' + in_data['Array_size'].str.split('_', 1).str[0]
									 + '_' + in_data['Ideal_Response'], 'probe_item_' 
									 + in_data['Ideal_Response'])
			if 'Stimulus_2_End' not in cols:
				out_data.duration = 200/1000
		elif _type=='Delay':
			out_data.trial_type = 'delay_' + in_data['Search_type']

	return out_data
	
def check_presence(filename,list_of_files):
    if filename in list_of_files:
        count = 0
        for f in list_of_files:
            if f==filename:
                count+=1
        filename = filename.split('.')[0]+'('+str(count)+').'+filename.split('.')[1]
        return check_presence(filename,list_of_files)
    else:
        return filename

def extract_desc(files):
	if len(files) == 0:
		print("Can't find data for subject {}".format(sub_num))
		quit()
	for file in files:
		file_path = os.path.join(data_dir, file)
		data = ex.misc.data_preprocessing.read_datafile(file_path)
		if len(data[0]) == 0:
			print('Data file empty - {}'.format(file))
		else:
			df = pd.DataFrame(data=data[0],columns=data[1])
			subj = df['subject_id'][0]
			df = df.groupby('Run')
			for _run,_df in df:
				event_dfs = []
				for event in ['Onset','Stimulus_1','Delay','Stimulus_2','Response']:
					event_df = create_df(event,_df)
					event_dfs.append(event_df)

				descriptors_df = pd.concat(event_dfs).sort_index(kind='merge')
				subject = '%02d' %int(subj) 
				run = '%02d' %int(_run)
				task = 'vs-wm'

				if file.split('_')[0] == 'protocol':
					save_as = 'task-{}_sub-{}_run-{}_events.tsv'.format(task,subject,run)
				else:
					save_as = 'x_task-{}_sub-{}_run-{}_events.tsv'.format(task,subject,run)

				save_as = check_presence(save_as,out_files)

				save_as = os.path.join(out_dir, save_as)
				descriptors_df.to_csv(save_as,index=False,sep='\t')
			print('Paradigm descriptors calculated for subject {}'.format(subj))

extract_desc(main)
