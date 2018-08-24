# -*- coding: utf-8 -*-
"""
Paradigm descriptors' estimation for HCP tasks

@author: Ana Luisa Pinho, ana.pinho@inria.fr
contributor: Andres Hoyos Idrobo

Last update: Jan 2017

Note: Run the script with the input csv files per subject and session under the
      same directory
"""

import os
import sys
import csv
import numpy as np
from collections import OrderedDict

import lists
from savefiles import write_csv, write_tsv
from confparser import load_config

# %%
# =============================================================================
# IMPORTANT NOTE: Before running this script, it is mandatory to extract for
#                 each task, the values of the parameters mentioned below with
#                 the parser_eprime_logtxt_HCP.py
#
#
# HCP Emotion task
# Parameters extracted from the log files: SyncSlide.OnsetTime
#                                          face.OnsetTime
#                                          shape.OnsetTime
#                                          StimSlide.OnsetTime
#                                          TwoSecFix.OnsetTime
#                                          Procedure
#
# HCP Gambling task
# Parameters extracted from the log files: SyncSlide.OnsetTime
#                                          QuestionMark.OnsetTime
#                                          FifteenSecFixation.OnsetTime
#                                          TrialType
#
# HCP Motor task
# Parameters extracted from the log files: CountDownSlide.OnsetTime
#                                          LeftHandCue.OnsetTime
#                                          RightHandCue.OnsetTime
#                                          LeftFootCue.OnsetTime
#                                          RightFootCue.OnsetTime
#                                          TongueCue.OnsetTime
#                                          CrossLeft.OnsetTime
#                                          CrossRight.OnsetTime
#                                          CrossCenter.OnsetTime
#                                          Fixdot.OnsetTime
#                                          BlockType
#
# HCP Language task
# Parameters extracted from the log files: SyncSlide.OnsetTime
#                                          PresentBlockChange.OnsetTime
#                                          PresentMathFile.OnsetTime
#                                          PresentStoryFile.OnsetTime
#                                          FeelFreeToRest.OnsetTime
#                                          Procedure
#
# HCP Relational task
# Parameters extracted from the log files: SyncSlide.OnsetTime
#                                          RelationalPrompt.OnsetTime
#                                          ControlPrompt.OnsetTime
#                                          RelationalSlide.OnsetTime
#                                          ControlSlide.OnsetTime
#                                          FixationBlock.OnsetTime
#                                          Procedure
#
# HCP Social task
# Parameters extracted from the log files: CountDownSlide.OnsetTime
#                                          MovieSlide.OnsetTime
#                                          ResponseSlide.OnsetTime
#                                          FixationBlock.OnsetTime
#                                          Type
#
# HCP WM task
# Parameters extracted from the log files: SyncSlide.OnsetTime
#                                          CueTarget.OnsetTime
#                                          Cue2Back.OnsetTime
#                                          Stim.OnsetTime
#                                          Fix15sec.OnsetTime
#                                          Procedure
#                                          StimType
#
# =============================================================================

# %%
# ################### PARAMETERS TO BE CHANGED BY THE USER  ###################
# List of participants
participants = [1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]
# Number of runs
runs = 2
# Name of output files
output = 'paradigm_descriptors'
output_short = 'paradigm_descriptors_sh'
# Name of columns in the outputs files according to BIDS convention
label1 = 'onset'
label2 = 'duration'
label3 = 'trial_type'
# Names of .ini files
hcp_emotion = 'emotion'
hcp_gambling = 'gambling'
hcp_motor = 'motor'
hcp_language = 'language'
hcp_relational = 'relational'
hcp_social = 'social'
hcp_wm = 'wm'


# %%
def list_converter(columnheaders, labels):
    """
    Convert input strings into input lists
    """
    if not isinstance(columnheaders, list):
        if columnheaders is None:
            columnheaders = ''
            labels = ''
        columnheaders = columnheaders.split()
        labels = labels.split()
    return columnheaders, labels


