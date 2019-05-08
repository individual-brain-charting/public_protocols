"""
Script for paradigm descriptors' extraction for the tom_loc task

author: Ana Luisa Pinho
e-mail: ana.pinho@inria.fr
"""

import os
import csv
import numpy as np

# %%
# ========================== GENERAL PARAMETERS ===============================
# List of participants id
participant_list = [14]

# Subject or Pilot?
# prefix = "pilot"
prefix = "sub"

# Folder to store the output files
output_folder = "paradigm_descriptors"

# ==============================================================================

# %%
# Header for output files
HEADER = ["onset", "duration", "trial_type"]

# For every participant...
for participant in participant_list:
    # ...and for every run:
    for run in np.arange(1, 3):
        # Load the log files:
        # (1) define the filenames;
        log_fname = "IBC_" + prefix + "-" + \
                    "%02d" % participant + ".tom_localizer." + "%01d" % run + \
                    ".mat"
        # (2) define the pathways;
        log_path = os.path.abspath("behavioural" + "/" + log_fname)

        # *************** If log file does not exist, ... *********************

        no_log_flag = int()
        # ****** ...print warning...
        if not os.path.exists(log_path):
            print "Warning: No log file for participant " + \
                  "%s" % participant + " and run " + "%s" % run
            no_log_flag = 1
        # ****** ...and continue.
        if no_log_flag == 1:
            continue

        # *********************************************************************

        # and (3) read the log files.
        log_mat = [line for line in csv.reader(open(log_path), delimiter=',')]
        # Flatten list of lists
        log_mat_flatten = np.hstack(log_mat).tolist()
        # Extract onsets and durations
        counter_onset = int()
        onset = []
        for r, row in enumerate(log_mat_flatten):
            # Extract trial_type
            if log_mat_flatten[r - 4] == "# name: design":
                name_comma = row.split(' ')
                name_code = np.delete(name_comma, 0).tolist()
                name = ["belief" if j == "1" else "photo" for j in name_code]
            # Extract onsets
            elif log_mat_flatten[r - 4 - counter_onset] == \
                    "# name: trialsOnsets":
                # Stops collecting onset after end of array in log file
                if row[0] == '#':
                    continue
                # Otherwise, keep collecting trial_type
                else:
                    onset.append(round(float(row), 3))
                    counter_onset = counter_onset + 1
            # Extract duration
            elif log_mat_flatten[r - 2] == "# name: storyDur":
                story_duration = int(row)
            elif log_mat_flatten[r - 2] == "# name: questDur":
                question_duration = int(row)

        # Create array for duration
        duration = [story_duration + question_duration] * len(onset)

# %%
        # Stack onset, duration, trial_type and rating arrays
        liste = np.vstack((HEADER, np.vstack((onset, duration, name)).T))

# %%
        # Create directory for output files
        output_dir = output_folder + "/" + prefix + "-" + "%02d" % participant

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Set pathway of output file
        output_path = output_dir + "/" + "paradigm_descriptors_tomloc_" + \
            prefix + "-" + "%02d" % participant + "_run" + \
            "%01d" % run + ".csv"

        # Save liste in the output file
        with open(output_path, "w") as fp:
            a = csv.writer(fp, delimiter="\t")
            a.writerows(liste)
