# -*- coding: utf-8 -*-
"""
Script for paradigm descriptors' extraction on the Self-Representation effect
protocol

author: Ana Luisa Pinho
e-mail: ana.pinho@inria.fr

Last update: February 2019

"""
import os
import glob
import csv
import numpy as np

# %%
# ========================== TASK PARAMETERS ===============================
# Which file to load? (numbering starts from 0)
input_no = 0
# Sessions's ID (numbering starts from 0)
first_sess = 0
last_sess = 3

# List of participants id
participant_list = [15]

# Subject or Pilot?
# fname_prefix = "pilot"
fname_prefix = "sub"

# Output folders
# folder_name = "pilots/mri_pilots/"
folder_name = "subjects/"

# Output files
HEADER = ['onset', 'duration', 'trial_type']
output_fname = 'paradigm_descriptors_self_ref'

# %%
# ============================== FUNCTIONS ====================================


def stack_descriptors(onsets, durations, names):
    """ Create table of paradigm descriptors """
    table = np.vstack((HEADER, np.vstack((onsets, durations, names)).T))
    return table


def set_output_path(folder, fprefix, particip, output_file, sess):
    """ Define pathway of output files """
    output_path = folder + '/' + fprefix + '-' + \
        '%02d' % particip + '/' + output_file + '_' + fprefix + \
        '-' + '%02d' % particip + '_' + 'run' + \
        str(sess) + '.tsv'
    return output_path


def save_output(file_path, liste):
    """ Save ouput file """
    with open(file_path, 'w') as fp:
        a = csv.writer(fp, delimiter='\t')
        a.writerows(liste)

# %%
# Create a file for each participant and ...
for participant in participant_list:
    filename_participant_id = folder_name + fname_prefix + "-" + \
      "%02d" % participant
    # Set the pathway of the input files
    inputs_path = os.path.abspath(filename_participant_id)
    inputs = glob.glob(os.path.join(inputs_path, "*.xpd"))
    inputs.sort()
    fname = inputs[input_no]
    # Load the file
    input_list = []
    input_list = [line for line in csv.reader(open(fname), delimiter=',')]
    # Parse only the necessary information
    for r, row in enumerate(input_list):
        if row[0] == str(participant):
            break
        else:
            continue
    input_list = input_list[r:]
    # Create a list of runs' list
    data_list = []
    length = 0
    for b, block in enumerate(np.arange(first_sess, last_sess + 1)):
        data_block = []
        idx = b * length
        for dl, line in enumerate(input_list[idx:]):
            if line[1] == str(block):
                data_block.append(line)
            else:
                length = dl
                break
        data_list.append(data_block)
        continue
    # ...per block
    for n, data in enumerate(data_list):
        # Read the table
        name = []
        onset = []
        duration = []
        key = []
        for datum in data:
            if datum[4] == 'instructions':
                onset.append(float(datum[5]) / 1000)
                duration.append(float(datum[6]) / 1000)
                name.append('instructions')
            elif datum[6] in ['self', 'other', '0']:
                onset.append(float(datum[8]) / 1000)
                duration.append(float(datum[9]) / 1000)
                if datum[5] == 'encoding':
                    if datum[10] == 'None':
                        name.append(datum[6] + '_relevance_no_response')
                    else:
                        name.append(datum[6] + '_relevance_with_response')
                elif datum[5] == 'recognition':
                    if datum[10] == 'y':
                        if datum[6] == '0':
                            name.append('new_cr')
                        else:
                            name.append('old_' + datum[6] + '_hit')
                    elif datum[10] == 'g':
                        if datum[6] == '0':
                            name.append('new_fa')
                        else:
                            name.append('old_' + datum[6] + '_miss')
                    elif datum[10] == 'None':
                        if datum[6] == '0':
                            name.append('new_no_response')
                        else:
                            name.append('old_' + datum[6] + '_no_response')
        # Stack onset, duration and trial_type arrays
        pd_table = []
        pd_table = stack_descriptors(onset, duration, name)
        # Set pathway of output file for the present run
        pd_path = set_output_path(folder_name, fname_prefix, participant,
                                  output_fname, n + first_sess)
        # Save list in the output file for the present run
        save_output(pd_path, pd_table)
