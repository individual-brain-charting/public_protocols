## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1920 x 1080, refresh rate - 60 Hz.

## How to run

* Go to `aomic\protocol`

### Practice

* Training is in-scanner.
* Just make sure the subject is clear about the instructions before going in the scanner.

### Scanner task

* Open `PIOP_main_experiment.exp` and run each protocol one-by-one
* Protocols after `piopworkingmemory_run2.sce` have not been implemented in this session.

* Use `PIOP_main_experiment_duplicate-screen.exp` only if screen extension does not work

## How to quit

Press ESC anytime.

## Responses

* Two responses - index and middle finger.

## After the acquisition

`Log` folder contains log of the run.  

### Data extraction

* Run `paradigm_descriptors.py` as follows:

    ```
    python paradigm_descriptors.py
    ```
    
* Enter subject number when prompted.

* Output event files would be stored in `output_paradigm_descriptors` folder

## Design

* Movie protocol in `movie_aomic` (see `movie_aomic\README.txt` for more info)
* Four other protocols:
    - Faces
    - Gender Stroop
    - Emotion matching (Harriri)
    - Working memory
* Two runs each
* Each preceded by a 45 sec (usually shorter) training
* Faces runs are each followed by attention tests that are to be run without the scanner on

## Software info

* Presentation (Version 20.1, Neurobehavioral Systems, Inc., Berkeley, CA)
* Primary file `PIOP_main_experiment.exp`
