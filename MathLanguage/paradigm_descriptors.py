"""
Script for paradigm descriptors' extraction of our
version of the MathLangage protocol

author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""

import argparse
import os
import sys
import glob

import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='Parameters for the logfiles')
parser.add_argument('-n', '--number', metavar='SubjectNum', type=int,
                    help="Subject number. It will be formatted as "
                         "a 2-digit number.")

parser.add_argument('-t', '--type', metavar='SubjectType', type=str,
                    default='sub', choices=['sub', 'MRI_pilot'],
                    help="Session type. Choices: "
                         "%(choices)s. Default: %(default)s")

args = parser.parse_args()
sub_num = "%02d" % args.number
sub_type = args.type

# Functions


def _filter_pulses(data):
    """
    Remove rows related to scanner pulses, preserving the TTL

    Parameters
    ----------

    data: pd.Dataframe
          Dataframe containing the experiment info for one session

    Returns
    -------

    filtered_data: pd.Dataframe
                 Dataframe without the rows corresponding to scanner pulses
    """

    data.loc[0, 'pm'] = '999'
    data.loc[0, 'cond'] = 'TTL'

    data.drop(labels=data[data['pm'] == '116'].index, inplace=True)
    data.reset_index(inplace=True, drop=True)


def _fix_timings(data):
    """
    Remove rows related to scanner pulses, preserving the TTL

    Parameters
    ----------

    data: pd.Dataframe
          Dataframe containing the experiment info for one session

    Returns
    -------

    filtered_data: pd.Dataframe
                 Dataframe without the rows corresponding to scanner pulses
    """

    # Get the TTL time
    ttl_time = data.loc[0, :].time

    # Subtract it from every row's time
    data["time"] -= ttl_time

    # Put the time in seconds (default ms)
    data["time"] /= 1000


def _clean_conditions(data):
    """
    Clean or modify the condition names

    Parameters
    ----------

    data: pd.Dataframe
          Dataframe containing the experiment info for one session

    Returns
    -------

    filtered_data: pd.Dataframe
                   Dataframe with clean condition names
    """

    # Remove NaN values for condition names
    data["cond"] = data["cond"].fillna("blank")

    # Remove the numbers from the visually presented trials
    data["cond"] = data["cond"].str.replace('\d+', '')


def _rename_conditions(data):
    """
    Rename conditions for clarity, and include the stim type

    Parameters
    ----------

    data: pd.Dataframe
          Dataframe containing the experiment info for one session

    Returns
    -------

    filtered_data: pd.Dataframe
                   Dataframe with clean condition names
    """

    cond_dict = {'arithprin': 'arithmetic_principle',
                 'colorlessg': 'colorlessg',
                 'control': 'wordlist',
                 'arithfact': 'arithmetic_fact',
                 'tom': 'theory_of_mind',
                 'context': 'context',
                 'general': 'general',
                 'geomfact': 'geometry_fact'}

    stype_dict = {'sound': 'auditory',
                  'text': 'visual'}

    for i in data.index:
        cond = data.loc[i, 'cond']
        stype = data.loc[i, 'stype']
        if cond in cond_dict.keys():
            new_name = "{}_{}".format(cond_dict[cond], stype_dict[stype])
            data.loc[i, 'cond'] = new_name


def _create_durations(data):
    """
    Generate a durations column

    Parameters
    ----------

    data: pd.Dataframe
          Dataframe containing the experiment info for one session

    Returns
    -------

    filtered_data: pd.Dataframe
                   Dataframe with the new column
    """

    data['duration'] = data['time'].shift(-1) - data['time']


def filter_logfile(logfile):
    """
    Perform several actions of the logfile dataframe: remove the rows relative
    to scanner pulses, modify the timings taking the TTL as 0, set it to
    seconds, and clean/modify the names of the conditions

    Parameters
    ----------

    logfile: pd.Dataframe
             Dataframe containing the experiment info for one session

    Returns
    -------

    copy_df: pd.Dataframe
             Dataframe without the rows corresponding to scanner pulses
    """

    copy_df = logfile.copy(deep=True)

    _filter_pulses(copy_df)
    _fix_timings(copy_df)
    _clean_conditions(copy_df)
    _rename_conditions(copy_df)
    _create_durations(copy_df)

    return copy_df


def get_run(filename):
    """
    Parse the path passed to the function to get the run type (1 or 2) and
    the run number (1-4)

    Parameters
    ----------

    filename: str or path object
              Filename to parse

    Returns
    -------

    run_num: int
             Number of the run

    run_type: int
              Type of the run. It can be 1 or 2
    """

    run = logfile.split('.')[-2]

    if 'a' in run:
        run_type = 1
    elif 'b' in run:
        run_type = 2
    else:
        print("Invalid run name, it must contain 'a' or 'b' after the run"
              "number. Exiting...")
        sys.exit()

    run_num = run[:2]

    return run_num, run_type


def get_correct_responses(logfile, keymap):
    """
    Get the correct and incorrect responses of the run

    Parameters
    ----------

    logfile: pd.DataFrame
             Run info

    keymap: dict
            Keys are key codes, values are values in the experiment

    Returns
    -------

    responses: pd.DataFrame
               Information about the responses
    """
    pass


def remove_quotations(file):
    """Remove all quotations from a file"""
    with open(file, 'r+') as f:
        data = f.read()
        f.seek(0)
        for line in data:
            f.write(line.replace('"', ''))
        f.truncate()


# Parameters
path = os.getcwd()

keymap = {'98': 'false',
          '121': 'true'}

input_path = os.path.join(path, '../data')
output_path = os.path.join(path, 'paradigm_descriptors_logfiles')
if not os.path.exists(output_path):
    os.mkdir(output_path)

glob_str = os.path.join(input_path, '*_{}_*'.format(sub_num))
logfile_list = glob.glob(glob_str)

for logfile in logfile_list:

    # Remove quotations
    remove_quotations(logfile)

    # Load logfile
    raw_df = pd.read_csv(logfile, sep=',', skiprows=10, encoding='ISO-8859-1', engine='python')

    # Prepare the datafrma
    filter_df = filter_logfile(raw_df)

    # Get the info about the responses before removing that from the dataframe
    responses = get_correct_responses(filter_df, keymap)

    # from IPython import embed; embed()

    # Prepare the columns of interest
    input_columns = ['time', 'duration', 'cond']
    output_columns = ['onset', 'duration', 'trial_type']

    col_dict = {input_columns[i]: output_columns[i]
                for i in range(len(input_columns))}

    # Slice the final dataframe
    filter_df = filter_df[input_columns]

    # Rename the columns
    filter_df.rename(columns=col_dict, inplace=True)
    filter_df = filter_df.round(3)

    # Save the logfile
    run_num, run_type = get_run(os.path.basename(logfile))
    filename = "{}-{}_task-MathLang{}_run{}.tsv".format(sub_type, sub_num,
                                                        run_type, run_num)
    file_path = os.path.join(output_path, filename)

    filter_df.to_csv(file_path, sep='\t', index=False)
