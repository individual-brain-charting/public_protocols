"""
Script for paradigm descriptors' extraction
on the vSTM+Enumeration task

author: Ana Luisa Pinho
e-mail: ana.pinho@inria.fr
"""

import os
import glob
import csv
import numpy as np

# %%
# ========================== GENERAL PARAMETERS ===============================

# List of participants id
participant_list = [01]

# Subject or Pilot?
# prefix = "pilot"
prefix = "sub"

# Input/Output filename specifications
folder_name = 'log_files'
output_fname = 'paradigm_descriptors'

# Header of log_file
run_group = 'run_group_no.'
log_file = 'log_file_no.'
bars_num = 'numerosity'
fix_start = 'real_t1'
mem_start = 'real_t2'
mem_end = 'real_t3'

# Output file labels
HEADER = ['onset', 'duration', 'trial_type']
mem_name = 'memorization'
answ_name = 'response'
num_label = 'num'

# =========================== TASK PARAMETERS =================================

# For visual Short-Term Memory
task = 'vSTM'
ntrials = 72
input_fname = 'vWM'
answ_start = 'real_t4'
answ_end = 'real_t5'

# For Enumeration
# task = 'enumeration'
# ntrials = 96
# input_fname = 'Enum'
# answ_start = 'real_t3'
# answ_end = 'real_t4'

# %%
# ============================== FUNCTIONS ====================================


def stack_descriptors(onsets, durations, names):
    """ Create table of paradigm descriptors """
    table = np.vstack((HEADER, np.vstack((onsets, durations, names)).T))
    return table


def set_output_path(folder, protocol, fprefix, particip, output_file, sess):
    """ Define pathway of output files """
    output_path = folder + '/' + protocol + '/' + fprefix + '-' + \
        '%02d' % particip + '/' + output_file + '_' + protocol + \
        '_' + fprefix + '-' + '%02d' % particip + '_' + 'run' + \
        str(sess) + '.tsv'
    return output_path


def save_output(file_path, liste):
    """ Save ouput file """
    with open(file_path, 'w') as fp:
        a = csv.writer(fp, delimiter='\t')
        a.writerows(liste)

# =========================== PARSER ==========================================
# For every participant...
for participant in participant_list:
    # Define the pathway of the log files (.dat)
    vstm_folder = folder_name + '/' + task + '/' + prefix + '-' + \
                  '%02d' % participant
    vstm_log_path = os.path.abspath(vstm_folder)
    # List and sort .dat files inside the directory;
    vstm_log_files = glob.glob(os.path.join(vstm_log_path, "*.dat"))
    vstm_log_files.sort()
    # For every group of runs,
    for b, block in enumerate(vstm_log_files, start=1):
        print block
        # Open the corresponding log file
        vstm_mat = [line for line in csv.reader(open(block), delimiter='\t')]
        # Read header of log file
        g_idx, l_idx, n_idx, f_idx, ms_idx, me_idx, as_idx, \
            ae_idx = [int() for _ in range(8)]
        for h, hline in enumerate(vstm_mat[0]):
            if hline == ' ' + run_group:
                g_idx = h
            if hline == ' ' + log_file:
                l_idx = h
            if hline == ' ' + bars_num:
                n_idx = h
            if hline == ' ' + fix_start:
                f_idx = h
            if hline == ' ' + mem_start:
                ms_idx = h
            if hline == ' ' + mem_end:
                me_idx = h
            if hline == ' ' + answ_start:
                as_idx = h
            if hline == ' ' + answ_end:
                ae_idx = h
        # Extract run-group number
        group_number = int(vstm_mat[1][g_idx])
        # Extract log-file number
        log_number = int(vstm_mat[1][l_idx])
        # Set initial value for number of run
        run_number = 2*group_number - 1
        # Extract onsets, durations and trial_type...
        mem_start_onset, mem_end_onset, mem_duration, answ_start_onset, \
            answ_end_onset, answ_duration = [int() for _ in range(6)]
        onset, duration, trial_type = [[] for _ in range(3)]
        num_suffix = str()
        flag = 0
        TTL = 0
        # ...by reading every row in the log file
        for r, row in enumerate(vstm_mat[1:]):
            if flag > 0:
                fix_onset = round(float(vstm_mat[ntrials*flag + 1][f_idx]), 3)
                TTL = fix_onset - 0.05
            mem_start_onset = round(float(row[ms_idx]) - TTL, 3)
            mem_end_onset = round(float(row[me_idx]) - TTL, 3)
            mem_duration = round(mem_end_onset - mem_start_onset, 3)
            answ_start_onset = round(float(row[as_idx]) - TTL, 3)
            answ_end_onset = round(float(row[ae_idx]) - TTL, 3)
            answ_duration = round(answ_end_onset - answ_start_onset, 3)
            onset.extend([mem_start_onset, answ_start_onset])
            duration.extend([mem_duration, answ_duration])
            num_suffix = num_label + '_' + row[n_idx].strip()
            trial_type.extend([mem_name + '_' + num_suffix,
                               answ_name + '_' + num_suffix])
            # Save file of first run of the group
            if r == ntrials*(1+flag) - 1:
                run_number = run_number + flag + log_number - 1
                pd_table = []
                pd_path = str()
                # Stack onset, duration, trial_type arrays
                pd_table = stack_descriptors(onset, duration, trial_type)
                # Set pathway of output file for the present run
                pd_path = set_output_path(folder_name, task, prefix,
                                          participant, output_fname,
                                          run_number)
                # Save list in the output file for the present run
                save_output(pd_path, pd_table)
                # Reset var and lists
                mem_start_onset, mem_end_onset, mem_duration, \
                    answ_start_onset, answ_end_onset, \
                    answ_duration = [int() for _ in range(6)]
                onset, duration, trial_type = [[] for _ in range(3)]
                print 'Saving file of run #%s from group %s ' \
                    % (flag + log_number, group_number) + \
                    'for participant %s ' % participant + \
                    '=> acq. run no. = %s' % run_number
                flag = flag + 1
                continue
