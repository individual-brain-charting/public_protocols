# Biological Motion protocol

This file contains information on the required software to run the tasks and get
logfiles to use for posterior analysis, as well as instructions and clarifications
about the naming conventions, software and file structure used by us.

## Table of contents
1. [Software requirements](#Software requirements)
2. [How to run the tasks](#How to run the tasks)
3. [How to get logfiles from the tasks](#How to get logfiles from the tasks)

## Software requirements

This protocol uses MATLAB/Octave. We acquired our data using Octave 4.4 ([Official webpage](https://www.gnu.org/software/octave/)).

No special toolboxes are required for the protocol to function properly.

## How to run the tasks

The files to run the task are located in the octave_protocol folder. There are two files that
we are going to look at:

* BMtraining.m
* BMdirection.m

These are the training and main task, respectively. As with most of the IBC protocols, we ran a 
short training outside of the scanner in order for our participants to familiarize with the task.
To run the training, navigate to the folder containing BMtrainng.m with Octave, and run:

    BMtraining([name], 1, 1)
    
The 'name' parameter will be used to store the logfile for the training (which we did not use for anything), 
and the two other parameters are leftovers from the main experiment, so they can be left at 1.

The training consists of one block for every condition in the main tasks, always in the same order.

For the main task, it is important to note that there are two task types: 1 and 2. The different types contain
different conditions, and in our case we acquired data on both alternatively. To run the main task, navigate
to the pertinent directory in Octave and run:
    
    BMdirection([name], [run_number], [run_type])
    
The name will be used in the logfile, we usually name the files as 'sub-XX' with the participant number. The run
number does not affect the protocol per se, it is just for the logfiles to capture it. In our case, we ran 4 runs
of each type, so 8 runs total. Run type must be 1 or 2, and will change the conditions presented to the participant.

## How to get logfiles from the tasks

Once you have finished acquiring data for a participant, you will find their logfiles in the octave_protocol/Data folder.
To extract the useful information from them, navigate to paradigm_descriptors and run paradigm_descriptors_extraction.py like this:

    $ python paradigm_descriptors_extraction.py -n [sub_number]
    
The 'sub_number' parameter must be only the digit of the participant. Note that the script will look for logfiles starting
with 'sub-[sub_number]'. If you with to change the naming conventions of participants, be sure to check the python script
so it looks for the names you have chosen. 

Once you have processed the files, you will find them in the 'events_files' folder in the same directory as the python script.

