01.12.2015
----------

Summary of changes
------------------

- The main change is that the `experiment_structure` argument within the `jspsych.init` function that runs the experiment is now called a `timeline`

> Implied change: wherever `jspsych.init` function is called all `experiment_structure` s should be replaced with `timeline` referring to the same experiment array that contains the blocks

- In `jspsych-text` plugin the `cont_key` parameter now only accepts arrays for numeric key codes

> Implied change: convert any `cont_key = 13` to `cont_key = [13]`

- `jspsych-instructions` plugin no longer has the `timing_post_trial` parameter

> Implied change: remove the `timing_post_trial` parameter wherever it was used within the `jspsych-instructions` plugin

- `jspsych-single-stim` plugin `stimuli` parameter has been changed to `stimulus` and the type is no longer and array but a string.

> Implied change: change `stimuli` parameter to read `stimulus` and remove the square brackets to leave only strings as inputs.

- Multiple stimuli within the `jspsych-single-stim` plugin must now be specified by the `timeline` parameter instead of the `stimuli` parameter. 

> Implied change: within the `jspsych-single-stim` plugin the `stimuli` parameter should be replaced by a `timeline` that consists of that consists of an array with `stimulus` and, if desired, additional parameters specified within objects, as well. The added functionality can be used for many of the hacks that we had been using in creating random lists, conditional loops etc.

- Functions can be used as parameters in different plugins to generate trials that should change throughout the task. There are various kinds of callback functions that can be added to `jspsych-init` if there is antyhing that should be updated before or after each trial, block or experiment.

- From the documentation on media preloading: "Note: If you are using HTML strings as stimuli, such as in the single-stim plugin, **you will see a series of error messages in the JavaScript console about failing to find files. These messages can be ignored.**"

- In custom plugins `jspsych-stim-feedback-IE` and `jspsych-single-stim-button` which appeared to be based on `jspsych-single-stim` I changed the parameter `stimuli` to `stimulus` to be in line with the rest of the structure. I think using the `timeline` parameter for these custom plugins when multiple stimuli are necessary should work the same way.

> Implied change: Replace `stimuli` parameter with `stimulus` or `timeline` for the `jspsych-stim-feedback-IE` and `jspsych-single-stim-button` custom plugins.


To-Do:
------

- go over the .js files for all the experiments in expfactory-experiments
- code questionnaires