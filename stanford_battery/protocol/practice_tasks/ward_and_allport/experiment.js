/* ************************************ */
/* Define helper functions */
/* ************************************ */

//random ITIs for practice
var practice_ITIs = [0.5,0.1,0.2,0.0]
//optimized ITIs for test
var test_ITIs = [0.816,0.544,1.904,0.816,0.408,0.136,1.088,0.272,3.944,2.176,2.176,2.312,2.176,0.0,0.272,0.272,0.544,0.544,1.36,3.4,0.68,2.176,0.272,0.272,0.408,0.68,0.272,0.544,0.136,0.0,1.496,0.0,0.136,0.272,0.408,0.408,0.408,0.544,0.136,0.408,0.544,1.36,0.136,0.136,0.952,0.816,0.952,0.408]
var get_ITI = function() {
  return 2000 + ITIs.shift()*1000
 }

var getStim = function() {
  var ref_board = makeBoard('your_board', curr_placement, 'ref')
  var goal_state_board = makeBoard('peg_board', problems[problem_i].goal_state.problem)
  var canvas = '<div class = watt_canvas><div class="watt_vertical_line"></div></div>'
  var hold_box;
  if (held_ball !== 0) {
    ball = colors[held_ball - 1]
    hold_box = '<div class = watt_hand_box><div class = "watt_hand_ball watt_' + ball +
      '"><div class = watt_ball_label>' + ball[0] +
      '</div></div></div><div class = watt_hand_label><strong>Boule en main</strong></div>'
  } else {
    hold_box =
      '<div class = watt_hand_box></div><div class = watt_hand_label><strong>Boule en main</strong></div>'
  }
  return canvas + ref_board + goal_state_board + hold_box
}

var getFB = function() {
  var data = jsPsych.data.getLastTrialData()
  var goal_state = data.goal_state
  var isequal = true
  correct = false
  for (var i = 0; i < goal_state.length; i++) {
    isequal = arraysEqual(goal_state[i], data.current_position[i])
    if (isequal === false) {
      break;
    }
  }
  var feedback;
  if (isequal === true) {
    feedback = "Complete"
    correct = true
  } else {
    feedback = "Didn't get that one."
  }
  var ref_board = makeBoard('your_board', curr_placement)
  var goal_state_board = makeBoard('peg_board', goal_state)
  var canvas = '<div class = watt_canvas><div class="watt_vertical_line"></div></div>'
  var feedback_box = '<div class = watt_feedbackbox><p class = center-text>' + feedback +
    '</p></div>'
  return canvas + ref_board + goal_state_board + feedback_box
}

var pegClick = function(choice) {
  var peg = curr_placement[choice]
  var ball_location = 0
  if (held_ball === 0) {
    for (var i = peg.length - 1; i >= 0; i--) {
      if (peg[i] !== 0) {
        held_ball = peg[i]
        peg[i] = 0
        num_moves += 1
        break;
      }
    }
  } else {
    var open_spot = peg.indexOf(0)
    if (open_spot != -1) {
      peg[open_spot] = held_ball
      held_ball = 0
    }
  }
}

var makeBoard = function(container, ball_placement, board_type) {
  var board = '<div class = watt_' + container + '><div class = watt_base></div>'
  if (container == 'your_board') {
    board += '<div class = watt_board_label><strong>Votre Planche</strong></div>'
  } else {
    board += '<div class = watt_board_label><strong>Planche Cible</strong></div>'
  }
  for (var p = 0; p < 3; p++) {
    board += '<div id = watt_peg_' + (p + 1) + '><div class = watt_peg></div></div>' //place peg
      //place balls
    if (board_type == 'ref') {
      if (ball_placement[p][0] === 0 & held_ball === 0) {
        board += '<div id = watt_peg_' + (p + 1) + ' onclick = "pegClick(this.id)">'
      } else if (ball_placement[p].slice(-1)[0] !== 0 & held_ball !== 0) {
        board += '<div id = watt_peg_' + (p + 1) + ' onclick = "pegClick(this.id)">'
      } else {
        board += '<div class = special id = watt_peg_' + (p + 1) + ' onclick = "pegClick(this.id)">'
      }
    } else {
      board += '<div id = watt_peg_' + (p + 1) + ' >'
    }
    var peg = ball_placement[p]
    for (var b = 0; b < peg.length; b++) {
      if (peg[b] !== 0) {
        ball = colors[peg[b] - 1]
        board += '<div class = "watt_ball watt_' + ball + '"><div class = watt_ball_label>' + ball[0] +
          '</div></div>'
      }
    }
    board += '</div>'
  }
  board += '</div>'
  return board
}

