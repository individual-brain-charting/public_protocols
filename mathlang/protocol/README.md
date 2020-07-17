# Math-Language protocol

This file contains information on the required software to run the tasks and get
logfiles to use for posterior analysis, as well as instructions and clarifications
about the naming conventions, software and file structure used by us.

## Table of contents
1. [Python version and dependencies](#Python version and dependencies)
2. [Randomization of the stimuli](#Randomization of the stimuli)
3. [How to run the tasks](#How to run the tasks)
3. [How to get logfiles from the tasks](#How to get logfiles from the tasks)
4. [Where can I find X in the code? (Adjustments help)](#Where can I find X in the code?)

## Python version and dependencies

To run the tasks, you will need to install Expyriment. This task was developed and run using the version 0.9.0 for
Python 3. To get instructions on how to install Expyriment, refer to its [documentation](https://docs.expyriment.org/Installation.html).

No other Python packages are needed to run the tasks.

## Randomization of the stimuli

The randomization performed to divide the stimuli between 5 blocks (although we only used blocks 1-4) was performed by estipulating the contents of a single block:

    * 8 false for control
    * 4 true and 4 false for arithfact, arithprin, general and geomfact
    * 2 true-true, 2 true-false, 2 false-true, 2 false-false for context and tom
    * Half of each type are auditory and half are visual (written)

After grouping all sentences in a single file, random picks were performed for the five blocks in order to conform the conditions described above. Every sentence exists in visual and auditory formats. Only one of those was picked for the all-sentences file, with a 50% auditory and 50% visual. Then, after making the picks for each block, 8 new stimuli were added for the empty stimuli, and then the order of the stimuli within a block is randomized. Lastly, the "b" blocks are generated changing the file type of each sentence in its corresponding "a" block.

## How to run the tasks

The files of this protocol contain personalized audio and text files for a number of different participants. We used
the same files for every participant, but you can change that if changing the order suits your needs better. Check the 
["Where can I find X in the code?"](#Where can I find X in the code?) section to learn more about that.

There are two files in the protocol folder that you are interested in: mathlang.py and run_experiment.py. The latter
one contains the launching sequence, and internally calls mathlang.py. You can initiate it typing:

    $ python run_experiment.py -t [type] -r [run]
    
To get more information about the command line arguments, you can type:
    
    $ python run_experiment.py -h
    
There you will see what each argument represents and what are the possible choices for each one.

### Testing the audio

Before launching the protocol, you might want to test the audio. To do so, type:

    $ python run_experiment_test_audio.py
    
This will play a short audio probe that you can test together with the noise of the machine.

## How to get logfiles from the tasks

In the paradigm_descriptors folder you can type:

    $ paradigm_descriptors_extraction_mathlang.py -n [number]
    
Again, to get useful information about the arguments, type:

    $ paradigm_descriptors_extraction_mathlang.py -h
    
The logfiles will be in the paradigm_descriptors_logfiles folder.

## Encoding error when running the script

Depending whether you acquire the data in Windows or Linux, you may encounter a python encoding
error with the pandas library

## Where can I find X in the code?
 
In this last section we provide pointers to some features of the battery you might want/need to change for your
own project. It may look similar to this:

    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xda in position 6: invalid continuation byte
    
If you find this error, you will have to try different 'encoder' arguments for the function in line
272. Please refer to [this link](https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python)
to find more information and possible encodings to try.

### Files for each participant

As said at the beginning of the document, we used the same files for every participant, while the protocol has enough data to
have different orders for different participants. If you want to include this variation when running the tasks, simply
go to the run_experiment.py script and:
 
 - Include a new argument at the beginning of the script to reflect the subject number when calling the script
 - Change the format of the string to change the "15" for the additional argument, the result should be something like:
     
       os.system("python mathlang.py all_stimuli/"
                 "stim_subject{}_bloc_{}{}.csv -r {} -t {}".format(sub, run, ses_type, 
                                                                   run, ses_type))
                                                                   
### Session structure

One reason we used the same files for everybody was because we wanted to use only 4 of the 5 runs available (so, for 
types a and b, we had 8 in total). 

Each run needs a call of the script mentioned above, so there is nothing to change in the code. Just be mindful of the
run number and type when executing the script.

### Additional information about Audiovis

Audiovis is a general audio visual stimulus presentation with expyriment. The 'mathlang.py' script is a slightly modified
version of audiovis. It can be found [here](https://github.com/chrplr/audiovis).

Audiovis plays audio or visual stimuli listed in csv files passed as command line arguments (several csv files can be 
listed: they will simply be merged)

Each csv file must contain 3 columns:

- col1 contains onset times in milliseconds, from the start of the experiment
- col2 contains a label for the stimulus type: currently the program recognizes 'sound', 'picture', 'text' or 'rsvp'
- the content of col3 depends on the stimulus type. It must be a filename in the case of 'sound' or 'picture', or a string to be displayed in case of 'text' or 'rsvp'

You can try:

    $ python audiovis.py  sounds/list1.csv  pictures/list1.csv  speech/list1.csv 

And:

    $ python audiovis.py  rsvp/list1.csv sounds/list1.csv

Or, in case you need help:

    $ python audiovis.py -h






