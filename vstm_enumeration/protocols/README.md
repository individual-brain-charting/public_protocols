## Protocols of the *Visual Short-term Memory* and *Enumeration* task battery

Author of the original protocols: André Knops  

Author of the current implementation: Ana Luisa Pinho  
e-mail address: ana.pinho@inria.fr  

Compatibility: Psychophysics Toolbox Version 3 (PTB-3), aka Psychtoolbox-3, for GNU Octave or Matlab and Python 2.7.  

Preset resolution: 1024x768  


### Visual Short-term Memory task

#### Run the protocol

The run sequence in the session was as follows: 
VSTM, VSTM, Enumeration, Enumeration, VSTM, VSTM

To launch the protocol of the *Visual Short-term Memory* task, run in the command window of Octave/MATLAB:  

1. For the main session:  

`WM_EnumWM_CTRL_fMRI.m`

2. For the training session:  

`WM_EnumWM_CTRL_fMRI_ts.m`  

The functions take 3 arguments as input: subject number, run group (1 or 2) and log file number (legacy argument; 1 works). Run group identifies the initial or final set of VSTM runs. 
For training runs the run group and log file number are meaningless; just use 1.

#### Paradigm descriptors extraction

To extract the paradigm descriptors of this task, run:  

`paradigm_descriptors_extraction.py`

from the vstm_enumeration folder. Within the python file set the subject number(s) and uncomment the appropriate task details. The inputs should be in the folder `log_files/vSTM/<sub>`. The outputs will be stored in the same directory.


### Enumeration task

#### Run the protocol

To launch the protocol of the *Theory-of-Mind and Pain Matrix Narrative Localizer*, go to the `ep_localizer` folder and run in the command window of Octave/MATLAB:  

1. For the main session:  

`Enum_EnumWM_CTRL_fMRI.m`

2. For the training session:  

`Enum_EnumWM_CTRL_fMRI_ts.m`  

The functions take 3 arguments as input: subject number, run group (1 or 2) and log file number (legacy argument; 1 works). Run group is meaningless but required; 1 works.
For training runs the run group and log file number are meaningless; just use 1.

#### Paradigm descriptors extraction

To extract the paradigm descriptors of this task, run:  

`paradigm_descriptors_extraction.py`

from the vstm_enumeration folder. Within the python file set the subject number(s) and uncomment the appropriate task details. The inputs should be in the folder `log_files/enumeration/<sub>`. The outputs will be stored in the same directory.

