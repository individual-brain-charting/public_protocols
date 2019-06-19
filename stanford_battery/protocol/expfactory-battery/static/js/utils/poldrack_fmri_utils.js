/* ************************************ */
/* Setup fMRI trigger listener and functions */
/* ************************************ */
var trigger_times = []

document.onkeypress = function(evt) {
	evt = evt || window.event;
	var charCode = evt.keyCode || evt.which; 
	var which_key = String.fromCharCode(charCode);
	if (which_key == 't') {
		time = jsPsych.totalTime().toString();
		trigger_times.push(time)
	} else {
		time = jsPsych.totalTime().toString();
		if (which_key == ' ') {
			which_key = 'space'
		}
		console.log(which_key, time)
	}
}

var clear_triggers = function() {
	trigger_times = []
}

function addID(exp_id) {
	jsPsych.data.addDataToLastTrial({
		exp_id: exp_id,
		trigger_times: trigger_times
	})
	clear_triggers()
}


/* ************************************ */
/* default jsPsych fMRI blocks */
/* ************************************ */

var fmri_scanner_wait_block = {
	type: 'poldrack-text',
	text: "<div class = centerbox><div  class = center-text>Scanner Setup</div></div>",
	cont_key: [32],
	data: {
		trial_id: "fmri_scanner_wait"
	},
	timing_response: -1,
	timing_post_trial: 0
};

// blank block to put after the last ignored trigger as a buffer before experiment
var fmri_buffer_block = {
	type: 'poldrack-single-stim',
	stimulus: '',
	is_html: true,
	choices: 'none',
	timing_stim: 1000, 
	timing_response: 1000,
	data: {
		trial_id: "fmri_buffer"
	},
	timing_post_trial: 0
};

// block to wait for triggers
var create_trigger_block = function(trigger) {
	var fMRI_wait_block = {
		type: 'poldrack-text',
		text: "<div class = centerbox><div style='color:red'; class = center-text>+</div></div>",
		cont_key: [trigger],
		data: {
			trial_id: "fmri_trigger_wait"
		},
		timing_response: -1,
		timing_post_trial: 0
	};
	return fMRI_wait_block
}

var get_finger = function (choice) {
	var keycode_lookup = {'B': 'pouce', 'Y': 'index', 'G': 'majeur', 
					'R': 'annulaire', 'M': 'auriculaire'}
	var finger = keycode_lookup[String.fromCharCode(choice)]
	return finger
}

// test response keys
var create_key_test_block = function(choice) {
	var button = get_finger(choice)
	var instruct_text = "Veuillez appuyer avec votre " + button
	if (button == null) {
		instruct_text = "Attendre les instructions de l\'experimentateur."
	}
	var key_test_block = {
		type: 'poldrack-text',
		text: "<div class = centerbox><div style = 'font-size: 50px' class = center-text>" + instruct_text + "</p></div>",
		cont_key: [choice],
		data: {
			trial_id: "fmri_response_test"
		},
		timing_response: -1,
		timing_post_trial: 500
	};
	return key_test_block
}

var test_keys = function(lst, choices = []) {
	for (var i=0; i < choices.length; i++) {
		lst.push(create_key_test_block(choices[i]))
	}
}

// setup function
var setup_fmri_intro = function(lst, num_ignore = 1, trigger = 84) {
	lst.push(fmri_scanner_wait_block)
	for (var j = 0; j < num_ignore; j++) {
		lst.push(create_trigger_block(trigger))
	}
	lst.push(fmri_buffer_block)
}

// setup function
var setup_fmri_run = function(lst, num_ignore = 1, trigger = 84) {
	for (var j = 0; j < num_ignore; j++) {
		lst.push(create_trigger_block(trigger))
	}
	lst.push(fmri_buffer_block)
}
