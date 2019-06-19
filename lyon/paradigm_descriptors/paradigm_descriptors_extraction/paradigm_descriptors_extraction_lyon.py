# -*- coding: utf-8 -*-
"""
Script for paradigm descriptors' extraction
on the lyon protocols

author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""
import os
import sys
import pandas as pd

# %% GENERAL PARAMETERS

#Determine if participant is subject or pilot

if int(sys.argv[1]) == 0:
    sub_type = 'MRI_pilot-'
elif int(sys.argv[1]) == 1:
    sub_type = 'sub-'       

#Participant number
sub = '%02d' % (int(sys.argv[2]))

#Session 1 or 2
session = int(sys.argv[3])

# Labels
output_header = ['onset', 'duration', 'trial_type']
input_columns = ['Time', 'Duration', 'Code']
columns_dict = {}

for column in range(len(input_columns)):
        columns_dict[input_columns[column]] = output_header[column]

# %% TASK PARAMETERS
        
task_list = [['moto', 'mcse', 'mveb', 'mvis'],
             ['audi', 'lec1', 'lec2', 'visu']]

response_dict = {'moto': 0, 'mcse': 0, 'mveb': 1, 'mvis': 1,
                 'audi': 0, 'lec1': 1, 'lec2': 0, 'visu': 1}

moto_dict= {11: 'hand_left', 12: 'hand_right',
            21: 'finger_left', 22: 'finger_right',
            31: 'saccade_left', 32: 'sacaade_right',
            51: 'foot_left', 52: 'foot_right',
            61: 'tongue_left', 62: 'tongue_right',
            71: 'fixation_left', 72: 'fixation_right'}

mcse_dict = {11: 'hi_salience_left', 12: 'hi_salience_right',
             61: 'low_salience_left', 62: 'low_salience_right'}

mveb_dict = {20: '2_letters_different', 21: '2_letters_same',
             40: '4_letters_different', 41: '4_letters_same',
             60: '6_letters_different', 61: '6_letters_same'}

mvis_dict = {'test': 'response',
             20: '2_dots', 21: '2_dots_control',
             40: '4_dots', 41: '4_dots_control',
             60: '6_dots', 61: '6_dots_control'}

audi_dict = {'parol': 'speech',
             'yawny': 'yawn',
             'rever': 'reverse',
             'silen': 'silence',
             'pleur': 'tear',
             'rires': 'laugh',
             'animo': 'animals',
             'alpha': 'alphabet'}

lec1_dict = {10: 'word', 20: 'pseudoword', 30: 'random_string',
             'change_to_15': 'start_word',
             'change_to_25': 'start_pseudoword',
             'change_to_35': 'start_random_string'}

lec2_dict = {10: 'attend', 20: 'unattend'}

visu_dict = {10: 'house',
             20: 'visage',
             30: 'animal',
             40: 'scene',
             50: 'tool',
             60: 'pseudoword',
             70: 'characters',
             80: 'target_fruit',
             90: 'scrambled'}

extra_fun_dict = {0: moto_dict, 1: mcse_dict, 2: mveb_dict, 3: mvis_dict,
                  4: audi_dict, 5: lec1_dict, 6: lec2_dict, 7: visu_dict}

# %% PATHS

#General path
my_path = os.getcwd()

#Path to output logfiles
#output_file_path = os.path.join(my_path, 
#                               '../paradigm_descriptors_logfiles/' + task_list[0])

# %% FUNCTIONS

#OPEN INPUT LOGFILE
def open_logfile(sub_type, subject, task, session, run):
    #Path to task logfile folder
    input_file_path = os.path.join(my_path, 
                               '../../protocols/session_' + str(session) + '/loca_' + \
                               task + '_adapt/logfiles')  
    
    #Path to subject logfiles
    if run == 1:
        run_path = os.path.join(input_file_path, 
                                  sub_type + subject + '_1-loca_' + task + '.log')
    if run == 2:
        run_path = os.path.join(input_file_path, 
                                  sub_type + subject + '_2-loca_'+ task + '_bis.log')
    
    #Open them and put them into dataframes
    raw_df = pd.read_csv(run_path, sep='\t', skiprows=3)
    
    return raw_df

#CHANGES COMMON TO ALL PROTOCOLS
def general_changes(subject, task, input_, response):
    #Extract TTL onset
    t0 = input_[(input_['Trial'] == 0) & (input_['Event Type'] == 'Pulse')].Time.values
    
    if t0.size == 0:
        t0 = int(input_[input_['Trial'] == '0'].Time.values)
    
    #Create a second dataframe wih columns of interest
    if task == 'audi':
        output_df = input_[input_['Event Type'] != 'Pulse'] \
        [['Time', 'Duration', 'Code']]
        
    else:
        output_df = input_[input_['Event Type'] == 'Picture'][['Time', 'Duration', 'Code']]
    
    if response == 1:
        output_df = input_[input_['Event Type'] == 'Picture'][['Time','Duration', \
                          'Code', 'Stim Type']]
    
    #Extract the TTL time to all onsets
    output_df['Time'] = output_df['Time'].fillna(0)
    output_df['Time'] = output_df['Time'].astype(int)
    output_df['Time'] -= t0
    
    #Convert time to seconds
    output_df['Time'] /= 10000
    output_df['Duration'] = output_df['Duration'].fillna(0)
    output_df['Duration'] = output_df['Duration'].astype(int)
    output_df['Duration'] /= 10000
    
    #Rename collumns
    output_df.rename(columns = columns_dict, inplace = True)
    if 'Stim Type' in output_df.columns:
        output_df.rename(columns = {'Stim Type': 'response'}, inplace = True)

    if task == 'audi':
        index_counter = 0
        index_list = output_df[output_df['trial_type'] == 'start_sound']['onset'].index
        
        for index in index_list:
            if index_counter == len(index_list) - 1:

                bfix_list = output_df[output_df['trial_type'] == 'Bfix']['onset'].index
                bfix_after_last = bfix_list[bfix_list > index]

                output_df['duration'][index] = output_df['onset'][bfix_after_last[0]] - output_df['onset'] \
                    [index_list[index_counter]]
            else:
                 output_df['duration'][index] = output_df['onset']\
                 [index_list[index_counter + 1]] - output_df['onset']\
                 [index_list[index_counter]]
                 
                 index_counter += 1 
                 
        output_df['duration'] = round(output_df['duration'], 4)

        output_df.dropna(inplace=True)

    
    return output_df


# SAVE THE NEW FILES
def save_output(sub_type, subject, task, input_, run):
    
    #Path to logfile folder
    output_file_path = os.path.join(my_path, 
                                    '../paradigm_descriptors_logfiles/' + task)
    input_.to_csv(os.path.join(output_file_path,
                               sub_type + subject + '_task-' + task + '_run' + \
                               str(run) + '_events.tsv'), sep='\t', index = False)

def cond_change(input_, task_dict):
    for number, condition in task_dict.items():
        input_ = input_.replace(str(number), condition)
        
    return input_

# %% MAIN

extra_fun_index = 4 if session == 2 else 0
    
for task in task_list[session - 1]:
    
    run_index = 1
    #Open the files
    raw_list = [open_logfile(sub_type, sub, task, session, 1),
                open_logfile(sub_type, sub, task, session, 2)]
    
    #Do general changes
    for raw in raw_list:
        gen_output = general_changes(sub, task, raw, response_dict[task])
        extra_output = cond_change(gen_output, extra_fun_dict[extra_fun_index])
        save_output(sub_type, sub, task, extra_output, run_index)
        run_index += 1
        
    extra_fun_index += 1
