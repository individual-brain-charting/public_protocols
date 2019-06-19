/* ************************************ */
/* Define helper functions */
/* ************************************ */
var randomDraw = function(lst) {
	var index = Math.floor(Math.random() * (lst.length))
	return lst[index]
}

var ITIs = [0.0,0.408,0.408,0.0,0.0,0.136,0.544,0.136,0.0,0.0,0.0,0.408,0.408,0.0,0.272,0.0,0.272,0.272,0.272,0.136,0.272,0.272,0.136,0.0,0.272,0.544,0.272,0.136,0.0,0.0,0.0,0.0,0.272,0.0,0.0,0.0,0.0,0.136,0.0,0.0,0.0,0.0,0.272,0.136,0.272,0.0,0.136,0.136,0.0,0.136,0.136,0.136,0.408,0.272,0.0,0.68,0.0,0.272,0.0,0.0,0.0,0.0,0.272,0.816,0.0,0.136,0.136,0.272,0.136,0.136,0.544,0.136,0.0,0.272,0.136,0.136,0.0,0.136,0.0,0.0,0.0,0.136,0.0,0.0,0.136,0.136,0.0,0.272,0.0,0.136,0.0,0.0,0.136,0.272,0.136,0.272,0.68,0.272,0.272,0.0,0.272,0.136,0.0,0.136,0.0,0.136,0.272,0.0,0.136,0.408,0.0,0.952,0.136,0.136,0.272,0.0,0.0,0.0,0.68,0.272,0.272,0.0,0.272,0.0,0.136]
var get_ITI = function() {
  return 2250 + ITIs.shift()*1000
 }


/* Staircase procedure. After each successful stop, make the stop signal delay longer (making stopping harder) */
var updateSSD = function(data) {
	if (data.SS_trial_type == 'stop') {
		if (data.rt == -1 && SSD < 1000) {
			SSD = SSD + 50
		} else if (data.rt != -1 && SSD > 0) {
			SSD = SSD - 50
		}
	}
}

var getSSD = function() {
	return SSD
}

var getPracticeTrials = function() {
	var practice = []
	var trials = jsPsych.randomization.repeat(stims, practice_len/4)
	for (i=0; i<trials.length; i++) {
		trials[i]['key_answer'] = trials[i].data.correct_response
	}
	var practice_block = {
		type: 'poldrack-categorize',
		timeline: trials, 
		is_html: true,
		choices: choices,
		timing_stim: 850,
		timing_response: 1850,
		correct_text: '<div class = feedbackbox><div style="color:#4FE829"; class = center-text>Correct!</p></div>',
		incorrect_text: '<div class = feedbackbox><div style="color:red"; class = center-text>Incorrect</p></div>',
		timeout_message: '<div class = feedbackbox><div class = center-text>Repondre plus rapidement!</div></div>',
		show_stim_with_feedback: false,
		timing_feedback_duration: 500,
		timing_post_trial: 250,
		on_finish: function(data) {
			jsPsych.data.addDataToLastTrial({
				exp_stage: 'practice',
				trial_num: current_trial,
			})
			current_trial += 1
			console.log('Trial: ' + current_trial +
              '\nCorrect Response? ' + data.correct + ', RT: ' + data.rt)
		}
	}
	practice.push(practice_block)
	return practice
}

/* ************************************ */
/* Define experimental variables */
/* ************************************ */
var practice_repeats = 0
// task specific variables
// Define and load images
var prefix = '/static/experiments/stop_signal/images/'
var images = [prefix + 'moon.png', prefix + 'oval.png', prefix + 'rectangle.png', prefix +
	'trapezoid.png'
]
jsPsych.pluginAPI.preloadImages(images);
/* Stop signal delay in ms */
var SSD = 250
var stop_signal =
	'<div class = coverbox></div><div class = stopbox><div class = centered-shape id = stop-signal></div><div class = centered-shape id = stop-signal-inner></div></div>'

/* Instruction Prompt */
var possible_responses = [
	["Index", 89],
	["Majeur", 71]
]

// set up responses
var choices = [possible_responses[0][1], possible_responses[1][1]]
var response_permutations = [[0,0,1,1], [0,1,0,1], [0,1,1,0],
							[1,1,0,0], [1,0,1,0], [1,0,0,1]]
var permutation_index = 0
var permutation = response_permutations[permutation_index]
var correct_responses = []
for (var i=0; i<4; i++) {
	correct_responses.push(possible_responses[permutation[i]])
}


jsPsych.randomization.shuffle([possible_responses[0], possible_responses[0],
	possible_responses[1], possible_responses[1]
])


var prompt_text = '<ul list-text>' + 
					'<li><div class = prompt_container><img class = prompt_stim src = ' + 
					images[0] + ' width= "50%" height= "50%"></img>' + correct_responses[0][0] + '</div></li>' +
					'</li><li><div class = prompt_container><img class = prompt_stim src = ' +
					images[1] + ' width= "50%" height= "50%"></img>'  + correct_responses[1][0] + '</div></li>' +
					' </li><li><div class = prompt_container><img class = prompt_stim src = ' 
					+ images[2] + ' width= "50%" height= "50%"></img>' + correct_responses[2][0] + '</div></li>' +
					' </li><li><div class = prompt_container><img class = prompt_stim src = ' +
					images[3] + ' width= "50%" height= "50%"></img>' + correct_responses[3][0] + '</div></li></ul>'