# %%
def make_descriptors(protocol, pts_list, blocks, fname, fname_sh, c1, c2, c3):
    """
    This function reads csv files created by e-prime parser script and generate
    output files with paradigm descriptors for a pre-specified HCP task
    """
    # ######################### GENERAL SETTINGS ##############################
    # Lowercase strings
    protocol = protocol.lower()
    # Set type of session
    if protocol in ['emotion', 'gambling', 'motor', 'language']:
        session = 'HCP1'
    else:
        session = 'HCP2'

    # Set names_map according to the labels to be given to the paradigm
    # descriptors and order of presentation, i.e. the first key of the
    # following dictionary listed it is displayed at the most left side of the
    # table
    names_map = OrderedDict()
    names_map['onsets'] = c1
    names_map['durations'] = c2
    names_map['names'] = c3
    descript = names_map.values()
    # ######################## LOAD .INI FILES ################################
    protocol_file = protocol + '.ini'
    setting = load_config(protocol_file)
    # Convert input strings into input lists
    setting["cue_columnheaders"], setting["cue_labels"] = \
        list_converter(setting["cue_columnheaders"], setting["cue_labels"])
    setting["activecond_columnheaders"], setting["activecond_labels"] = \
        list_converter(setting["activecond_columnheaders"],
                       setting["activecond_labels"])
    # Set disctionaries for types of conditions
    init = {setting["init_columnheader"]: 'sync'}
    cue = dict((cue_key, setting["cue_labels"][ck])
               for ck, cue_key in enumerate(setting["cue_columnheaders"]))
    active_cond = dict((cond_key, setting["activecond_labels"][ack])
                       for ack, cond_key in enumerate(setting[
                           "activecond_columnheaders"]))
    ans = {setting["ans_columnheader"]: 'response'}
    fix = {setting["fix_columnheader"]: 'fixcross'}
    # ############### READ CSV FILES AND GENERATE OUTPUTS #####################
    # Create a file for each participant and ...
    for participant in pts_list:
        participant_id = 'sub-%02d' % participant
        # ... per block
        for block in range(1, blocks + 1):
            # Define input file containing the table
            filename_data = 'extracted_' + participant_id + '_' + protocol + \
                            '_run%d.csv' % block
            path_data = os.path.join(participant_id, session, protocol,
                                     filename_data)
            # Read the table
            data_list = [line for line in csv.reader(open(path_data))]
            # Extract constants
            HEADERS = data_list[0]
            # Go through the table row-by-row
            cond_onset = []
            cond_name = []
            for row in data_list[1:]:
                # Check whether all the elements from the array, apart from the
                # one belonging to trial_type, are empty or not
                # If there's a non-empty cell, it will next read the row
                if any(np.delete(row, HEADERS.index(setting["trialref"]))):
                    # Check what is the index of the first non-empty cell
                    nidx = map(bool, row).index(True)
                    # ################# ONSETS ################################
                    cond_onset.append(float(row[nidx]))
                    if protocol == hcp_social and \
                       HEADERS[nidx] in active_cond.keys():
                        cond_onset.append(float(row[HEADERS.index(
                            'ResponseSlide.OnsetTime')]))
                    # ############### NAMES ###################################
                    # If non-empty cell contains a sync parameter
                    if HEADERS[nidx] in init.keys():
                        cond_name.append(init[HEADERS[nidx]].lower())
                    # If non-empty cell contains a parameter from a cue
                    # condition
                    elif HEADERS[nidx] in cue.keys():
                        cond_name.append(cue[HEADERS[nidx]].lower())
                        if protocol == hcp_wm:
                            if cue[HEADERS[nidx]] == \
                               cue['CueTarget.OnsetTime']:
                                main_stim = setting["stim_control"].lower()
                            elif cue[HEADERS[nidx]] == \
                                    cue['Cue2Back.OnsetTime']:
                                        main_stim = setting["stim_eoi"].lower()
                    # If non-empty cell contains a parameter from an
                    # active condition
                    elif HEADERS[nidx] in active_cond.keys():
                        # Emotion protocol
                        if protocol == hcp_emotion:
                            # Attribute name to face condition
                            if cond_name[-1] == cue['face.OnsetTime'] or \
                               cond_name[-1] == setting["stim_eoi"]:
                                cond_name.append(setting["stim_eoi"].lower())
                            # Attribute name to shape condition
                            elif cond_name[-1] == cue['shape.OnsetTime'] or \
                                    cond_name[-1] == setting["stim_control"]:
                                        cond_name.append(
                                            setting["stim_control"].lower())
                        # WM protocol
                        elif protocol == hcp_wm:
                            # Take the category specific representation
                            stim_category = row[HEADERS.index(
                                setting["stim_type"])].lower()
                            # Create label for condition name according to
                            # main stimuli plus type of category
                            stim_label = main_stim + '_' + stim_category
                            # Add to name conditions' vector
                            cond_name.append(stim_label.lower())
                        # Either Gambling or Motor protocols
                        elif protocol in [hcp_gambling, hcp_motor, hcp_social]:
                            cond_name.append(
                                row[HEADERS.index(
                                    setting["trialref"])].lower())
                            if protocol == hcp_social:
                                cond_name.append(
                                    ans['ResponseSlide.OnsetTime'].lower())
                        # Language protocol
                        else:
                            cond_name.append(
                                active_cond[HEADERS[nidx]].lower())
                    # If non-empty cell contains a parameter from
                    # a fixation condition
                    elif HEADERS[nidx] in fix.keys():
                        cond_name.append(fix[HEADERS[nidx]].lower())
                # If all cells are empty
                else:
                    continue
            # Get value for TTL
            if cond_name[0] in init.values():
                # Protocols with info on synchronization
                TTL = float(cond_onset[0])
            else:
                # Language protocols with no info on synchronization
                TTL = float(cond_onset[0]) - 1000
            # Subtract TTL value from onset and convert it from
            # milliseconds to seconds
            cond_onset_sec = [(onset - TTL) / 1000 for onset in cond_onset]
            # Calculate the durations of the conditions
            cond_duration = [cond_onset_sec[i + 1] - cond_onset_sec[i]
                             for i in np.arange(len(cond_onset_sec) - 1)]
            # Remove fix_onset only used to get the last block duration
            cond_name = cond_name[: -1]
            cond_onset_sec = cond_onset_sec[: -1]
            # Switch strings from uppercase to lowercase and
            # transform spaces into underscores
            cond_name = [name.replace(' ', '_') for name in cond_name]
            cond_name = [name.lower() for name in cond_name]
            # Set dummy session of last condition in the language protocol
            if protocol == hcp_language:
                cond_name[-1] = 'dummy'
            # ###################### STACKED LIST #############################
            # Stack the name, onset and duration regressors in one single list
            stacked_list = lists.stacker(cond_onset_sec, cond_duration,
                                         cond_name, names_map)
            # ################## NON-ACTIVE CONDITIONS ########################
            # Indexes of the rows corresponding to non-active conditions
            noactive_cond_name = init.values() + cue.values() + \
                ans.values() + fix.values()
    #        noactive_cond_name = init.values() + ans.values() + fix.values()
            indexes = [d for d in np.arange(len(stacked_list))
                       if stacked_list[d][descript.index('trial_type')] in
                       noactive_cond_name]
            # ###################### STANDARD LIST ############################
            # Remove rows from stacked_list corresponding to non-active
            # conditions.
            # This is the long-version final list to be printed.
            new_list = np.delete(stacked_list, indexes, axis=0)
            # Generating the outputs
            filename_output_csv = (fname + '_' + protocol + '_' +
                                   participant_id + '_run%d.csv' % block)
            filename_output_tsv = (fname + '_' + protocol + '_' +
                                   participant_id + '_run%d.tsv' % block)
            write_csv(participant_id, session, protocol, filename_output_csv,
                      new_list)
            write_tsv(participant_id, session, protocol, filename_output_tsv,
                      new_list)
            # ##################### SHORT LIST ################################
            new_short_list = lists.short_list(new_list, descript, names_map)
            # Generating the outputs
            filename_output_sh_csv = (fname_sh + '_' + protocol + '_' +
                                      participant_id + '_run%d.csv' % block)
            filename_output_sh_tsv = (fname_sh + '_' + protocol + '_' +
                                      participant_id + '_run%d.tsv' % block)
            write_csv(participant_id, session, protocol,
                      filename_output_sh_csv, new_short_list)
            write_tsv(participant_id, session, protocol,
                      filename_output_sh_tsv, new_short_list)

# Run script
if len(sys.argv) > 1:
    # Argument concerning task name to be given after name of the script file
    task = sys.argv[1]
    if task in [hcp_emotion, hcp_gambling, hcp_motor, hcp_language,
                hcp_relational, hcp_social, hcp_wm]:
        make_descriptors(task, participants, runs, output, output_short,
                         label1, label2, label3)
    else:
        print 'Error: This task does not exist.'
else:
    print 'Error: You must provide the name of the task!'
    print str(''.join(('FORMAT: ipython paradigm_descriptor_HCP.py ',
                       '<NAME_OF_THE_TASK>\n')))
