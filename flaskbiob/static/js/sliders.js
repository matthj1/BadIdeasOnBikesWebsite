import '../nouislider/distribute/nouislider.min.js'

// Distance Slider

let distance_slider = document.getElementById("distance-slider");
let distance_low = document.getElementById("distance-slider-min");
let distance_high = document.getElementById("distance-slider-max");
let distance_input_low = document.getElementById("length_min");
let distance_input_high = document.getElementById("length_max");

noUiSlider.create(distance_slider, {
    start: [0,250],
    range: {
        "min": [0],
        "max": [250]
    },
    step: 10,
    connect: [false, true, false],
});

distance_slider.noUiSlider.on('update', function(){
    let values = distance_slider.noUiSlider.get();
    distance_low.innerText = values[0];
    distance_high.innerText = values[1];
    distance_input_low.value = values[0];
    distance_input_high.value = values[1];
})

// Ascent Slider

let ascent_slider = document.getElementById("ascent-slider");
let ascent_low = document.getElementById("ascent-slider-min");
let ascent_high = document.getElementById("ascent-slider-max");
let ascent_input_low = document.getElementById("ascent_min");
let ascent_input_high = document.getElementById("ascent_max");

noUiSlider.create(ascent_slider, {
    start: [0,5000],
    range: {
        "min": [0],
        "max": [4000]
    },
    step: 50,
    connect: [false, true, false],
});

ascent_slider.noUiSlider.on('update', function(){
    let values = ascent_slider.noUiSlider.get();
    ascent_low.innerText = values[0];
    ascent_high.innerText = values[1];
    ascent_input_low.value = values[0];
    ascent_input_high.value = values[1];
})

// Scenery Slider

let scenery_slider = document.getElementById("scenery-slider");
let scenery_low = document.getElementById("scenery-slider-min");
let scenery_high = document.getElementById("scenery-slider-max");
let scenery_input_low = document.getElementById("scenery_min");
let scenery_input_high = document.getElementById("scenery_max");

noUiSlider.create(scenery_slider, {
    start: [0,10],
    range: {
        "min": [0],
        "max": [10]
    },
    step: 1,
    connect: [false, true, false],
});

scenery_slider.noUiSlider.on('update', function(){
    let values = scenery_slider.noUiSlider.get();
    scenery_low.innerText = values[0];
    scenery_high.innerText = values[1];
    scenery_input_low.value = values[0];
    scenery_input_high.value = values[1];
})

// Brutality Slider

let brutality_slider = document.getElementById("brutality-slider");
let brutality_low = document.getElementById("brutality-slider-min");
let brutality_high = document.getElementById("brutality-slider-max");
let brutality_input_low = document.getElementById("brutality_min");
let brutality_input_high = document.getElementById("brutality_max");

noUiSlider.create(brutality_slider, {
    start: [0,10],
    range: {
        "min": [0],
        "max": [10]
    },
    step: 1,
    connect: [false, true, false],
});

brutality_slider.noUiSlider.on('update', function(){
    let values = brutality_slider.noUiSlider.get();
    brutality_low.innerText = values[0];
    brutality_high.innerText = values[1];
    brutality_input_low.value = values[0];
    brutality_input_high.value = values[1];
})

// Quietness Slider

let quietness_slider = document.getElementById("quietness-slider");
let quietness_low = document.getElementById("quietness-slider-min");
let quietness_high = document.getElementById("quietness-slider-max");
let quietness_input_low = document.getElementById("quietness_min");
let quietness_input_high = document.getElementById("quietness_max");

noUiSlider.create(quietness_slider, {
    start: [0,10],
    range: {
        "min": [0],
        "max": [10]
    },
    step: 1,
    connect: [false, true, false],
});

quietness_slider.noUiSlider.on('update', function(){
    let values = quietness_slider.noUiSlider.get();
    quietness_low.innerText = values[0];
    quietness_high.innerText = values[1];
    quietness_input_low.value = values[0];
    quietness_input_high.value = values[1];
})
