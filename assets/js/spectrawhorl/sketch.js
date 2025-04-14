window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

// An array to store the sound files
window.spectrawhorl_namespace.soundFiles = [];

// The function that builds the p5js sketch
window.spectrawhorl_namespace.build_sketch = function (p) {

    p.preload = function () {

        // Load sample sound files
        window.spectrawhorl_namespace.soundFiles[0] = p.loadSound("assets/mp3/COSTE.mp3");
        window.spectrawhorl_namespace.soundFiles[1] = p.loadSound("assets/mp3/SCHUBERT.mp3");
        window.spectrawhorl_namespace.soundFiles[2] = p.loadSound("assets/mp3/BACH.mp3");

    };

    p.setup = function () {

        p.createCanvas(window.innerWidth, window.innerHeight, p.WEBGL);

        p.setAttributes('antialias', true);

    };

    p.draw = function() {

        p.clear(0, 0, 0, 0);


    };

}

