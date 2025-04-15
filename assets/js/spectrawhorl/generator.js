window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** spectrawhorl generator variables w/ defaults */

// the parallel web worker for sequence playing
//window.spectrawhorl_namespace.sequencePlayerWorker;
window.spectrawhorl_namespace.oscillatorType = "sine"; //  'sine' (default), 'triangle', 'sawtooth', 'square'
window.spectrawhorl_namespace.generatorSource = "free"; // 'free', 'sequence', or 'midi',
window.spectrawhorl_namespace.midiAccess = null;
// Used for 'free'
window.spectrawhorl_namespace.freeOscillator;
window.spectrawhorl_namespace.freeOscillatorAmplitude = 0;
window.spectrawhorl_namespace.freeOscillatorFundamental = 440;
// Used for all but 'free'
window.spectrawhorl_namespace.polyphonicOscillators = [];
window.spectrawhorl_namespace.polyphonicEnvelopes = [];
window.spectrawhorl_namespace.snapToState = "NONE"; // "NONE", "CHROMATIC", "KEY", or "TRIAD"
// Helper function for snapping to the nearest key or triad
// defined in the overlay script
window.spectrawhorl_namespace.findNearestInteger = function(arr, num) {
    //console.log(arr, num);
    return arr.reduce((prev, curr) => {
        return Math.abs(curr - num) < Math.abs(prev - num) ? curr : prev;
    });
}
// Snap to global function
window.spectrawhorl_namespace.snapFreqTo = function (freq) {
    if (window.spectrawhorl_namespace.snapToState === "NONE") {
        return freq;
    } else if (window.spectrawhorl_namespace.snapToState === "CHROMATIC") {
        return window.spectrawhorl_namespace.noteToFreq(Math.round(window.spectrawhorl_namespace.freqToNote(freq)));
    } else if (window.spectrawhorl_namespace.snapToState === "KEY") {
        return window.spectrawhorl_namespace.noteToFreq(window.spectrawhorl_namespace.findNearestInteger(window.spectrawhorl_namespace.overlayKeyNotes, window.spectrawhorl_namespace.freqToNote(freq)));
    } else {
        return window.spectrawhorl_namespace.noteToFreq(window.spectrawhorl_namespace.findNearestInteger(window.spectrawhorl_namespace.overlayTriadNotes, window.spectrawhorl_namespace.freqToNote(freq)));
    }
};
// envelope settings
window.spectrawhorl_namespace.attack = 0.5;
window.spectrawhorl_namespace.decay = 0.1;
window.spectrawhorl_namespace.sustain = 0.15;
window.spectrawhorl_namespace.sustainTime = 0.5;
window.spectrawhorl_namespace.release = 0;
// Used for 'sequence*'
window.spectrawhorl_namespace.bpm = 120;
window.spectrawhorl_namespace.npb = 1;
window.spectrawhorl_namespace.nps = (window.spectrawhorl_namespace.bpm / 60) * window.spectrawhorl_namespace.npb; // calculated from BPM
window.spectrawhorl_namespace.sequencePlaying = false; // whether or not the frequency is playing
window.spectrawhorl_namespace.currentNoteTime = 0;
window.spectrawhorl_namespace.currentNote = 60; // default first sequence note to middle C
window.spectrawhorl_namespace.baseFrequencyNote = 60; // base frequency of the sequence
window.spectrawhorl_namespace.sequenceAlong = "CHROMATIC";
window.spectrawhorl_namespace.sequenceDirection = "DOWN";
window.spectrawhorl_namespace.sequenceLength = 12;

/** Functions for playing the sequence. */

window.spectrawhorl_namespace.getNextNoteTime = function(currentTime) {
    let newTime = (Math.floor(currentTime * window.spectrawhorl_namespace.nps) + 1) / window.spectrawhorl_namespace.nps;
    if (currentTime >= newTime) {
        // adjust if you fall behind
        newTime = (Math.floor(currentTime * window.spectrawhorl_namespace.nps) + 2) / window.spectrawhorl_namespace.nps;
    }
    return newTime;
}

window.spectrawhorl_namespace.playSequence = function() {
    window.spectrawhorl_namespace.sequencePlaying = true;
    window.spectrawhorl_namespace.startPolyphonicOscillators();
}

window.spectrawhorl_namespace.stopSequence = function() {
    window.spectrawhorl_namespace.sequencePlaying = false;

    //
    window.spectrawhorl_namespace.cancelScheduledNotes();

    window.spectrawhorl_namespace.resetNote();

    //("Scheduled Notes after cancellation: ", scheduledNotes);
    window.spectrawhorl_namespace.polyphonicOscillators.forEach((oscillator, index) => {
        window.spectrawhorl_namespace.polyphonicEnvelopes[index].triggerRelease(oscillator);
    });
}

