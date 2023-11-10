## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1920 x 1080, refresh rate - 60 Hz.

## Practice

* For practice sessions, run the script `training.py`:
	
	```
	python training.py
	```

* Enter subject number when prompted

* Presents 1 cycle - stationary, incoherent, stationary, coherent, stationary.

## Scanner task

* Run the script `protocol.py` as follows:
	
	```
	python protocol.py
	```

* Enter subject and run numbers when prompted. Run numbers go from 1 to 4.

## How to quit

Press ESC anytime.

## Responses

* One response responses - index-finger key.
* For practice sessions Y.

## After the acquisition

`log` folder contains log of the run.  

### Data extraction

* Run `paradigm_descriptors.py` as follows:

	```
    python paradigm_descriptors.py
	```

* Enter subject number when prompted.

* Choose whether event files should have  (option 1) both repsonses and stimuli or (option 2) just the stimuli

* Output event files would be stored in `output_paradigm_descriptors` folder

## Design

* 4 runs (starting from 1)
* 8 cycles + 1 stim, 4 stimuli per cycle (12 sec for each stimulus, 2 sec delay after each stimulus, ~7.6 min for each run)

## Software info

* Python 3.8.5, Psychopy 2021.1.3.
* Primary script `protocol.py`
* Other dependencies: `numpy`, `sklearn`, `pandas` and `os`
* Protocol based off [Helfrich 2013, Brain Topogr.](https://doi.org/10.1007/s10548-012-0226-1)
