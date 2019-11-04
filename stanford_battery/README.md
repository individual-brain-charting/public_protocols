# Scrips of protocols for the *Stanford Self-Regulation* task battery

This file contains information on the required software to run the tasks and get
logfiles to use for posterior analysis, as well as instructions and clarifications
about the naming conventions, software and file structure used by us.

## Table of contents
1. [Python version and dependencies](#Python version and dependencies)
2. [How to run the tasks](#How to run the tasks)
3. [How to get logfiles from the tasks](#How to get logfiles from the tasks)
4. [Where can I find X in the code? (Adjustments help)](#Where can I find X in the code?)

## Python version and dependencies

To run the tasks, you will need to install expfactory-python, which can be installed
with the following command:

    pip install git+https://github.com/IanEisenberg/expfactory-python/
    
This will also install some classical packages (numpy, pandas, etc.) that are
needed for the tasks to run. Also, it is important to note that the package is designed to
work with **Python 2.7**.

If you are using anaconda, you can find an environment file in this directory
called 'environment.yml'. This file is the environment we used to run the tasks,
and can be installed with: 

    conda env create -f stan27.yml
    
With this, the tasks should open and work without problems. If you are not familiar with
virtual environments, please refer to [this handy guide](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
from the Anaconda documentation.

For the steps posterior to running the tasks, we used python 3.7. Here you can find a list
of the packages and versions used in the scripts of this directory:

* argparse (v1.1)
* numpy (v1.15.4)
* pandas (v0.24.1)

## How to run the tasks

This battery was divided in 3 sessions, with 3 tasks for each session, for a total of 9
tasks. If you want to run the tasks differently, please check [Changing the session structure](#Changing the session structure).
To run the tasks, navigate to the protocol directory in a terminal and run:

    $ python run_session.py
    
Of course, it is also possible to run it in ipython, in which case your command is:

    In[1]: %run run_session.py
    
Either way, a prompt will appear and you will have to fill some parameters. First you
will be asked for the participant number. Here we used a naming convention that needs
to be preserved in order for other scripts to work, using the following structure:

    sub-[sub_number]_ses-[session_number]_[run_number]

Where sub number is any number between 1 and 99, session number can be anything according to 
the amount of sessions you have planned for the battery, and
run number would be either 1 or 2 in our case, since we ran all the tasks twice.

An example for session 1, participant number 1 would be:

    sub-01_ses-01
    
The run number won't give any problems with the scripts if you decide to run the tasks once and
not include it in the name. Also, the 0s before numbers lower to 10 are
important and if omitted will produce errors when trying to get the logfiles.

The second parameter you will be asked to enter refers to whether you want to run
the practice tasks or the main tasks. Enter '0' for practice and '1' for the main session.

Lastly, enter the number of the session (as it is, the program only accepts '1', 
'2', and '3').

After this point, several terminal windows will open (if you are on Windows). You can close them
when you finish running the tasks. After a short while, a browser window will open and you will
get a tab for each task. We used Mozilla Firefox in our case, and we recommend previously having an empty
tab open for the experiments to load smoothly.

### Inside the tasks
For all the tasks, you will see a big blue button you need to click on to start the task.
The tab will go fullscreen and you will see the name of the task you are about to run. Also
a text message will prompt you to press Enter. The task will start after doing so.

The first thing for all tasks is a button check for the necessary buttons. Note that these are
different for training and main tasks:

* Training:
  * Index: left arrow
  * Majeur: down arrow
  * Annulaire: right arrow
* Main tasks:
  * Index: Y
  * Majeur: G
  * Annulaire: R
  
 The training is designed to be performed before the session, directly on the acquisition
 computer, while the main tasks are configured for MRI-compatible response boxes, using general
 conventions.
 
 Some tasks will then prompt the experimenter to introduce some parameters. If you
 are confused about this, please check [Experimenter Setup](#Experimenter Setup) at the end of this section.
 After that, almost all the tasks will include a short training in which the participant will receive feedback for
 their performance. Note that this part is intended to be done **before** starting the scanning sequence.
 
 The length of the training is variable, and will finish when the participant reachs a certain number of correct responses.
 After that, a message saying 'Scanner Setup' will appear on screen. When you press spacebar, a red fixation cross
 will appear on the center of the screen. This indicates that the task is waiting for a scanner pulse to commence. In our case,
 this was done receiving the scanner pulse as a keypress of the key 'T'.
 
 ### Experimenter Setup
 
 Some tasks will show this message together with one of more boxes for the experimenter to enter
 additional parameters at the beginning of the main tasks. The tasks that use this feature are:
 
 * stop_signal
 * motor_selective_stop_signal
 * dot_pattern_expectancy
 * twobytwo
 
 The purpose of this parameters is to provide personalized and randomized parameters for
 the tasks. They are showed at the end of their corresponding training task. Let's go over them one by one:
 
 For both stop_signal tasks, the parameter given by the training is SSD, this is the delay between
 the shape presentation and the stop signal(red star) on the stop/ignore trials. In this case, the delay starts low,
 and will increase every time the participant successfully avoids answering to a stop trial, to a top of 250ms.
 
 During the main task, the SSD will start at the value provided in the experimenter setup window, and increase to a top of
 1000ms.
 
 For the dot_pattern_expectancy tasks, the two parameters needed are the cue and the probe. There are 6 of each of them,
 and you only have to put the number (e.g.m if you get 'probe6.png' at the end of the training, you just need to enter 
 '6' in the experimenter setup).
 
 In the case of twobytwo, the parameters are color_order and mag_order. This refers to which response
 (index-majeur) corresponds to which one of the possible responses. For example, color_order 1 indicates that index is the correct answer
 for orange, and majeur for blue, while color_order 2 is the opposite. Again, only the number is 
 required in the window.
 
 For the tasks that need more than one parameter, they must be entered in the same order that they are given
 by the training. The first value should go in the upper box, and the second in the lower one.
 
 ## How to get logfiles from the tasks
 
 Once the task ends, you will see a 'Fin' text message on screen (with the exception of the columbia_card task
 and the ward_and_allport task, which end with a fixation cross due to variable task length), at this point you will 
 have to press spacebar and then enter, and you will see a pop-up window from your browser that is trying to download
 the logfile. This will go to your downloads folder, and while you could move the files by hand, we provide a script
 that will do that and other things for you, please check [Setting up the logfile parser](#Setting up the logfile mover).
 
 Since expfactory was designed to run all the tasks in one go, and generate only one logfile at the end, you will
 have as many logfiles with the same name as tasks you run per session. As a result, you will have duplicate names
 and no way of knowing which file corresponds to this task. 
 
 After setting up the file with the path to your downloads folder, you can go to the
 paradigm_descriptors folder and run logfile_parser.py with the following command:
 
     $ python logfile_parser.py -t [sub_type] -n [sub_number] -s [ses_number]
     
 sub_type can either be 'sub' or 'pilot'. It defaults to sub, so you only need to specify it if you are running a pilot.
 sub_number has to be a number from 1 to 99, but no extra 0s to the left are needed. Same goes for
 ses_number, which in our case is either '1', '2', or '3'.
     
 If you set up the script with the path to your downloads folder and followed the naming
 conventions we proposed, the script should work fine. If you changed either the session
 structure, please check [Changing the session structure](#Changing the session structure).
 If you changed the naming conventions, you can adapt the script to adjust to yours or otherwise you won't
 be able to use it, please check [Changing the name conventions](#Changing the naming conventions).
 
 Once the script is run, the logfiles for that participant will be moved from your downloadas folder
 to the logfiles folder (located in the same directory). These are the logfiles as they come from expfactory, with
 names for the task they contain info from.
 
 In our case, we use BIDS-compliant event files for our analysis. The script logfiles_to_BIDS.py will take
 the logfiles you just moved and generate new ones following the BIDS conventions. To run it, simply do:
 
     $ python logfiles_to_BIDS.py -t [sub_type] -n [sub_number] -s [ses_number]
     
 The arguments are exactly the same than before, so same rules apply. Once you run this, you will have your files
 ready for analysis!
 
 ## Where can I find X in the code?
 
 In this last section we provide pointers to some features of the battery you might want/need to change for your
 own project.
 
 ### Changing the session structure
 
 As stated previously, we ran 3 sessions with 3 tasks each. The original authors ran 2 sessions with 5 tasks each, 
 because we decided to not use the survey_medley task. If you want to run it in 2 or more, the files you will need to
 change are:
 
 * run_session.py
 * logfile_parser.py
 * logfiles_to_BIDS.py
 
 In run_session.py, in line 14, you will find the prompt and if/elif/else statement that selects
 the tasks for each session. You can change the valid inputs and tasks on each session according to your needs
 
 Both logfiles files have an argument for the session number. It is the same for both, so I will go over it once.
On line 15 in both files you can find the argparser that controls the command-line arguments. The third 
parser.add_argument statement is for the session number. You will see a 'choices' argument in the function, containing
the valid values for it. You can change this or remove it altogether according to your needs. If you remove it, be mindful
that we use it for the file naming, so you will need to remove the references to the parameter further in
the code too (e.g., in line 129 of logfile_parser.py).

### Setting up the logfile parser

The code in logfile_parser.py is done to automatically look for the default path that Windows and Ubuntu uses.
If, for whatever reason, you have your downloads elsewhere, you can go and put your parth in the file.

You can find said parameter in line 28 of logfile_parser.py, being assigned to the 'file_path' variable. If you are in
Linux, navigate to your Downloads folder in a terminal and type 'pwd', then press enter. You can copy/paste what you get
into the program (line 30) like:

    file_path = r"whatever/pwd/gives/you"
    
Quotes or doublequotes are important. If you are on windows, you can go to your downloads folder, click on the path on 
upper part of your file manager, and copy/paste it on line 34. Remove all what there is to the left of the equal sign 
and paste your path so it looks like this:

    file_path = r"the\path\to\your\downloads\folder"
    
### I need to change text from the experiments

For each protocol's particular text prompts, you can go to scanner_task_order1/[experiment]/experiment.js and open it
with a text editor or anything that works for you, and you can do a text search with Ctrl+f for the message you want to
translate/change and do it there.

### I need to change the font size/alignment of text

We originally ran the tasks at 3200x1800 resolution, so it's possible that you will need to make
some adjustments to alignment or font size for the tasks.

For the font size, almost every experiment has a font size parameter in some of the text, so you can search it and
change it as you need, and use that as a template to apply it in text that does not have it.

For the alignment of each text box, each experiment has a style.css file. This is a bit trickier, but inside experiment.js
you can look for the text you want to find, and then look at the 'div class' and 'p class' that each text element has.
With that, you can go to the style.css file and look for these names to get access to all kinds of parameters (alignment,
vertical and horizontal position, etc). You can play with the values and adjust it to your needs.
 
### I need to change text that I can't find in any experiment.js file

You are probably looking for the text for the button check, which is common to all tasks. You can find it in 
expfactory-battery/static/js/utils/poldrack_fmri_utils.js, lines 79 and 87.

### I need to change the key for the first scanner pulse, or the number of pulses needed to start

Same as above, you can find it on line 122 of poldrack_fmri_utils.js. The argument 'num_ignore' determines how many pulses
are needed to start the task, and the 'trigger' argument determines the key. In our case, it is the letter 't', which
is expressed in javascript by the code 84.

If you don't know the javascript code for the key you want, check out [this handsome tool](https://keycode.info/).