window.spectrawhorl_namespace.startFreeOscillator = function () {
    // Start Free Oscillator
    window.spectrawhorl_namespace.freeOscillator.disconnect();
    window.spectrawhorl_namespace.freeOscillator.connect(window.spectrawhorl_namespace.bassFilter);
    //bassFilter.chain(midFilter, highFilter);
    window.spectrawhorl_namespace.bassFilter.chain(window.spectrawhorl_namespace.midFilter, window.spectrawhorl_namespace.highFilter);

    window.spectrawhorl_namespace.freeOscillator.amp(window.spectrawhorl_namespace.freeOscillatorAmplitude);
    window.spectrawhorl_namespace.freeOscillator.freq(window.spectrawhorl_namespace.freeOscillatorFundamental);
    window.spectrawhorl_namespace.freeOscillator.start();
    //console.log("Free Oscillator started.");
};

window.spectrawhorl_namespace.startPolyphonicOscillators = function () {
    window.spectrawhorl_namespace.polyphonicOscillators.forEach((oscillator, index) => {
        oscillator.disconnect(); // Disconnect the oscillator from any previous connections
        oscillator.connect(window.spectrawhorl_namespace.bassFilter); // Connect to the bass filter
    });
    window.spectrawhorl_namespace.bassFilter.chain(window.spectrawhorl_namespace.midFilter, window.spectrawhorl_namespace.highFilter); // Chain the filters together

    window.spectrawhorl_namespace.polyphonicOscillators.forEach((oscillator) => oscillator.amp(0));
    window.spectrawhorl_namespace.polyphonicOscillators.forEach((oscillator) => oscillator.start());
    //console.log("Polyphonic Oscillators started.");
};

window.spectrawhorl_namespace.midiInitiated = false;

window.spectrawhorl_namespace.startGenerator = function () {
    //console.log("Generator started.");
    if (window.spectrawhorl_namespace.generatorSource === "free") {
        // Initialize Free oscillator
        window.spectrawhorl_namespace.startFreeOscillator();
    } else if (window.spectrawhorl_namespace.generatorSource === "sequence") {
        // Initialize Sequencer
        window.spectrawhorl_namespace.startPolyphonicOscillators();
    } else if (window.spectrawhorl_namespace.generatorSource === "midi") {
        // Initialize midi controls for midi

            // Request MIDI access
        if (!window.spectrawhorl_namespace.midiInitiated) {
            if (navigator.requestMIDIAccess) {
                navigator.requestMIDIAccess().then(onMIDISuccess, onMIDIFailure);
                window.spectrawhorl_namespace.midiInitiated = true;
            } else {
                console.error("WebMIDI is not supported in this browser.");
            }
        }

        // reset the double-clicks
        window.spectrawhorl_namespace.resetDoubleClicks();

        window.spectrawhorl_namespace.startPolyphonicOscillators();
    }
};

window.spectrawhorl_namespace.stopGenerator = function () {
    window.spectrawhorl_namespace.freeOscillator.stop();
    window.spectrawhorl_namespace.polyphonicOscillators.forEach((oscillator) => oscillator.amp(0));
    window.spectrawhorl_namespace.polyphonicOscillators.forEach((oscillator) => oscillator.stop());
    //
    window.spectrawhorl_namespace.cancelScheduledNotes();
    window.spectrawhorl_namespace.resetNote();
};

window.spectrawhorl_namespace.initOscillators = function () {
    // Initialize free oscillator
    window.spectrawhorl_namespace.freeOscillator = new p5.Oscillator(window.spectrawhorl_namespace.oscillatorType);

    window.spectrawhorl_namespace.polyphonicOscillators = [];
    window.spectrawhorl_namespace.polyphonicEnvelopes = [];
    
    // Initialize polyphonic oscillators
    for (let i = 24; i <= 127; i++) {
        window.spectrawhorl_namespace.polyphonicOscillators.push(
            new p5.Oscillator(window.spectrawhorl_namespace.noteToFreq(i), window.spectrawhorl_namespace.oscillatorType)
        );
        let envelope = new p5.Envelope();
        envelope.setADSR(window.spectrawhorl_namespace.attack, window.spectrawhorl_namespace.sustain, window.spectrawhorl_namespace.decay, window.spectrawhorl_namespace.release);
        envelope.setRange(0.2, 0);
        window.spectrawhorl_namespace.polyphonicEnvelopes.push(envelope);
    }
};

