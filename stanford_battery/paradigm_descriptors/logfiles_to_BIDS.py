"""
Script to generate BIDS-compliant events files from the original logfiles

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import argparse
import glob
import os

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Parameters for the logfiles')
parser.add_argument('-t', '--type', metavar='SubjectType', default='sub',
                    choices=['sub', 'pilot'],
                    help="Subject type. It can only be 'pilot' or 'sub'. "
                         "Choices: %(choices)s. Default: %(default)s")
parser.add_argument('-n', '--number', metavar='SubjectNum', type=int,
                    help="Subject number. It will be formatted as a "
                         "2-digit number (Max. 99)")
parser.add_argument('-s', '--session', metavar='SessionNum', type=int,
                    default=1, choices=[1, 2, 3],
                    help="Session number. Choices: %(choices)s. "
                         "Default: %(default)s")

args = parser.parse_args()
sub_type = args.type
sub_num = "%02d" % args.number
session = "%02d" % args.session


class LogFile:
    """
    Class to hold logfile info.

    Parameters
    ----------

    path: path to a csv file
          Absolute or relative path to the logfile.

    Attributes
    ----------

    path: path to a csv file
          Absolute or relative path to the logfile

    task: str
          Task which the logfile holds data about. Extracted from the filename

    """

    def __init__(self, path: str):
        self.path = path
        self.task = self._get_task()

    def _get_task(self):
        """
        Get task from filename

        Returns
        -------

        task_name: str
                   name of the task
        """

        task = self.path.strip('.csv').split('_')[-1]

        return task


class StanConverter:
    """
    Opens and modifies a logfile according to BIDS-specification.

    Parameters
    ----------

    output_path: path to a directory
                 Absolute or relative path to the directory where the new
                 files will be stored

    Attributes
    ----------

    out_path: path to a directory
                 Absolute or relative path to the directory where the new
                 files will be stored
    """

    def __init__(self, out_path: str):
        self.out_path = out_path

    def convert(self, logfile, task):
        """Calculates onset, duration and trial type of the logfile"""

        log_df = pd.read_csv(logfile)

        ttl_trial = log_df[log_df["trial_id"] == "fmri_trigger_wait"].index[0]
        t0 = log_df.iloc[ttl_trial]["time_elapsed"]

        task_df = log_df.iloc[ttl_trial:]
        task_df.reset_index(inplace=True)

        task_df["onset"] = task_df["time_elapsed"] - t0
        task_df["duration"] = task_df["onset"].shift(-1) - task_df["onset"]
        task_df["onset"] /= 1000
        task_df["duration"] /= 1000

        # Specific task operations
        conv_df = self.convert_task(task_df, task)

        if task == 'DiscountFixed':
            columns = ["onset", "duration", "trial_type",
                       "large_amount", "later_delay"]
        elif task == 'CardTaskHot':
            columns = ["onset", "duration", "trial_type",
                       "gain_amount", "loss_amount", "num_loss_cards"]
        else:
            columns = ["onset", "duration", "trial_type"]

        # We remove the last row becase it is after the experiment ends
        shift_columns = ~conv_df.columns.isin(["onset", "duration"])
        conv_df.loc[:, shift_columns] = conv_df.loc[:, shift_columns].shift(-1)
        conv_df = conv_df[columns][:-2]

        return conv_df

    def convert_task(self, logfile, task: str):
        converter = self._get_converter(task)
        return converter(logfile)

    def _get_converter(self, task: str):
        if task == 'StopSignal':
            return self._convert_ss
        elif task == 'Attention':
            return self._convert_ant
        elif task == 'TwobyTwo':
            return self._convert_twobytwo
        elif task == 'MotorSelectiveStopSignal':
            return self._convert_ms_ss
        elif task == 'Stroop':
            return self._convert_stroop
        elif task == 'DiscountFixed':
            return self._convert_discount_fixed
        elif task == 'Tower':
            return self._convert_towertask
        elif task == 'CardTaskHot':
            return self._convert_cardtask
        elif task == 'DotPatternExpectancy':
            return self._convert_dpx
        else:
            raise ValueError("{0} is not a valid task".format(task))

    @staticmethod
    def _convert_ss(logfile):
        """Converter for the stop_signal task"""

        logfile['trial_type'] = np.where(logfile['trial_id'] == 'stim',
                                         logfile['SS_trial_type'],
                                         logfile['trial_id'])

        return logfile

    @staticmethod
    def _convert_ant(logfile):
        """Converter for the attention_network_task"""

        logfile['trial_type'] = np.where(logfile['trial_id'] == 'stim',
                                         logfile['cue'] + "_" +
                                         logfile['flanker_type'],
                                         logfile['trial_id'])

        return logfile

    @staticmethod
    def _convert_twobytwo(logfile):
        """Converter for the twobytwo task"""

        logfile['trial_type'] = np.where(logfile['trial_id'] == 'stim',
                                         "task" + logfile['task_switch'] +
                                         "_cue" + logfile['cue_switch'],
                                         logfile['trial_id'])

        return logfile

    @staticmethod
    def _convert_ms_ss(logfile):
        """Converter for the motor_selective_SS task"""

        logfile['trial_type'] = np.where(logfile['trial_id'] == 'stim',
                                         logfile['condition'],
                                         logfile['trial_id'])

        # We remove the last row becase it is after the experiment ends
        conv_df = logfile[["onset", "duration", "trial_type"]][:-1]

        return logfile

    @staticmethod
    def _convert_stroop(logfile):
        """Converter for the stroop task"""

        logfile['trial_type'] = np.where(logfile['trial_id'] == 'stim',
                                         logfile['condition'],
                                         logfile['trial_id'])

        return logfile

    @staticmethod
    def _convert_discount_fixed(logfile):
        """Converter for discount_fixed"""

        logfile.replace(np.nan, 'stim', regex=True, inplace=True)
        logfile['trial_type'] = logfile['trial_id']

        return logfile

    @staticmethod
    def _convert_towertask(logfile):
        """Converter for towertask"""

        condition = np.logical_or(logfile['trial_id'] == 'to_hand',
                                  logfile['trial_id'] == 'to_board')
        logfile['trial_type'] = np.where(condition,
                                         logfile['condition'],
                                         np.where(logfile['trial_id']
                                                  == 'feedback',
                                                  'trial_end_and_next_start',
                                                  logfile['trial_id']))

        return logfile

    @staticmethod
    def _convert_cardtask(logfile):
        """Converter for Columbia card task hot"""

        logfile['trial_type'] = np.where(logfile['trial_id'] == 'stim',
                                         'card_flip',
                                         np.where(logfile['trial_id'] == 'ITI',
                                                  'inter_trials',
                                                  logfile['trial_id']))

        return logfile

    @staticmethod
    def _convert_dpx(logfile):
        """Converter for dot_pattern_expectancy"""

        condition = np.logical_or(logfile['trial_id'] == 'cue',
                                  logfile['trial_id'] == 'probe')
        logfile['trial_type'] = np.where(condition,
                                         logfile['trial_id'] + "_" +
                                         logfile['condition'],
                                         logfile['trial_id'])

        return logfile

    def save_log(self, path, df):
        """Saves the logfile as .tsv"""

        log_pieces = os.path.basename(path).replace('.csv', '').split('_')
        log_name = log_pieces[0] + "_task-" + \
                   log_pieces[-1] + "_run" + \
                   log_pieces[-2] + "_events.tsv"
        df.to_csv(os.path.join(self.out_path, log_name), index=False, sep='\t')


base_path = os.getcwd()
input_path = os.path.join(base_path, 'logfiles')
output_path = os.path.join(base_path, 'events_files')

glob_string = sub_type + "-" + sub_num + "_ses-" + session + "*"
logfiles = [LogFile(logfile) for logfile
            in glob.glob(os.path.join(input_path, glob_string))]

converter = StanConverter(output_path)

for logfile in logfiles:

    bids_df = converter.convert(logfile.path, logfile.task)
    converter.save_log(logfile.path, bids_df)


# if __name__ == '__main__':
#     main()