var arraysEqual = function(arr1, arr2) {
  if (arr1.length !== arr2.length)
    return false;
  for (var i = arr1.length; i--;) {
    if (arr1[i] !== arr2[i])
      return false;
  }
  return true;
}

var reset_problem = function() {
    colors = jsPsych.randomization.shuffle(['Green', 'Red', 'Blue'])
    held_ball = 0
    problem_start_time = new Date()
    num_moves = 0;
    if (problem_i < problems.length) {
      curr_placement = jQuery.extend(true, [], problems[problem_i].start_state)
    }
}

var get_hand_choices = function() {
  var trial_choices = []
  var sum = 0
  for (var i=0; i<choices.length; i++) {
    sum = curr_placement[i].reduce(function(a,b) {return a+b;}, 0)
    if (sum > 0) {
      trial_choices.push(choices[i])
    }
  }
  return trial_choices
}

var get_board_choices = function() {
  var trial_choices = []
  for (var i=0; i<choices.length; i++) {
    if (curr_placement[i].indexOf(0) != -1) {
      trial_choices.push(choices[i])
    }
  }
  return trial_choices
}

/* ************************************ */
/* Define experimental variables */
/* ************************************ */
// task specific variables
var choices = [37,40,39]
var correct = false
var colors = ['Green', 'Red', 'Blue']
var problem_i = 0
var num_moves = 0 //tracks number of moves for a problem
var held_ball = 0
var ref_board = ''
// timing variables
var problem_start_time = 0
var start_time = new Date()
var task_limit = 600000

var problems = []
var test_problems = []
var practice_problems = []
// Problems can be either partially ambiguous or unambiguous (goal hierarchy)
// and either with and intermediate step or without (search depth)
// In this implementation all practice problems are unambiguous (UA) and
// all test are partially ambiguous (PA)
// set up practice problems
practice_problems = [
  {'start_state': [
      [2, 3, 0],
      [0, 0, 0],
      [1, 0, 0]
  ], 
  'goal_state': {
    'condition': 'UA_with_intermeidate',
    'problem': [
      [0, 0, 0],
      [0, 0, 0],
      [1, 2, 3]
    ]
  }},
  {'start_state': [
      [3, 0, 0],
      [1, 2, 0],
      [0, 0, 0]
  ], 
  'goal_state': {
    'condition': 'UA_with_intermeidate',
    'problem': [
      [0, 0, 0],
      [1, 3, 2],
      [0, 0, 0]
    ]
  }},
  {'start_state': [
      [0, 0, 0],
      [3, 0, 0],
      [1, 2, 0]
  ], 
  'goal_state': {
    'condition': 'UA_without_intermeidate',
    'problem': [
      [3, 2, 1],
      [0, 0, 0],
      [0, 0, 0]
    ]
  }},
  {'start_state': [
  	  [3, 0, 0],
      [0, 0, 0],
      [1, 2, 0]
  ], 
  'goal_state': {
    'condition': 'UA_without_intermeidate',
    'problem': [
      [0, 0, 0],
      [2, 3, 1],
      [0, 0, 0]
    ]
  }},
]


// set up practice
var exp_stage = 'practice'
var problems = practice_problems
var ITIs = practice_ITIs
// setup blocks
var curr_placement = jQuery.extend(true, [], problems[problem_i].start_state)

/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
/* define static blocks */
 var end_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text><i>+</i></div></div>',
  is_html: true,
  choices: [32],
  timing_response: -1,
  response_ends_trial: true,
  data: {
    trial_id: "end",
    exp_id: 'ward_and_allport'
  },
  timing_post_trial: 0
};

 var reminder_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Planifiez d\'avance!<br></br><br></br>Travaillez prudemment mais rapidement!</div></div>',
  is_html: true,
  choices: 'none',
  timing_response: 5000,
  response_ends_trial: true,
  data: {trial_id: "reminder"},
  timing_post_trial: 0
};