window.spectrawhorl_namespace.getNextNote = function() {
    if (window.spectrawhorl_namespace.sequenceAlong === "CHROMATIC") {
        if (
            window.spectrawhorl_namespace.sequenceDirection === "UP" &&
            window.spectrawhorl_namespace.currentNote + 1 < window.spectrawhorl_namespace.baseFrequencyNote + window.spectrawhorl_namespace.sequenceLength &&
            window.spectrawhorl_namespace.currentNote < 115
        ) {
            window.spectrawhorl_namespace.currentNote++;
        } else if (
            window.spectrawhorl_namespace.sequenceDirection === "DOWN" &&
            window.spectrawhorl_namespace.currentNote - 1 > window.spectrawhorl_namespace.baseFrequencyNote - window.spectrawhorl_namespace.sequenceLength &&
            window.spectrawhorl_namespace.currentNote > 24
        ) {
            window.spectrawhorl_namespace.currentNote--;
        } else {
            window.spectrawhorl_namespace.currentNote = window.spectrawhorl_namespace.baseFrequencyNote;
        }
    } else if (window.spectrawhorl_namespace.sequenceAlong === "KEY") {
        let nearestNote = window.spectrawhorl_namespace.findNearestInteger(
            window.spectrawhorl_namespace.overlayKeyNotes,
            window.spectrawhorl_namespace.baseFrequencyNote
        );
        let baseIndex = window.spectrawhorl_namespace.overlayKeyNotes.indexOf(nearestNote);
        let currentIndex = window.spectrawhorl_namespace.overlayKeyNotes.indexOf(currentNote);

        if (currentIndex === -1) {
            currentIndex = baseIndex;
        }

        if (window.spectrawhorl_namespace.sequenceDirection === "UP") {
            if (
                currentIndex < window.spectrawhorl_namespace.overlayKeyNotes.length - 1 &&
                currentIndex >= baseIndex
            ) {
                currentIndex++;
            } else {
                currentIndex = baseIndex;
            }
        } else if (window.spectrawhorl_namespace.sequenceDirection === "DOWN") {
            if (currentIndex > 0 && currentIndex <= baseIndex) {
                currentIndex--;
            } else {
                currentIndex = baseIndex;
            }
        }

        if (Math.abs(currentIndex - baseIndex) >= window.spectrawhorl_namespace.sequenceLength) {
            currentIndex = baseIndex;
        }

        window.spectrawhorl_namespace.currentNote = window.spectrawhorl_namespace.overlayKeyNotes[currentIndex];

    } else if (sequenceAlong === "TRIAD") {
        let nearestNote = window.spectrawhorl_namespace.findNearestInteger(
            window.spectrawhorl_namespace.overlayTriadNotes,
            window.spectrawhorl_namespace.baseFrequencyNote
        );
        let baseIndex = window.spectrawhorl_namespace.overlayTriadNotes.indexOf(nearestNote);
        let currentIndex = window.spectrawhorl_namespace.overlayTriadNotes.indexOf(currentNote);

        if (currentIndex === -1) {
            currentIndex = baseIndex;
        }

        if (window.spectrawhorl_namespace.sequenceDirection === "UP") {
            if (
                currentIndex < window.spectrawhorl_namespace.overlayTriadNotes.length - 1 &&
                currentIndex >= baseIndex
            ) {
                currentIndex++;
            } else {
                currentIndex = baseIndex;
            }
        } else if (window.spectrawhorl_namespace.sequenceDirection === "DOWN") {
            if (currentIndex > 0 && currentIndex <= baseIndex) {
                currentIndex--;
            } else {
                currentIndex = baseIndex;
            }
        }

        if (Math.abs(currentIndex - baseIndex) >= window.spectrawhorl_namespace.sequenceLength) {
            currentIndex = baseIndex;
        }

        currentNote = window.spectrawhorl_namespace.overlayTriadNotes[currentIndex];
    }
}

window.spectrawhorl_namespace.scheduledNotes = [];
window.spectrawhorl_namespace.cancelScheduledNotes = function() {
    window.spectrawhorl_namespace.scheduledNotes.forEach((note) => {
        window.spectrawhorl_namespace.polyphonicEnvelopes[note - 24].setRange(0, 0);
    });

    window.spectrawhorl_namespace.scheduledNotes = [];

    // Reset currentNoteTime 
    window.spectrawhorl_namespace.currentNoteTime = 0;

    //console.log("Scheduled notes canceled.");
}

window.spectrawhorl_namespace.resetNote = function() {
    if (window.spectrawhorl_namespace.sequenceAlong === "KEY") {
        window.spectrawhorl_namespace.currentNote = window.spectrawhorl_namespace.findNearestInteger(window.spectrawhorl_namespace.overlayKeyNotes, window.spectrawhorl_namespace.baseFrequencyNote);
    } else if (window.spectrawhorl_namespace.sequenceAlong === "TRIAD") {
        window.spectrawhorl_namespace.currentNote = window.spectrawhorl_namespace.findNearestInteger(window.spectrawhorl_namespace.overlayTriadNotes, window.spectrawhorl_namespace.baseFrequencyNote);
    } else {
        window.spectrawhorl_namespace.currentNote = window.spectrawhorl_namespace.baseFrequencyNote;
    }

    //console.log("Note reset.");
}

window.spectrawhorl_namespace.initGenerator = function (p) {
    window.spectrawhorl_namespace.initOscillators();
};

