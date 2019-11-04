## Protocols of the *Visual Short-term Memory* and *Enumeration* task battery

Author of the original protocols: André Knops  

Author of the current implementation: Ana Luisa Pinho  
e-mail address: ana.pinho@inria.fr  

Compatibility: Psychophysics Toolbox Version 3 (PTB-3), aka Psychtoolbox-3, for GNU Octave or Matlab and Python 2.7.  

Preset resolution: 1024x768  


### Visual Short-term Memory task

#### Run the protocol

To launch the protocol of the *Visual Short-term Memory* task, run in the command window of Octave/MATLAB:  

1. For the main session:  

`WM_EnumWM_CTRL_fMRI.m`

2. For the training session:  

`WM_EnumWM_CTRL_fMRI_ts.m`  

#### Paradigm descriptors extraction

To extract the paradigm descriptors of this task, run:  

`paradigm_descriptors_extraction.py`

Make sure you have set the correctly the task parameters for this task on the top of the script. The inputs are stored in the folder `log_files/vSTM*`; they have been created in the same directory after running the protocol. The outputs will be stored in the same directory.


### Enumeration task

#### Run the protocol

To launch the protocol of the *Theory-of-Mind and Pain Matrix Narrative Localizer*, go to the `ep_localizer` folder and run in the command window of Octave/MATLAB:  

1. For the main session:  

`Enum_EnumWM_CTRL_fMRI.m`

2. For the training session:  

`Enum_EnumWM_CTRL_fMRI_ts.m`  

#### Paradigm descriptors extraction

To extract the paradigm descriptors of this task, run:  

`paradigm_descriptors_extraction.py`

Make sure you have set the correctly the task parameters for this task on the top of the script. The inputs are stored in the folder `log_files/enumeration*`; they have been created in the same directory after running the protocol. The outputs will be stored in the same directory.

