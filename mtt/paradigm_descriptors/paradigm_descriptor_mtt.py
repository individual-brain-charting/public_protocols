# -*- coding: utf-8 -*-
"""
Script for paradigm descriptors' extraction on the Mental Time Travel protocol

author: Ana Luisa Pinho
e-mail: ana.pinho@inria.fr

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
last_sess = 2
# Number of trials
ntrials = 20
# Labels for the headers in the paradigm descriptor's files
HEADERS = ['onset', 'duration', 'trial_type', 'response_time', 'key']
HEADERS_SH = ['onset', 'duration', 'trial_type']

REFERENCES_WE = ['lermite_observe', 'debit_reduit',
                 'les_animaux_broutent', 'premiere_rencontre',
                 'seconde_rencontre']

REFERENCES_SN = ['dolmens_sous_la_pluie', 'le_grand_pretre_observe',
                 'les_feux_follets_sallument', 'premier_rituel',
                 'second_rituel']

CUES_SPACE = ['sud_ou_nord', 'sud_ou_nord', 'ouest_ou_est', 'ouest_ou_est']

CUES_TIME = ['avant_ou_apres', 'avant_ou_apres']

# Type of list
# pilot_list = []
subject_list = [15]

# folder's name
# fname_prefix = "pilot"
fname_prefix = "sub"

# Pilot or subject?
participant_list = subject_list

# Island story
island = 'we'

# %%
# Create a file for each participant and ...
for participant in participant_list:
    filename_participant_id = fname_prefix + "-" + "%02d" % participant
    raw_fname = 'log_' + island
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
    # ...per block
    for n, data in enumerate(data_list):
        # Read the table
        name = []
        onset = []
        duration = []
        rt = []
        key = []
        for datum in data:
            datum = datum[4:]
            onset.append(float(datum[5]) / 1000)
            duration.append(float(datum[6]) / 1000)
            if datum[4] in REFERENCES_WE + REFERENCES_SN:
                name.append('r' + datum[0] + '_' + datum[1] + '_' + datum[2])
                rt.append('None')
                key.append('None')
            elif datum[4] in CUES_SPACE:
                lcue = 'space'
                name.append('c' + datum[0] + '_' + lcue + '_' + datum[3])
                rt.append('None')
                key.append('None')
            elif datum[4] in CUES_TIME:
                lcue = 'time'
                name.append('c' + datum[0] + '_' + lcue + '_' + datum[3])
                rt.append('None')
                key.append('None')
            else:
                key.append(datum[8])
                if datum[7] == 'None':
                    rt.append(datum[7])
                else:
                    rt.append(float(datum[7]) / 1000)
                if datum[4] == 'response':
                    name.append('response_' + datum[0] + '_' + datum[1] + '_' +
                                datum[2] + '_' + lcue + '_' + datum[3])
                else:
                    name.append('e' + datum[0] + '_' + datum[1] + '_' +
                                datum[2] + '_' + lcue + '_' + datum[3])

        # Create short version lists
        # ... for onsets
        onset_sh = [onset[ost*10:ost*10 + 3] for ost in np.arange(len(onset))]
        onset_sh = np.concatenate(onset_sh).tolist()
        # ... for durations
        duration_eventsum = [round(np.sum(duration[m*10 + 2:m * 10 + 10]), 2)
                             for m in np.arange(len(duration)/10)]
        duration_sh = [duration[k*10:k*10 + 2]
                       for k in np.arange(len(duration))]
        duration_sh = np.concatenate(duration_sh).tolist()
        duration_new = []
        count_sh = 0
        count_eventsum = 0
        for entry in np.arange(len(duration_eventsum) + len(duration_sh)):
            if entry in np.arange(len(duration_eventsum) +
                                  len(duration_sh))[2::3]:
                duration_new.append(duration_eventsum[count_eventsum])
                count_eventsum = count_eventsum + 1
            else:
                duration_new.append(duration_sh[count_sh])
                count_sh = count_sh + 1
        # ... for names
        name_sh = [name[ns*10:ns*10 + 3] for ns in np.arange(len(name))]
        name_sh = np.concatenate(name_sh).tolist()

        # Stack onset, duration and trial_type vectors
#        liste = np.vstack((HEADERS, np.vstack((onset, duration, name, rt,
#                                                  key)).T))

        liste = np.vstack((HEADERS_SH, np.vstack((onset, duration, name)).T))

        liste_sh = np.vstack((HEADERS_SH, np.vstack((onset_sh, duration_new,
                                                     name_sh)).T))
        # Set the output file and its pathway
        filename_output = ('paradigm_descriptors' + '_mtt_' + island + '_' +
                           filename_participant_id + '_run%d.csv' %
                           (n + first_sess))

        filename_output_sh = ('paradigm_descriptors' + '_sh_mtt_' + island +
                              '_' + filename_participant_id + '_run%d.csv' %
                              (n + first_sess))

        path_output = os.path.join(filename_participant_id, filename_output)
        path_output_sh = os.path.join(filename_participant_id,
                                      filename_output_sh)

        # Save new_list in output file
        with open(path_output, 'w') as fp:
            a = csv.writer(fp, delimiter='\t')
            a.writerows(liste)

        with open(path_output_sh, 'w') as fp:
            a = csv.writer(fp, delimiter='\t')
            a.writerows(liste_sh)
