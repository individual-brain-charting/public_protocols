Software/Package:
-----------------
E-Prime 2


To quit the experiment:
-----------------------
Ctrl+Alt+Shift (data file not saved), or
Ctrl+Alt+Backspace (data file saved)


Display settings:
-----------------
There are 2 versions of the task, one which is run using an extended display (*extend-display*), for which the settings are:
Display: Extend
Slave resolution: 1920 x 1080
Refresh rate: 60Hz (make sure both monitors are set to this refresh rate, or as close to it as possible).

The other version uses the mirrored display setup and the setting for that are:
Display: Mirror/Duplicate
Resolution: 1920 x 1080

Restart laptop after altering display setting.

The extended display setup is preferred. Use the mirrored display setup only if extended display setup doesn't work.



Response:
---------
5 button button-box; 2 buttons used (index and middle)
The responses are recorded as y and g, for index and middle fingers.

Practice:
---------
2 practice scripts available for outside the scanner: 
	- Practice_scenes (possible/impossible scene)
	- Practice_dots (dot left/right)

There are 2 parts to each practice run, the first part is self-paced and the second part has the same response duration as the scanner task. 

Output:
	- data\scene-perception_sub-<subno>_practice*, or 
	- data\dot-perception_sub-<subno>_practice*


Task:
-----
4 task runs: scene_perception_run*_extend-display
	
Each task run takes 9:30 minutes from first TTL pulse.

Output:
	- scene-perception_sub-<subno>_ses-<sesno>_*


Post-run:
---------

Generate events file. We only use the .txt files.
Script for data extraction is in Protocol\paradigm_descriptors. 

Before running the script on the behavior laptop:
>> conda activate py27psypy 

Navigate to the data folder and run the script. The columns of data that should be extracted are in the file 'Columns of interest.txt'. The command to generate log files looks like this:
>> python ..\paradigm_descriptors\parser_eprime_logtxt_emotion_recognition.py <txt file name> <columns of interest>

