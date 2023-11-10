# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 13:18:56 2015

author: Ana Luisa Pinho, Bertrand Thirion
e-mail: ana.pinho@inria.fr, bertrand.thirion@inria.fr

Compatibility: Python 2.7

"""
import os
import glob
import csv
import numpy as np

# %%
# ========================== GENERAL PARAMETERS ===============================
# Which file to load? (numbering starts from 0)
input_no = 0
# Sessions's ID (numbering starts from 0)
first_sess = 0
last_sess = 5
# Number of trials
ntrials = 60
# Labels for the headers and probes in the log files
HEADERS = ["onset", "duration", "trial_type"]
PROBES = ['word_present', 'word_absent']

# ============================= For pilots ====================================
# Let this list empty if you're running subjects
pilot_list = []

# # Comment the next three parameters, if you're running subjects
# # Pt folder's name
# fname_prefix = "pilot"
# # Pilot or subject?
# participant_list = pilot_list
# # Labels for the conditions in the log files
# CONDITIONS = ['complexsent', 'consstring', 'jabberwocky', 'pseudolist',
#              'simplesent', 'wordlist']

# ============================ For subjects ===================================
# Let this list empty if you're running pilots
subject_list = [1, 4, 6, 8, 9, 11, 12, 13, 14]

# Comment the next three parameters, if you're running pilots
# Pt folder's name
fname_prefix = "sub"
# Pilot or subject?
participant_list = subject_list
# Labels for the conditions in the log files
CONDITIONS = ['complex_sentence', 'consonant_strings', 'jabberwocky',
              'pseudoword_list', 'simple_sentence', 'word_list']

# %%
# Create a file for each participant and ...
for participant in participant_list:
    filename_participant_id = fname_prefix + "-" + "%02d" % participant
    raw_fname = 'raw/data/'
    # Set the pathway of the input files
    inputs_path = os.path.abspath(filename_participant_id + '/' + raw_fname)
    inputs = glob.glob(os.path.join(inputs_path, "*.xpd"))
    inputs.sort()
    fname = inputs[input_no]
    # Load the file
    input_list = []
    input_list = [line for line in csv.reader(open(fname), delimiter=',')]
    # Parse the necessary information
    for r, row in enumerate(input_list):
        if row[0] == str(participant):
            break
        elif participant_list == pilot_list and participant == 8 and \
                row[0] == '4':
                    break
        else:
            continue
    input_list = input_list[r:]
    # Create a list of sessions' list
    if participant_list == pilot_list and participant in [8, 10]:
        data_list = [input_list[block * ntrials * 3:(block + 1 ) * ntrials * 3]
                     for block in np.arange(first_sess, last_sess + 1)]
    else:
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
        condition_name = []
        condition_type = []
        condition_onset = []
        condition_duration = []
        condition_namtype = []
        for datum in data:
            if participant_list == pilot_list and participant in [8, 10]:
                datum = datum[1:]
            else:
                datum = datum[3:]
            # This is a probe
            if datum[0] in PROBES:
                condition_name.append("probe")
                condition_type.append(datum[0])
                condition_onset.append(float(datum[1]) / 1000)
                condition_duration.append(float(datum[2]) / 1000)
            if not (participant_list == pilot_list and participant == 8):
                datum = datum[1:]
            # This is not a condition; skip it
            if datum[0] not in CONDITIONS:
                continue
            else:
                condition_name.append(datum[0])
                condition_type.append(datum[3])
                condition_onset.append(float(datum[4]) / 1000)
                condition_duration.append(float(datum[5]) / 1000)
        # Merge label of S0 and S1 conditions with type of syntax
        for i in np.arange(len(condition_name)):
            if condition_name[i] not in ['probe', 'jabberwocky',
                                         condition_type[i]]:
                namtype = condition_name[i] + '_' + condition_type[i]
            else:
                namtype = condition_name[i]
            condition_namtype.append(namtype)
        # Lowercase for all string labels of conditions' names
        condition_namtype = [label.lower() for label in condition_namtype]
        # Stack onset, duration and trial_type vectors
        new_list = np.vstack((HEADERS, np.vstack((condition_onset,
                                                  condition_duration,
                                                  condition_namtype)).T))
        # Set the output file and its pathway
        filename_output = ('paradigm_descriptors' + '_' +
                           filename_participant_id + '_run%d.tsv' %
                           (n + first_sess))
        path_output = os.path.join(filename_participant_id, filename_output)
        # Save new_list in output file
        with open(path_output, 'w') as fp:
            a = csv.writer(fp, delimiter='\t')
            a.writerows(new_list)
