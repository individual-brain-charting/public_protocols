"""
Event extraction script for the face_body.
Creates .tsv files with relevant events from logs

Adapted for IBC by:
Himanshu Aggarwal
himanshu.aggarwal@inria.fr
June 2021
"""

import numpy as np
import pandas as pd
import os
import scipy.io

while True:
    try:
        sub_num = int(input("Enter subject number: "))
    except ValueError:
        print("Invalid subject number. Expecting an integer.")
        #better try again... Return to the start of the loop
        continue
    else:
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

practice = []
main = []
for file in data_files:
    if len(file.split('.')) > 1:
        continue
    elif file.split('_')[0]=='pract':
        if file.split('_')[1] == str(sub_num):
            practice.append(os.path.join(data_dir, file, file+'_fLocSession.mat'))
    else:
        if file.split('_')[0] == str(sub_num):
            main.append(os.path.join(data_dir, file, file+'_fLocSession.mat'))

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
        mat = scipy.io.loadmat(file)
        mdata = mat['session']
        mtype = mat['session'].dtype
        ses = {n: mdata[n][0, 0] for n in mtype.names}
        seq = {n: ses['sequence'][n][0, 0] for n in ses['sequence'].dtype.names}
        stim = pd.DataFrame({'run1':np.concatenate(seq['stim_names'].T[0]),
                            'run2':np.concatenate(seq['stim_names'].T[1]),
                            'run3':np.concatenate(seq['stim_names'].T[2]),
                            'run4':np.concatenate(seq['stim_names'].T[3])}).iloc[::12, :]
        stim = stim.reset_index(drop=True)
        
        ons = {'run1':ses['true_onsets'][0][0].flatten(),
                'run2':ses['true_onsets'][0][1].flatten(),
                'run3':ses['true_onsets'][0][2].flatten(),
                'run4':ses['true_onsets'][0][3].flatten()}
        onset = pd.DataFrame.from_dict(ons, orient='index')
        onset = onset.transpose()
        run_end_time = onset.iloc[onset.shape[0]-1, :]+0.5
        onset = onset.iloc[::12, :]
        onset = onset.reset_index(drop=True)

        block = pd.DataFrame(data=seq['block_conds'],
                            columns=['run1','run2','run3','run4'])
        block = block.replace([0, 1, 2, 3, 4, 5],
        ['Baseline','Bodies', 'Characters', 'Faces', 'Objects', 'Places'])
        
        if block.shape not in [(76,4), (16,1)]:
            print('Incomplete session file: {}' .format(file))
        else:
            components = file.split(os.sep)[-1].split('_')
            task = 'face-body'
            subj = '%02d' %int(components[0])
            run_num = 0
            for col in list(onset.columns):
                run_num += 1
                run = '%02d' %int(run_num)

                df = pd.DataFrame(columns=['onset','duration','trial_type'])
                df['onset'] = onset[col]
                df['duration'] = df['onset'].shift(-1,fill_value=run_end_time[col])-df['onset']
                df['trial_type'] = block[col] + '_' + stim[col].str.split('-',1).str[0]
                df['trial_type'] = np.where(df['trial_type'] == 'Baseline_baseline',
                                'Baseline', df['trial_type'])
                df = df.round(2)
                if file.split('_')[0]=='pract':
                    save_as = 'pract_task-{}_sub-{}_run-{}_events.tsv'.format(task,subj,run)
                else:
                    save_as = 'task-{}_sub-{}_run-{}_events.tsv'.format(task,subj,run)
                save_as = check_presence(save_as, out_files)
                save_as = os.path.join(out_dir, save_as)
                df.to_csv(save_as,index=False,sep='\t')
                print('Event file created for subject {}, run {}'.format(subj, run))

extract_desc(main, sub_num)
