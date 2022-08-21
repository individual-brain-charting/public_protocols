"""
Event extraction script for color perception task.

Himanshu Aggarwal
himanshu.aggarwal@inria.fr
November 2021
"""

import pandas as pd
import os

while True:
    try:
        sub_num = int(input("Enter subject number: "))
        design = int(input(
                    "Output 1- with responses or 2- just stimuli?: "))
    except ValueError:
        print("Invalid subject number. Expecting an integer.")
        continue
    else:
        break

path = os.getcwd()
data_dir = os.path.join(path, 'log')
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
    if file.split('_')[0]=='pract':
        if int(file.split('_')[1].split('-')[1]) == sub_num:
            practice.append(file)
    elif file.split('_')[0]=='par':
        continue
    else:
        if int(file.split('_')[1].split('-')[1]) == sub_num:
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
        data = pd.read_csv(file_path)
        if len(data) == 0:
            print('Data file empty - {}'.format(file))
            continue
        else:
            components = file.split('_')

            task = components[0]
            sub = components[1]
            run = components[2]

            blanks = data.loc[data.event.isin(['blank',
                     'fix', 'End'])].reset_index(drop=True)
            stimuli = data.loc[~data.event.isin(['blank',
                     'y', 'No response', 'Start'])].reset_index(drop=True)
            
            blanks = blanks[(blanks.index % 13 == 0) | (blanks.event=='fix')]
            stimuli = stimuli[(stimuli.index % 13 == 0) | (stimuli.event=='fix')]
            block_names = stimuli['event'].str.split(os.sep).str[1].str.split(
                            '_').str[0].dropna()
            stimuli.update(block_names)

            stimuli['t'].update(blanks['t'])

            stimuli['duration'] = stimuli['t'].shift(-1)-stimuli['t']
            stimuli = stimuli[:-1]
            stimuli = stimuli.rename(columns={'t': 'onset', 'event': 'trial_type'})
            stimuli = stimuli[['onset', 'duration', 'trial_type']]
            stimuli = stimuli.round(1)

            if design == 1:
                probes = data.loc[~data.event.isin(['blank', 'fix', 'Start', 'End', 'y'])]
                probes = probes.loc[probes['event'].duplicated(keep='first')]
                probes['event'] = '1-back'
                resp = data.loc[data.event.isin(['y'])]
                probes_resp = probes.append(resp, ignore_index=False)
                probes_resp = probes_resp.sort_values('t')

                probes_resp = probes_resp.rename(columns={'t': 'onset', 'event': 'trial_type'})
                probes_resp["duration"] = ""
                probes_resp = probes_resp[['onset', 'duration', 'trial_type']]
                probes_resp = probes_resp.round(1)

                stimuli = stimuli.append(probes_resp, ignore_index=False)
                stimuli = stimuli.sort_values('onset')

            save_as = f'{task}_{sub}_{run}_events.tsv'

            save_as = check_presence(save_as,out_files)
            save_as = os.path.join(out_dir, save_as)
            stimuli.to_csv(save_as,index=False,sep='\t')

        print('Event file created for {}, {}'.format(sub, run))

extract_desc(main, sub_num)
# extract_desc(practice, sub_num)