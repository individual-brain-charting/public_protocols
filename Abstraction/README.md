## Display settings

* ON 3T SCANNER STIM PC
* Duplicate the primary display to the slave monitor.
* Display resolution - 1920 x 1080, refresh rate - 60 Hz.

## How to run

* Start MATLAB by opening terminal and typing
	
	```
	matlab
	```

* Go into the task folder:
	
	```
	cd /home/neurostim/Experiments/ibc_cognitive_protocols/abstraction_Theo
	```

## Practice

* No practice/training

* Just make sure the instructions are clear to the subject

## Scanner task

* Run the localiser first:

	```
	localiser
	```
	- Enter 0 when asked `Run on 0 - scanner or 1 - debug mode:`
	- Then enter the subject number

* Followed by the protocol:
	
	```
	protocol
	```
	- Enter 0 when asked `Run on 0 - scanner or 1 - debug mode:`
	- Then enter the subject number
	- And the run numbers from 1 to 8.

## How to quit

Press ESC anytime.

## Responses

* One response responses - index-finger key.

## After the acquisition

`log` folder contains log of the run.  

### Data extraction

* Activate conda environment py38psypy 
	
	```
    conda activate py38psypy
	```

* Run `paradigm_descriptors.py` as follows:

	```
    python paradigm_descriptors.py
	```

* Enter subject number when prompted.

* Output event files would be stored in `output_paradigm_descriptors` folder

## Design

* 8 runs (starting from 1)

## Software info

* MATLAB, PsychToolBox 
