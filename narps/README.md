## About this protocol

Codes for the mixed gamble task, Neuroimaging Analysis Replication and Prediction Study (NARPS).
Modified for IBC by [Himanshu Aggarwal](himanshu.aggarwal@inria.fr) - May 2021
Repo for original code - [here](https://github.com/rotemb9/NARPS_scientific_data).

Relevant references:
* [Botvinik-Nezer et al., 2019](https://doi.org/10.1038/s41597-019-0113-7)
* [Botvinik-Nezer et al., 2020](https://doi.org/10.1038/s41586-020-2314-9)
* [NARPS imaging dataset](10.18112/openneuro.ds001734.v1.0.4)
* [Tom et al., 2007](https://doi.org/10.1126/science.1134239)

## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1600 x 1200, refresh rate - 60 Hz.

## Before running

<mark>Set FORP USB button box mode to "HID NAR BYGRT"</mark>

Open `narps` directory in Octave GUI.

## Training

Run the script `training` in command window of Octave GUI.

Enter the subject number when prompted.

## Scanner task

Run the script `protocol` in command window of Octave GUI to run the protocol.

Enter the subject number and run number when prompted.

## How to quit

Press Escape when the gamble is on screen.

## Responses

* Four responses - index-finger key if you "strongly accept" to the gamble, middle if "weakly accept", ring if "weakly reject" and pinky if "strongly reject".
* For training sessions, U, I, O and P respectively for each of the above-mentioned responses.

## After the acquisition

* `Outputs` folder contains `.txt` files: trial-by-trial info about trial type, subject response, response time and onset times.

* `logs` folder contains `.log` files: each run's trial-by-trial info is appended in this file for each subject.

### Data extraction

Run `paradigm_descriptors.py` as follows:

    ```
    python paradigm_descriptors.py
    ```

* This will create BIDS compliant `.tsv` events files from the `.txt` files in the `output_paradigm_descriptors` folder. 

* If there are multiple `.txt` files for the same subject and same run, the script adds a suffix '(`some number`)' to the `.tsv` files. 

* But to avoid confusions at a later stage, you must first delete unnecessary `.txt` files.

## Design

* 4 runs
* 64 trials in each run (~7 sec for each trial, 7.5 min for each run)

## Software info

* Modified for Octave 5.2.0, psychtoolbox-3 (3.0.17, Debian flavor).
* Primary script `protocol.m` and `training.m` for training session.
