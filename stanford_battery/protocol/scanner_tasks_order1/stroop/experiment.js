/* ************************************ */
/* Define helper functions */
/* ************************************ */
var ITIs = [0.0,0.0,0.272,0.0,0.136,0.0,0.136,0.0,0.0,0.0,0.272,0.0,0.136,0.408,0.272,0.68,0.0,0.408,0.136,0.68,0.0,0.136,0.952,0.0,0.272,0.0,0.0,0.0,0.0,0.136,0.0,0.0,0.136,0.0,0.0,0.136,0.136,0.272,0.68,0.0,0.0,0.272,0.0,0.0,0.0,0.0,0.0,0.0,0.272,0.0,0.408,0.0,0.136,0.0,0.0,0.0,0.272,0.0,0.272,0.272,0.0,0.68,0.0,0.272,0.0,0.0,0.272,0.136,0.544,0.408,0.0,0.0,0.0,0.544,0.136,0.0,0.0,0.272,0.0,0.0,0.136,0.0,0.272,0.136,0.408,0.0,0.0,0.816,0.0,0.0,0.136,0.0,0.0,0.0,0.0,0.0]

var get_ITI = function() {
  return 2000 + ITIs.shift()*1000
 }

var getPracticeTrials = function() {
	var practice = []
	var practice_stims  = jsPsych.randomization.repeat(stims, practice_len / 12)
	for (var i=0; i<practice_stims.length; i++) {
		var practice_block = {
			timeline: [practice_stims[i]],
			type: 'poldrack-categorize',
			is_html: true,
			choices: choices,
			timing_response: 1500,
			timing_stim: 1500,
			timing_post_trial: 0,
			prompt: '<div class = centerbox><div class = fixation>+</div></div>',
			timing_feedback_duration: 500,
			show_stim_with_feedback: true,
			correct_text: '<div class = fb_box><div class = center-text><font size = 20>Correct!</font></div></div>',
			incorrect_text: '<div class = fb_box><div class = center-text><font size = 20>Incorrect</font></div></div>',
			timeout_message: '<div class = fb_box><div class = center-text><font size = 20>Repondre plus rapidement!</font></div></div>' + instructions_prompt,
			prompt: instructions_prompt,
			on_finish: function(data) {
				var correct = false
				if (data.correct_response == data.key_press) {
					correct = true
				}
				console.log('Trial: ' + current_trial +
              '\nCorrect Response? ' + correct + ', RT: ' + data.rt)
				jsPsych.data.addDataToLastTrial({
					correct: correct,
					trial_id: 'stim',
					trial_num: current_trial,
					exp_stage: exp_stage
				})
				current_trial += 1
			}
		}
		practice.push(practice_block)
		practice.push(practice_fixation_block)
	}
	return practice
}

/* ************************************ */
/* Define experimental variables */
/* ************************************ */
var practice_repeats = 0
// task specific variables
var choices = [89, 71, 82]
var congruent_stim = [{
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:red">ROUGE</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'congruent',
		stim_color: 'red',
		stim_word: 'red',
		correct_response: choices[0]
	},
	key_answer: choices[0]
}, {
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:#1F45FC">BLEU</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'congruent',
		stim_color: 'blue',
		stim_word: 'blue',
		correct_response: choices[1]
	},
	key_answer: choices[1]
}, {
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:#4FE829">VERT</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'congruent',
		stim_color: 'green',
		stim_word: 'green',
		correct_response: choices[2]
	},
	key_answer: choices[2]
}];

var incongruent_stim = [{
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:red">BLEU</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'incongruent',
		stim_color: 'red',
		stim_word: 'blue',
		correct_response: choices[0]
	},
	key_answer: choices[0]
}, {
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:red">VERT</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'incongruent',
		stim_color: 'red',
		stim_word: 'green',
		correct_response: choices[0]
	},
	key_answer: choices[0]
}, {
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:#1F45FC">ROUGE</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'incongruent',
		stim_color: 'blue',
		stim_word: 'red',
		correct_response: choices[1]
	},
	key_answer: choices[1]
}, {
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:#1F45FC">VERT</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'incongruent',
		stim_color: 'blue',
		stim_word: 'green',
		correct_response: choices[1]
	},
	key_answer: choices[1]
}, {
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:#4FE829">ROUGE</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'incongruent',
		stim_color: 'green',
		stim_word: 'red',
		correct_response: choices[2]
	},
	key_answer: choices[2]
}, {
	stimulus: '<div class = stroopbox><div class = stroop-stim style = "color:#4FE829">BLEU</div></div>',
	data: {
		trial_id: 'stim',
		condition: 'incongruent',
		stim_color: 'green',
		stim_word: 'blue',
		correct_response: choices[2]
	},
	key_answer: choices[2]
}];
var exp_len = 96
var practice_len = 12
var stims = congruent_stim.concat(incongruent_stim)
var congruent_stim = jsPsych.randomization.repeat(congruent_stim, (exp_len/2)/3)
var incongruent_stim = jsPsych.randomization.repeat(incongruent_stim, (exp_len/2)/6)