/* Global task variables */
var current_trial = 0
var rtMedians = []
var stopAccMeans =[]	
var RT_thresh = 1000
var rt_diff_thresh = 75
var missed_response_thresh = 0.1
var accuracy_thresh = 0.8
var stop_thresh = 0.2	
var practice_len = 12
var exp_len = 125
var num_blocks = 3
var block_len = exp_len/num_blocks
var test_block_data = []

/* Define stims */
var stims = [{
	stimulus: '<div class = coverbox></div><div class = shapebox><img class = stim src = ' + images[0] + '></img></div>',
	data: {
		correct_response: correct_responses[0][1],
		trial_id: 'stim',
	}
}, {
	stimulus: '<div class = coverbox></div><div class = shapebox><img class = stim src = ' + images[1] + '></img></div>',
	data: {
		correct_response: correct_responses[1][1],
		trial_id: 'stim',
	}
}, {
	stimulus: '<div class = coverbox></div><div class = shapebox><img class = stim src = ' + images[2] + '></img></div>',
	data: {
		correct_response: correct_responses[2][1],
		trial_id: 'stim',
	}
}, {
	stimulus: '<div class = coverbox></div><div class = shapebox><img class = stim src = ' + images[3] + '></img></div>',
	data: {
		correct_response: correct_responses[3][1],
		trial_id: 'stim',
	}
}]

// set up stim order based on optimized trial sequence
var stim_index = [1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,1,0,1,1,0,0,0,0,1,1,0]
var trials = []
var go_stims = jsPsych.randomization.repeat(stims, exp_len*0.6 / 4)
var stop_stims = jsPsych.randomization.repeat(stims, exp_len*0.4 / 4)
for (var i=0; i<stim_index.length; i++) {
	var stim = {}
	if (stim_index[i] == 0) {
		stim = jQuery.extend({},go_stims.shift())
		stim['SS_trial_type'] = 'go'
	} else {
		stim = jQuery.extend({},stop_stims.shift())
		stim['SS_trial_type'] = 'stop'
	} 
	trials.push(stim)
	// refill if necessary
	if (go_stims.length == 0) {
		go_stims = jsPsych.randomization.repeat(stims, exp_len*0.6 / 4)
	} 
	if (stop_stims.length == 0) {
		stop_stims = jsPsych.randomization.repeat(stims, exp_len*0.4 / 4)
	} 
}

var blocks = []
for (b=0; b<num_blocks; b++) {
	blocks.push(trials.slice(block_len*b, (block_len*(b+1))))
}

/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
/* define static blocks  */
var task_setup_block = {
	type: 'survey-text',
	data: {
		trial_id: "task_setup"
	},
	questions: [
		[
			"<p class = center-block-text>Experimenter Setup</p>"
		]
	], on_finish: function(data) {
		SSD = parseInt(data.responses.slice(7, 10))
		SSD = math.max(100,math.min(400,SSD))
	}
}

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
		exp_id: 'stop_signal'
	},
	timing_post_trial: 0
};

 var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = instructbox><p class = instruct-text><font size="+2">Une seule cle est correcte pour chaque forme. Ne repondez pas si vous voyez l\'etoile rouge! Les cles correctes son les suivantes:</font>' + prompt_text + '</div>',
  is_html: true,
  timing_stim: -1, 
  timing_response: -1,
  response_ends_trial: true,
  choices: [32],
  data: {
    trial_id: "instructions",
  },
  timing_post_trial: 0
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

// set up practice trials
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
    	current_trial = 0
      return false
    } else {
      practice_trials = getPracticeTrials()
      return true
    }
  }
};

/* ************************************ */
/* Set up experiment */
/* ************************************ */

var stop_signal_experiment = []
test_keys(stop_signal_experiment, choices)
stop_signal_experiment.push(task_setup_block);
stop_signal_experiment.push(instructions_block);
stop_signal_experiment.push(practice_loop);
setup_fmri_intro(stop_signal_experiment)

/* Test blocks */
// Loop through each trial within the block
for (b = 0; b < num_blocks; b++) {
	stop_signal_experiment.push(start_test_block)
	var stop_signal_block = {
		type: 'stop-signal',
		timeline: blocks[b], 
		SS_stimulus: stop_signal,
		is_html: true,
		choices: choices,
		timing_stim: 850,
		timing_response: get_ITI,
		SSD: getSSD,
		timing_SS: 500,
		timing_post_trial: 0,
		prompt: '<div class = centerbox><div class = fixation>+</div></div>',
		on_finish: function(data) {
			correct = false
			if (data.key_press == data.correct_response) {
				correct = true
			}
			updateSSD(data)
			jsPsych.data.addDataToLastTrial({
				exp_stage: 'test',
				trial_num: current_trial,
				correct: correct
			})
			current_trial += 1
			test_block_data.push(data)
			console.log('Trial: ' + current_trial +
              '\nCorrect Response? ' + correct + ', RT: ' + data.rt + ', SSD: ' + data.SS_delay)
		}
	}
	stop_signal_experiment.push(stop_signal_block)
	if ((b+1)<num_blocks) {
		stop_signal_experiment.push(rest_block)
	}
}

stop_signal_experiment.push(end_block)
