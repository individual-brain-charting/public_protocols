# FaceBody

## About this protocol

Functional localizer experiment used to define category-selective cortical regions (published in [Stigliani et al., 2015](http://www.jneurosci.org/content/35/36/12412))

Modified for IBC by [Himanshu Aggarwal](himanshu.aggarwal@inria.fr) - June 2021
Repo for original code - [here](https://github.com/VPNL/fLoc).

## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1920 x 1080, refresh rate - 60 Hz.

## Training

Open `FaceBody` directory in Octave GUI and type `training` in command window to run the training protocol.

Enter the subject number when prompted.

## Scanner task

Open `FaceBody` directory in Octave GUI and type `protocol` in command window to run the protocol.

Enter the subject number and initial run number when prompted.

Note it takes ~1 min to load stimuli images in the beginning of each run.

Press SPACE at the "FIN" screen at the end of each run to move to next run.

## How to quit

Press Escape when the fixation dot is on screen.

## Responses

* One response - index finger key when an image reappears but mirrored.
* For training sessions, Y key.

## After the acquisition

* `data` folder contains folders corresponding each session with `.mat` files. `_run<run num>.mat` for each run and `_fLocSession.mat` with all vars for session.

### Data extraction

* Run `paradigm_descriptors.py` as follows:

```bash
python paradigm_descriptors.py
```

* This will create BIDS compliant `.tsv` events files from the `.mat` files in the `output_paradigm_descriptors` folder.

* If there are multiple folders in `data` folder for the same subject and same run, the script adds a suffix '(`some number`)' to the `.tsv` files.

* But to avoid confusions at a later stage, you must first delete unnecessary folders.

## Design

* 4 runs
* 76 blocks in each run (~6 sec for each trial, ~8 min for each run)
* 12 blocks in training sess (~ 1.2 min long)

## Software info

* Modified for Octave 5.2.0, psychtoolbox-3 (3.0.17, Debian flavor).
* Primary script `protocol.m` and `training.m` for training session.
