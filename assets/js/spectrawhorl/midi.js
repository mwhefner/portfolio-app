window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** spectrawhorl midi variables w/ defaults */

window.spectrawhorl_namespace.midi_keyModeValue = 1;
window.spectrawhorl_namespace.midi_keyNoteValue = 0;

window.spectrawhorl_namespace.cc_double_click_20 = true;
window.spectrawhorl_namespace.cc_double_click_21 = true;
window.spectrawhorl_namespace.cc_double_click_22 = true;
window.spectrawhorl_namespace.cc_double_click_23 = true;
window.spectrawhorl_namespace.cc_double_click_16 = true;
window.spectrawhorl_namespace.cc_double_click_17 = true;
window.spectrawhorl_namespace.cc_double_click_18 = true;
window.spectrawhorl_namespace.cc_double_click_19 = true;
window.spectrawhorl_namespace.cc_double_click_24 = true;
window.spectrawhorl_namespace.cc_double_click_28 = true;

window.spectrawhorl_namespace.resetDoubleClicks = function () {
    window.spectrawhorl_namespace.cc_double_click_20 = true;
    window.spectrawhorl_namespace.cc_double_click_21 = true;
    window.spectrawhorl_namespace.cc_double_click_22 = true;
    window.spectrawhorl_namespace.cc_double_click_23 = true;
    window.spectrawhorl_namespace.cc_double_click_16 = true;
    window.spectrawhorl_namespace.cc_double_click_17 = true;
    window.spectrawhorl_namespace.cc_double_click_18 = true;
    window.spectrawhorl_namespace.cc_double_click_19 = true;
    window.spectrawhorl_namespace.cc_double_click_24 = true;
    window.spectrawhorl_namespace.cc_double_click_28 = true;
};

window.spectrawhorl_namespace.onMIDISuccess = function (midi) {
    //console.log("MIDI ready!");
    midiAccess = midi;

    // Listen to all MIDI inputs
    for (let input of midiAccess.inputs.values()) {
        input.onmidimessage = window.spectrawhorl_namespace.handleMIDIMessage;
        //console.log(`Connected to MIDI device: ${input.name}`);
        document.getElementById('spectrawhorl-midiControlIndicator').innerText = `Connected to MIDI device: ${input.name}`;
    }
};

window.spectrawhorl_namespace.onMIDIFailure = function () {
    console.error("Could not access your MIDI devices.");
    document.getElementById('spectrawhorl-midiControlIndicator').innerText = `Could not access your MIDI device.`;
};

window.spectrawhorl_namespace.updateKeyWithMIDI = function(keyNoteValue, keyModeValue) {
    window.spectrawhorl_namespace.cancelScheduledNotes();

    window.spectrawhorl_namespace.SCALE = window.spectrawhorl_namespace.getRelativeMajorScale(window.spectrawhorl_namespace.keyNoteValue, Math.abs(keyModeValue));

    //console.log("RELATIVE MAJOR SCALE:", SCALE);

    window.spectrawhorl_namespace.overlayKeyNotes = window.spectrawhorl_namespace.expandScale(window.spectrawhorl_namespace.SCALE);

    window.spectrawhorl_namespace.overlayTriadNotes = window.spectrawhorl_namespace.expandScale(window.spectrawhorl_namespace.getTriadFromScale(window.spectrawhorl_namespace.SCALE, window.spectrawhorl_namespace.triadScaleDegree));

    window.spectrawhorl_namespace.SCALE = window.spectrawhorl_namespace.SCALE.slice(Math.abs(keyModeValue) - 1).concat(
        window.spectrawhorl_namespace.SCALE.slice(0, Math.abs(keyModeValue) - 1)
    );

    window.spectrawhorl_namespace.overlayTriadNotes = window.spectrawhorl_namespace.expandScale(window.spectrawhorl_namespace.getTriadFromScale(window.spectrawhorl_namespace.SCALE, window.spectrawhorl_namespace.triadScaleDegree));

    //
    window.spectrawhorl_namespace.resetNote();
}

