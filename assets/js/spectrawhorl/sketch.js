window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** This is the p5.js sketch itself */

// An array to store the sound files
window.spectrawhorl_namespace.soundFiles = [];
window.spectrawhorl_namespace.sketch = null;

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

        window.spectrawhorl_namespace.canvasSize = p.height;

        if (p.width < p.height) {
            window.spectrawhorl_namespace.canvasSize = p.width;
        }

        overlayWidth = (window.spectrawhorl_namespace.overlayWidthPercent / 100) * window.spectrawhorl_namespace.canvasSize;

        p.setAttributes('antialias', true);

    };

    p.draw = function() {

        p.background(window.spectrawhorl_namespace.viewerBackground);

        if (p.getAudioContext().state === "running") {

            // Initialize each if not yet done
            if (window.spectrawhorl_namespace.unloaded) {

                window.spectrawhorl_namespace.initSound(p);
                window.spectrawhorl_namespace.initGenerator(p);
                window.spectrawhorl_namespace.initSpectrogram(p);
                window.spectrawhorl_namespace.initOverlay(p);

                window.spectrawhorl_namespace.unloaded = false;

            }

            if (window.spectrawhorl_namespace.inputSource === "GENERATOR" && window.spectrawhorl_namespace.generatorSource !== "free") {

                // TODO: Improve the drum machine.
                // This has a known issue of not working when the tab is not focused.

                // With all of the latest information gathered,
                // schedule the next notes if the sequence is playing
                if (window.spectrawhorl_namespace.sequencePlaying & (p.getAudioContext().currentTime > window.spectrawhorl_namespace.currentNoteTime)) {
                    
                    // schedule one note, unless there's more than one note per beat,
                    window.spectrawhorl_namespace.currentNoteTime = window.spectrawhorl_namespace.getNextNoteTime(p.getAudioContext().currentTime);
            
                    //console.log("Next note-on-beat time:", currentNoteTime);
            
                    window.spectrawhorl_namespace.polyphonicEnvelopes[window.spectrawhorl_namespace.currentNote - 24].setADSR(
                        window.spectrawhorl_namespace.attack,
                        
                        window.spectrawhorl_namespace.decay,
            
                        window.spectrawhorl_namespace.sustain,
            
                        window.spectrawhorl_namespace.release
                    );
            
                    window.spectrawhorl_namespace.polyphonicEnvelopes[window.spectrawhorl_namespace.currentNote - 24].play(
                        window.spectrawhorl_namespace.polyphonicOscillators[window.spectrawhorl_namespace.currentNote - 24],
                        window.spectrawhorl_namespace.currentNoteTime - p.getAudioContext().currentTime,
                        window.spectrawhorl_namespace.sustainTime
                    );
            
                    // Start the envelope
                    window.spectrawhorl_namespace.getNextNote();
            
                    window.spectrawhorl_namespace.scheduledNotes = [];
            
                    for (let i = 1; i < window.spectrawhorl_namespace.npb; i++) {
                        window.spectrawhorl_namespace.currentNoteTime = window.spectrawhorl_namespace.getNextNoteTime(window.spectrawhorl_namespace.currentNoteTime);
            
                        window.spectrawhorl_namespace.polyphonicEnvelopes[window.spectrawhorl_namespace.currentNote - 24].setRange(0.2, 0);
            
                        // in which case, schedule as many notes as there are per beat
                        window.spectrawhorl_namespace.polyphonicEnvelopes[window.spectrawhorl_namespace.currentNote - 24].setADSR(
                            window.spectrawhorl_namespace.attack,
                            
                            window.spectrawhorl_namespace.decay,
            
                            window.spectrawhorl_namespace.sustain,
                            
                            window.spectrawhorl_namespace.release
                        );
            
                        window.spectrawhorl_namespace.polyphonicEnvelopes[window.spectrawhorl_namespace.currentNote - 24].play(
                            window.spectrawhorl_namespace.polyphonicOscillators[window.spectrawhorl_namespace.currentNote - 24],
                            window.spectrawhorl_namespace.currentNoteTime - p.getAudioContext().currentTime,
                            window.spectrawhorl_namespace.sustainTime
                        );
            
                        window.spectrawhorl_namespace.scheduledNotes.push(window.spectrawhorl_namespace.currentNote);
            
                        // Start the envelope
                        window.spectrawhorl_namespace.getNextNote();

                    }
            
                }
            
            }

            if (window.spectrawhorl_namespace.REINIT_SPECTROGRAM) {
                window.spectrawhorl_namespace.initSpectrogram(p);
                window.spectrawhorl_namespace.REINIT_SPECTROGRAM = false;
            }
            
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

            window.spectrawhorl_namespace.canvasSize = p.height;

            if (p.width < p.height) {
                window.spectrawhorl_namespace.canvasSize = p.width;
            }

            overlayWidth = (window.spectrawhorl_namespace.overlayWidthPercent / 100) * window.spectrawhorl_namespace.canvasSize;

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

    // User gesture to start audio
    p.keyPressed = function () {
        if (p.getAudioContext().state !== "running") {
            p.getAudioContext().resume().then(() => {
                p.userStartAudio();
            });
        }

        const keyNum = parseInt(p.key, 10);
        if (keyNum >= 1 && keyNum <= 7) {
            const fromKeyInputs = [0, 0, 0, 0, 0, 0, 0];
            fromKeyInputs[keyNum - 1] = true;
        
            window.spectrawhorl_namespace.triadButtonSelection(
                0, 0, 0, 0, 0, 0, 0,
                window.spectrawhorl_namespace.uiLightTheme,
                ...fromKeyInputs
            );
        }

        // TODO: Add spacebar freezeframe
    };

}

