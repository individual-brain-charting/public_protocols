"""
Event extraction script for motion perception task.

Himanshu Aggarwal
himanshu.aggarwal@inria.fr
January 2021
"""

import pandas as pd
import os
import numpy as np

def take_input():
    while True:
        try:
            sub_num = int(input("Enter subject number: "))
            design = int(input("Output 1- with responses and stim\n or 2- just the stimuli?: "))
        except ValueError:
            print("Invalid input. Expecting integers.")
            continue
        else:
            break

    return sub_num, design


def setup_io_files(sub_num):
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
    return data_dir, main, practice, out_dir, out_files


def check_presence(filename, list_of_files):
    if filename in list_of_files:
        count = 0
        for f in list_of_files:
            if f==filename:
                count+=1
        filename = filename.split('.')[0]+'('+str(count)+').'+filename.split('.')[1]
        return check_presence(filename,list_of_files)
    else:
        return filename


def extract_desc(design, file, data_dir, out_files, out_dir):

    file_path = os.path.join(data_dir, file)
    data = pd.read_csv(file_path)
    if len(data) == 0:
        print('Data file empty - {}'.format(file))
        return 0
    else:
        components = file.split('_')

        task = components[0]
        sub = components[1]
        run = components[2]


        stimuli = data.loc[~data.events.isin(['att_fix_green', 'att_fix_white',
                        'att_fix_magenta', 'att_fix_red', 'att_fix_yellow',
                        'att_fix_blue', 'y'])].reset_index(drop=True)
        stimuli['duration'] = stimuli['time_points'].shift(-1)-stimuli['time_points']
        stimuli = stimuli[:-1]
        stimuli = stimuli.rename(columns={'time_points': 'onset', 'events': 'trial_type'})
        stimuli = stimuli[['onset', 'duration', 'trial_type']]
        stimuli = stimuli.round(1)

        fields = pd.read_csv('seq/task-motion_display_field_seq_1.csv')
        fields = list(np.repeat(fields['Display Field Sequence'], 3))

        motion = pd.read_csv('seq/task-motion_trial_type_seq_1.csv')
        motion = list(motion['Trial type Sequence'])

        new_fields = []
        for field_, motion_ in zip(fields, motion):
            if motion_ == 'incoherent' or motion_ == 'coherent':
                for i in range(0, 6):
                    new_fields.append(field_)
            else:
                new_fields.append(field_)
            new_fields.append('')
        new_fields.append(field_)
        new_fields.append('')

        stimuli['fields'] = new_fields
        stimuli['trial_type'] = stimuli['fields'] + '_' + stimuli['trial_type']
        stimuli = stimuli.drop(columns=['fields'])
        stimuli = stimuli.replace('_iti_fix', 'iti_fix')

        if design == 1:
            responses = data.loc[data.events.isin(['y'])].reset_index(drop=True)
            responses = responses.rename(columns={'time_points': 'onset', 'events': 'trial_type'})
            responses["duration"] = ""
            responses = responses[['onset', 'duration', 'trial_type']]
            responses = responses.round(1)

            stimuli = stimuli.append(responses, ignore_index=False)
            stimuli = stimuli.sort_values('onset')

        save_as = f'{task}_{sub}_{run}_events.tsv'

        save_as = check_presence(save_as, out_files)
        save_as = os.path.join(out_dir, save_as)
        stimuli.to_csv(save_as, index=False, sep='\t')

    print('Event file created for {}, {}'.format(sub, run))
    return 1


if __name__ == "__main__":

    sub_num, design = take_input()
    data_dir, main, practice, out_dir, out_files = setup_io_files(sub_num)
    
    if len(main) == 0:
        print("Can't find data for subject {}".format(sub_num))
        quit()
    else:
        for file in main:
            extract_desc(design, file, data_dir, out_files, out_dir)
