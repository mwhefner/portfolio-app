window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** This is the p5.js sketch itself */

// An array to store the sound files
window.spectrawhorl_namespace.soundFiles = [];

// The function that builds the p5js sketch
window.spectrawhorl_namespace.build_sketch = function (p) {

    p.preload = function () {

        // Load sample sound files to finish sound initialization
        window.spectrawhorl_namespace.soundFiles[0] = p.loadSound("assets/mp3/COSTE.mp3");
        window.spectrawhorl_namespace.soundFiles[1] = p.loadSound("assets/mp3/SCHUBERT.mp3");
        window.spectrawhorl_namespace.soundFiles[2] = p.loadSound("assets/mp3/BACH.mp3");

    };

    p.setup = function () {

        p.createCanvas(window.innerWidth, window.innerHeight);

        p.setAttributes('antialias', true);

    };

    p.draw = function() {

        p.background(window.spectrawhorl_namespace.viewerBackground);

        if (p.getAudioContext().state === "running") {

            // Initialize each if not yet done
            if (window.spectrawhorl_namespace.unloaded) {

                window.spectrawhorl_namespace.initSound();
                window.spectrawhorl_namespace.initGenerator(p);
                window.spectrawhorl_namespace.initSpectrogram(p);
                window.spectrawhorl_namespace.initOverlay(p);

                window.spectrawhorl_namespace.unloaded = false;

            }

            // For each:
            // // UPDATE
            //updateSound(p);
            //updateGenerator(p);
            //updateSpectrogram(p);
            //updateOverlay(p);
            
            // // DRAW
            if (window.spectrawhorl_namespace.overlayOnTop) {
                window.spectrawhorl_namespace.drawSpectrogram(p);
                window.spectrawhorl_namespace.drawOverlay(p);
            } else {
                window.spectrawhorl_namespace.drawOverlay(p);
                window.spectrawhorl_namespace.drawSpectrogram(p);
            }

        } 

    };

    p.windowResized = function () {

        if (p._renderer) {

            p.resizeCanvas(window.innerWidth, window.innerHeight);

            // Re-initialize spectrogram and overlay parameters after resizing
            if (p.getAudioContext().state === "running" & !window.spectrawhorl_namespace.unloaded) {
                window.spectrawhorl_namespace.initSpectrogram(p);
                window.spectrawhorl_namespace.initOverlay(p);

                // Clear and redraw the canvas
                p.clear();
                window.spectrawhorl_namespace.drawSpectrogram(p);
                window.spectrawhorl_namespace.drawOverlay(p);
            } 

        }
    };

    // User gesture to start audio
    p.mousePressed = function () {
        if (p.getAudioContext().state !== "running") {
            p.getAudioContext().resume().then(() => {
                p.userStartAudio();
            });
        }
    };

}

