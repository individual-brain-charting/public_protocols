# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:39:58 2016

@author: Ana Luisa Pinho
e-mail: ana.pinho@inria.fr

"""

import os
import sys
import glob
import csv
import random
import numpy as np

import dirfiles
from confparser import load_config


def randomization(setting, island):
    """
    Performs the randomization of the csv files containing the names and
    correspondence of references, cues and events. Creates a final csv file
    with the randomized stim to be loaded by the protocol mtt.py
    """
    # Define the pathway of the inputs directory
    stimuli_path = os.path.abspath(setting['stim_dir'])

    # List input csv files
    stim_filenames = dirfiles.listdir_csvnohidden(stimuli_path)
    stim_filenames.sort(reverse=True)
    if island == 'we':
        stim_filenames.pop(1)
    elif island == 'sn':
        stim_filenames.pop(0)
    else:
        pass

    # Stimuli of the protocol
    stim_list = [[i for i in csv.reader(open(stim_filename))]
                 for stim_filename in stim_filenames]

    # Keep array with the header
    headers = [[header for header in stim_block[0]]
               for stim_block in stim_list]

    # Creates directory of output files (input files for the protocol)
    if not os.path.exists(setting['inputs_dir']):
        os.makedirs(setting['inputs_dir'])
    else:
        filelist = glob.glob(setting['inputs_dir'] + "/" + "*.csv")
        for f in filelist:
            os.remove(f)

    # Randomization and generation of the csv files
    # Rows and columns concerning the events are randomized
    for n in np.arange(setting["n_repetitions"] + 1):

        # Generate list of lists only with events
        events_list = []
        events_list = [[row[7:] for row in stim_block[1:]]
                       for stim_block in stim_list]

        # Aggregate events and answers in pair lists
        new_events_list = []
        for events_island in events_list:
            new_events_island = []
            for events_trial in events_island:
                new_events_trial = []
                for ev, event in enumerate(events_trial):
                    if ev % 2 == 0:
                        prev_event = event
                        continue
                    else:
                        pair_events = [prev_event, event]
                    new_events_trial.append(pair_events)
                new_events_island.append(new_events_trial)
            new_events_list.append(new_events_island)

        # Shuffle the pair lists within a trial (entry)
        for events_block in new_events_list:
            for entry in events_block:
                random.shuffle(entry)

        new_events_list_concat = []
        new_events_list_concat = [[np.concatenate(trial).tolist()
                                   for trial in block_island]
                                  for block_island in new_events_list]

        newstim_list = []
        newstim_list = [[line[0:7] for line in stim_block[1:]]
                        for stim_block in stim_list]

        for bl, blocklist in enumerate(newstim_list):
            for nr, nrow in enumerate(blocklist):
                nrow.extend(new_events_list_concat[bl][nr])
            random.shuffle(blocklist)
            if bl % 2 == 0:
                blocklist.insert(0, headers[0])
            else:
                blocklist.insert(0, headers[1])

        for b in np.arange(len(newstim_list)):
            with open(setting['inputs_dir'] + '/' + setting['inputs_fname'] +
                    '%s.csv' % (n + b * len(np.arange(
                        setting["n_repetitions"] + 1))), 'w') as fp:
                a = csv.writer(fp, delimiter=',')
                a.writerows(newstim_list[b])

# Error messages
type_sess = str(''.join(("'ms' for main session\n",
                         "'ts' for training session")))
type_island = str(''.join(("'we' for west-east island\n",
                           "'sn' for south-north island\n",
                           "'both' for both islands\n")))
cmd_line_format = str(''.join(("FORMAT: ipython randinputs.py ",
                               "<ARG_TYPE_OF_SESSION> ",
                               "<ARG_TYPE_OF_ISLAND>\n")))
# Run the script
flag = 0
if len(sys.argv) == 3:
    # Arg for type of session and which island
    sess = sys.argv[1]
    isl = sys.argv[2]
    # Load corresponding config .ini file
    if sess in ['ms', 'ts'] and isl in ['we', 'sn', 'both']:
        if sess == 'ms':
            setting = load_config("configrandom_main_session.ini")
        elif sess == 'ts':
            setting = load_config("configrandom_training_session.ini")
        # Perform the randomization
        randomization(setting, isl)
        # Print in the terminal the generation of the input files
        print "Input files were successfully created."
    else:
        flag = 1
        if sess not in ['main_session', 'training_session']:
            print "ERROR: Valid arg for type of session must be used."
        if isl not in ['we', 'sn', 'both']:
            print "ERROR: Valid arg for type of island must be used."
        print ""
else:
    flag = 1
    err_msg = str(''.join(("ERROR: Correct arg's for type of session",
                           " and island must be used only.\n")))
    print err_msg

if flag == 1:
    print type_sess
    print type_island
    print cmd_line_format
