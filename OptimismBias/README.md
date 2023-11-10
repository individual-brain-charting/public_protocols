## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1920 x 1080, refresh rate - 60 Hz.

## How to run

* Go into the task folder

### Practice

* For practice sessions, run the script `training.py`:

	```
	python training.py
	```

* Enter subject number when prompted

* Presents 4 stimuli.

### Scanner task

* Run the script `protocol.py` as follows:

	```
	python protocol.py
	```

* Enter subject and run numbers when prompted. Run numbers go from 1 to 5.

## How to quit

Press ESC anytime.

## Responses

* Three responses - index-finger, middle and ring-finger keys.
* For practice sessions Y, U and I.

## After the acquisition

`log` folder contains log of the run.  

### Data extraction

* Run `paradigm_descriptors.py` as follows:

	```
    python paradigm_descriptors.py
	```

* Enter subject number when prompted.

* Choose whether event files should have (option 1) just the relevant or (option 2) all events.

* Output event files would be stored in `output_paradigm_descriptors` folder

## Design

* 5 runs (starting from 1)
* 20 trials each run (14 sec for each stimulus, 2+2 sec feedbacks after each stimulus, 12 sec delay, ~10 min for each run)

## Software info

* Python 3.8.5, Psychopy 2021.1.3.
* Primary script `protocol.py`
* Other dependencies: `numpy`, `sklearn`, `pandas`, `os`, `glob`.
