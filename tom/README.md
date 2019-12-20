## Protocols of the *Theory-of-Mind* task battery

Author of the original protocols: Rebecca Saxe & collaborators  

Author of the current implementation: Ana Luisa Pinho  
e-mail address: ana.pinho@inria.fr  

Date: May 2019  

Compatibility: Psychophysics Toolbox Version 3 (PTB-3), aka Psychtoolbox-3, for GNU Octave or Matlab and Python 2.7.  

Preset resolutions:  
Main session - 800x600  
Training session - 3200x1800  


### Theory-of-Mind Localizer

#### Run the protocol

To launch the protocol of the *Theory-of-Mind Localizer*, go to the `tom_localizer` folder and run in the command window of Octave/MATLAB:  

1. For the main session:  

`tom_localizer('subject_id',<run_number>)`

2. For the training session:  

`tom_localizer_ts('subject_id',<run_number>)` 

The protocol starts with a short set of instructions about the stimuli. The participant is asked to press 'y' if TRUE or 'g' if FALSE.

#### Paradigm descriptors extraction

To extract the paradigm descriptors of this task, go to the `tom_localizer` folder and run:  

`paradigm_descriptors_tomloc.py`  

The inputs are stored in the folder `behavioural`; they have been created in the same directory after running the protocol. The outputs will be stored in the folder `paradigm_descriptors` that will be created in the same directory.


### Theory-of-Mind and Pain Matrix Narrative Localizer

#### Run the protocol

To launch the protocol of the *Theory-of-Mind and Pain Matrix Narrative Localizer*, go to the `ep_localizer` folder and run in the command window of Octave/MATLAB:  

1. For the main session:  

`ep_localizer('subject_id',<run_number>)`

2. For the training session:  

`ep_localizer_ts('subject_id',<run_number>)`  

The protocol starts with a short set of instructions about the stimuli. The participant is asked to press 'b' if NO_PAIN, 'y' if LITTLE_PAIN, 'g' if MODERATE_PAIN or 'r' if STRONG_PAIN.

#### Paradigm descriptors extraction

To edit the stimuli of this task, create/edit the `.txt` files in the folder `stim*` and run:

`stim_into_mat.m`

It will generate the corresponding `.mat` files to be used by the scripts `ep_localizer*.m`.  

To extract the paradigm descriptors of this task, go to the `ep_localizer` folder and run:  

`paradigm_descriptors_eploc.py`

The inputs are stored in the folder `behavioural`; they have been created in the same directory after running the protocol. The outputs will be stored in the folder `paradigm_descriptors` that will be created in the same directory.


### Theory-of-Mind and Pain Matrix Movie Localizer

#### Run the protocol

To launch the protocol of the *Theory-of-Mind and Pain Matrix Movie Localizer*, go to the `mov_localizer` folder and run in the command window of Octave/MATLAB:  

`mov_localizer('subject_id')`  

#### Paradigm descriptors extraction

The paradigm descriptors of this task are fixed and provided in the file `paradigm_descriptors_movloc.csv` under the same directory.  


### Additional Notes
For all scripts, there are non-ascii characters in some strings. Make sure you have configured, in your editor, "UTF-8" as the default text encoding. Additionally, if you're running the protocol in Win OS, you may have to uncomment the following line, in order to prevent bad decoding of non-ascii characters:  

`Screen('Preference','TextEncodingLocale','UTF-8');`

