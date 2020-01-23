# -*- coding: utf-8 -*-
"""
Script for paradigm descriptors' extraction on the Mental-Time-Travel protocol
for both models

author: Ana Luisa Pinho
e-mail: ana.pinho@inria.fr

Last update: November 2019

Compatibility: Python 3.5

"""
import os
import glob
import csv
import numpy as np

# %%
# ========================== GENERAL PARAMETERS ===============================

REFERENCES_WE = ['lermite_observe', 'debit_reduit',
                 'les_animaux_broutent', 'premiere_rencontre',
                 'seconde_rencontre']

REFERENCES_SN = ['dolmens_sous_la_pluie', 'le_grand_pretre_observe',
                 'les_feux_follets_sallument', 'premier_rituel',
                 'second_rituel']

CUES_SPACE = ['sud_ou_nord', 'sud_ou_nord', 'ouest_ou_est', 'ouest_ou_est']

CUES_TIME = ['avant_ou_apres', 'avant_ou_apres']


# *****************************************************************************

# #######################################################

# # Island story
# island = 'we'
# # Participants' list
# participant_list = [1, 4, 5, 7, 8, 9, 12, 13, 14]
# # Which file to load? (numbering starts from 0)
# input_no = 0
# # Sessions's ID (numbering starts from 0)
# first_sess = 0
# last_sess = 2

# #######################################################

'''
Exceptions for IBC participants of island "we":
Participant: input_no, first_sess, last_sess
sub-06: 0, 0, 0
sub-06: 1, 1, 2
sub-11: 0, 0, 1
sub-11: 1, 2, 2
sub-15: 0, 0, 0 (very incomplete)
sub-15: 1, 1, 2
'''

# # Island story
# island = 'we'
# # Participants' list
# participant_list = [06]
# # Which file to load? (numbering starts from 0)
# input_no = 0
# # Sessions's ID (numbering starts from 0)
# first_sess = 0
# last_sess = 0

# #######################################################

# # Island story
# island = 'sn'
# # Participants' list
# participant_list = [1, 4, 5, 6, 7, 9, 11, 12, 13, 14]
# # Which file to load? (numbering starts from 0)
# input_no = 0
# # Sessions's ID (numbering starts from 0)
# first_sess = 0
# last_sess = 2

'''
Exceptions for IBC participants of island "sn":
sub-15: no runs
'''

# #######################################################

# *****************************************************************************

# #### DEFINE PATHWAYS ####
# Parent directory
main_dir = '../../../../analysis_pipeline/ibc_main/neurospin_data/info'
# Subject folder
# fname_prefix = 'pilot'
fname_prefix = 'sub'
# Name of the task protocol
protocol = 'mtt'
# fname of folder with log_files
raw_fname = 'log_' + island

# %%
# ============================== FUNCTIONS ====================================


def create_new_dir(dir_path):
    """
    Creates directory of output files
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def load_log_file(input_dir, prefix, subject, task, logdir, no):
    """
    Load the log files
    """
    filename_participant_id = prefix + "-" + "%02d" % subject
    # Set the pathway of the input files
    inputs_path = os.path.join(input_dir, filename_participant_id, task,
                               logdir)
    inputs = glob.glob(os.path.join(inputs_path, "*.xpd"))
    inputs.sort()
    fname = inputs[no]
    # Load the file
    inlist = []
    inlist = [line for line in csv.reader(open(fname), delimiter=',')]
    return inlist


def stack_descriptors(onsets, durations, names):
    """
    Create table of paradigm descriptors
    """
    # Headers of the paradigm descriptors' files according to BIDS
    header = ['onset', 'duration', 'trial_type']
    table = np.vstack((header, np.vstack((onsets, durations, names)).T))
    return table


def save_output(file_path, liste):
    """
    Save output file
    """
    with open(file_path, 'w') as fp:
        a = csv.writer(fp, delimiter='\t')
        a.writerows(liste)


# %%
# ============================== PARSER =======================================

# %%
# Create a file for each participant and ...
for participant in participant_list:
    # Clean or create output folders
    path1 = os.path.join(main_dir, fname_prefix + '-' + '%02d' % participant,
                         protocol, 'absolute_model_' + island)
    path2 = os.path.join(main_dir, fname_prefix + '-' + '%02d' % participant,
                         protocol, 'relative_model_' + island)
    create_new_dir(path1)
    create_new_dir(path2)
    # Load input files
    input_list = load_log_file(main_dir, fname_prefix, participant, protocol,
                               raw_fname, input_no)
    # Parse the necessary information
    for r, row in enumerate(input_list):
        if row[0] == str(participant):
            break
        else:
            continue
    input_list = input_list[r:]
    # Create a list of sessions' list
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
    # ... for every block
    for n, data in enumerate(data_list):
        # Read the table
        onset = []
        duration = []
        name_abs = []
        name_relat = []
        for datum in data:
            if participant == 15 and datum[1] == '0' and datum[2] != '0' and \
               island == 'we':
                print(datum[8])
                break
            datum = datum[4:]
            # Onsets and durations of conditions
            onset.append(float(datum[5]) / 1000)
            duration.append(float(datum[6]) / 1000)
            # Names of conditions for both models
            # Beginning of a trial
            if datum[4] in REFERENCES_WE + REFERENCES_SN:
                # References of relative model
                name_relat.append(datum[0] + '_all_reference')
            elif datum[4] in CUES_SPACE:
                # References of absolute model for space
                name_abs.append(datum[0] + '_' + datum[1] + '_reference')
                # Space cues
                name_abs.append(datum[0] + '_all_reference_space_cue')
                name_relat.append(datum[0] + '_all_space_cue')
            elif datum[4] in CUES_TIME:
                # References of absolute model for time
                name_abs.append(datum[0] + '_' + datum[2] + '_reference')
                # Time cues
                name_abs.append(datum[0] + '_all_reference_time_cue')
                name_relat.append(datum[0] + '_all_time_cue')
            elif datum[4] == 'response':
                # Events of the relative model...
                # ... for time
                if datum[9] in ['before', 'after']:
                    name_abs.append(datum[0] + '_' + datum[2] + \
                                    '_reference_' + datum[3] + '_event')
                    name_relat.append(datum[0] + '_' + datum[9] + '_' + \
                                      datum[3] + '_event')
                # ... for space
                else:
                    name_abs.append(datum[0] + '_' + datum[1] + \
                                    '_reference_' + datum[3] + '_event')
                    name_relat.append(datum[0] + '_' + datum[9] + 'side_' + \
                                      datum[3] + '_event')
                # Responses for both models
                name_abs.append(datum[0] + '_all_reference_response')
                name_relat.append(datum[0] + '_all_event_response')
            # Events of the absolute model
            else:
                continue
        # Stack onset, duration and trial_type arrays
        abs_descriptors = stack_descriptors(onset, duration, name_abs)
        relat_descriptors = stack_descriptors(onset, duration, name_relat)
        # Output files
        abs_fname = 'paradigm_descriptors_mtt_absolute-model' + '_' + \
                    island + '_' + fname_prefix + '-' + \
                    '%02d' % participant + '_run' + \
                    '%01d' % (n + first_sess) + '.tsv'
        relat_fname = 'paradigm_descriptors_mtt_relative-model' + '_' + \
                      island + '_' + fname_prefix + '-' + \
                      '%02d' % participant + '_run' + \
                      '%01d' % (n + first_sess) + '.tsv'
        output1 = os.path.join(path1, abs_fname)
        output2 = os.path.join(path2, relat_fname)
        print(output1, output2)
        # Save files
        save_output(output1, abs_descriptors)
        save_output(output2, relat_descriptors)
