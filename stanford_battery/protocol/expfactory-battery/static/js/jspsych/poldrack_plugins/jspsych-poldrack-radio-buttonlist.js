/**
 * jspsych-radio-buttonlist
 * a jspsych plugin for displaying a form with a list of radio buttons
 *
 * A. Zeynep Enkavi 
 NOTE: survey-multi-choice might be a better plugin for most cases. 
 This plugin requires more raw html work when specifying questions
 (thouhg this may cater to more flexible formatting needs).
 Additionally data is saved in rows for each questions minimizing 
 required text parsing later on.
 
 */

 jsPsych.plugins["poldrack-radio-buttonlist"] = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

    // set default values for parameters
    trial.preamble = (typeof trial.preamble === 'undefined') ? "" : trial.preamble;
    trial.buttonlist = trial.buttonlist;
    trial.checkAll = trial.checkAll;
    trial.numq = trial.numq;

    // allow variables as functions
    // this allows any trial variable to be specified as a function
    // that will be evaluated when the trial runs. this allows users
    // to dynamically adjust the contents of a trial as a result
    // of other trials, among other uses. you can leave this out,
    // but in general it should be included
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

    display_element.append($('<div>', {
        "id": 'jspsych-radio-buttonlist-preamble',
        "class": 'jspsych-radio-buttonlist-preamble'
      }));

      $('#jspsych-radio-buttonlist-preamble').append(trial.preamble);
      
      //Display form with a specific name (referred to later when submit button is clicked)
      //Appending directly instead of adding a div first and then populating it
      display_element.append('<form id = "jspsych-radio-buttonlist">' + trial.buttonlist + '</form>');

      // helper function to loop through each button in form and submit data
      function loopForm(form, checkAll) {
      // measure response time (to be submitted with data - per page for now)
      var endTime = (new Date()).getTime();
      var response_time = endTime - startTime;
        // count question number for trial_index
      var qnum = 1;

      //alert if all q's on page are mandatory but not answered and stay on page if not
      if (checkAll){
        if($("input[type=radio]:checked").length < trial.numq){
          alert("Please make sure to answer all questions.");
          return;
        }
      }

      //loop through all checked radio buttons
      for (var i = 0; i < form.elements.length; i++ ) {
          if (form.elements[i].type == 'radio') {
            if (form.elements[i].checked == true) {
              //write data for each checked radio button
              jsPsych.data.write({
                'rt': response_time,
                'response': (form.elements[i].value)
              });
              //add trial number to data
              jsPsych.data.addDataToLastTrial({trial_index: form.elements[i].name});
              }
            }
          }
        

        display_element.html('');

        // next trial
        jsPsych.finishTrial();
      };      

      // add submit button
      display_element.append($('<button>', {
        'id': 'jspsych-radio-buttonlist-next',
        'class': 'jspsych-radio-buttonlist'
      }));

      //add display text to button
      $("#jspsych-radio-buttonlist-next").html('Submit Answers');
      
      //define on click function for button
      $("#jspsych-radio-buttonlist-next").click(function() {
        
        var thisForm = document.getElementById("jspsych-radio-buttonlist");

        loopForm(thisForm, trial.checkAll);

      });

      var startTime = (new Date()).getTime();
  };

  return plugin;
})();