// Handle control change messages
window.spectrawhorl_namespace.handleControlChange = function(controller, value) {
    //console.log(`Control change: controller ${controller}, value ${value}`);

    // Example: Map controller 1 to oscillator frequency and controller 2 to amplitude
    switch (controller) {

        case 1:
            const new_baseFrequencyNote = Math.round(24 + (84 * value) / 127);

            if (new_baseFrequencyNote != window.spectrawhorl_namespace.baseFrequencyNote) {
                window.spectrawhorl_namespace.baseFrequencyNote = new_baseFrequencyNote;
            }

            break;

        case 2:
            const new_midi_sequenceLength = Math.round(1 + (59 * value) / 127);

            if (new_midi_sequenceLength != window.spectrawhorl_namespace.sequenceLength) {
                window.spectrawhorl_namespace.sequenceLength = new_midi_sequenceLength;
            }

            break;

        case 3:
            const new_midi_keyModeValue = Math.round(1 + (6 * value) / 127);

            if (window.spectrawhorl_namespace.midi_keyModeValue != new_midi_keyModeValue) {
                window.spectrawhorl_namespace.midi_keyModeValue = new_midi_keyModeValue;

                window.spectrawhorl_namespace.updateKeyWithMIDI(window.spectrawhorl_namespace.midi_keyNoteValue, window.spectrawhorl_namespace.midi_keyModeValue);
            }

            break;

        case 4:
            const new_midi_keyNoteValue = Math.floor((11 * value) / 127);

            if (window.spectrawhorl_namespace.midi_keyNoteValue != new_midi_keyNoteValue) {
                window.spectrawhorl_namespace.midi_keyNoteValue = new_midi_keyNoteValue;

                window.spectrawhorl_namespace.updateKeyWithMIDI(window.spectrawhorl_namespace.midi_keyNoteValue, window.spectrawhorl_namespace.midi_keyModeValue);
            }

            break;

        case 5:
            const new_BPM = Math.round(20 + (200 * value) / 128);

            if (new_BPM != window.spectrawhorl_namespace.bpm) {
                //console.log("BPM CHANGED TO:");
                window.spectrawhorl_namespace.bpm = new_BPM;
                window.spectrawhorl_namespace.nps = (window.spectrawhorl_namespace.bpm / 60) * window.spectrawhorl_namespace.npb;
                //console.log(bpm);
            }

            break;

        case 6:
            const new_NPB = value / 8;

            if (new_NPB != window.spectrawhorl_namespace.npb) {
                //console.log("NPB CHANGED TO:");
                window.spectrawhorl_namespace.npb = new_NPB;
                window.spectrawhorl_namespace.nps = (window.spectrawhorl_namespace.bpm / 60) * window.spectrawhorl_namespace.npb;
                //console.log(npb);
            }

            break;

        case 16:
            if (window.spectrawhorl_namespace.cc_double_click_16) {
                window.spectrawhorl_namespace.cc_double_click_16 = false;

                window.spectrawhorl_namespace.triadButtonSelection(
                    0, 0, 0, 0, 0, 0, 0,
                    window.spectrawhorl_namespace.uiLightTheme,
                    true, false, false, false, false, false, false
                );

            } else {
                window.spectrawhorl_namespace.cc_double_click_16 = true;
            }
            break;
        case 17:
            if (window.spectrawhorl_namespace.cc_double_click_17) {
                window.spectrawhorl_namespace.cc_double_click_17 = false;

                window.spectrawhorl_namespace.triadButtonSelection(
                    0, 0, 0, 0, 0, 0, 0,
                    window.spectrawhorl_namespace.uiLightTheme,
                    false, true, false, false, false, false, false
                );

            } else {
                window.spectrawhorl_namespace.cc_double_click_17 = true;
            }
            break;
        case 18:
            if (window.spectrawhorl_namespace.cc_double_click_18) {
                window.spectrawhorl_namespace.cc_double_click_18 = false;
                
                window.spectrawhorl_namespace.triadButtonSelection(
                    0, 0, 0, 0, 0, 0, 0,
                    window.spectrawhorl_namespace.uiLightTheme,
                    false, false, true, false, false, false, false
                );

            } else {
                window.spectrawhorl_namespace.cc_double_click_18 = true;
            }
            break;
        case 19:
            if (window.spectrawhorl_namespace.cc_double_click_19) {
                window.spectrawhorl_namespace.cc_double_click_19 = false;
                
                window.spectrawhorl_namespace.triadButtonSelection(
                    0, 0, 0, 0, 0, 0, 0,
                    window.spectrawhorl_namespace.uiLightTheme,
                    false, false, false, true, false, false, false
                );

            } else {
                window.spectrawhorl_namespace.cc_double_click_19 = true;
            }
            break;
        case 21:
            if (window.spectrawhorl_namespace.cc_double_click_21) {
                window.spectrawhorl_namespace.cc_double_click_21 = false;
                
                window.spectrawhorl_namespace.triadButtonSelection(
                    0, 0, 0, 0, 0, 0, 0,
                    window.spectrawhorl_namespace.uiLightTheme,
                    false, false, false, false, true, false, false
                );

            } else {
                window.spectrawhorl_namespace.cc_double_click_21 = true;
            }
            break;
        case 22:
            if (window.spectrawhorl_namespace.cc_double_click_22) {
                window.spectrawhorl_namespace.cc_double_click_22 = false;
                
                window.spectrawhorl_namespace.triadButtonSelection(
                    0, 0, 0, 0, 0, 0, 0,
                    window.spectrawhorl_namespace.uiLightTheme,
                    false, false, false, false, false, true, false
                );

            } else {
                window.spectrawhorl_namespace.cc_double_click_22 = true;
            }
            break;
        case 23:
            if (window.spectrawhorl_namespace.cc_double_click_23) {
                window.spectrawhorl_namespace.cc_double_click_23 = false;
                
                window.spectrawhorl_namespace.triadButtonSelection(
                    0, 0, 0, 0, 0, 0, 0,
                    window.spectrawhorl_namespace.uiLightTheme,
                    false, false, false, false, false, false, true
                );

            } else {
                window.spectrawhorl_namespace.cc_double_click_23 = true;
            }
            break;

        case 20:
            if (window.spectrawhorl_namespace.cc_double_click_20) {
                // play/pause
                if (!window.spectrawhorl_namespace.sequencePlaying) {
                    //console.log("SEQUENCE STARTED");
                    window.spectrawhorl_namespace.playSequence();
                } else {
                    //console.log("SEQUENCE STOPPED");
                    window.spectrawhorl_namespace.stopSequence();
                }
                // timeout for double click
                window.spectrawhorl_namespace.cc_double_click_20 = false;
            } else {
                window.spectrawhorl_namespace.cc_double_click_20 = true;
            }

            break;

        case 24:
            if (window.spectrawhorl_namespace.cc_double_click_24) {
                if (window.spectrawhorl_namespace.sequenceAlong === "CHROMATIC") {
                    window.spectrawhorl_namespace.sequenceAlong = "KEY";
                } else if (window.spectrawhorl_namespace.sequenceAlong === "KEY") {
                    window.spectrawhorl_namespace.sequenceAlong = "TRIAD";
                } else if (window.spectrawhorl_namespace.sequenceAlong === "TRIAD") {
                    window.spectrawhorl_namespace.sequenceAlong = "CHROMATIC";
                }
                // timeout for double click
                window.spectrawhorl_namespace.cc_double_click_24 = false;
            } else {
                window.spectrawhorl_namespace.cc_double_click_24 = true;
            }

            break;

        case 28:
            if (window.spectrawhorl_namespace.cc_double_click_28) {
                if (window.spectrawhorl_namespace.sequenceDirection === "DOWN") {
                    window.spectrawhorl_namespace.sequenceDirection = "UP";
                } else if (window.spectrawhorl_namespace.sequenceDirection === "UP") {
                    window.spectrawhorl_namespace.sequenceDirection = "DOWN";
                }
                // timeout for double click
                window.spectrawhorl_namespace.cc_double_click_28 = false;
            } else {
                window.spectrawhorl_namespace.cc_double_click_28 = true;
            }

            break;

        case 70:
            const new_attack = value / 127.0;

            if (window.spectrawhorl_namespace.attack != new_attack) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.attack = new_attack;
            }

            break;

        case 71:
            const new_decay = value / 127.0;

            if (window.spectrawhorl_namespace.decay != new_decay) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.decay = new_decay;
            }

            break;

        case 72:
            const new_sustainTime = value / 127.0;

            if (window.spectrawhorl_namespace.sustainTime != new_sustainTime) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.sustainTime = new_sustainTime;
            }

            break;

        case 73:
            const new_release = value / 127.0;

            if (window.spectrawhorl_namespace.release != new_release) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.release = new_release;
            }

            break;

        case 74:
            const new_sustain = value / 127.0;

            if (window.spectrawhorl_namespace.sustain != new_sustain) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.sustain = new_sustain;
            }

            break;

        case 75:
            const new_bassGain = 47 * (2 * (value / 127.0) - 1);

            if (window.spectrawhorl_namespace.bassGain != new_bassGain) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.bassGain = new_bassGain;
                window.spectrawhorl_namespace.bassFilter.gain(window.spectrawhorl_namespace.bassGain);
            }

            break;

        case 76:
            const new_middleGain = 47 * (2 * (value / 127.0) - 1);

            if (window.spectrawhorl_namespace.middleGain != new_middleGain) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.middleGain = new_middleGain;
                window.spectrawhorl_namespace.midFilter.gain(window.spectrawhorl_namespace.middleGain);
            }

            break;

        case 77:
            const new_trebleGain = 47 * (2 * (value / 127.0) - 1);

            if (window.spectrawhorl_namespace.trebleGain != new_trebleGain) {
                window.spectrawhorl_namespace.cancelScheduledNotes();
                window.spectrawhorl_namespace.resetNote();

                window.spectrawhorl_namespace.trebleGain = new_trebleGain;
                window.spectrawhorl_namespace.highFilter.gain(window.spectrawhorl_namespace.trebleGain);
            }

            break;
    }
}

