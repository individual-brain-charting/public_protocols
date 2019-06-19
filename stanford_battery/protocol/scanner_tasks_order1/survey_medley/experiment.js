/* ************************************ */
/* Define helper functions */
/* ************************************ */
ITIs = [1.36,0.68,1.156,0.204,2.176,0.272,0.612,0.068,0.0,5.304,0.068,1.292,2.788,0.204,0.476,0.952,2.856,0.204,2.516,0.0,0.136,0.612,0.612,1.292,1.088,0.068,1.156,0.884,0.68,0.544,2.312,0.612,0.204,0.544,0.476,0.204,1.088,1.904,0.884,0.136]

var get_ITI = function() {
  return 9000 + ITIs.shift()*1000 //500 minimum ITI
}

/* ************************************ */
/* Define experimental variables */
/* ************************************ */
var choices = [66,89,71,82,77]

// task specific variables
var grit_items = [
	'New ideas and projects sometimes distract me from previous ones.',
	"Setbacks don't discourage me.",
	'I have been obsessed with a certain idea or project for a short time but later lost interest.',
	'I am a hard worker.',
	'I often set a goal but later choose to pursue a different one.',
	'I have difficulty maintaining my focus on projects that take more than a few months to complete.',
	'I finish whatever I begin.', 'I am diligent.'
]

var grit_responses = ['<span style="font-weight: normal; font-size: 30px">Not at all like me</span>', '1', '2', '3', '4', '5', '<span style="font-weight: normal; font-size: 30px">Very much like me</span>']

var grit_codings = ['reverse', 'forward', 'reverse', 'forward', 'reverse', 'reverse', 'forward', 'forward']

var brief_items = [
'I am good at resisting temptation.',
 'I have a hard time breaking bad habits.',
 'I am lazy.',
 'I say inappropriate things.',
 'I do certain things that are bad for me, if they are fun.',
 'I refuse things that are bad for me.',
 'I wish I had more self-discipline.',
 'People would say that I have iron self-discipline.',
 'Pleasure and fun sometimes keep me from getting work done.',
 'I have trouble concentrating.',
 'I am able to work effectively toward long-term goals.',
 "Sometimes I can't stop myself from doing something, even if I know it is wrong.",
 'I often act without thinking through all the alternatives.'
 ]

var brief_responses = ['<span style="font-weight: normal; font-size: 30px">Not at all</span>', '1', '2', '3', '4', '5', '<span style="font-weight: normal; font-size: 30px">Very much</span>']

var brief_codings = ['forward', 'reverse', 'reverse', 'reverse', 'reverse', 'forward', 'reverse', 'forward', 'reverse', 'reverse', 'forward', 'reverse', 'reverse']

var future_time_items = [
'Many opportunities await me in the future.',
 'I expect that I will set many new goals in the future.',
 'My future is filled with possibilities.',
 'Most of my life lies ahead of me.',
 'My future seems infinite to me.',
 'I could do anything I want in the future.',
 'There is plenty of time left in my life to make new plans.',
 'I have the sense that time is running out.',
 'There are only limited possibilities in my future.',
 'As I get older, I begin to experience time as limited.'
 ]

var future_time_responses = ['<span style="font-weight: normal; font-size: 30px">Very Untrue</span>', '1', '2', '3', '4', '5',  '<span style="font-weight: normal; font-size: 30px">Very True</span>']

var future_time_codings = ['forward', 'forward', 'forward', 'forward', 'forward', 'forward', 'forward', 'forward', 'forward', 'forward', 'forward']

var impulse_venture_items = [
'Do you welcome new and exciting experiences and sensations even if they are a little frightening and unconventional?',
'Do you sometimes like doing things that are a bit frightening?',
'Would you enjoy the sensation of skiing very fast down a high mountain slope?'
]

var impulse_venture_responses = ['No', 'Yes']

var impulse_venture_codings = ['forward', 'forward', 'forward']

var upps_items = [
"Sometimes when I feel bad, I can't seem to stop what I am doing even though it is making me feel worse.",
'Others would say I make bad choices when I am extremely happy about something.',
'When I get really happy about something, I tend to do things that can have bad consequences.',
'When overjoyed, I feel like I cant stop myself from going overboard.',
'When I am really excited, I tend not to think of the consequences of my actions.',
'I tend to act without thinking when I am really excited.']

var upps_responses = ['<span style="font-size: 30px">Disagree Strongly</span>', '<span style="font-size: 30px">Disagree Some</span>', '<span style="font-size: 30px">Agree Some</span>', '<span style="font-size: 30px">Agree Strongly</span>']

var upps_codings = ['forward', 'forward', 'forward', 'forward', 'forward', 'forward']

var survey_items = [grit_items, brief_items, future_time_items, impulse_venture_items, upps_items]
var responses = [grit_responses, brief_responses, future_time_responses, impulse_venture_responses, upps_responses]
var surveys = ['grit', 'brief', 'future_time', 'impulsive_venture', 'upps']
var survey_choices = [[66,89,71,82,77],[66,89,71,82,77],[66,89,71,82,77],[66,89],[66,89,71,82]]
var item_codings = [grit_codings, brief_codings, future_time_codings, impulse_venture_codings, upps_codings]
var stims = []
for (var si=0; si<survey_items.length; si++) {
	var items = survey_items[si]
	for (var i=0; i<items.length; i++) {
		var item_text = '<div class = centerbox><p class=item-text>' + items[i] + '</p></div><div class=response-text><div class=response-item>' + responses[si].join('</div><div class=response-item>') + '</div></div>'
		var item_coding = item_codings[si][i]
		var item_data = {'survey': surveys[si], 
						'item_responses': survey_choices[si],
						'item_coding': item_coding,
						'item_text': items[i],
						'options': responses[si]}
		stims.push({'stimulus': item_text, 'data': item_data, 'choices': [66,89,71,82,77]})
	}
}
var stim_index = [16,34,8,0,29,13,5,26,15,39,6,4,30,23,25,14,24,27,18,11,21,10,2,33,37,3,17,28,20,9,38,1,12,35,32,36,7,19,22,31]
stim_reorder = []
for (var i=0; i<stim_index.length; i++) {
	stim_reorder.push(stims[stim_index[i]])
}
stims = stim_reorder



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
	prompt: 'Left most response: thumb',
	on_finish: function(data) {
		var response = data.item_responses.indexOf(data.key_press)+1
		var coded_response = response
		if ((data.item_coding == 'reverse') & (response>0)) {
			coded_response = (data.item_responses.length+1) - response
		}
		jsPsych.data.addDataToLastTrial({'response': response, 'coded_response': coded_response})
	}
}

/* create experiment definition array */
survey_medley_experiment = []
test_keys(survey_medley_experiment, choices)
survey_medley_experiment.push(instructions_block)
setup_fmri_intro(survey_medley_experiment)
survey_medley_experiment.push(test_block)
survey_medley_experiment.push(end_block)