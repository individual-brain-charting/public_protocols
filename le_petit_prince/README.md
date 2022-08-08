## Display settings

* Clone the primary display to the slave monitor.
* Display resolution - 1920 x 1080, refresh rate - 60 Hz.

## How to run

* Download the audio files from OpenNeuro: 
* Print the `protocol/questions_reponses_a_imprimer.pdf` file to mark participant's answers after each run
* Go into the task folder:
	
	```
	$ cd le_petit_prince/protocol
	```

### Practice

* No practice

### Scanner task

* Run the script `run-lepetitprince-mri.sh` as follows:
	
	```
	$ sh run-lepetitprince-mri.sh
	```

* Select the run and press Enter.

* Ask the questions between each run and write down the answers to the MCQ. Open the file `questions_a_presenter.pdf` for the participant with the command shown, eg.:

	```
    $ evince -s -p 4 questions_a_presenter.pdf
	```

* This would open the pdf at page 4 after run 1 and similarly, prompts after each run show corresponding page number in the pdf.

## How to quit

Don't. (`Ctrl + C` in emergency)

## Responses

* No responses except for the verbal ones after each acquisition run

## Design

* 2 sessions
* 5 runs (session 1) + 4 runs and 1 localizer (session 2)

## Software info

* Python 3.8.5, Expyriment 0.10.0.
* Primary script `run-lepetitprince-mri.sh`
* Secondary scripts `lepp_mri.py` for runs 1-9 and `localizer/localizer-speech.py` for the localizer.

## Other info

* Specified paths and scripts were originally run and tested on Ubuntu OS, so might need mods for running on Windows OS.
* `instructions_for_participants` contain original instructions in French and their English translations (from Google Translate) with `EN_` prefix
* same goes for `protocol/questions_reponses_a_imprimer.pdf` and `protocol/questions_a_presenter.pdf`