window.spectrawhorl_namespace.handleMIDIMessage = function (event) {
    // MIDI data is an array of numbers
    let data = event.data;
    let command = data[0];
    let note = data[1];
    let velocity = data[2];

    //console.log(`MIDI message received: [${data.join(", ")}]`);

    switch (command & 0xf0) {
        case 144: // note on
            if (velocity > 0) {
                //console.log(note, velocity);

                // Set ADSR for the envelope
                window.spectrawhorl_namespace.polyphonicEnvelopes[note - 24].setADSR(
                    window.spectrawhorl_namespace.attack,
                    window.spectrawhorl_namespace.decay,
                    window.spectrawhorl_namespace.sustain,
                    window.spectrawhorl_namespace.release
                );

                window.spectrawhorl_namespace.polyphonicEnvelopes[note - 24].setRange(velocity / 127, 0);

                // Trigger the attack phase
                window.spectrawhorl_namespace.polyphonicEnvelopes[note - 24].triggerAttack(
                    window.spectrawhorl_namespace.polyphonicOscillators[note - 24],
                    0
                );
            } else {
                //console.log(note, " OFF");
                window.spectrawhorl_namespace.polyphonicEnvelopes[note - 24].triggerRelease();
            }
            break;
        case 128: // note off
            //console.log(note, " OFF");
            window.spectrawhorl_namespace.polyphonicEnvelopes[note - 24].triggerRelease();
            break;
        case 176: // control change
            window.spectrawhorl_namespace.handleControlChange(note, velocity);
            break;
        // Add more cases to handle other MIDI commands if needed
    }
};
