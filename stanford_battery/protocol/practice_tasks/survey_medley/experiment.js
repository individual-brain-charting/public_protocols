/* ************************************ */
/* Define helper functions */
/* ************************************ */
ITIs = [0.272, 0.8]
var get_ITI = function() {
  return 9000 + ITIs.shift()*1000 //500 minimum ITI
}

/* ************************************ */
/* Define experimental variables */
/* ************************************ */
var choices = [71,72,74,75,76]

// task specific variables
var practice1_items = [
	'I like modern art',
]

var practice1_responses = ['<span style="font-weight: normal; font-size: 30px">Not at all</span>', '1', '2', '3', '4', '5', '<span style="font-weight: normal; font-size: 30px">Very much</span>']

var practice1_codings = ['forward']

var practice2_items = [
	'Cats are better than dogs',
]

var practice2_responses = ['No', 'Yes']

var practice_codings = ['forward']



var survey_items = [practice1_items, practice2_items]
var responses = [practice1_responses, practice2_responses]
var surveys = ['practice1', 'practice2']
var survey_choices = [[71,72,74,75,76],[71,72]]
var item_codings = [practice_codings, practice_codings]
var stims = []
for (var si=0; si<survey_items.length; si++) {
	var items = survey_items[si]
	for (var i=0; i<items.length; i++) {
		var item_text = '<div class = centerbox><p class=item-text>' + items[i] + '</p></div><div class=response-text><div class=response-item>' + responses[si].join('</div><div class=response-item>') + '</div></div></div>'
		var item_coding = item_codings[si][i]
		var item_data = {'survey': surveys[si], 
						'item_coding': item_coding,
						'item_text': items[i],
						'options': responses[si]}
		var item_choice = survey_choices[si]
		stims.push({'stimulus': item_text, 'data': item_data, 'choices': item_choice})
	}
}


/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
/* define static blocks */
var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Respond to the questions!</div></div>',
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

var start_test_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Get ready!</p></div>',
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
		exp_id: 'survey_medley'
	},
	timing_post_trial: 0
};


var test_block = {
	timeline: stims,
	type: 'poldrack-single-stim',
	is_html: true,
	timing_response: get_ITI,
	timing_stim: 8500,
	timing_post_trial: 0,
	on_finish: function(data) {
		var response = data.possible_responses.indexOf(data.key_press)+1
		var coded_response = response
		if (data.item_coding == 'reverse') {
			coded_response = (data.possible_responses.length+1) - response
		}
		jsPsych.data.addDataToLastTrial({'response': response, 'coded_response': coded_response})
	}
}

/* create experiment definition array */
survey_medley_experiment = []
survey_medley_experiment.push(instructions_block)
survey_medley_experiment.push(test_block)
survey_medley_experiment.push(end_block)