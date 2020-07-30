"""
Script to parse the original logfiles of the protocol and generate BIDS-compliant files

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import ast
import argparse
import glob
import os

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Parameters for the logfiles')
parser.add_argument('-n', '--number', metavar='SubjectNum', type=int,
                    help="Subject number. It will be formatted as "
                         "a 2-digit number.")

parser.add_argument('-t', '--type', metavar='SubjectType', type=str,
                    default='sub', choices=['sub', 'MRI-pilot'],
                    help="Session type. Choices: "
                         "%(choices)s. Default: %(default)s")

args = parser.parse_args()
sub_num = "%02d" % args.number
sub_type = args.type

# Functions


def filter_events(logfile):
    """Keep only rows corresponding to events, and remove unused columns"""

    logfile.drop(labels=logfile[logfile['Data type'] != 'EVENT'].index, inplace=True)
    logfile.dropna(axis=1, inplace=True)
    logfile.reset_index(inplace=True, drop=True)


def correct_onsets(logfile):
    """
    Set the MR pulse to be time 0, and correct the rest of the timestamps, as well
    as expressing them in seconds
    """

    ttl = logfile.iloc[0, 1]
    logfile["Time"] -= ttl
    logfile["Time"] = logfile["Time"].round(2)


def extract_events(logfile):
    """
    Extract the onset and event type of all the events of interest and make a new DataFrame
    with them

    Parameters
    ----------

    logfile: pd.DataFrame
             Input logfile. Events will be extracted from it

    Returns
    -------

    events_df: pd.DataFrame
               New DaraFrame with organized information from the input
    """

    events = []
    cols = ['onset', 'duration', 'trial_type']

    encoding = 0  # No encoding at the beginning
    # intersect = 0  # Flag for intersections to avoid weird behavior
    for index, row in logfile.iterrows():
        trial_info = row.iloc[2]
        if trial_info == 'Moving subject through city':
            encoding = 1  # We start encoding
            trial = [row.Time, 0.0, 'encoding_start']
        elif trial_info == 'Movement along path ended':
            encoding = 0  # Finished encoding
            trial = [row.Time, 0.0, 'encoding_end']
        elif encoding and "closing in on intersection" in trial_info:
            # intersect = 1  # Now looking for the end of this intersection
            intersection_n = ast.literal_eval(trial_info)[1]
            trial = [row.Time, 0.0, 'intersection_{0}'.format(intersection_n)]
        elif encoding and "away from intersection" in trial_info:
            # intersect = 0
            trial = [row.Time, 0.0, 'navigation']
        elif 'trial' in trial_info:
            trial_type = trial_info.split(' ')[1]
            trial = [row.Time, 0.0, trial_type]
        elif trial_info == 'Crosshair displayed':
            trial = [row.Time, 0.0, 'pointing_{0}'.format(trial_type)]
        elif 'ITI' in trial_info:
            trial = [row.Time, 0.0, 'fixation']
        # This last row is only to get durations later
        elif index == logfile.tail(1).index:
            trial = [row.Time, 0.0, 'last']
        else:
            continue

        events.append(trial)

    events_df = pd.DataFrame(events, columns=cols)
    # Get durations
    _get_durations(events_df)
    # Drop last row
    events_df.drop(events_df.tail(1).index, inplace=True)

    return events_df


def _get_durations(logfile):
    """Calculate events' using next row's onset."""

    logfile["duration"] = logfile.shift(-1)["onset"] - logfile["onset"]
    logfile["duration"] = logfile["duration"].round(2)


def clean_run_end(arr):
    """Remove extra indicators for run end when two of them are very close"""
    diff = np.diff(arr)

    bad_idx = []
    for idx, i in enumerate(diff):
        if i < 100:
            bad_idx.append(idx + 1)

    clean_list = [i for j, i in enumerate(arr) if j not in bad_idx]

    return clean_list


# Number of exp and control tials per run
n_trials = 8
n_control = 4
events_per_trial = 3  # All trials have beginning, pointing and fixation phases

# Paths
path = os.getcwd()
input_path = os.path.join(path, '../protocol/logs')
output_path = os.path.join(path, 'paradigm_descriptors_logfiles')

if not os.path.exists(output_path):
    os.mkdir(output_path)

# Main
glob_str = os.path.join(input_path, '*_{}_*main.csv'.format(sub_num))
logfiles_path = glob.glob(glob_str)

for logfile in logfiles_path:
    first_run = int(logfile.split('_')[-2])  # Get the first run from the logfile name
    log = pd.read_csv(logfile, skiprows=4)

    filter_events(log)

    run_onsets = log[log['sPos (x)'] == "['Onset']"].index
    run_end = log[(log['sPos (x)'] == 'Simulation continued')
                  | (log['sPos (x)'] == 'Test ended')].index

    # In case there are extra button presses for run end
    run_end = clean_run_end(run_end)

    for idx, (onset, end) in enumerate(zip(run_onsets, run_end)):
        # Add the first run to the index get the real run number
        run_num = idx + first_run

        # Get the expected length of the run
        length = (n_trials + n_control) * events_per_trial

        # if run_num != 0:
        #     length += 1  # All runs except the first one also have the encoding phase

        # Get the data corresponding to the run and correct the timings around the TTL
        run = log.iloc[onset:end + 1, :]
        run_copy = run.copy(deep=True)

        correct_onsets(run_copy)
        # Select the events of interest and put them in a new dataframe
        new_df = extract_events(run_copy)

        # Save the logfile
        filename = "{}-{}_task-SpatialNavigation_run{}.tsv".format(sub_type, sub_num, run_num + 1)
        file_path = os.path.join(output_path, filename)

        # if len(new_df) == length:
        new_df.to_csv(file_path, sep='\t', index=False)
