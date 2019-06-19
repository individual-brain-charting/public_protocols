/* ************************************ */
/* Define helper functions */
/* ************************************ */
var get_ITI = function() {
  // ref: https://gist.github.com/nicolashery/5885280
  function randomExponential(rate, randomUniform) {
    // http://en.wikipedia.org/wiki/Exponential_distribution#Generating_exponential_variates
    rate = rate || 1;

    // Allow to pass a random uniform value or function
    // Default to Math.random()
    var U = randomUniform;
    if (typeof randomUniform === 'function') U = randomUniform();
    if (!U) U = Math.random();

    return -Math.log(U) / rate;
  }
  gap = randomExponential(1/2)*500
  if (gap > 6000) {
    gap = 6000
  } else if (gap < 0) {
  	gap = 0
  } else {
  	gap = Math.round(gap/1000)*1000
  }
  return 500 + gap //500 (minimum ITI)
 }
 
var appendTestData = function() {
	jsPsych.data.addDataToLastTrial({
		num_cards: numCards,
		num_loss_cards: numLossCards,
		gain_amount: gainAmt,
		loss_amount: lossAmt,
		round_points: roundPointsArray.slice(-1),
		whichRound: whichRound
	})
}

var randomDraw = function(lst) {
  var index = Math.floor(Math.random() * (lst.length))
  return lst[index]
}

function chunkify(a, n, balanced) {
    if (n < 2)
        return [a];
    var len = a.length, out = [], i = 0, size;
    if (len % n === 0) {
        size = Math.floor(len / n);
        while (i < len) {
            out.push(a.slice(i, i += size));
        }
    }
    else if (balanced) {
        while (i < len) {
            size = Math.ceil((len - i) / n--);
            out.push(a.slice(i, i += size));
        }
    }
    else {
        n--;
        size = Math.floor(len / n);
        if (len % size === 0)
            size--;
        while (i < size * n) {
            out.push(a.slice(i, i += size));
        }
        out.push(a.slice(size * n));
    }
    return out;
}

var getButtons = function(nCards) {
	var card_array = []
	for (var i=0; i<nCards; i++) {
		card_array.push(i)
	}
	var chunk_index = 0
	var chunks = chunkify(card_array,choices.length,true)
	button_values = []
	for (var i=0; i<chunks.length; i++) {
		button_values.push(randomDraw(chunks[i]))
	}
	var buttons = ""
	buttons = "<div class = allbuttons>"
	for (i = 0; i < choices.length; i++) {
		buttons += "<button type = 'button' class = 'CCT-btn chooseButton' id = " + i +
			" >" + button_values[i] + "</button>"
	}
	return buttons
}

var getBoard = function(nCards) {
	var board = "<div class = cct-box>"+
	"<div class = titleBigBox>   <div class = titleboxLeft><div class = game-text id = game_round>Game Round: </div></div>   <div class = titleboxLeft1><div class = game-text id = loss_amount>Loss Amount: </div></div>    <div class = titleboxMiddle1><div class = game-text id = gain_amount>Gain Amount: </div></div>    <div class = titlebox><div class = game-text>How many cards do you want to take? </div></div>     <div class = titleboxRight1><div class = game-text id = num_loss_cards>Number of Loss Cards: </div></div>   <div class = titleboxRight><div class = game-text id = current_round>Current Round Points: 0</div></div>" +
	getButtons(nCards)+
	"</div><div class = cardbox>"
	for (i = 1; i < nCards+1; i++) {
		board += "<div class = square><input type='image' id = " + i +
			" class = 'card_image' src='/static/experiments/columbia_card_task_cold/images/beforeChosen.png'></div>"
	}

	board += "</div>"
	return board
}

var getText = function() {
	return '<div class = centerbox><p class = block-text>Overall, you earned ' + totalPoints + ' points. These are the points used for your bonus from three randomly picked trials:  ' +
		'<ul list-text><li>' + prize1 + '</li><li>' + prize2 + '</li><li>' + prize3 + '</li></ul>' + '</div>'
}

