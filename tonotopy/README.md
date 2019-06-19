# About this protocol
The experimental protocol presented here has been adapted from Santoro 
et al. (2017), for the analysis of sound processing using fMRI.

## Python version

This protocol was developed in Python 3.6, using expyriment 0.9.0.

## Settings

The screen resolution used for this protocol was 3200x1800. Note that the
experiment does not contain any visual stimuli, besides fixation crosses and
end of session prompts, so using a different resolution should not be of great
importance.

## How to run

From this directory, run the 'formisano_protocol.py' script. The task was
designed to be run in two different acquisition sessions, thus the script
must be called with an argument to indicate the session number.

    $ python formisano_protocol.py 1
    
There is also a shorter version that can be used for testing or training. It
is 'formisano_training.py'.

Once the protocol launches, it will ask for the participant number, as well as
the starting run number. This was implemented in case an acquisition has to be
interrupted, so it can be resumed in the same run without losing time. Selecting
'1' will start from the first run, and the experiment is composed of 6 runs.

## After the acquisition

Expyriment creates two folders in the script's directory to save the logfiles:
data and events.

The .xpd files that can be found in the data folder contain all the information
on a trial by trial fashion. However, we also provide scripts to generate BIDS compliant
events files from the .xpd files. The script, as well as another README document
detailing the process, can be found on the 'paradigm_descriptors' folder in the 
root directory of this experiment.



