## About this protocol

Experimental protocol for visual search and working memory, adapted from [Kuo et al. (2016)](https://www.researchgate.net/publication/297895192_Top-Down_Activation_of_Spatiotopic_Sensory_Codes_in_Perceptual_and_Working_Memory_Search).

## Display settings

* Set the slave monitor to clone the primary one.
* Display resolution - 1280 x 960, refresh rate - 60 Hz.

## Practice

* Run the script `practice.py`

  ```
  python practice.py
  ```

* Presents 8 trials - first 4 have longer stimulus and response duration, and shorter inter-trial intervals and the rest 4 have the actual durations (just as in the main task).

## Scanner task
	
* Run the script `protocol.py` as follows:

  ```
  python protocol.py
  ```

* When prompted, enter the current run number (0-3, including 0 and 3) and then the subject number.

* Press ENTER on the "Fin" screen to continue to the next run.

## Responses

* Two responses - index-finger key for "target present" and middle-finger key for "target absent". 
* For practice sessions, J key for "target present", and K key for "target absent".

## How to quit

Simply press ESC key any time during the experiment.

## After the acquisition

* `data` folder contains `.xpd` files: Trial-by-trial info about trial type, subject response, response time and event times.

* `events` folder contains `.xpe` files: Detailed log of all the events such as stimulus loading/plotting, stimulus presentation, key presses etc.

### Data extraction

Run `paradigm_descriptors.py` as follows:

  ```
  python paradigm_descriptors.py
  ```

* This will create BIDS compliant `.tsv` events files from the `.xpd` files in the `output_paradigm_descriptors` folder. 

* If there are multiple `.xpd` files for the same subject and same run, the script adds a suffix '(`some number`)' to the `.tsv` files. 

* But to avoid confusions at a later stage, you must first delete unnecessary `.xpd` files.

## Design

* 4 runs
* 48 trials in each run (9 - 18 sec for each trial, 7 - 15 min for each run)
* 2 x 2 x 2 factorial design
  * 2 search types (visual search and working memory search)
  * 2 array sizes (two and four)
  * 2 responses (target present and target absent)

## Software info

* Python 3.8.5, Expyriment 0.10.0. 

* Primary script `protocol.py` imports `prerandomise.py` for generating randomised trial and stimuli sequences. 

* Other dependencies: `numpy`, `pandas`, `os`, `ast` and `time`.
