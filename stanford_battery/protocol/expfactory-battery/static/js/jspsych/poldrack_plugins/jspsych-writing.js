/**
 * jspsych-writing
 * Ian Eisenberg
 *
 * plugin for writing text
 *
 * documentation: docs.jspsych.org
 *
 **/


jsPsych.plugins["writing"] = (function() {

  var plugin = {};


  plugin.trial = function(display_element, trial) {

    // if any trial variables are functions
    // this evaluates the function and replaces
    // it with the output of the function
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

    // set default values for the parameters
    trial.text_class = trial.text_class || 'jspsych-writing-box'
    trial.choices = trial.choices || [];
    trial.initial_text = trial.initial_text || ''
    trial.timing_response = trial.timing_response || -1;
    trial.is_html = (typeof trial.is_html == 'undefined') ? false : trial.is_html;
    trial.prompt = trial.prompt || "";

    // this array holds handlers from setTimeout calls
    // that need to be cleared if the trial ends early
    var setTimeoutHandlers = [];

    // display text area the first time this plugin is called in a series
    var myElem = document.getElementById('jspsych-writing-box');
    if (myElem === null) {
      display_element.append($('<textarea>', {
        "id": 'jspsych-writing-box',
        "class": trial.text_class
      }))
      $("#jspsych-writing-box").focus()
    }

    //show prompt if there is one
    if (trial.initial_text !== "") {
      $("#jspsych-writing-box").attr('placeholder', trial.initial_text);
    }

    // store writing
    var key_strokes = []

    // store response
    var response = {
      rt: -1,
      key: -1
    };
    var last_response_time = 0

    // function to end trial when it is time
    var end_trial = function() {

      // kill any remaining setTimeout handlers
      for (var i = 0; i < setTimeoutHandlers.length; i++) {
        clearTimeout(setTimeoutHandlers[i]);
      }

      // kill keyboard listeners
      if (typeof keyboardListener !== 'undefined') {
        jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
      }
      
      
      //get text
      final_text = $('#jspsych-writing-box').val()
      // clear the display
      display_element.html('');
      //jsPsych.data.write(trial_data);
      $("#jspsych-writing-box").unbind()
      // move on to the next trial
      jsPsych.finishTrial({'key_strokes': key_strokes, 'final_text': final_text});
    };

    var after_response = function(info) {
      // after a valid response, the stimulus will have the CSS class 'responded'
      // which can be used to provide visual feedback that a response was recorded
      // only record the first response
      response = info
    
      // gather the data to store for the trial
      var trial_data = {
        "rt": response.rt - last_response_time,
        "key_press": response.key
      };
      last_response_time = response.rt
      key_strokes.push(trial_data)
    };


    // start the response listener
    if (JSON.stringify(trial.choices) != JSON.stringify(["none"])) {
      var keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
        callback_function: after_response,
        valid_responses: trial.choices,
        rt_method: 'date',
        persist: true,
        allow_held_key: false
      });
    }

    $("#jspsych-writing-box").on('focusout', function() {
      alert('Please write for the full time! Disable this alert if you really need to leave this page.')
      setTimeout(function() {$("#jspsych-writing-box").focus()}, 1);
    });

    // end trial if time limit is set
    if (trial.timing_response > 0) {
      var t1 = setTimeout(function() {
        end_trial();
      }, trial.timing_response);
      setTimeoutHandlers.push(t1);
    }

  }
                            
  return plugin;
})();