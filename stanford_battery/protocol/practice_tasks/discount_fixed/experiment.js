/* ************************************ */
/* Define helper functions */
/* ************************************ */

ITIs = [0,0.136,0.136,0.612]

var get_ITI = function() {
  return 4500 + ITIs.shift()*1000
 }

 var randomDraw = function(lst) {
  var index = Math.floor(Math.random() * (lst.length))
  return lst[index]
}

/* ************************************ */
/* Define experimental variables */
/* ************************************ */

// task specific variables
var choices = [37, 40]
var bonus_list = [] //keeps track of choices for bonus
//hard coded options 
var options = {
  small_amt: [20,20,20,20],
  large_amt: [50, 100, 100, 30],
  later_del: [40, 40, 80, 20]
}

var stim_html = []

//loop through each option to create html
for (var i = 0; i < options.small_amt.length; i++) {
  stim_html[i] =
      '<div class = dd-stim><div class = amtbox style = "color:white">'+options.large_amt[i]+'\u20AC</div><br><br>'+
      '<div class = delbox style = "color:white">'+ options.later_del[i]+' days</div></div>'
}

data_prop = []

for (var i = 0; i < options.small_amt.length; i++) {
  data_prop.push({
    small_amount: options.small_amt[i],
    large_amount: options.large_amt[i],
    later_delay: options.later_del[i]
  });
}

trials = []

//used new features to include the stimulus properties in recorded data
for (var i = 0; i < stim_html.length; i++) { 
  trials.push({
    stimulus: stim_html[i],
    data: data_prop[i]
  });
}

/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */

var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text></font size="+2">Choisissez entre <strong>20\u20AC aujourd\'hui</strong> ou l\'option presentee.<br><strong>Index:</strong> Accepter l\'option a l\'ecran (rejeter 20\u20AC aujourd\'hui). <br><strong>Majeur:</strong> Rejeter l\'option a l\'ecran (accepter 20\u20AC today)</font></div></div>',
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
  stimulus: '<div class = centerbox><div class = center-text>Preparez-vous</p></div>',
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
    exp_id: 'discount_fixed'
  },
  timing_post_trial: 0,
  on_finish: function() {
    var bonus = randomDraw(bonus_list)
    jsPsych.data.addDataToLastTrial({'bonus': bonus})
  }
};

//Set up experiment
var discount_fixed_experiment = []
discount_fixed_experiment.push(instructions_block);
discount_fixed_experiment.push(start_test_block);
for (i = 0; i < options.small_amt.length; i++) {
  var test_block = {
  type: 'poldrack-single-stim',
  data: {
    trial_id: "stim",
    exp_stage: "test"
  },
  stimulus:trials[i].stimulus,
  timing_stim: 4000,
  timing_response: get_ITI,  
  data: trials[i].data,
  is_html: true,
  choices: choices,
  response_ends_trial: false,
  timing_post_trial: 0,
  on_finish: function(data) {
    var choice = false;
    if (data.key_press == 37) {
      choice = 'larger_later';
      bonus_list.push({'amount': data.large_amount, 'delay': data.later_delay})
    } else if (data.key_press == 40) {
      choice = 'smaller_sooner';
      bonus_list.push({'amount': data.small_amount, 'delay': 0})
    }
    jsPsych.data.addDataToLastTrial({
      choice: choice
    });
  }
};

  discount_fixed_experiment.push(test_block)
}
discount_fixed_experiment.push(end_block);
