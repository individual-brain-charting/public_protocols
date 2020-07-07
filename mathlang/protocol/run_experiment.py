# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 10:04:33 2018

MathLangage experiment adaptation for the IBC project.

@author: am985309, Juan Jesus Torre Tresols
"""
import os
import argparse

# IMPORTANT: adapt TOTAL_EXPE_DURATION in file mathlang.py if necessary
# Higher onset for last white cross : 567000 ms = 567 s = 9,46 min = 9 min 27 s

parser = argparse.ArgumentParser(description='Parameters for the logfiles')
# parser.add_argument('-n', '--number', metavar='SubjectNum', type=int,
#                     choices=[1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15],
#                     help="Subject number. It will be formatted as "
#                          "a 2-digit number. Choices: %(choices)s")
parser.add_argument('-r', '--run', metavar='RunNum', type=int,
                    default=1, choices=[1, 2, 3, 4, 5],
                    help="Run number. Choices: "
                         "%(choices)s. Default: %(default)s")
parser.add_argument('-t', '--type', metavar='SessionType', type=str,
                    default='a', choices=['a', 'b'],
                    help="Session type. Choices: "
                         "%(choices)s. Default: %(default)s")

args = parser.parse_args()
# sub_num = "%02d" % args.number
run = "%01d" % args.run
ses_type = args.type

# We use the files for sub-15 for all participants, and specify the
# participant number inside the experiment
os.system("python mathlang.py all_stimuli/"
          "stim_subject15_bloc_{}{}.csv -r {} -t {}".format(run, ses_type, run,
                                                            ses_type))
