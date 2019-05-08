## Script of the Positive-incentive Value protocol

Authors of the original protocol: Nicolas Clairis and Mathias Pessiglione  

Author of the current implementation: Ana Luisa Pinho  
e-mail address: ana.pinho@inria.fr  

Compatibility: Psychophysics Toolbox Version 3 (PTB-3), aka Psychtoolbox-3, for GNU Octave or MATLAB.  
Preset resolution of the screen: 1920x1080

To run the protocol, typewrite in the command window of Octave or MATLAB:  

`ratings_full_Nspin`

Before the launch of the protocol, you'll be asked:  

1. the subject id;  
2. the number of the run (according to the nomenclature of the protocol: session number);  
3. the category of the stimuli, and; 
4. which of the two available sequences within category you want to run.  

The current response-box setup allows for two levels of scrolling speed of the rating scale in both sideways, i.e. both left and right. Please, make sure the key-code configuration of the script is in agreement with the setup of your equipment.

Always check the device number assigned to your keyboard, by running in the command window of Octave/MATLAB:  

`GetKeyboardIndices`

This value may change if you restart your machine.

There are some non-ascii characters in some strings. Make sure you have configured, in your editor, "UTF-8" as the default text encoding. Additionally, if you're running the protocol in Win OS, you may have to uncomment the following line, in order to prevent bad decoding of non-ascii characters:

`Screen('Preference','TextEncodingLocale','UTF-8');`

The present protocol was implemented for 8 runs of 4 categories of images: __food__, __paintings__, __faces__ and __houses__. Two sets of images are provided per category and each set is to be presented in one run. There are thus 8 available runs, each of them containing a unique set of images. The sequence of display of each set is randomized upon launching the protocol.  

Due to copyright restrictions, the images pertaining to the face category could not be provided.  

In addition, note that the images of the food category are available in the french market. Adaptation of these stimuli might be required in future implementations, depending where the experiment is taking place.


