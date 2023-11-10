# Reward Processing

## About this protocol

Experimental protocol for probabilistic reversal learning task with gains and losses, adapted from O'Doherty et al. [2001](https://doi.org/10.1038/82959) and [2003](https://doi.org/10.1523/JNEUROSCI.23-21-07931.2003).

## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1600 x 1200, refresh rate - 60 Hz.

## How to run

Go into the task folder

### Practice

* For practice sessions, run the script `training.py`:

```bash
python training.py <SubNo>
```

* Presents 20 trials.

### Scanner task

* Run the script `protocol.py` as follows:

```bash
python protocol.py <SubNo> <RunNo>
```

The subject and run numbers both start from 1.

## How to quit

Press ESC when the stimulus is on the screen.

## Responses

* Two responses - index-finger key for selecting the left image and middle-finger key for the image on the right side.
* For practice sessions, left arrow key for image on the left, and right arrow key for the one on the right.

## After the acquisition

* `Output` folder contains `.pkl` files:

    * data for practice run would be saved as `sub{subject-number}pract_sess{run-number}_data_{timestamp}.pkl` file.

    * data for the task would be saved as `sub{subject-number}_sess{run-number}_data_{timestamp}.pkl` file.

### Data extraction

* Run `paradigm_descriptors.py` as follows:

```bash
python paradigm_descriptors.py
```

* This will create BIDS compliant `.tsv` events files from the `.pkl` files in the `output_paradigm_descriptors` folder. 

* If there are multiple `.pkl` files for the same subject and same run, the script adds a suffix '(`some number`)' to the `.tsv` files. 

* But to avoid confusions at a later stage, you must first delete unnecessary `.pkl` files.

## Design

* 2 runs (starting from 1)
* 85 trials in each run (8.5 sec for each trial, 12 min for each run)

## Software info

* Python 3.8.5, Psychopy 2021.1.3.
* Primary script `protocol.py` imports `config.py`, `initTask.py` and `runBandit.py`.
* Other dependencies: `numpy`, `scipy`, `sys`, `os`, `dill`, `pickle` and `PIL`.
