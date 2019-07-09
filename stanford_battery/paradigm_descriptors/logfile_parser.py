"""
File to move and rename the logfiles generated and downloaded from
expfactory-python

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import argparse
import glob
import os
import shutil

import pandas as pd

parser = argparse.ArgumentParser(description='Parameters for the logfiles')
parser.add_argument('-t', '--type', metavar='SubjectType', default='sub',
                    choices=['sub', 'pilot'],
                    help="Subject type. It can only be 'pilot' or 'sub'. "
                         "Choices: %(choices)s. Default: %(default)s")
parser.add_argument('-n', '--number', metavar='SubjectNum', type=int,
                    help="Subject number. It will be formatted as "
                         "a 2-digit number (Max. 99)")
parser.add_argument('-s', '--session', metavar='SessionNum', type=int,
                    default=1, choices=[1, 2, 3],
                    help="Session number. Choices: %(choices)s. "
                         "Default: %(default)s")

args = parser.parse_args()
sub_type = args.type
sub_num = "%02d" % args.number
session = "%02d" % args.session

if os.name == "posix":
    # case Linux
    file_path = os.path.expanduser("~") + '/Downloads'
else:
    # case Windows
    user = os.getlogin()
    file_path = "C:\\Users\\" + user + "\\Downloads"

output_path = os.path.join(os.getcwd(),
                           'logfiles')


def logfile_mover(sub_id: str, origin: str, destination: str) -> None:
    """
    Get logfiles according to some parameters and move them to the
    corresponding folder.

    Parameters
    ----------

    sub_id: str
            String to find the logfiles corresponding to the participant.
            It should be a wildcard so glob can use it to find all the
            corresponding files

    origin: str
            Path where the program is going to look for the logfiles
    destination: str
                 Path where the logfiles are going to be moved

    """
    logfiles = glob.glob(os.path.join(origin, sub_id))

    for logfile in logfiles:
        shutil.move(logfile, destination)


def _get_new_name(logfile: str):
    """
    Rename a logfile based on the task performed

    Parameters
    ----------

    logfile: str
             Absolute path to a .csv file

    Returns
    -------

    new_name: str
              New name for the logfile
    """
    
    logfile = os.path.join(os.path.dirname(logfile), os.path.basename(logfile))
    log_df = pd.read_csv(logfile)
    
    if 'SS_trial_type' in log_df.columns:
        if 'condition' in log_df.columns:
            task = 'MotorSelectiveStopSignal'
        else:
            task = 'StopSignal'
    elif 'flanker_type' in log_df.columns:
        task = 'Attention'
    elif 'task_switch' in log_df.columns:
        task = 'TwobyTwo'
    elif 'goal_state' in log_df.columns:
        task = 'Tower'
    elif 'stim_color' in log_df.columns:
        task = 'Stroop'
    elif 'large_amount' in log_df.columns:
        task = 'DiscountFixed'
    elif 'num_cards' in log_df.columns:
        task = 'CardTaskHot'
    elif 'dot_pattern_expectancy' in log_df.exp_id.values:
        task = 'DotPatternExpectancy'
    else:
        raise ValueError("The logfile provided do not seem to be part of "
                         "this battery of experiments.")

    base_name = os.path.basename(logfile).replace(".csv", "").split("(")[0]

    new_name = base_name + "_" + task + ".csv"

    return new_name


def logfile_renamer(sub_id: str, logfile_path: str) -> None:
    """
    Rename the logfiles depending on their contents

    Parameters
    ----------

    sub_id: str
        String to find the logfiles corresponding to the participant. It
        should be a wildcard so glob can use it to find all the corresponding
        files


    logfile_path: str
                  Path to the logfiles
    """

    logfile_list = glob.glob(os.path.join(logfile_path, sub_id))

    for logfile in logfile_list:
        new_name = _get_new_name(logfile)
        os.rename(logfile, os.path.join(logfile_path, new_name))


def main():
    glob_string = sub_type + "-" + sub_num + "_ses-" + session + "*"

    logfile_mover(glob_string, file_path, output_path)
    logfile_renamer(glob_string, output_path)


if __name__ == "__main__":
    main()