var reminder_node = {
    timeline: [reminder_block],
    conditional_function: function(){
        if(problem_i%15 == 0 && problem_i > 0){
            return true;
        } else {
            return false;
        }
    }
}


var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: "<div class = centerbox><div class = center-text>Resolvez les taches de la tour !<br><br>Planifiez d\'avance et travaillez rapidement!<br><br>Nous allons commencer par un peu de pratique.</div></div>",
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


var start_practice_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>+</p></div>',
  is_html: true,
  choices: 'none',
  timing_stim: 1500, 
  timing_response: 1500,
  data: {
    trial_id: "practice_start_block"
  },
  timing_post_trial: 500,
  on_finish: function() {
    reset_problem()
  }
};

var tohand_block = {
  type: 'poldrack-single-stim',
  stimulus: getStim,
  choices: get_hand_choices,
  is_html: true,
  data: {
    trial_id: "to_hand",
    exp_stage: exp_stage
  },
  timing_stim: -1,
  timing_response: -1,
  response_ends_trial: true,
  timing_post_trial: 0,
  on_finish: function(data) {
    pegClick(choices.indexOf(data.key_press))
    jsPsych.data.addDataToLastTrial({
      'current_position': jQuery.extend(true, [], curr_placement),
      'num_moves_made': num_moves,
      'min_moves': 3,
      'start_state': problems[problem_i].start_state,
      'goal_state': problems[problem_i].goal_state.problem,
      'condition': problems[problem_i].goal_state.condition,
      'problem_id': problem_i
    })
  }
}

var toboard_block = {
  type: 'poldrack-single-stim',
  stimulus: getStim,
  choices: get_board_choices,
  is_html: true,
  data: {
    trial_id: "to_board",
    exp_stage: exp_stage
  },
  timing_stim: -1,
  timing_response: -1,
  response_ends_trial: true,
  timing_post_trial: 0,
  on_finish: function(data) {
    pegClick(choices.indexOf(data.key_press))
    jsPsych.data.addDataToLastTrial({
      'current_position': jQuery.extend(true, [], curr_placement),
      'num_moves_made': num_moves,
      'min_moves': 3,
      'start_state': problems[problem_i].start_state,
      'goal_state': problems[problem_i].goal_state.problem,
      'condition': problems[problem_i].goal_state.condition,
      'problem_id': problem_i
    })
  }
}

var feedback_block = {
  type: 'poldrack-single-stim',
  stimulus: getFB,
  choices: 'none',
  is_html: true,
  data: {
    trial_id: 'feedback'
  },
  timing_stim: 1000,
  timing_response: get_ITI,
  timing_post_trial: 0,
  on_finish: function() {
    var time_elapsed = new Date() - problem_start_time
    jsPsych.data.addDataToLastTrial({
      'exp_stage': exp_stage,
      'problem_time': time_elapsed,
      'num_moves_made': num_moves,
      'min_moves': 3,
      'correct': correct
    })
    //advance round
    problem_i += 1
    reset_problem()
  },
}

var problem_node = {
  timeline: [tohand_block, toboard_block],
  loop_function: function(data) {
    data = data[1]
    var goal_state = data.goal_state
    var isequal = true
    for (var i = 0; i < goal_state.length; i++) {
      isequal = arraysEqual(goal_state[i], data.current_position[i])
      if (isequal === false) {
        break;
      }
    }
    return !isequal
  }
}

var task_node = {
  timeline: [problem_node, feedback_block, reminder_node],
  loop_function: function(data) {
    var time_elapsed = new Date() - start_time
    if (time_elapsed < task_limit && problem_i < problems.length) {
      return true
    } else {
      return false
    }
  },
  timing_post_trial: 1000
}


/* create experiment definition array */
var ward_and_allport_experiment = [];

ward_and_allport_experiment.push(instructions_block);
ward_and_allport_experiment.push(start_practice_block);
ward_and_allport_experiment.push(task_node)
ward_and_allport_experiment.push(end_block);
