#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for paradigm descriptors' extraction of our 
version of the experiment used by Santoro et al. (2017)

author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""

import os
import sys
import glob

import pandas as pd
import numpy as np

# %% GENERAL PARAMETERS

# Determine if participant is subject or pilot
if int(sys.argv[1]) == 0:
    sub_type = 'MRI_pilot-'
elif int(sys.argv[1]) == 1:
    sub_type = 'sub-'       

# Participant number
sub = '%02d' % (int(sys.argv[2]))

# Session number
ses_num = '%02d' % (int(sys.argv[3]))

# Logfile number
logfile_id = sys.argv[4]

# Labels
output_header = ['onset', 'duration', 'trial_type']
input_columns = ['Onset', 'Duration', 'Condition']
columns_dict = {}

for column in range(len(input_columns)):
        columns_dict[input_columns[column]] = output_header[column]


def concatenate_logfiles(path, first, last):
    """
    Returns a single dataframe with the inputs of several files combined.

    Parameters
    ----------

    path: str
          directory where the logfiles are stored

    first: int
           number corresponding to the first file (inclusive) desired in
           the output dataframe

    last: int
          number corresponding to the last file (inclusive) desured in
          the output dataframe

    Returns
    -------

    concat_logfile: DataFrame
                    pd.DataFrame containing informations of all the files
                    provided, concatenated in order
    """

    glob_list = [os.path.join(path, 'formisano_protocol_' + str(_) + '*')
                 for _ in range(int(first), (int(last) + 1))]

    path_list = [glob.glob(card)[0] for card in glob_list]

    concat_df = pd.concat(pd.read_csv(path, sep= ',', skiprows= 40)
                          for path in path_list)

    return concat_df

# %% PATHS

# General path
my_path = os.getcwd()

# Input/Output paths
input_path = os.path.join(my_path, '../protocol/data/')
output_path = os.path.join(my_path, 'paradigm_descriptors_logfiles')


# Open the logfile

glob_string = os.path.join(input_path,
                           'formisano_protocol_' + str(logfile_id) + '*')

print(glob_string)

all_logfiles = sorted(glob.glob(glob_string))

print(all_logfiles)

for idx, file in enumerate(all_logfiles):

    logfile_path = all_logfiles[idx]

    print(logfile_path)

    logfile = pd.read_csv(logfile_path, sep=',', skiprows=40)

    # For each run (block) ...

    for run_idx, run in enumerate(np.unique(logfile['Block'].values)):

        # Slice the columns of interest on a second DataFrame
        raw_df = logfile[logfile['Block'] == run][input_columns]

        # Rename collumns
        raw_df.rename(columns=columns_dict, inplace=True)

        # Convert time to seconds
        raw_df['onset'] /= 1000

        raw_df.duration = pd.to_numeric(raw_df.duration, errors='coerce')
        raw_df['duration'] /= 1000

        # Take only acquisition periods
        output_df = raw_df[raw_df['trial_type'] != 'sound_presentation']

        output_df['trial_type'] = output_df['trial_type'].map(
            lambda x: x.lstrip('_'))

        output_df = output_df[(output_df['trial_type'] != 'TTL1') &
                              (output_df['trial_type'] != 'TTL2')]

        # Save the logfile

        if idx > 0:

            save_path = os.path.join(output_path,
                                     sub_type + sub + '-' + str(idx) + '_ses-'
                                     + ses_num + '_task-formisano_run' +
                                     str(int(run[3]) + 1) + '_events.tsv')
        else:

            save_path = os.path.join(output_path,
                                     sub_type + sub + '_ses-' + ses_num +
                                     '_task-formisano_run' +
                                     str(run_idx + 1) + '_events.tsv')

        output_df.to_csv(save_path, sep='\t', index=False)
