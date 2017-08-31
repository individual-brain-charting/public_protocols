# -*- coding: utf-8 -*-
"""
Paradigm descriptors' estimation for ARCHI protocols

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
# ARCHI standard
# Parameters extracted from the log files: mot1.OnsetTime
#                                          StimuliAudio.OnsetTime
#                                          check1.OnsetTime
#                                          StimuliAudioClic.OnsetTime
#                                          rien.OnsetTime
#                                          Manip
#
# ARCHI spatial
# Parameters extracted from the log files: StartOfBloc.OnsetTime
#                                          SideConsigne.OnsetTime
#                                          PalmConsigne.OnsetTime
#                                          ObjectgraspConsigne.OnsetTime
#                                          ObjectorientConsigne.OnsetTime
#                                          Hand.OnsetTime
#                                          SaccadeTarget1.OnsetTime
#                                          cross6000.OnsetTime
#                                          delai
#                                          Running
#
# ARCHI social
# Parameters extracted from the log files: StartOfBloc.OnsetTime
#                                          mot1.OnsetTime
#                                          ToMaudio.OnsetTime
#                                          Pourquoi.OnsetTime
#                                          SpeechSound.OnsetTime
#                                          NonSpeechSound.OnsetTime
#                                          TriangleMovie.OnsetTime
#                                          FilmDuration
#                                          BlankTrials.OnsetTime
#                                          RestEndOfBloc.OnsetTime
#                                          typetask
#
# ARCHI emotional
# Parameters extracted from the log files: StartOfBloc.OnsetTime
#                                          Question.OnsetTime
#                                          regardImage3.OnsetTime
#                                          ChoixBloc.OnsetTime
#                                          delai
#                                          typetask
#                                          Running
# =============================================================================

# %%
# ######################## GENERAL PARAMETERS #################################
# List of participants
participants = [16]
# Number of runs
runs = 2
# Name of current session
session_name = '3ARCHI'
# Output files
output = 'paradigm_descriptors'
output_short = 'paradigm_descriptors_sh'
# Name of columns in the outputs files according to BIDS convention
label1 = 'onset'
label2 = 'duration'
label3 = 'trial_type'
# Names of .ini files
loc_standard = 'standard'
loc_spatial = 'spatial'
loc_social = 'social'
loc_emot = 'emotionnel'
# Names of all possible sessions
session1 = 'screening3'
session2 = '3ARCHI'


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
def make_descriptors(protocol, pts_list, session, blocks, fname, fname_sh, c1,
                     c2, c3):
    """
    This function reads csv files created by e-prime parser script and generate
    output files with paradigm descriptors for a pre-specified HCP task
    """
    # ######################### GENERAL SETTINGS ##############################
    # Lowercase strings
    protocol = protocol.lower()
    # Set names_map according to the labels to be given to the paradigm
    # descriptors and order of presentation, i.e. the first key of the
    # following dictionary listed, it is displayed at the most left side of the
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
    setting["init_columnheaders"], setting["init_label"] = \
        list_converter(setting["init_columnheaders"], setting["init_label"])
    setting["cue_columnheaders"], setting["cue_labels"] = \
        list_converter(setting["cue_columnheaders"], setting["cue_labels"])
    setting["activecond_columnheaders"], setting["activecond_labels"] = \
        list_converter(setting["activecond_columnheaders"],
                       setting["activecond_labels"])
    setting["fix_columnheaders"], setting["fix_labels"] = \
        list_converter(setting["fix_columnheaders"], setting["fix_labels"])
    setting["names_columnheaders"], setting["names_labels"] = \
        list_converter(setting["names_columnheaders"], setting["names_labels"])
    # Set disctionaries for types of conditions
    init = dict((init_key, setting["init_label"][ik])
                for ik, init_key in enumerate(setting["init_columnheaders"]))
    cue = dict((cue_key, setting["cue_labels"][ck])
               for ck, cue_key in enumerate(setting["cue_columnheaders"]))
    active_cond = dict((cond_key, setting["activecond_labels"][ack])
                       for ack, cond_key in enumerate(setting[
                           "activecond_columnheaders"]))
    ans = {setting["ans_columnheader"]: 'response'}
    fix = dict((fix_key, setting["fix_labels"][fk])
               for fk, fix_key in enumerate(setting["fix_columnheaders"]))
    names = dict((name_key, setting["names_labels"][nk])
                 for nk, name_key in enumerate(setting["names_columnheaders"]))
    # Create a file for each participant and ...
    for participant in pts_list:
        participant_id = "%02d" % participant
        foldername_participant_id = 'pilot-' + participant_id
        localizer_name = 'localizer_' + protocol
        # ... per block
        for block in range(1, blocks + 1):
            # Define input file containing the table
            filename_data = 'extracted_localizer_' + protocol + '-' + \
                            participant_id + '-' + '%d.csv' % block
            path_data = os.path.join(foldername_participant_id, session,
                                     localizer_name, filename_data)
            # If input file does not exist, go to the next run
            if not os.path.exists(path_data):
                continue
            # Read the table
            data_list = [line for line in csv.reader(open(path_data))]
            # Extract constants
            HEADERS = data_list[0]
            # Go through the table row-by-row
            cond_onset = []
            cond_onset_new = []
            cond_duration = []
            cond_duration_new = []
            cond_name = []
            for row in data_list[1:]:
                # Check whether the row without trial_type is empty or not.
                row_del = np.delete(row, [HEADERS.index(setting["trialref"])])
                # If it is not,
                if any(row_del):
                    nidx = map(bool, row).index(True)
                    # ################# ONSETS ################################
                    cond_onset.append(float(row[nidx]))
                    # Sync
                    if HEADERS[nidx] in init.keys():
                        cond_onset.insert(0, cond_onset.pop(-1))
                    # Localizer Spatial
                    if protocol == loc_spatial:
                        if HEADERS[nidx] in cue.keys():
                            cond_onset.insert(-3, cond_onset.pop(-1))
                        elif HEADERS[nidx] == setting["time_delay"]:
                            cond_onset.pop()
                    # Localizer Social
                    elif protocol == loc_social:
                        # Responses
                        if HEADERS[nidx] in ['mot1.OnsetTime',
                                             'ToMaudio.OnsetTime']:
                            cond_onset.append(float(row[HEADERS.index(
                                                    ans.keys()[0])]))
                        # End of session
                        elif HEADERS[nidx] in init.keys():
                            cond_onset.append(float(row[HEADERS.index(
                                'RestEndOfBloc.OnsetTime')]))
                    # Localizer Emotional
                    elif protocol == loc_emot:
                        if row[HEADERS.index(setting["trialref"])] is not '':
                            cond_onset.pop()
                            if row[HEADERS.index(setting["trialref"])] == '0':
                                cond_onset.append(-1)
                        # End of session
                        elif HEADERS[nidx] in init.keys():
                            cond_onset.append(float(row[HEADERS.index(
                                'ChoixBloc.OnsetTime')]))
                        else:
                            cond_onset.append(float(row[HEADERS.index(
                                'regardImage3.OnsetTime')]))
                    # ############### DURATIONS ###############################
                    # Localizer Spatial
                    if protocol == loc_spatial:
                        if row[HEADERS.index(setting["time_delay"])] is not '':
                            if HEADERS[nidx] == setting["time_delay"]:
                                cond_duration.pop()
                            cond_duration.append(float(row[HEADERS.index(
                                                 setting["time_delay"])]))
                        elif HEADERS[nidx] in init.keys():
                            cond_duration.insert(0, -1)
                        else:
                            cond_duration.append(-1)
                    # Localizer Social
                    elif protocol == loc_social:
                        if HEADERS[nidx] == 'TriangleMovie.OnsetTime':
                            cond_duration.append(float(row[HEADERS.index(
                                                       'FilmDuration')]))
                        elif HEADERS[nidx] in ['SpeechSound.OnsetTime',
                                               'NonSpeechSound.OnsetTime']:
                            cond_duration.append(
                                setting["duration_audio_cond"])
                        elif HEADERS[nidx] in init.keys():
                            # Sync
                            cond_duration.insert(0, -1)
                            # End of Session
                            cond_duration.append(setting["duration_rest"])
                        elif HEADERS[nidx] == 'BlankTrials.OnsetTime':
                            cond_duration.append(setting["duration_blank"])
                        elif HEADERS[nidx] == 'RestEndOfBloc.OnsetTime':
                            cond_duration.append(setting["duration_rest"])
                        # ToM video and audio
                        else:
                            cond_duration.extend([-1, -1])
                    # Localizer Emotional
                    elif protocol == loc_emot:
                        if row[HEADERS.index(setting["procedure"])] == \
                           'MainLocalizer':
                                if row[HEADERS.index(
                                   setting["trialref"])] != '0':
                                    cond_duration.pop()
                                cond_duration.append(float(row[HEADERS.index(
                                                     setting["time_delay"])]))
                        elif HEADERS[nidx] in init.keys():
                            # Sync
                            cond_duration.insert(0, -1)
                            # End of Session
                            cond_duration.append(setting["duration_rest"])
                        else:
                            cond_duration.extend([-1, -1])
                    # ############### NAMES ###################################
                    # Cues
                    if HEADERS[nidx] in cue.keys():
                        cond_name.append(cue[HEADERS[nidx]].lower())
                        # Localizer Spatial
                        if protocol == loc_spatial:
                            cond_name.insert(-3, cond_name.pop(-1))
                        # Localizer Emotional
                        elif protocol == loc_emot:
                            cond_name.append(names[row[HEADERS.index(
                                setting["procedure"])]].lower())
                    # Active conditions
                    elif HEADERS[nidx] in active_cond.keys():
                        # Localizer Standard
                        if protocol == loc_standard:
                            cond_name.append(names[row[HEADERS.index(
                                setting["trialref"])]].lower())
                        # Localizer Spatial
                        elif protocol in [loc_spatial]:
                            cond_name.append(names[row[HEADERS.index(
                                setting["trialref"])]].lower())
                        # Localizer Social
                        elif protocol == loc_social:
                            # Active conditions that require response
                            if HEADERS[nidx] == 'TriangleMovie.OnsetTime':
                                if row[HEADERS.index(
                                   setting["trialref"])] == '1':
                                        cond_name.append(setting["stim_eoi"])
                                elif row[HEADERS.index(
                                     setting["trialref"])] == '2':
                                        cond_name.append(
                                            setting["stim_control"])
                            # Other conditions
                            else:
                                cond_name.append(active_cond[
                                                 HEADERS[nidx]].lower())
                            # Response conditions
                            if HEADERS[nidx] in ['mot1.OnsetTime',
                                                 'ToMaudio.OnsetTime']:
                                cond_name.append(ans.values()[0].lower())
                    # Blank/fixation condition
                    elif HEADERS[nidx] in fix.keys():
                        # Localizer Social
                        if HEADERS[nidx] == 'BlankTrials.OnsetTime':
                            cond_name.append(
                                fix['BlankTrials.OnsetTime'].lower())
                        # Other Localizers
                        else:
                            cond_name.append(fix[HEADERS[nidx]].lower())
                    # Sync and End_of_Session
                    elif HEADERS[nidx] in init.keys():
                        # #### Sync ####
                        cond_name.insert(0, init[HEADERS[nidx]].lower())
                        # #### End of Session ####
                        # Localizer Social
                        if protocol == loc_social:
                            cond_name.append(
                                fix['RestEndOfBloc.OnsetTime'].lower())
                        # Localizer Emotional
                        elif protocol == loc_emot:
                            cond_name.append(fix.values()[0])
                    # Blank periods with no onsets (applicable for loc
                    # emotional)
                    else:
                        if protocol == loc_spatial:
                            pass
                        elif protocol == loc_emot:
                            cond_name.append(names[row[HEADERS.index(
                                                   setting["procedure"])]])
                            if row[HEADERS.index(setting["trialref"])] != '0':
                                cond_name.pop()
                # If all cells are empty
                else:
                    continue
            # Get value for TTL
            TTL = float(cond_onset[0])
            # Remove -1 elements from array containing the onsets
            cond_onset_new = cond_onset
            if protocol == loc_emot:
                while np.any([onset == -1 for onset in cond_onset_new]):
                    cond_onset_new = [cond_onset_new[k+1] -
                                      setting["duration_blank"] -
                                      cond_duration[k]
                                      if cond_onset_new[k] == -1 and
                                      cond_onset_new[k+1] != -1
                                      else cond_onset_new[k]
                                      for k in np.arange(len(cond_onset_new))]
            # Subtract TTL value from onset and convert it from
            # milliseconds to seconds
            cond_onset_sec = [(onset - TTL) / 1000 for onset in cond_onset_new]
            # Calculate the durations of the conditions
            if protocol == loc_spatial:
                cond_duration_new = [cond_onset_sec[i + 1] - cond_onset_sec[i]
                                     if cond_duration[i] == -1
                                     else cond_onset_sec[i + 1] -
                                     cond_onset_sec[i] -
                                     setting["duration_blank"]/1000 -
                                     cond_duration[i]/1000 for i in
                                     np.arange(len(cond_onset_sec) - 1)]
                cond_duration_new.append(setting["duration_rest"])
            elif protocol == loc_social:
                cond_duration_new = [cond_onset_sec[i + 1] - cond_onset_sec[i]
                                     if cond_duration[i] == -1
                                     else cond_duration[i] / 1000
                                     for i in np.arange(len(cond_onset_sec))]
            elif protocol == loc_emot:
                cond_duration_new = [cond_onset_sec[i + 1] - cond_onset_sec[i]
                                     if cond_duration[i] == -1
                                     else cond_onset_sec[i + 1] -
                                     cond_onset_sec[i] - cond_duration[i]/1000
                                     for i in
                                     np.arange(len(cond_onset_sec) - 1)]
                cond_duration_new = [duration_new -
                                     setting["duration_blank"]/1000
                                     if cond_name[n] == names['MainLocalizer']
                                     else duration_new for n, duration_new in
                                     enumerate(cond_duration_new)]
                cond_duration_new.append(setting["duration_rest"])
            # and finally for Localizer Standard
            else:
                cond_duration_new = [cond_onset_sec[i + 1] - cond_onset_sec[i]
                                     for i in
                                     np.arange(len(cond_onset_sec) - 1)]
                cond_duration_new.append(setting["duration_rest"])
            # ###################### STACKED LIST #############################
            # Stack the name, onset and duration regressors in one single list
            stacked_list = lists.stacker(cond_onset_sec, cond_duration_new,
                                         cond_name, names_map)
            # ################## NON-ACTIVE CONDITIONS ########################
            # Indexes of the rows corresponding to non-active conditions
            if protocol == loc_emot:
                noactive_cond_name = init.values() + fix.values() + \
                    [names['MainLocalizer']]
            else:
                noactive_cond_name = init.values() + cue.values() + \
                                     fix.values()
            indexes = [d for d in np.arange(len(stacked_list))
                       if stacked_list[d][descript.index('trial_type')] in
                       noactive_cond_name]
            # ###################### STANDARD LIST ############################
            # Remove rows from stacked_list corresponding to non-active
            # conditions
            # This is the long-version final list to be printed.
            new_list = np.delete(stacked_list, indexes, axis=0)
            # Generating the outputs
            filename_output_csv = (fname + '_' + protocol + '_' +
                                   participant_id + '_run%d.csv' % block)
            filename_output_tsv = (fname + '_' + protocol + '_' +
                                   participant_id + '_run%d.tsv' % block)
            write_csv(foldername_participant_id, session, localizer_name,
                      filename_output_csv, new_list)
            write_tsv(foldername_participant_id, session, localizer_name,
                      filename_output_tsv, new_list)
            # ################### SHORT LIST 4 ITEMS ##########################
            # ... only applicable for Localizer Emotional
            if protocol == loc_emot:
                new_chunk_list = lists.four_short_list(new_list, descript,
                                                       names_map)
                # Generating the outputs
                filename_output_sh_csv = (fname_sh + '_' + protocol + '_' +
                                          participant_id +
                                          '_run%d.csv' % block)
                filename_output_sh_tsv = (fname_sh + '_' + protocol + '_' +
                                          participant_id +
                                          '_run%d.tsv' % block)
                write_csv(foldername_participant_id, session, localizer_name,
                          filename_output_sh_csv, new_chunk_list)
                write_tsv(foldername_participant_id, session, localizer_name,
                          filename_output_sh_tsv, new_chunk_list)
            # ##################### SHORT LIST ################################
            else:
                new_short_list = lists.short_list(new_list, descript,
                                                  names_map)
                # Generating the outputs
                filename_output_sh_csv = (fname_sh + '_' + protocol + '_' +
                                          participant_id +
                                          '_run%d.csv' % block)
                filename_output_sh_tsv = (fname_sh + '_' + protocol + '_' +
                                          participant_id +
                                          '_run%d.tsv' % block)
                write_csv(foldername_participant_id, session, localizer_name,
                          filename_output_sh_csv, new_short_list)
                write_tsv(foldername_participant_id, session, localizer_name,
                          filename_output_sh_tsv, new_short_list)

# Run script
if len(sys.argv) > 1:
    # Argument concerning task name to be given after name of the script file
    task = sys.argv[1]
    if task in [loc_standard, loc_spatial, loc_social, loc_emot]:
        if len(sys.argv) > 2:
            session_name = sys.argv[2]
            if session_name in [session1, session2]:
                make_descriptors(task, participants, session_name, runs,
                                 output, output_short, label1, label2, label3)
            else:
                print 'Error: Session does not exist.'
        else:
            print 'Error: You must provide the name of the session!'
            print str(''.join(('FORMAT: ipython paradigm_descriptor_ARCHI.py ',
                               '<NAME_OF_THE_TASK> <NAME_OF_THE_SESSION>\n')))
    else:
        print 'Error: Task does not exist.'
else:
    print 'Error: You must provide the name of the task!'
    print str(''.join(('FORMAT: ipython paradigm_descriptor_ARCHI.py ',
                       '<NAME_OF_THE_TASK> <NAME_OF_THE_SESSION>\n')))
