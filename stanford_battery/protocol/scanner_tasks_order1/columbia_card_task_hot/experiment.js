/* ************************************ */
/* Helper Functions                     */
/* ************************************ */
var ITIs = [0.204,0.204,0.272,0.204,0.408,0.136,0.272,0.34,0.136,0.34,0.068,0.0,0.204,1.02,0.0,0.0,0.068,0.476,0.136,0.068,0.0,0.0,0.204,0.204,0.272,0.136,0.204,0.272,0.272,0.34,0.204,0.068,0.0,0.408,0.204,0.136,0.34,0.068,0.34,0.136,0.068,0.068,0.068,0.136,0.0,0.136,0.34,0.408,0.136,0.136,0.0,0.068,0.0,0.0,0.136,0.136,0.476,0.204,0.068,0.068,0.34,0.476,0.272,0.884,0.136,0.136,0.068,0.068,0.612,0.476,0.0,0.068,0.204,0.272,0.068,0.272,0.748,0.068,0.0,0.204,0.068,0.068,0.34,0.0,0.0,0.272,0.204,0.0]
var get_ITI = function() {
  return 2250 + ITIs.shift()*1000
 }

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

function deleteText(input, search_term) {
	index = input.indexOf(search_term)
	indexAfter = input.indexOf(search_term) + search_term.length
	return input.slice(0, index) + input.slice(indexAfter)
}


function appendTextAfter(input, search_term, new_text) {
	var index = input.indexOf(search_term) + search_term.length
	return input.slice(0, index) + new_text + input.slice(index)
}

function appendTextAfter2(input, search_term, new_text, deleted_text) {
	var index = input.indexOf(search_term) + search_term.length
	var indexAfter = index + deleted_text.length
	return input.slice(0, index) + new_text + input.slice(indexAfter)
}

var getBoard = function(nCards) {
	var board = "<div class = cct-box>"+
	"<div class = titleBigBox>   <div class = titleboxLeft><div class = game-text id = game_round>Tour: </div></div>   <div class = titleboxLeft1><div class = game-text id = loss_amount>Pertes: </div></div>    <div class = titleboxMiddle1><div class = game-text id = gain_amount>Gains: </div></div>    <div class = titlebox><div class = game-text>Combien de cartes voulez-vous prendre? </div></div>     <div class = titleboxRight1><div class = game-text id = num_loss_cards><font size='+3'>Mauveaises Cartes: </font></div></div>   <div class = titleboxRight><div class = game-text id = current_round>Points du tour: 0</div></div>"+
	"<div class = cardbox>"
	for (i = 1; i < nCards+1; i++) {
		board += "<div class = square><input type='image' id = " + i +
			" class = 'card_image' src='/static/experiments/columbia_card_task_hot/images/beforeChosen.png'></div>"
	}
	board += "</div>"
	return board
}

var getCardArray = function(nCards){
	var cardArray = []
	for (var i = 0; i<nCards; i++) {
		cardArray.push(i+1)
	}
	return cardArray
}

var getText = function() {
	return '<div class = centerbox><div class = center-text>+</div></div>'
}

var appendPayoutData = function(){
	jsPsych.data.addDataToLastTrial({reward: [prize1, prize2, prize3]})
}

var appendTestData = function() {
	jsPsych.data.addDataToLastTrial({
		which_round: whichRound,
		num_click_in_round: whichClickInRound,
		num_cards: numCards,
		num_loss_cards: numLossCards,
		gain_amount: gainAmt,
		loss_amount: lossAmt,
		round_points: roundPoints,
		clicked_on_loss_card: lossClicked
	})
}

// Functions for "top" buttons during test (no card, end round, collect)
var endRound = function() {
	currID = 'endRoundButton'
	roundOver=2
}

// Clickable card function during test
var chooseCard = function() {
	var notClicked = cardArray.filter(function(x) { return (jQuery.inArray(x,clickedGainCards) == -1)})
	currID = notClicked[getRandomInt(0,notClicked.length)]
	whichClickInRound = whichClickInRound + 1
	if (whichLossCards.indexOf(currID) != -1) {
		clickedLossCards.push(currID)
		index = unclickedCards.indexOf(currID, 0)
		unclickedCards.splice(index, 1)
		roundPoints = roundPoints + lossAmt
		lossClicked = true
		roundOver = 2
	} else { // if you click on a gain card
		clickedGainCards.push(currID) //as a string
		index = unclickedCards.indexOf(currID, 0)
		unclickedCards.splice(index, 1)
		roundPoints = roundPoints + gainAmt
	}
}

