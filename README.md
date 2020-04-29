# Public Protocols
This public repository hosts the software protocols used to launch the behavioral tasks in the [_Individual Brain Charting_ (IBC)](https://project.inria.fr/IBC/) project.  

The code related to the preprocessing and statistical analysis of the corresponding neuroimaging data can be found on the following github repository: [hbp-brain-charting/public\_analysis\_code](https://github.com/hbp-brain-charting/public_analysis_code).

## Organization of the repository

Main directories are dedicated to the protocol(s) of one task or a group of tasks.  

Each directory is structured as follows:  
1. the protocol's scripts pertaining the randomization (when applicable) and launching of the stimuli;  
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

The `mtt` directory contains the protocol employed for the *Mental Time Travel* task.  

The `preference` directory contains the protocol employed for the *Preference* task.  

The `tom` directory contains the protocols of:  
* _Theory-of-Mind Localizer_ task in the `tom_localizer` folder
* _Theory-of-Mind_ and _Pain Matrix Narrative Localizer_ task in the `ep_localizer` folder
* _Theory-of-Mind_ and _Pain Matrix Movie Localizer_ task  in the `mov_localizer` folder

The `vstm_enumeration` directory contains the protocols of:  
* _Visual Short-Term Memory_ task  
* _Enumeration_ task  

The `self` directory contains the protocol employed for the *Self* task.  

The `bang` directory contains the protocol employed for the *Bang* task.

The `clips` directory contains the protocol employed for the *Clips* task.

The `retinotopy` directory contains the protocol employed for the *Retinotopy* task.

The `raiders` directory contains the protocol employed for the *Raiders* task.

The `lyon` directory contains the protocols of:  
* _Lyon Moto_ task in the `localizers/session_1/loca_moto_adapt`
* _Lyon MCSE_ task in the `localizers/session_1/loca_mcse_adapt`
* _Lyon MVIS_ task in the `localizers/session_1/loca_mvis_adapt`
* _Lyon MVEB_ task in the `localizers/session_1/loca_mveb_adapt`
* _Lyon AUDI_ task in the `localizers/session_2/loca_audi_adapt`
* _Lyon VISU_ task in the `localizers/session_2/loca_visu_adapt`
* _Lyon LEC1_ task in the `localizers/session_2/loca_lec1_adapt`
* _Lyon LEC2_ task in the `localizers/session_2/loca_lec2_adapt`

The `tonotopy` directory contains the protocol employed for the *Tonotopy* task.

The `stanford_battery` directory contains the protocols of:
* _Attention network_ task
* _Columbia card_ task
* _Discount fixed_ task
* _Dot pattern expectancy_ task
* _Stop signal_ task
* _Motor selective stop signal_ task
* _Stroop_ task
* _Two-by-two_ task
* _Ward and Allport_ task


## Notes
Because these protocols were implemented for native-french speakers, the text stimuli as well as instructions to the participants are written in french. Nevertheless, all the information pertaining the usage and adaptation of the protocols in other experimental settings are provided in english.

## Future work
More protocols will be made available following the releases of the IBC dataset on neuroimaging data.

## Contributions
Please, feel free to report any issue and propose improvements on github.

## Authors
- Ana Luísa Pinho, 2015 - present
- Juan Jesús Torre, 2018 - present
