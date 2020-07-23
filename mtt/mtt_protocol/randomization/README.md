## Script to generate the randomized input-trials for the IBC protocol on mental time travel   

Author: Ana Luisa Pinho  
e-mail: ana.pinho@inria.fr  

Compatibility: Python 2.7  

To generate the inputs, please run the script `randinputs_withanswers.py`. It will create a folder with the `inputs*` files. This folder contains shuffled stimuli according to a given reference condition; further, for each reference the corresponding events are also shuffled. The generated csv files are meant to be held by the script `mtt.py`. Please, check the folder in the parent directory `../protocol`.

When running the script, the arguments `ms` or `ts` and `we` or `sn` or `both` must be provided. They stand for *main session*, *training session*, *west-east*, *south-north* and *both*, respectively. Inputs for one of these two types of sessions will be thus generated. For example:  

`ipython randinputs.py ms we`

The names and paths of input and output files can be changed in the config file. Besides, the number of randomized output files per type of stimuli (aka *island*) can also be determined in the config file through the parameter `n_repetitions`.
