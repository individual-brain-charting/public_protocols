"""
Script to run a short training session of reversal learning task from O'Doherty lab
Imports from config.py, initPract.py, runBandit.py

Adapted for IBC by:
Himanshu Aggarwal
himanshu.aggarwal@inria.fr
January 2021
"""

import os
import sys
from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import *
homeDir = '.'
# Ensure that relative paths start from the same directory as this script
os.chdir(homeDir)
outDir = homeDir + os.sep + 'Output'
stimDir = homeDir + os.sep + 'Images'
payDir = homeDir + os.sep + 'PayOut'
# Create directories if they don't exist
if not os.path.exists(outDir):
    os.mkdir(outDir)
if not os.path.exists(stimDir):
    os.mkdir(stimDir)
if not os.path.exists(payDir):
    os.mkdir(payDir)


# Add dependencies
from config import *
from initPract import *
from runBandit import *

## Experiment start ##
# Store info about the experiment session
# Reference: allowable inputs
# SubNo. - integer, starts from 1
# RunNo. - integer, starts from 1
# Version - test or debug or pract
# BSCond - rl or hm
# Modality - behaviour or fMRI

if len(sys.argv) == 2:
    SubNo = sys.argv[1]  # get the first argument from command line
else:
    print('\nEnter subject and run number after the script name:\npython training.py <SubNo> <RunNo>')
    exit()

expInfo = {'date': data.getDateStr(),  # add a simple timestamp
        'expName': 'Practice',
        'homeDir': homeDir,
        'outDir': outDir,
        'stimDir': stimDir,
        'payDir': payDir,
        'Version': 'pract',
        'Modality': 'behaviour',
        'BSCond': 'rl',
        'RunNo': 1,
        'SubNo': int(SubNo)
        }
# Set up between-subject counterbalance
expInfo = dict2class(counterbalance(expInfo))  # output is given by expInfo.sub_cb
#####  Task Section  #####
taskClock = core.Clock()
# Initialize general parameters
[screen, dispInfo, taskInfo, taskObj, keyInfo] = initTask(expInfo)

if __name__ == "__main__":
    runBandit(expInfo, dispInfo, taskInfo, taskObj, keyInfo)
    # Close screen after experiment ends
    screen.close()
    # Print out the final payment amount across the session(s)
    sessionPay = 0
    for sI in np.arange(taskInfo.numSessions):
        sessionPay = sessionPay + np.sum(taskInfo.sessionInfo[sI].payOut)
    print('Payment: ' + str(sessionPay))
