"""
Event extraction script for the reward_proc.
Creates .tsv files with relevant events from .pkl logs

Adapted for IBC by:
Himanshu Aggarwal
himanshu.aggarwal@inria.fr
January 2021
"""

import numpy as np
import pandas as pd
import os
from config import load_obj

while True:
    try:
        sub_num = int(input("Enter subject number: "))
    except ValueError:
        print("Invalid subject number. Expecting an integer.")
        #better try again... Return to the start of the loop
        continue
    else:
        #age was successfully parsed!
        #we're ready to exit the loop.
        break

path = os.getcwd()
data_dir = os.path.join(path, 'Output')
data_files = sorted(os.listdir(data_dir))

out_dir = os.path.join(path, 'output_paradigm_descriptors')
try:
    os.mkdir(out_dir)
except OSError:
    pass
out_files = sorted(os.listdir(out_dir))

practice = []
main = []
for file in data_files:
    if file == 'ancillary':
        continue
    elif file.split('_')[0][-5:]=='pract':
        if file.split('pract')[-2:] == str(sub_num):
            practice.append(file)
    else:
        if file.split('_')[0].strip('sub') == str(sub_num):
            main.append(file)

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


def extract_desc(files, sub_num):
    if len(files) == 0:
        print("Can't find data for subject {}".format(sub_num))
        quit()
    for file in files:
        file_path = os.path.join(data_dir, file)
        data = load_obj(file_path)
        if len(vars(data)) == 0:
            print('Data file empty - {}'.format(file))
            continue
        else:
            components = file.split('_')

            task = 'reward-proc'
            run = '%02d' %int(components[1][-1])

            check_pract = components[0].split('pract')
            is_pract = type(check_pract) is list
            if is_pract:
                subj = '%02d' %int(''.join(list(filter(lambda x: x in '0123456789.',check_pract[0]))))
            else:
                subj = '%02d' %int(''.join(list(filter(lambda x: x in '0123456789.',components[0]))))

            attributes = pd.DataFrame({'reverseTrial': data.sessionInfo[0].reverseTrial,
                                    'stim1_left': data.sessionInfo[0].stim1_left,
                                    'selectedStim': data.sessionInfo[0].selectedStim,
                                    'payOut': data.sessionInfo[0].payOut
                                    })
            num_trials = len(attributes)
            attributes['stim'] = np.where(attributes.stim1_left == True,
                                'purple-left_green-right','purple-right_green-left')
            attributes['resp'] = np.where(attributes.selectedStim == 2,
                                attributes['stim'].str.split('_', 1).str[1],
                                attributes['stim'].str.split('_', 1).str[0])
            attributes['resp'] = np.where(attributes.selectedStim == 0, np.NaN, attributes['resp'])
            responses = list(attributes['resp'].str.split('-', 1).str[0])
            attributes['swtch'] = ['switch' if responses[i]!=responses[i-1] else 'stay' for i in range(0,len(responses))]
            attributes['swtch'][0] = 'init'
            attributes['resp'] = attributes['resp'] + '_' + attributes['swtch']

            attributes['out'] = attributes['payOut'].abs().astype(int).astype(str)
            attributes['gain'] = np.where(attributes.payOut >= 0,'+','-')
            attributes['out'] = attributes['gain'] + attributes['out']
            attributes['out'] = np.where(attributes.payOut == 0,np.NaN,attributes['out'])

            attributes = attributes.drop(columns=['stim1_left','selectedStim','payOut',
                                        'stim','swtch','gain'])
            attributes['empty'] = ['' for i in range(0,num_trials)]
            attributes['empty2'] = ['' for i in range(0,num_trials)]
            attributes['reverseTrial'] = ['' for i in range(0,num_trials)]
            attributes = attributes[['empty','reverseTrial', 'resp', 'out','empty2']]
            attributes = attributes.stack().reset_index()
            onsets = pd.DataFrame(data.sessionInfo[0].sessionOnsets.__dict__)
            onsets.columns = ['prefix','stim','resp','out','postfix']
            onsets = onsets.stack().reset_index()
            onsets['trial_type'] = np.where((onsets['level_1'] == 'resp') | (onsets['level_1'] == 'out'),
                                onsets['level_1'] + '_' + attributes[0].astype(str), onsets['level_1'])
            onsets = onsets.drop(columns=['level_0','level_1'])
            onsets['duration'] = onsets[0].shift(-1, fill_value=data.sessionInfo[0].EndTime)-onsets[0]
            onsets = onsets[[0,'duration','trial_type']]
            onsets.columns = ['onset','duration','trial_type']
            onsets = onsets.round(3)

            if file.split('_')[0][-5:]=='pract':
                save_as = 'pract_task-{}_sub-{}_run-{}_events.tsv'.format(task,subj,run)
            else:
                save_as = 'task-{}_sub-{}_run-{}_events.tsv'.format(task,subj,run)

            save_as = check_presence(save_as,out_files)
            save_as = os.path.join(out_dir, save_as)
            onsets.to_csv(save_as,index=False,sep='\t')
        print('Event file created for subject {}, run {}'.format(subj, run))

extract_desc(main, sub_num)