var getRound = function() {
	var gameState = getBoard(numCards)
	if (roundOver === 0) { //this is for the start of a round
		whichLossCards = jsPsych.randomization.shuffle(cardArray).slice(0,numLossCards)
		gameState = appendTextAfter(gameState, 'Tour: ', whichRound)
		gameState = appendTextAfter(gameState, 'Pertes: ', lossAmt)
		gameState = appendTextAfter2(gameState, 'Points du tour: ', roundPoints, '0')
		gameState = appendTextAfter(gameState, 'Mauveaises Cartes: ', numLossCards)
		gameState = appendTextAfter(gameState, 'Gains: ', gainAmt)
		roundOver = 1
	} else if (roundOver == 1) { //this is for during the round
		gameState = appendTextAfter(gameState, 'Tour: ', whichRound)
		gameState = appendTextAfter(gameState, 'Pertes: ', lossAmt)
		gameState = appendTextAfter2(gameState, 'Points du tour: ', roundPoints, '0')
		gameState = appendTextAfter(gameState, 'Mauveaises Cartes: ', numLossCards)
		gameState = appendTextAfter(gameState, 'Gains: ', gainAmt)
		for (i = 0; i < clickedGainCards.length; i++) {
			gameState = appendTextAfter2(gameState, "id = " + "" + clickedGainCards[i] + ""," class = 'card_image' src='/static/experiments/columbia_card_task_hot/images/chosen.png'", " class = 'card_image' src='/static/experiments/columbia_card_task_hot/images/beforeChosen.png'")
		}
	} else if (roundOver == 2) { //this is for end the round
		roundOver = 3
		gameState = appendTextAfter(gameState, 'Tour: ', whichRound)
		gameState = appendTextAfter(gameState, 'Pertes: ', lossAmt)
		gameState = appendTextAfter2(gameState, 'Points du tour: ', roundPoints, '0')
		gameState = appendTextAfter(gameState, 'Mauveaises Cartes: ', numLossCards)
		gameState = appendTextAfter(gameState, 'Gains: ', gainAmt)
		var clickedCards = clickedGainCards.concat(clickedLossCards)
		var notClicked = cardArray.filter(function(x) { return (jQuery.inArray(x,clickedCards) == -1)})
		notClicked = jsPsych.randomization.shuffle(notClicked)
		lossCardsToTurn = notClicked.slice(0,numLossCards-clickedLossCards.length)
		gainCardsToTurn = notClicked.slice(numLossCards-clickedLossCards.length)
		for (var i = 1; i < numCards+1; i++) {
			if (clickedGainCards.indexOf(i) != -1 ) {
				gameState = appendTextAfter2(gameState, "id = " + "" + i + ""," class = 'card_image' src='/static/experiments/columbia_card_task_hot/images/chosen.png'", " class = 'card_image' src='/static/experiments/columbia_card_task_hot/images/beforeChosen.png'")
			} else if (clickedLossCards.indexOf(i) != -1 ) {
				gameState = appendTextAfter2(gameState, "id = " + "" + i + ""," class = 'card_image' src='/static/experiments/columbia_card_task_hot/images/loss.png'", " class = 'card_image' src='/static/experiments/columbia_card_task_hot/images/beforeChosen.png'")
			} 
		}

		setTimeout(function() {
			for (var k = 0; k < lossCardsToTurn.length; k++) {
				document.getElementById('' + lossCardsToTurn[k] + '').src =
				'/static/experiments/columbia_card_task_hot/images/loss.png';
			}
			for (var j = 0; j < gainCardsToTurn.length; j++) {
				document.getElementById('' + gainCardsToTurn[j] + '').src =
				'/static/experiments/columbia_card_task_hot/images/chosen.png';
			}
		}, 750)
	}
	return gameState
}

var setNextRound = function() {
	roundParams = ParamsArray.shift()
	numCards = roundParams[0]
	numLossCards = roundParams[1]
	lossAmt = roundParams[2]
	gainAmt = roundParams[3]
	cardArray = getCardArray(numCards)
	unclickedCards = cardArray
	clickedGainCards = [] //num
	clickedLossCards = [] //num
	roundOver = 0
	roundPoints = 0
	whichClickInRound = 0
	whichRound = whichRound + 1
	lossClicked = false
}

