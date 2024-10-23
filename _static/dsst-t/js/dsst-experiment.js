//---------------------------------------//
// Define parameters.
//---------------------------------------//

// Define response parameters.
const valid_responses = ['1', '2', '3'];

// Define block length.
const block_length = 30000;

//---------------------------------------//
// Define images for preloading.
//---------------------------------------//

// Initialize images for preloading.
var img_files = js_vars.img_files;

//---------------------------------------//
// Define instructions.
//---------------------------------------//

var instructions_01 = {
  type: jsPsychDsstInstructions,
  pages: [
    "<p>In this task, you will see a series of symbols.<br>Each symbol is paired with a number (top row).</p>",
    "<p>When you see a symbol pop up, your task is to enter its<br>number using the 1,2,3 keys on your keyboard.</p>",
    `<p>Now let's practice a couple of trials.<br>Press the "Next" button when you're ready to start.</p>`
  ],
  stimuli: img_files.slice(0,3),
  target: 0,
  allow_keys: true,
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next"
}

var practice = {
  timeline: [{
    type: jsPsychDsst,
    stimuli: img_files.slice(0,3),
    target: jsPsych.timelineVariable('target'),
    valid_responses: jsPsych.timelineVariable('valid_responses')
  }],
  timeline_variables: [
    {target: 0, valid_responses: valid_responses[0]},
    {target: 0, valid_responses: valid_responses[0]},
    {target: 0, valid_responses: valid_responses[0]},
    {target: 0, valid_responses: valid_responses[0]},
    {target: 1, valid_responses: valid_responses[1]},
    {target: 1, valid_responses: valid_responses[1]},
    {target: 1, valid_responses: valid_responses[1]},
    {target: 1, valid_responses: valid_responses[1]},
    {target: 2, valid_responses: valid_responses[2]},
    {target: 2, valid_responses: valid_responses[2]},
    {target: 2, valid_responses: valid_responses[2]},
    {target: 2, valid_responses: valid_responses[2]}
  ],
  randomize_order: true
}

var instructions_02 = {
  type: jsPsychInstructions,
  pages: [
    `<p>Great job! Now we will get stared with the actual task.</p><p>You will have 90 seconds to complete as many trials as possible.</p><p>Try to work as quickly as you can. You will get a break every 30 seconds.</p><p>Press the "Next" button when you're ready to start.</p>`
  ],
  allow_keys: true,
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(data) {
    // Define block 1 start time.
    // Note: if this is deleted, the entire task will break.
    block_1_start = data.time_elapsed;
  }
}

var INSTRUCTIONS = [
  instructions_01,
  practice,
  instructions_02
];

//---------------------------------------//
// Define DSST blocks.
//---------------------------------------//

// Predefine start times.
var block_1_start = null;
var block_2_start = null;
var block_3_start = null;

function createBlockTimeline(img_files, block_number) {
    console.log(`Creating timeline for Block ${block_number} with images:`, img_files);
    var trials = [];
    repeatShuffles([0,0,0,1,1,1,2,2,2], 25).forEach((k, index) => {
        const trial = {
            type: jsPsychDsst,
            stimuli: img_files,
            target: k,
            valid_responses: valid_responses[k],
            data: {block: block_number, trial_index: index},
            trial_duration: 3000, // Ограничим время каждого испытания до 3 секунд
            on_finish: function(data) {
                console.log(`Trial ${index} in Block ${block_number} finished:`, data);
            }
        }
        trials.push(trial);
    });
    console.log(`Created ${trials.length} trials for Block ${block_number}`);
    return trials;
}

// Сделайте функцию доступной глобально
window.createBlockTimeline = createBlockTimeline;

// Define Block 1.
var DSST_01 = createBlockTimeline(img_files.slice(3,6), 1);

// Define Block 2.
var DSST_02 = createBlockTimeline(img_files.slice(6,9), 2);

// Define Block 3.
var DSST_03 = createBlockTimeline(img_files.slice(9,12), 3);

//---------------------------------------//
// Define transition screens.
//---------------------------------------//

var PAUSE_01 = {
  type: jsPsychInstructions,
  pages: [
    '<p>Take a break for a few moments and press "Next" when you are ready to continue.</p>',
    "<p>Get ready to begin <b>Block 2/3</b></p><p>Press next when you're ready to start.</p>",
  ],
  allow_keys: true,
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(data) {
    // Define block 2 start time.
    // Note: if this is deleted, the entire task will break.
    block_2_start = data.time_elapsed;
  }
}

var PAUSE_02 = {
  type: jsPsychInstructions,
  pages: [
    '<p>Take a break for a few moments and press "Next" when you are ready to continue.</p>',
    "<p>Get ready to begin <b>Block 3/3</b></p><p>Press next when you're ready to start.</p>",
  ],
  allow_keys: true,
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(data) {
    // Define block 3 start time.
    // Note: if this is deleted, the entire task will break.
    block_3_start = data.time_elapsed;
  }
}

var FINISHED = {
  type: jsPsychInstructions,
  pages: [
    `<p>Great job! You've finished the task.</p><p>Press "Next" to end the experiment.</p>`
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
}

//---------------------------------------//
// Define utility functions.
//---------------------------------------//

// Convenience function to generate concatenated array of arrays,
// where base array is iteratively shuffled.
function repeatShuffles(arr, n) {
  // Preallocate space
  var arrays = []

  // Iteratively append shuffled array.
  for (let i = 0; i < n; i++) {
    arrays.push(jsPsych.randomization.shuffle(arr));
  }

  // Return flattened array.
  return [].concat.apply([], arrays)
}

// Define timeline
var timeline = [
  INSTRUCTIONS,
  DSST_01,
  PAUSE_01,
  DSST_02,
  PAUSE_02,
  DSST_03,
  FINISHED
];

console.log('Timeline defined:', timeline);
window.timeline = timeline;
