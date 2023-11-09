# MathLanguage

## About this protocol

The **Mathematical Language** protocol was designed to comprehensively capture the activation related with several types of mathematical and other types of facts. 

Relevant references:

* [Amalric et al., 2016](https://www.pnas.org/doi/full/10.1073/pnas.1603205113)

## Display settings

* Extend the primary display to the slave monitor.
* Display resolution - 1600 x 1200, refresh rate - 60 Hz.

## Python version and dependencies

We provide a couple of files to replicate our implementation:

* Option 1: Create a python virtual environment

    ```bash
    python -m venv myenv
    source myenv/bin/activate
    pip install -r requirements.txt
    ```

* Option 2: Create a conda environment 

    ```bash
    conda env create -f environment.yml
    conda activate py36expy090
    ```

* Option 3: Install needed packages in your desired environment
  
  To run the tasks, you will need to install Expyriment. This task was developed and run using the version 0.9.0 for Python 3.6.9. To get instructions on how to install Expyriment, refer to its [documentation](https://docs.expyriment.org/Installation.html). Newer versions of Expyriment can cause a problem with the logfiles, although the current version of the script addresses compatibility issues encountered until version 0.10.0.
  
  No other Python packages are needed to run the tasks.

## Before running

Before launching the protocol, you might want to test the audio. To do so, type:

```bash
python test_audio.py
```

This will play a short audio probe that you can test together with the noise of the machine.

## Scanner tasks

The files of this protocol contain personalized audio and text files for a number of different participants. We used the same files for every participant, but you can change that if changing the order suits your needs better. Check the [Where can I find X in the code?](#where-can-i-find-x-in-the-code) section to learn more about that.

There are two files in the protocol folder that you are interested in: `mathlang.py` and `run_experiment.py`. The latter contains the launching sequence, and internally calls mathlang.py. You can initiate it typing:

```bash
python protocol.py -t [type] -r [run]
```

To get more information about the command line arguments, you can type:

```bash
python protocol.py -h
```

There you will see what each argument represents and what are the possible choices for each one.

## How to quit

Press `Escape` anytime.

## Responses

* Two responses: button in the left hand if the sentence is true, button in the right hand if the sentence is false.

## After the acquisition

### Data extraction

In the `paradigm_descriptors` folder you can type:

```bash
python paradigm_descriptors.py -n [number]
```

Again, to get useful information about the arguments, type:

```bash
paradigm_descriptors.py -h
```

The logfiles will be in the `paradigm_descriptors_logfiles` folder.

## Where can I find X in the code?

### Encoding error when running the script

Depending whether you acquire the data in Windows or Linux, you may encounter a python encoding error with the pandas library

In this last section we provide pointers to some features of the battery you might want/need to change for your own project. It may look similar to this:

```bash
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xda in position 6: invalid continuation byte
```

If you find this error, you will have to try different 'encoder' arguments for the function in line `272`. Please refer to [this link](https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python)
to find more information and possible encodings to try.

### Files for each participant

As said at the beginning of the document, we used the same files for every participant, while the protocol has enough data to have different orders for different participants. If you want to include this variation when running the tasks, simply go to the run_experiment.py script and:

* Include a new argument at the beginning of the script to reflect the subject number when calling the script
* Change the format of the string to change the `15` for the additional argument, the result should be something like:

```python
os.system("python mathlang.py stim/"
          "stim_subject{}_bloc_{}{}.csv -r {} -t {}".format(sub, run, ses_type, 
                                                            run, ses_type))
```

### Session structure

One reason we used the same files for everybody was because we wanted to use only 4 of the 5 runs available (so, for types a and b, we had 8 in total). 

Each run needs a call of the script mentioned above, so there is nothing to change in the code. Just be mindful of the run number and type when executing the script.

### Additional information about Audiovis

Audiovis is a general audio visual stimulus presentation with expyriment. The `mathlang.py` script is a slightly modified version of audiovis. It can be found [here](https://github.com/chrplr/audiovis).