var turnOneCard = function(whichCard, win) {
	if (win === 'loss') {
		document.getElementById("c" + whichCard + "").src =
			'/static/experiments/columbia_card_task_cold/images/loss.png';
	} else {
		document.getElementById("c" + whichCard + "").src =
			'/static/experiments/columbia_card_task_cold/images/chosen.png';
	}
}

var appendPayoutData = function(){
	jsPsych.data.addDataToLastTrial({reward: [prize1, prize2, prize3]})
}

var getChoice = function(key_press) {
	var choice = choices.indexOf(key_press)
	var cardID = button_values[choice]
	var roundPoints = 0
	for (var i=0; i<cardID; i++) {
		if (Math.random() > numLossCards/numCards) {
			roundPoints += gainAmt
		} else {
			roundPoints -= lossAmt
			break
		}
	}
	roundPointsArray.push(roundPoints)
	jsPsych.data.addDataToLastTrial({
		choice: choice,
		num_cards_chosen: cardID
	})
}

// appends text to be presented in the game
function appendTextAfter(input, search_term, new_text) {
	var index = input.indexOf(search_term) + search_term.length
	return input.slice(0, index) + new_text + input.slice(index)
}

var getCardArray = function(nCards){
	var cardArray = []
	for (var i = 0; i<nCards; i++) {
		cardArray.push(i+1)
	}
	return cardArray
}

var setNextRound = function() {
	roundParams = ParamsArray.shift()
	numCards = roundParams[0]
	numLossCards = roundParams[1]
	lossAmt = roundParams[2]
	gainAmt = roundParams[3]
	cardArray = getCardArray(numCards)
	roundOver = 0
	roundPoints = 0
	whichClickInRound = 0
	whichRound = whichRound + 1
	lossClicked = false
}

// this function sets up the round params (loss amount, gain amount, which ones are loss cards, initializes the array for cards to be clicked, )
var getRound = function() {
	var gameState = getBoard(numCards)
	gameState = appendTextAfter(gameState, 'Game Round: ', whichRound)
	gameState = appendTextAfter(gameState, 'Loss Amount: ', lossAmt)
	gameState = appendTextAfter(gameState, 'Number of Loss Cards: ', numLossCards)
	gameState = appendTextAfter(gameState, 'Gain Amount: ', gainAmt)
	return gameState
}




/* ************************************ */
/* Define experimental variables */
/* ************************************ */
// task specific variables
var choices = [66,89,71,82,77]
var currID = 0
// global variables to hold round params
var numCards = 6
var numLossCards = 1
var gainAmt = ""
var lossAmt = ""
var points = []
var whichRound = 0
var totalPoints = 0
var roundOver = 0
var roundPointsArray = []
var button_values = []
var prize1 = 0
var prize2 = 0
var prize3 = 0
// timing variables
var start_time = new Date()
var task_limit = 720000

//round params
block1_params = [[6,1,-70,12],[6,1,-75,14],[6,1,-70,15],
	[6,1,-75,17],[8,2,-60,24],[8,2,-75,29],[9,2,-65,17],[10,1,-95,14],
	[10,2,-65,15],[10,2,-65,17],[12,2,-70,13],[12,2,-80,15],[15,3,-65,14],
	[16,1,-45,1],[16,3,-70,15],[10,3,-50,30],[15,2,-70,17], [16,1,-95,7],
	[16,1,-100,9],[16,2,-80,15],[16,2,-70,16],[16,5,-45,30]]

block2_params = [[6,1,-75,13],[6,1,-70,14],[6,1,-80,16],[6,1,-70,17],
	[8,2,-65,25],[8,2,-80,30],[10,1,-95,13],[10,1,-90,14],[10,2,-70,16],
	[12,1,-100,7],[12,2,-80,14],[12,2,-75,15],[15,3,-65,15],[16,3,-70,14],
	[16,5,-30,11],[15,2,-75,15],[15,2,-75,17],[16,1,-25,2],[16,1,-95,9],
	[16,1,-100,11],[16,2,-75,16],[16,2,-80,17]]

