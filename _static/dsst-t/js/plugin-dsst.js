var jsPsychDsst = (function (jspsych) {
  'use strict';

  const info = {
    name: 'dsst',
    description: '',
    parameters: {
      stimuli: {
        type: jspsych.ParameterType.HTML_STRING,
        array: true,
        pretty_name: 'Stimuli',
        description: 'The paths of the image files to be displayed.'
      },
      target: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Target',
        description: 'The index of the target image to be matched.'
      },
      valid_responses: {
        type: jspsych.ParameterType.KEYCODE,
        pretty_name: 'Valid responses',
        description: 'The key the subject is allowed to press to respond to the stimulus.'
      },
      trial_duration: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show trial before it ends.'
      },
      feedback_duration: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Trial duration',
        default: 150,
        description: 'How long to show feedback before it ends.'
      },
      iti_duration: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'ITI duration',
        default: 150,
        description: 'How long to hide stimuli before trial starts.'
      }
    }
  }

  /**
  * jspsych-dsst
  * Sam Zorowitz
  *
  * plugin for running one trial of the digit symbol matching task
  *
  **/
  class DsstPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }
    trial(display_element, trial) {

      // ---------------------------------- //
      // Section 1: Define HTML             //
      // ---------------------------------- //

      // Define HTML
      var new_html = '';

      // Insert CSS
      new_html += `<style>
      .dsst-target-grid {
        animation: appear ${trial.iti_duration / 1000}s;
      }
      </style>`;

      // Draw container.
      new_html += '<div class="dsst-container">';

      // Draw stimulus grid.
      new_html += '<div class="dsst-stimulus-grid">';
      trial.stimuli.forEach((j, i) => {
        // Здесь мы используем полный путь к изображению из trial.stimuli
        new_html += '<div class="dsst-stimulus"><img src="' + j + '" onerror="console.error(\'Failed to load image:\', this.src)"></img></div>';
        new_html += '<div class="dsst-stimulus"><p>' + (i+1) + '</p></div>';
      });
      new_html += '</div>';

      // Draw target grid.
      new_html += '<div class="dsst-target-grid">';
      // И здесь также используем полный путь
      new_html += '<div class="dsst-stimulus"><img src="' + trial.stimuli[trial.target] + '" onerror="console.error(\'Failed to load image:\', this.src)"></img></div>';
      new_html += '<div class="dsst-stimulus"><p id="target"></p></div>';
      new_html += '</div>';

      // Close container.
      new_html += '</div>';

      // Draw stimuli to screen.
      display_element.innerHTML = new_html;

      // ---------------------------------- //
      // Section 2: Response handling       //
      // ---------------------------------- //

      // confirm screen resolution
      const screen_resolution = [window.innerWidth, window.innerHeight];
      if (screen_resolution[0] < 360 || screen_resolution[1] < 360) {
        var minimum_resolution = 0;
      } else {
        var minimum_resolution = 1;
      }

      // store response
      var response = {
        rt: null,
        key: null,
      };

      // Инициализируем счетчик неправильных нажатий для этого trial
      trial.incorrect_key_presses = 0;

      // function to handle responses by the subject
      var after_response = function(info) {
        // Kill all setTimeout handlers.
        jsPsych.pluginAPI.clearAllTimeouts();
        jsPsych.pluginAPI.cancelAllKeyboardResponses();

        // record response
        response.rt = info.rt;
        response.key = info.key;

        // check if response is correct
        var correct = response.key == trial.valid_responses;

        // present feedback
        display_element.querySelector('#target').innerHTML = response.key;

        // Pause for animation (2s).
        setTimeout(function() { end_trial(correct); }, trial.feedback_duration);
      };

      // function to end trial when it is time
      var end_trial = function(correct) {
        // kill any remaining setTimeout handlers
        jsPsych.pluginAPI.clearAllTimeouts();

        // kill keyboard listeners
        if (typeof keyboardListener !== 'undefined') {
          jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
        }

        // gather the data to store for the trial
        var trial_data = {
          stimuli: trial.stimuli,
          target: trial.target,
          key: response.key,
          rt: response.rt,
          correct: correct,
          incorrect_key_presses: trial.incorrect_key_presses,
          screen_resolution: screen_resolution,
          minimum_resolution: minimum_resolution
        };

        // move on to the next trial
        jsPsych.finishTrial(trial_data);
      };

      // start the response listener
      var keyboardListener = '';
      setTimeout(function() {
        keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
          callback_function: function(info) {
            if (info.key === trial.valid_responses) {
              after_response(info);
            } else {
              trial.incorrect_key_presses++; // Увеличиваем счетчик при неверном нажатии
              console.log('Incorrect key press. Total incorrect for this trial:', trial.incorrect_key_presses);
            }
          },
          valid_responses: "ALL_KEYS",
          rt_method: 'performance',
          persist: true,
          allow_held_key: false
        });
      }, trial.iti_duration);

      // end trial if trial_duration is set
      if (trial.trial_duration !== null) {
        jsPsych.pluginAPI.setTimeout(function() {
          end_trial();
        }, trial.trial_duration + trial.iti_duration);
      }

    }
  };
  DsstPlugin.info = info;

  return DsstPlugin;

})(jsPsychModule);
