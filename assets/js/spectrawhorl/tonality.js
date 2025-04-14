window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

// Hard code scales
window.spectrawhorl_namespace.C_MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11];
window.spectrawhorl_namespace.D_MAJOR_SCALE = [2, 4, 6, 7, 9, 11, 1];
window.spectrawhorl_namespace.E_MAJOR_SCALE = [4, 6, 8, 9, 11, 1, 3];
window.spectrawhorl_namespace.F_MAJOR_SCALE = [5, 7, 9, 10, 0, 2, 4];
window.spectrawhorl_namespace.G_MAJOR_SCALE = [7, 9, 11, 0, 2, 4, 6];
window.spectrawhorl_namespace.A_MAJOR_SCALE = [9, 11, 1, 2, 4, 6, 8];
window.spectrawhorl_namespace.B_MAJOR_SCALE = [11, 1, 3, 4, 6, 8, 10];
window.spectrawhorl_namespace.C_SHARP_MAJOR_SCALE = [1, 3, 5, 6, 8, 10, 0];
window.spectrawhorl_namespace.D_SHARP_MAJOR_SCALE = [3, 5, 7, 8, 10, 0, 2];
window.spectrawhorl_namespace.F_SHARP_MAJOR_SCALE = [6, 8, 10, 11, 1, 3, 5];
window.spectrawhorl_namespace.G_SHARP_MAJOR_SCALE = [8, 10, 0, 1, 3, 5, 7];
window.spectrawhorl_namespace.A_SHARP_MAJOR_SCALE = [10, 0, 2, 3, 5, 7, 9];
window.spectrawhorl_namespace.midiNoteToString = function (midiNote) {
    if (midiNote < 0 || midiNote > 127) {
        return "Invalid MIDI note value";
    }

    const notes = [
        "C",
        "C#\nDb",
        "D",
        "D# / Eb",
        "E",
        "F",
        "F#\nGb",
        "G",
        "G# / Ab",
        "A",
        "A# / Bb",
        "B",
    ];
    const octave = Math.floor(midiNote / 12) - 1;
    const note = notes[midiNote % 12];

    return [`${note}`, `${octave}`, `${note} ${octave}`];
};
window.spectrawhorl_namespace.midiNoteToStringForSVG = function (midiNote) {
    if (midiNote < 0 || midiNote > 127) {
        return "Invalid MIDI note value";
    }

    const notes = [
        "C",
        "C%23(Db)",
        "D",
        "D%23(Eb)",
        "E",
        "F",
        "F%23(Gb)",
        "G",
        "G%23(Ab)",
        "A",
        "A%23(Bb)",
        "B",
    ];

    const note = notes[midiNote % 12];

    return note;
};
window.spectrawhorl_namespace.midiNoteToStringForTitle = function (midiNote) {
    if (midiNote < 0 || midiNote > 127) {
        return "Invalid MIDI note value";
    }

    const notes = [
        "C",
        "C# / Db",
        "D",
        "D# / Eb",
        "E",
        "F",
        "F# / Gb",
        "G",
        "G# / Ab",
        "A",
        "A# / Bb",
        "B",
    ];

    const note = notes[midiNote % 12];

    return note;
};
window.spectrawhorl_namespace.scaleMap = {
    0: window.spectrawhorl_namespace.C_MAJOR_SCALE,
    2: window.spectrawhorl_namespace.D_MAJOR_SCALE,
    4: window.spectrawhorl_namespace.E_MAJOR_SCALE,
    5: window.spectrawhorl_namespace.F_MAJOR_SCALE,
    7: window.spectrawhorl_namespace.G_MAJOR_SCALE,
    9: window.spectrawhorl_namespace.A_MAJOR_SCALE,
    11: window.spectrawhorl_namespace.B_MAJOR_SCALE,
    1: window.spectrawhorl_namespace.C_SHARP_MAJOR_SCALE,
    3: window.spectrawhorl_namespace.D_SHARP_MAJOR_SCALE,
    6: window.spectrawhorl_namespace.F_SHARP_MAJOR_SCALE,
    8: window.spectrawhorl_namespace.G_SHARP_MAJOR_SCALE,
    10: window.spectrawhorl_namespace.A_SHARP_MAJOR_SCALE,
};
window.spectrawhorl_namespace.getRelativeMajorScale = function(midiNote, modeDegree) {
    const rootIndex = midiNote % 12;

    let relativeMajorIndex;

    switch (modeDegree) {
        case 1: // Ionian
            relativeMajorIndex = rootIndex; // Root is already the major scale root
            break;
        case 2: // Dorian
            relativeMajorIndex = (rootIndex + 10) % 12; // Major scale root is a whole step down
            break;
        case 3: // Phrygian
            relativeMajorIndex = (rootIndex + 8) % 12; // Major scale root is a minor third down
            break;
        case 4: // Lydian
            relativeMajorIndex = (rootIndex + 7) % 12; // Major scale root is a perfect fourth down
            break;
        case 5: // Mixolydian
            relativeMajorIndex = (rootIndex + 5) % 12; // Major scale root is a perfect fifth down
            break;
        case 6: // Aeolian
            relativeMajorIndex = (rootIndex + 3) % 12; // Major scale root is a minor sixth down
            break;
        case 7: // Locrian
            relativeMajorIndex = (rootIndex + 1) % 12; // Major scale root is a major seventh down
            break;
        default:
            return "Invalid mode degree";
    }

    return window.spectrawhorl_namespace.scaleMap[relativeMajorIndex];
}
window.spectrawhorl_namespace.expandScale = function (s) {
    // Create a copy of the input s array
    const expandedScale = [];

    // Iterate over MIDI notes from 24 to 127
    for (let i = 24; i <= 127; i++) {
        if (s.includes(i % 12)) {
            expandedScale.push(i);
        }
    }

    // Return the expanded scale array
    return expandedScale;
};
window.spectrawhorl_namespace.SCALE = window.spectrawhorl_namespace.C_MAJOR_SCALE;
window.spectrawhorl_namespace.overlayKeyNotes = window.spectrawhorl_namespace.expandScale(window.spectrawhorl_namespace.SCALE); // Overlay key notes % 12
window.spectrawhorl_namespace.triadScaleDegree = 1;
window.spectrawhorl_namespace.getTriadFromScale = function(scale, degree) {
    degree--;
    const rootIndex = degree;
    const root = scale[rootIndex] % 12;
    const third = scale[(rootIndex + 2) % 7] % 12;
    const fifth = scale[(rootIndex + 4) % 7] % 12;
    //console.log(root, third, fifth);
    return [root, third, fifth];
}
window.spectrawhorl_namespace.overlayTriadNotes = window.spectrawhorl_namespace.expandScale(
    window.spectrawhorl_namespace.getTriadFromScale(window.spectrawhorl_namespace.C_MAJOR_SCALE, window.spectrawhorl_namespace.triadScaleDegree)
); // Overlay triad notes % 12
window.spectrawhorl_namespace.updateScaleDegrees = function (keyNoteValue, keyModeValue, themeBoolean) {

    let themeValue = themeBoolean ? "Light" : "Dark";

    console.log(keyNoteValue, keyModeValue, themeValue);

    // TODO: Put back in!
    // window.spectrawhorl_namespace.cancelScheduledNotes();

    if (keyModeValue === -6) {
        // Here, minor has been requested as
        // the vi. of its relative major.
        // This sort of roman numeral analysis is
        // as common, from what I gathered

        keyModeValue = -1; // Safely set to major
        keyNoteValue = (keyNoteValue + 3) % 12; // Shift key note up 3 semitones
    }

    window.spectrawhorl_namespace.SCALE = window.spectrawhorl_namespace.getRelativeMajorScale(keyNoteValue, Math.abs(keyModeValue));

    window.spectrawhorl_namespace.overlayKeyNotes = window.spectrawhorl_namespace.expandScale(window.spectrawhorl_namespace.SCALE);

    //overlayTriadNotes = expandScale(getTriadFromScale(SCALE, triadScaleDegree));

    window.spectrawhorl_namespace.SCALE = window.spectrawhorl_namespace.SCALE.slice(Math.abs(keyModeValue) - 1).concat(
        window.spectrawhorl_namespace.SCALE.slice(0, Math.abs(keyModeValue) - 1)
    );

    overlayTriadNotes = window.spectrawhorl_namespace.expandScale(window.spectrawhorl_namespace.getTriadFromScale(window.spectrawhorl_namespace.SCALE, window.spectrawhorl_namespace.triadScaleDegree));

    // TODO: Put back in!
    // window.spectrawhorl_namespace.resetNote();

    //console.log("MODE SCALE: ", ms);
    //console.log("OVERLAY TRIAD: ", overlayTriadNotes);

    // We have to offset so that the notes' index scheme
    // matches the scale degree index sceme
    let modeScale = [];

    // Fill empty slow with an invalid MIDI note
    // in case you try to use it
    modeScale[0] = -1;

    // Increment the indexes
    for (let i = 0; i < window.spectrawhorl_namespace.SCALE.length; i++) {
        modeScale[i + 1] = window.spectrawhorl_namespace.SCALE[i];
    }

    let noteStringsForSVG = modeScale.map(window.spectrawhorl_namespace.midiNoteToStringForSVG);
    let noteStringsForTitle = modeScale.map(window.spectrawhorl_namespace.midiNoteToStringForTitle);

    //console.log("NOTE TITLES: ", noteStringsForTitle);

    //console.log(keyNoteValue, keyModeValue, SCALE, overlayKeyNotes, overlayTriadNotes);

    const updates = scaleDegreesData[Math.abs(keyModeValue)];

    let svgSuffix = "_BLACK.svg";

    if (themeValue === "Dark") {
        svgSuffix = "_WHITE.svg";
    }

    return [
        updates[4].title1,
        updates[4].svg + noteStringsForSVG[4] + svgSuffix,
        noteStringsForTitle[4] + " " + updates[4].title2,

        updates[5].title1,
        updates[5].svg + noteStringsForSVG[5] + svgSuffix,
        noteStringsForTitle[5] + " " + updates[5].title2,

        updates[3].title1,
        updates[3].svg + noteStringsForSVG[3] + svgSuffix,
        noteStringsForTitle[3] + " " + updates[3].title2,

        updates[1].title1,
        updates[1].svg + noteStringsForSVG[1] + svgSuffix,
        noteStringsForTitle[1] + " " + updates[1].title2,

        updates[6].title1,
        updates[6].svg + noteStringsForSVG[6] + svgSuffix,
        noteStringsForTitle[6] + " " + updates[6].title2,

        updates[2].title1,
        updates[2].svg + noteStringsForSVG[2] + svgSuffix,
        noteStringsForTitle[2] + " " + updates[2].title2,

        updates[7].title1,
        updates[7].svg + noteStringsForSVG[7] + svgSuffix,
        noteStringsForTitle[7] + " " + updates[7].title2,
    ];
};
window.spectrawhorl_namespace.sdn_clicks_1 = 0;
window.spectrawhorl_namespace.sdn_clicks_2 = 0;
window.spectrawhorl_namespace.sdn_clicks_3 = 0;
window.spectrawhorl_namespace.sdn_clicks_4 = 0;
window.spectrawhorl_namespace.sdn_clicks_5 = 0;
window.spectrawhorl_namespace.sdn_clicks_6 = 0;
window.spectrawhorl_namespace.sdn_clicks_7 = 0;
window.spectrawhorl_namespace.triadButtonSelection = function (
    n_clicks_1,
    n_clicks_2,
    n_clicks_3,
    n_clicks_4,
    n_clicks_5,
    n_clicks_6,
    n_clicks_7,
    themeBoolean) {

    let themeValue = themeBoolean ? "Light" : "Dark";
    let updatedIndex = 1;

    if (n_clicks_1 !== undefined && n_clicks_1 !== window.spectrawhorl_namespace.sdn_clicks_1) {
        window.spectrawhorl_namespace.sdn_clicks_1 = n_clicks_1;
        updatedIndex = 1;
    }
    if (n_clicks_2 !== undefined && n_clicks_2 !== window.spectrawhorl_namespace.sdn_clicks_2) {
        window.spectrawhorl_namespace.sdn_clicks_2 = n_clicks_2;
        updatedIndex = 2;
    }
    if (n_clicks_3 !== undefined && n_clicks_3 !== window.spectrawhorl_namespace.sdn_clicks_3) {
        window.spectrawhorl_namespace.sdn_clicks_3 = n_clicks_3;
        updatedIndex = 3;
    }
    if (n_clicks_4 !== undefined && n_clicks_4 !== window.spectrawhorl_namespace.sdn_clicks_4) {
        window.spectrawhorl_namespace.sdn_clicks_4 = n_clicks_4;
        updatedIndex = 4;
    }
    if (n_clicks_5 !== undefined && n_clicks_5 !== window.spectrawhorl_namespace.sdn_clicks_5) {
        window.spectrawhorl_namespace.sdn_clicks_5 = n_clicks_5;
        updatedIndex = 5;
    }
    if (n_clicks_6 !== undefined && n_clicks_6 !== window.spectrawhorl_namespace.sdn_clicks_6) {
        window.spectrawhorl_namespace.sdn_clicks_6 = n_clicks_6;
        updatedIndex = 6;
    }
    if (n_clicks_7 !== undefined && n_clicks_7 !== window.spectrawhorl_namespace.sdn_clicks_7) {
        window.spectrawhorl_namespace.sdn_clicks_7 = n_clicks_7;
        updatedIndex = 7;
    }

    window.spectrawhorl_namespace.triadScaleDegree = updatedIndex;

    window.spectrawhorl_namespace.overlayTriadNotes = window.spectrawhorl_namespace.expandScale(window.spectrawhorl_namespace.getTriadFromScale(window.spectrawhorl_namespace.SCALE, window.spectrawhorl_namespace.triadScaleDegree));

    // TODO: Add back in!!
    // resetNote();

    console.log(window.spectrawhorl_namespace.overlayKeyNotes, window.spectrawhorl_namespace.triadScaleDegree, window.spectrawhorl_namespace.overlayTriadNotes);

    returnArray = [
        "spectrawhorl-sd_" + themeValue,
        "spectrawhorl-sd_" + themeValue,
        "spectrawhorl-sd_" + themeValue,
        "spectrawhorl-sd_" + themeValue,
        "spectrawhorl-sd_" + themeValue,
        "spectrawhorl-sd_" + themeValue,
        "spectrawhorl-sd_" + themeValue,
    ];

    returnArray[window.spectrawhorl_namespace.triadScaleDegree - 1] += "_selected";

    return returnArray;
};