var turnCards = function(cards) {
	for (i = 0; i < numCards; i++) {
		if (whichGainCards.indexOf(i) != -1) {
			document.getElementById('' + i + '').src =
				'/static/experiments/columbia_card_task_hot/images/chosen.png';
		} else if (whichLossCards.indexOf(i) != -1) {
			document.getElementById('' + i + '').src =
				'/static/experiments/columbia_card_task_hot/images/loss.png';
		}
	}
}

var turnOneCard = function(whichCard, win) {
	if (win === 'loss') {
		document.getElementById("" + whichCard + "").src =
			'/static/experiments/columbia_card_task_hot/images/loss.png';
	} else {
		document.getElementById("" + whichCard + "").src =
			'/static/experiments/columbia_card_task_hot/images/chosen.png';
	}
}

/* ************************************ */
/* Experimental Variables               */
/* ************************************ */
// task specific variables
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

//generic params
var numCards = ParamsArray[0][0]
var choices = [89, 71]
var currID = ""
var numLossCards = ""
var gainAmt = ""
var lossAmt = ""
var lossClicked = false
var whichClickInRound = 0
var whichRound = 0
var roundPoints = 0
var totalPoints = 0
var roundOver = 0 //0 at beginning of round, 1 during round, 2 at end of round
var instructPoints = 0
var clickedGainCards = []
var clickedLossCards = []
var roundPointsArray = [] 
var whichGainCards = []
var whichLossCards = []
var prize1 = 0
var prize2 = 0
var prize3 = 0
var num_blocks = 0
// timing variables
var start_time = new Date()
var task_limit = 480000


/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
/* define static blocks */
var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text><font size="+3">Essayez d\'obtenir autant de points que possible<br><br>Le montant des pertres, le montant du gain et le nombre de cartes de perte peuvent changer a chaque essai<br><br>Index: Prendre autre carte <br>Majeur: Fin de la ronde</font></div></div>',
  is_html: true,
  timing_stim: -1, 
  timing_response: -1,
  response_ends_trial: true,
  choices: [32],
  data: {
    trial_id: "instructions",
  },
  timing_post_trial: 500,
  on_finish: function() {
  	start_time = new Date()
  }
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
		exp_id: 'columbia_card_task_hot'
	},
	timing_post_trial: 0
};

var rest_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>+</div></div>',
  is_html: true,
  choices: 'none',
  timing_response: 10000,
  data: {
    trial_id: "rest_block"
  },
  timing_post_trial: 1000
};


var task_block = {
	type: 'poldrack-single-stim',
	stimulus: getRound,
	choices: choices,
	is_html: true,
	data: {
		trial_id: 'stim',
		exp_stage: 'test'
	},
	timing_post_trial: 0,
	response_ends_trial: true,
	on_finish: function(data) {
		if (data.key_press == choices[0]) {
			chooseCard()
		} else {
			endRound()
		}
		appendTestData()
	}
};

var task_node = {
	timeline: [task_block],
	loop_function: function(data) {
		if (roundOver == 2) {
			return false
		} else {
			return true
		}
	},
	timing_post_trial: 1000
}

var ITI_block = {
	type: 'poldrack-single-stim',
	stimulus: getRound,
	is_html: true,
	choices: 'none',
	data: {
		trial_id: "ITI"
	},
	timing_post_trial: 0,
	timing_stim: 2250,
	timing_response: get_ITI,
	on_finish: function() {
		roundPointsArray.push(roundPoints)
		setNextRound()
	}
}

var rest_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>+</div></div>',
  is_html: true,
  choices: 'none',
  timing_response: 10000,
  data: {
    trial_id: "rest_block"
  },
  timing_post_trial: 1000
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
  timeline: [task_node, ITI_block, rest_node],
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
var columbia_card_task_hot_experiment = [];
test_keys(columbia_card_task_hot_experiment, choices)
columbia_card_task_hot_experiment.push(instructions_block)
setup_fmri_intro(columbia_card_task_hot_experiment)
columbia_card_task_hot_experiment.push(start_test_block);
columbia_card_task_hot_experiment.push(test_node)
columbia_card_task_hot_experiment.push(payoutTrial);
columbia_card_task_hot_experiment.push(payout_text);
columbia_card_task_hot_experiment.push(end_block);