// set up stim order based on optimized trial sequence
var stim_index = [1,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,1,1,1,0,1,1,1,0,0,1,0,0,1,0,1,1,1,0,0,1,0,0,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,1,0,0,1,1,1,1,0,0,0,0,0,1,0,1,1,1,0,1,0,0,1,1,1,0,0,1,0,1,0]
var test_stims = []
for (var i=0; i<exp_len; i++) {
	if (stim_index[i] == 0) {
		test_stims.push(congruent_stim.shift())
	} else {
		test_stims.push(incongruent_stim.shift())
	}
	if (congruent_stim.length == 0) {
		congruent_stim = jsPsych.randomization.repeat(congruent_stim, (exp_len/2)/3)
	}
	if (incongruent_stim.length == 0) {
		incongruent_stim = jsPsych.randomization.repeat(incongruent_stim, (exp_len/2)/6)
	}
}

var exp_stage = 'practice'
var current_trial = 1

/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
var instructions_prompt = '<div class=prompt_box><span style = "color:red;padding-right:40px">Index</span><span style = "color:#1F45FC;">Majeur</span><span style = "color:#4FE829;padding-left:40px">Annulaire</span></div>'

/* define static blocks */
var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text><font size = +4>Repondre a la <strong>coleur de l\'encre</strong> du mot!<br><br><span style = "color:red;padding-left:30px">MOT</span>: Index<br><span style = "color:#1F45FC;padding-left:65px">MOT</span>: Majeur<br><span style = "color:#4FE829;">MOT</span>: Annulaire<br><br>Nous allons commencer par un peu de pratique</div></div>',
  is_html: true,
  timing_stim: -1, 
  timing_response: -1,
  response_ends_trial: true,
  choices: [32],
  data: {
    trial_id: "instructions",
  },
  timing_post_trial: 500
};

var start_test_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Preparez-vous!</p></div>',
  is_html: true,
  choices: 'none',
  timing_stim: 1500, 
  timing_response: 1500,
  data: {
    trial_id: "test_start_block"
  },
  timing_post_trial: 500,
  on_finish: function() {
  	current_trial = 0
  	exp_stage = 'test'
  }
};

 var end_block = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = center-text><i>Fin</i></div></div>',
	is_html: true,
	choices: [32],
	timing_response: -1,
	response_ends_trial: true,
	data: {
		trial_id: "end",
		exp_id: 'stroop'
	},
	timing_post_trial: 0
};


var fixation_block = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = fixation>+</div></div>',
	is_html: true,
	choices: 'none',
	data: {
		trial_id: "fixation"
	},
	timing_post_trial: 0,
	timing_stim: -1,
	timing_response: 500
}

var practice_fixation_block = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = fixation>+</div></div>',
	is_html: true,
	choices: 'none',
	data: {
		trial_id: "fixation"
	},
	timing_post_trial: 0,
	timing_stim: -1,
	timing_response: 250,
	prompt: instructions_prompt
}

/* Set up practice trials */
var practice_trials = getPracticeTrials()
var practice_loop = {
	timeline: practice_trials,
	loop_function: function(data) {
		practice_repeats+=1
		total_trials = 0
		correct_trials = 0
		for (var i = 0; i < data.length; i++) {
			if (data[i].trial_id == 'stim') {
				total_trials+=1
				if (data[i].correct == true) {
					correct_trials+=1
				}
			}
		}
		console.log('Practice Block Accuracy: ', correct_trials/total_trials)
		if (correct_trials/total_trials > .75 || practice_repeats == 3) {
			return false
		} else {
			practice_trials = getPracticeTrials()
			return true
		}
	}
};

var test_block = {
	timeline: test_stims,
	type: 'poldrack-single-stim',
	is_html: true,
	choices: choices,
	timing_response: get_ITI,
	timing_stim: 1500,
	timing_post_trial: 0,
	prompt: '<div class = centerbox><div class = fixation>+</div></div>',
	on_finish: function(data) {
		var correct = false
		if (data.correct_response == data.key_press) {
			correct = true
		}
		console.log('Trial: ' + current_trial +
              '\nCorrect Response? ' + correct + ', RT: ' + data.rt)
		jsPsych.data.addDataToLastTrial({
			correct: correct,
			trial_id: 'stim',
			trial_num: current_trial,
			exp_stage: exp_stage
		})
		current_trial += 1
	}
}

/* create experiment definition array */
stroop_experiment = []
test_keys(stroop_experiment, choices)
stroop_experiment.push(instructions_block)
stroop_experiment.push(practice_loop)
setup_fmri_intro(stroop_experiment)
stroop_experiment.push(start_test_block)
stroop_experiment.push(fixation_block)
stroop_experiment.push(test_block)
stroop_experiment.push(end_block)
