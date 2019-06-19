/* ************************************ */
/* Define helper functions */
/* ************************************ */
var ITIs = [0.0,0.272,0.0,0.136,0.408,0.544,0.0,0.136,0.136,0.136,0.136,0.272,0.136,0.408,0.0,0.136,0.0,0.136,0.952,0.272,0.136,0.0,0.136,0.0,0.136,0.272,0.272,0.136,0.0,0.136,0.0,0.272,0.0,0.0,0.136,0.272,0.408,0.0,0.136,0.136,0.0,0.408,0.544,0.136,0.136,0.0,0.0,0.136,0.0,0.136,0.0,0.408,0.0,0.816,0.68,0.0,0.136,0.136,0.136,0.0,0.136,0.952,0.136,0.408,0.952,0.136,0.272,0.272,0.0,0.0,0.272,0.0,0.0,0.272,0.0,0.136,0.272,0.0,0.0,0.0,0.0,0.0,0.0,0.272,0.136,1.088,0.272,0.136,0.136,0.0,0.0,0.0,0.0,0.136,0.272,0.136,0.136,0.0,0.0,0.408,0.544,0.408,0.0,0.408,0.0,0.408,0.0,0.0,0.408,0.136,0.272,0.544,0.272,0.0,0.408,0.0,0.0,0.544,0.408,0.0,0.136,0.816,0.136,0.0,0.136,0.136,0.136,0.544]
var get_ITI = function() {
  return 2100 + ITIs.shift()
 }

var getPracticeTrials = function() {
	var practice_stim = jsPsych.randomization.repeat($.extend(true, [], base_practice_stim), 1, true)
	var practice_trials = []
	for (i=0; i<practice_length; i++) {
		if (practice_stim.data[i].cue == 'double') {
			practice_trials.push(double_cue)
		} else if (practice_stim.data[i].cue == 'center') {
			practice_trials.push(center_cue)
		} else {
			var spatial_cue = {
				type: 'poldrack-single-stim',
				stimulus: '<div class = centerbox><div class = ANT_text>+</div></div><div class = centerbox><div class = ANT_' + practice_stim.data[i].flanker_location +
					'><div class = ANT_text>*</p></div></div>',
				is_html: true,
				choices: 'none',
				data: {

					trial_id: "spatialcue",
					exp_stage: exp_stage
				},
				timing_post_trial: 0,
				timing_stim: 100,
				timing_response: 100
			}
			practice_trials.push(spatial_cue)
		}
		practice_trials.push(fixation)

		var practice_ANT_trial = {
			type: 'poldrack-categorize',
			stimulus: practice_stim.stimulus[i],
			is_html: true,
			key_answer: practice_stim.data[i].correct_response,
			correct_text: '<div class = centerbox><div style="color:#4FE829"; class = center-text>Correct!</div></div>',
			incorrect_text: '<div class = centerbox><div style="color:red"; class = center-text>Incorrect</div></div>',
			timeout_message: '<div class = centerbox><div class = center-text>Repondre plus rapidement!</div></div>',
			choices: choices,
			data: practice_stim.data[i],
			timing_response: 1700,
			timing_stim: 1700,
			response_ends_trial: false,
			timing_feedback_duration: 1000,
			show_stim_with_feedback: false,
			timing_post_trial: 500,
			on_finish: function(data) {
				jsPsych.data.addDataToLastTrial({
					exp_stage: exp_stage
				})
				console.log('Trial: ' + current_trial +
              		'\nCorrect Response? ' + data.correct + ', RT: ' + data.rt)
			}
		}
		practice_trials.push(practice_ANT_trial)
	}
	return practice_trials
}


/* ************************************ */
/* Define experimental variables */
/* ************************************ */
var practice_repeats = 0
// task specific variables
var practice_length = 12
var num_blocks = 2
var block_length = 64

var current_trial = 0
var exp_stage = 'practice'
var choices = [89, 71]
var path = '/static/experiments/attention_network_task/images/'
var images = [path + 'left_arrow.png', path + 'right_arrow.png', path + 'no_arrow.png']
//preload
jsPsych.pluginAPI.preloadImages(images)


/* set up stim: location (2) * cue (3) * direction (2) * condition (2) */
var base_practice_stim = []
var base_test_stim = [[],[],[],[]]
var test_stim = [[],[],[],[]] // track each cue/condition separately
var locations = ['up', 'down']
var cues = ['double', 'spatial']
var directions = ['left', 'right']
var conditions = ['congruent', 'incongruent']

for (ci = 0; ci < cues.length; ci++) {
	var c = cues[ci]
	for (coni = 0; coni < conditions.length; coni++) {
		var condition = conditions[coni]
		for (d = 0; d < directions.length; d++) {
			var center_image = images[d]
			var direction = directions[d]
			var side_image = ''
			if (condition == 'incongruent') {
				var side_image = images[1-d]
			} else {
				side_image = images[d]
			}
			for (l = 0; l < locations.length; l++) {
				var loc = locations[l]
				var stim = {
					stimulus: '<div class = centerbox><div class = ANT_text>+</div></div><div class = ANT_' + loc +
						'><img class = "ANT_img first" src = ' + side_image + '></img><img class = ANT_img src = ' + side_image + '></img><img class = ANT_img src = ' + center_image + '></img><img class = ANT_img src = ' + side_image + '></img><img class = ANT_img src = ' + side_image + '></img></div></div>',
					data: {
						correct_response: choices[d],
						flanker_middle_direction: direction,
						flanker_type: condition,
						flanker_location: loc,
						cue: c, 
						trial_id: 'stim'
					}
				}
				base_practice_stim.push(stim)
				base_test_stim[ci*2+coni].push(stim)
			}
		}
	}
}

