# Public Protocols
This repository hosts public behavioral protocols for the _Individual Brain Charting_ (IBC) project. More information about the project can be found in this [webpage](https://project.inria.fr/IBC/). The code related to the preprocessing and statistical analysis of the corresponding neuroimaging data can be found on the github repository [hbp-brain-charting/public\_analysis\_code](https://github.com/hbp-brain-charting/public_analysis_code).

## Organization of the repository

Main directories are dedicated to the protocol(s) of one task or a group of tasks.  

Each directory is structured as follows:  
1. the protocol's scripts pertaining the launch of the stimuli;  
2. video demonstrations of the sequence of events displayed at every run;  
3. documents containing instructions to the participants carried out during the training session; and  
4. scripts that parse + extract information from log files and compute the paradigm descriptors of the regressors-of-interest used in the GLM estimation. Log files are released upon launching the protocols and they contain experimental variables and behavioral data.

### Tasks  

The `archi` directory contains the protocols of:  
* _ARCHI Standard_ task  
* _ARCHI Spatial_ task  
* _ARCHI Social_ task  
* _ARCHI Emotional_ task  

The `hcp` directory contains the protocols of:  
* _HCP Emotion_ task  
* _HCP Gambling_ task  
* _HCP Motor_ task  
* _HCP Language_ task  
* _HCP Relational_ task  
* _HCP Social_ task  
* _HCP Working Memory_ task      

The `rsvp_language` directory contains the protocol employed for the *RSVP Language* task.  

The `mental_time_travel` directory contains the protocol employed for the *Mental Time Travel* task.  

The `positive_incentive_value` directory contains the protocol employed for the *Positive-incentive Value* task.  

The `tom` directory contains the protocols of:  
* _Theory-of-Mind Localizer_ task  
* _Theory-of-Mind_ and _Pain Matrix Narrative Localizer_ task  
* _Theory-of-Mind_ and _Pain Matrix Movie Localizer_ task  

The `vstm_enum` directory contains the protocols of:  
* _Visual Short-Term Memory_ task  
* _Enumeration_ task  

## Notes
Because these protocols were implemented for native-french speakers, please notice that text stimuli as well as instructions to the participants are written in french. Nevertheless, all the information pertaining the usage and adaptation of the protocols in other experimental settings are provided in english.

## Future work
More protocols will be made available following the releases of the IBC dataset on neuroimaging data.

## Contributions
Please, feel free to report any issue and propose improvements on github.

## Author
Ana Luísa Pinho, 2015 - present
