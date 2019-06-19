/*
jspsych-consent

a jspsych plugin to create a consent page and check for response without requring an external html page

Ayse Zeynep Enkavi*/

jsPsych.plugins["consent"] = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

    // set default values for parameters
    trial.consent_text = trial.consent_text || "";
    trial.checkbox_text = trial.checkbox_text || "Check here";
    trial.button_text = trial.button_text || "Continue";
    trial.container = trial.container || -1;

    // allow variables as functions
    // this allows any trial variable to be specified as a function
    // that will be evaluated when the trial runs. this allows users
    // to dynamically adjust the contents of a trial as a result
    // of other trials, among other uses. you can leave this out,
    // but in general it should be included
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

    //display consent text, checkbox and button
      display_element.append($('<div>', {
          html: trial.consent_text + //consent_text - should specify a container
            "<p class = block-text><input type='checkbox' id = 'checkbox'>" + trial.checkbox_text + "</p>" +
            "<button type='button' id = 'start'>" + trial.button_text +"</button>",
          id: 'jspsych-consent-text'
        }));


      //specify what happens when start button is clicked
      $("#start").click(function() {
        
        // measure response time
        var endTime = (new Date()).getTime();
        var response_time = endTime - startTime;

        // check if consent given
        if ($('#checkbox').is(':checked')) {
          // save data
          jsPsych.data.write({
            "rt": response_time,
          });

          display_element.html('');

          // next trial
          jsPsych.finishTrial();
          
          //return true;
        }

        // if consent not given alert subject and don't start
        else {
          alert("If you wish to participate, you must check the box to agree to participate in this study.");
          return false;
        }

      });
      
   var startTime = (new Date()).getTime();  

  };

  return plugin;
})();
