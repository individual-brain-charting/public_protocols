## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1920 x 1080, refresh rate - 60 Hz.

## Practice

* For practice sessions, run the script `training.py`:

	```
	python training.py
	```

* Enter subject number when prompted

* Presents 4 blocks.

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

`log` folder contains log of the run if it ran completely.  

### Data extraction

* Run `paradigm_descriptors.py` as follows:

	```
    python paradigm_descriptors.py
	```
	
* Enter subject number when prompted.

* Choose whether event files should have names of (option 1) just the blocks or (option 2) all stimuli

## Design

* 4 runs (starting from 1)
* 36 blocks, 12 stimuli per block (7.2 sec for each block, 5 sec delay after each block, 7.24 min for each run)

## Software info

* Python 3.8.5, Psychopy 2021.1.3.
* Primary script `protocol.py`
* `colored_patch.py` creates stim images in a tmp folder to avoid overwriting images already in use.
* Other dependencies: `numpy`, `sklearn`, `pandas`, `os` and `PIL`.