for (var i=0; i<test_stim.length; i++) {
	test_stim[i] = jsPsych.randomization.repeat(base_test_stim[i], block_length*num_blocks/16)
}
// set up stim order based on optimized trial sequence
var stim_index = [2,1,2,2,1,0,1,3,1,3,0,3,3,3,1,0,2,1,2,0,0,1,3,0,3,1,3,0,1,1,2,0,3,3,2,2,1,0,0,2,0,1,2,2,2,3,0,0,0,0,0,2,3,1,2,2,2,1,1,1,3,3,1,1,3,1,1,1,0,3,2,2,3,0,3,2,2,2,1,0,3,0,3,0,1,1,2,2,0,0,3,2,1,3,1,2,0,1,2,0,0,3,2,0,2,2,3,3,3,3,1,1,3,3,3,2,0,1,2,2,2,3,0,2,1,3,1,2]
var ordered_stim = []
for (var i=0; i<stim_index.length; i++) {
	var stim = test_stim[stim_index[i]].shift()
	ordered_stim.push(stim)
	//refill if necessary
	if (test_stim[stim_index[i]].length == 0) {
		test_stim[stim_index[i]] = jsPsych.randomization.repeat(base_test_stim[stim_index[i]], block_length*num_blocks/16)
	}
}

/* set up repeats for test blocks */
var blocks = []
for (b = 0; b < num_blocks; b++) {
	blocks.push(ordered_stim.slice(b*block_length,(b+1)*block_length))
}



/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
/* define static blocks */
 var test_intro_block = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = center-text>Preparez-vous!</div></div>',
	is_html: true,
	choices: 'none',
	timing_stim: 1500, 
	timing_response: 1500,
	data: {
		trial_id: "test_start_block"
	},
	timing_post_trial: 500,
	on_finish: function() {
		exp_stage = 'test'
	}
};

var rest_block = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = center-text>+</div></div>',
	is_html: true,
	choices: 'none',
	timing_response: 7500,
	data: {
		trial_id: "rest_block"
	},
	timing_post_trial: 1000
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
		exp_id: 'attention_network_task'
	},
	timing_post_trial: 0
};

 var instructions_block = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = center-text>Indiquez dans quelle direction la fleche centrale pointe.<br>Apuyez sur l\'index (gauche) ou le majeur (droite).</div>',
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

var fixation = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = ANT_text>+</div></div>',
	is_html: true,
	choices: 'none',
	data: {
		trial_id: 'fixation'
	},
	timing_post_trial: 0,
	timing_stim: 400,
	timing_response: 400,
	on_finish: function() {
		jsPsych.data.addDataToLastTrial({
			exp_stage: exp_stage
		})
	}
}

var double_cue = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = ANT_text>+</div></div><div class = ANT_down><div class = ANT_text>*</div></div><div class = ANT_up><div class = ANT_text>*</div><div></div>',
	is_html: true,
	choices: 'none',
	data: {
		trial_id: 'doublecue'
	},
	timing_post_trial: 0,
	timing_stim: 100,
	timing_response: 100,
	on_finish: function() {
		jsPsych.data.addDataToLastTrial({
			exp_stage: exp_stage
		})
	}
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

/* set up ANT experiment */
var attention_network_task_experiment = [];
test_keys(attention_network_task_experiment, choices)
attention_network_task_experiment.push(instructions_block);
attention_network_task_experiment.push(practice_loop)
setup_fmri_intro(attention_network_task_experiment)

/* Set up test trials */
var trial_num = 0
for (b = 0; b < blocks.length; b++) {
	attention_network_task_experiment.push(test_intro_block);
	var block = blocks[b]
	for (i = 0; i < block.length; i++) {

		if (block[i].data.cue == 'double') {
			attention_network_task_experiment.push(double_cue)
		} else {
			var spatial_cue = {
				type: 'poldrack-single-stim',
				stimulus: '<div class = centerbox><div class = ANT_text>+</div></div><div class = centerbox><div class = ANT_' + block[i].data.flanker_location +
					'><div class = ANT_text>*</p></div></div>',
				is_html: true,
				choices: 'none',
				data: {

					trial_id: "spatialcue",
					exp_stage: 'test'
				},
				timing_post_trial: 0,
				timing_stim: 100,
				timing_response: 100
			}
			attention_network_task_experiment.push(spatial_cue)
		}
		attention_network_task_experiment.push(fixation)

		var ANT_trial = {
			type: 'poldrack-single-stim',
			stimulus: block[i].stimulus,
			is_html: true,
			choices: choices,
			data: block[i].data,
			timing_response: get_ITI,
			timing_stim: 1700,
			response_ends_trial: false,
			timing_post_trial: 0,
			prompt: '<div class = centerbox><div class = ANT_text>+</div></div>',
			on_finish: function(data) {
				correct = data.key_press === data.correct_response
				console.log('Trial: ' + current_trial +
              '\nCorrect Response? ' + correct + ', RT: ' + data.rt)
				jsPsych.data.addDataToLastTrial({ 
					correct: correct,
					exp_stage: exp_stage,
					trial_num: trial_num
				})
				trial_num = trial_num + 1
			}
		}
		attention_network_task_experiment.push(ANT_trial)

	}
	if (b < (blocks.length-1)) {
		attention_network_task_experiment.push(rest_block)
	}
}
attention_network_task_experiment.push(end_block)