block3_params = [[6,1,-70,13],[6,1,-80,15],[6,1,-75,16],[8,2,-55,21],
	[8,2,-65,26],[9,2,-60,15],[10,1,-90,13],[10,1,-95,15],[10,2,-65,16],
	[12,1,-95,7],[12,2,-75,14],[12,2,-70,15],[15,3,-70,16],[16,3,-65,14],
	[16,3,-75,16],[15,2,-80,16],[15,2,-80,17],[16,1,-15,1],[16,1,-100,10],
	[16,2,-75,15],[16,2,-80,16],[16,5,-5,4]]

block4_params = [[6,1,-80,14],[6,1,-75,15],[6,1,-70,16],[8,2,-60,23],
	[8,2,-70,27],[9,2,-65,16],[10,1,-85,13],[10,2,-65,14],[10,2,-70,17],
	[12,2,-75,13],[12,2,-70,14],[12,2,-80,16],[15,3,-65,16],[16,3,-75,15],
	[16,5,-35,14],[15,2,-75,16],[15,2,-70,16],[16,1,-90,8],[16,1,-95,10],
	[16,2,-70,15],[16,2,-85,16],[16,2,-75,17]]

ParamsArray = block1_params.concat(block2_params,block3_params,block4_params)




/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
/* define static blocks */
var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Try to get as many points as possible!<br><br>Select the number of cards you want by pressing the finger corresponding to the buttons on the screen<br><br>The loss amount, the gain amount, and the number of loss cards may change each trial</div></div>',
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
  	setNextRound()
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

var rest_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Take a break!<br>Next run will start in a moment</div></div>',
  is_html: true,
  choices: 'none',
  timing_response: 10000,
  data: {
    trial_id: "rest_block"
  },
  timing_post_trial: 1000
};


var test_block = {
	type: 'poldrack-single-stim',
	stimulus: getRound,
	choices: choices,
	is_html: true,
	response_ends_trial: true,
	data: {
		trial_id: 'stim',
		exp_stage: 'test'
	},
	timing_post_trial: get_ITI,
	on_finish: function(data) {
		getChoice(data.key_press)
		appendTestData()
		setNextRound()
	}
};

var rest_node = {
    timeline: [rest_block],
    conditional_function: function(){
        if(whichRound%44 == 1 && whichRound > 2){
            return true;
        } else {
            return false;
        }
    }
}


var test_node = {
  timeline: [test_block, rest_node],
  loop_function: function(data) {
    var time_elapsed = new Date() - start_time
    if (time_elapsed < task_limit && ParamsArray.length>0) {
      return true
    } else {
      return false
    }
  },
  timing_post_trial: 1000
}

var payout_text = {
	type: 'poldrack-text',
	text: getText,
	data: {
		trial_id: 'reward'
	},
	cont_key: [32],
	timing_post_trial: 1000,
	on_finish: appendPayoutData,
};

var payoutTrial = {
	type: 'call-function',
	data: {
		trial_id: 'calculate reward'
	},
	func: function() {
		totalPoints = math.sum(roundPointsArray)
		randomRoundPointsArray = jsPsych.randomization.repeat(roundPointsArray, 1)
		prize1 = randomRoundPointsArray.pop()
		prize2 = randomRoundPointsArray.pop()
		prize3 = randomRoundPointsArray.pop()
		performance_var = prize1 + prize2 + prize3
	}
};



/* create experiment definition array */
var columbia_card_task_cold_experiment = [];
test_keys(columbia_card_task_cold, choices)
columbia_card_task_cold_experiment.push(instructions_block);
setup_fmri_intro(columbia_card_task_cold_experiment)
columbia_card_task_cold_experiment.push(start_test_block);
columbia_card_task_cold_experiment.push(test_node)
columbia_card_task_cold_experiment.push(payoutTrial);
columbia_card_task_cold_experiment.push(payout_text);
columbia_card_task_cold_experiment.push(end_block);
