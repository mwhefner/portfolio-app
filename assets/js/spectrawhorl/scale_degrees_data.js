
var scaleDegreesData = {
    // Sharp/Flat values are identified like this example string: "C#/Db"
    // MIDI note % 12; e.g. C = 0

    1: {
        // IONIAN

        1: {
            // title 1 contains 2 parts:
            // first: the conventional roman numeral analysis
            // second: the function of the scale degree, lowercase
            // (note: these are dynamic; see examples below)
            title1: "I. tonic",

            // next, the stem of the path for an SVG of the triad of this mode
            svg: "assets/svg/spectrawhorl/IONIAN_",

            // finally, the name of the mode, mode quality
            title2: "Ionian (Major)",
        },
        2: {
            title1: "ii. supertonic",
            svg: "assets/svg/spectrawhorl/DORIAN_",
            title2: "Dorian (minor)",
        },
        3: {
            title1: "iii. mediant",
            svg: "assets/svg/spectrawhorl/PHRYGIAN_",
            title2: "Phrygian (minor)",
        },
        4: {
            title1: "IV. subdominant",
            svg: "assets/svg/spectrawhorl/LYDIAN_",
            title2: "Lydian (Major)",
        },
        5: {
            title1: "V. dominant",
            svg: "assets/svg/spectrawhorl/MIXOLYDIAN_",
            title2: "Mixolydian (Major)",
        },
        6: {
            title1: "vi. submediant",
            svg: "assets/svg/spectrawhorl/AEOLIAN_",
            title2: "Aeolian (Minor)",
        },
        7: {
            title1: "vii°. leading tone",
            svg: "assets/svg/spectrawhorl/LOCRIAN_",
            title2: "Locrian (dim)",
        },
    },

    2: {
        // DORIAN
    
        1: {
            // title 1 contains 2 parts:
            // first: the conventional roman numeral analysis
            // second: the function of the scale degree, lowercase
            // (note: these are dynamic; see examples below)
            title1: "i. tonic",
    
            // next, the stem of the path for an SVG of the triad of this mode
            svg: "assets/svg/spectrawhorl/DORIAN_",
    
            // finally, the name of the mode, mode quality
            title2: "Dorian (minor)",
        },
        2: {
            title1: "ii. supertonic",
            svg: "assets/svg/spectrawhorl/PHRYGIAN_",
            title2: "Phrygian (minor)",
        },
        3: {
            title1: "♭III. mediant",
            svg: "assets/svg/spectrawhorl/LYDIAN_",
            title2: "Lydian (Major)",
        },
        4: {
            title1: "IV. subdominant",
            svg: "assets/svg/spectrawhorl/MIXOLYDIAN_",
            title2: "Mixolydian (Major)",
        },
        5: {
            title1: "v. dominant",
            svg: "assets/svg/spectrawhorl/AEOLIAN_",
            title2: "Aeolian (Minor)",
        },
        6: {
            title1: "vi°. submediant",
            svg: "assets/svg/spectrawhorl/LOCRIAN_",
            title2: "Locrian (dim)",
        },
        7: {
            title1: "♭VII. subtonic",
            svg: "assets/svg/spectrawhorl/IONIAN_",
            title2: "Ionian (Major)",
        },
    },
    
    3: {
        // PHRYGIAN
    
        1: {
            // title 1 contains 2 parts:
            // first: the conventional roman numeral analysis
            // second: the function of the scale degree, lowercase
            // (note: these are dynamic; see examples below)
            title1: "i. tonic",
    
            // next, the stem of the path for an SVG of the triad of this mode
            svg: "assets/svg/spectrawhorl/PHRYGIAN_",
    
            // finally, the name of the mode, mode quality
            title2: "Phrygian (minor)",
        },
        2: {
            title1: "♭II. supertonic",
            svg: "assets/svg/spectrawhorl/LYDIAN_",
            title2: "Lydian (Major)",
        },
        3: {
            title1: "♭III. mediant",
            svg: "assets/svg/spectrawhorl/MIXOLYDIAN_",
            title2: "Mixolydian (Major)",
        },
        4: {
            title1: "iv. subdominant",
            svg: "assets/svg/spectrawhorl/AEOLIAN_",
            title2: "Aeolian (Minor)",
        },
        5: {
            title1: "v°. dominant",
            svg: "assets/svg/spectrawhorl/LOCRIAN_",
            title2: "Locrian (dim)",
        },
        6: {
            title1: "♭VI. submediant",
            svg: "assets/svg/spectrawhorl/IONIAN_",
            title2: "Ionian (Major)",
        },
        7: {
            title1: "♭vii. subtonic",
            svg: "assets/svg/spectrawhorl/DORIAN_",
            title2: "Dorian (minor)",
        },
    },

    4: {
        // LYDIAN
    
        1: {
            // title 1 contains 2 parts:
            // first: the conventional roman numeral analysis
            // second: the function of the scale degree, lowercase
            // (note: these are dynamic; see examples below)
            title1: "I. tonic",
    
            // next, the stem of the path for an SVG of the triad of this mode
            svg: "assets/svg/spectrawhorl/LYDIAN_",
    
            // finally, the name of the mode, mode quality
            title2: "Lydian (Major)",
        },
        2: {
            title1: "II. supertonic",
            svg: "assets/svg/spectrawhorl/MIXOLYDIAN_",
            title2: "Mixolydian (Major)",
        },
        3: {
            title1: "iii. mediant",
            svg: "assets/svg/spectrawhorl/AEOLIAN_",
            title2: "Aeolian (Minor)",
        },
        4: {
            title1: "♯iv°. subdominant",
            svg: "assets/svg/spectrawhorl/LOCRIAN_",
            title2: "Locrian (dim)",
        },
        5: {
            title1: "V. dominant",
            svg: "assets/svg/spectrawhorl/IONIAN_",
            title2: "Ionian (Major)",
        },
        6: {
            title1: "vi. submediant",
            svg: "assets/svg/spectrawhorl/DORIAN_",
            title2: "Dorian (minor)",
        },
        7: {
            title1: "vii. leading tone",
            svg: "assets/svg/spectrawhorl/PHRYGIAN_",
            title2: "Phrygian (minor)",
        },
    },

    5: {
        // MIXOLYDIAN

        1: {
            // title 1 contains 2 parts:
            // first: the conventional roman numeral analysis
            // second: the function of the scale degree, lowercase
            // (note: these are dynamic; see examples below)
            title1: "I. tonic",

            // next, the stem of the path for an SVG of the triad of this mode
            svg: "assets/svg/spectrawhorl/MIXOLYDIAN_",

            // finally, the name of the mode, mode quality
            title2: "Mixolydian (Major)",
        },
        2: {
            title1: "ii. supertonic",
            svg: "assets/svg/spectrawhorl/AEOLIAN_",
            title2: "Aeolian (Minor)",
        },
        3: {
            title1: "iii°. mediant",
            svg: "assets/svg/spectrawhorl/LOCRIAN_",
            title2: "Locrian (dim)",
        },
        4: {
            title1: "IV. subdominant",
            svg: "assets/svg/spectrawhorl/IONIAN_",
            title2: "Ionian (Major)",
        },
        5: {
            title1: "v. dominant",
            svg: "assets/svg/spectrawhorl/DORIAN_",
            title2: "Dorian (minor)",
        },
        6: {
            title1: "vi. submediant",
            svg: "assets/svg/spectrawhorl/PHRYGIAN_",
            title2: "Phrygian (minor)",
        },
        7: {
            title1: "♭VII. subtonic",
            svg: "assets/svg/spectrawhorl/LYDIAN_",
            title2: "Lydian (Major)",
        },
    },

    6: {
        // AEOLIAN
    
        1: {
            // title 1 contains 2 parts:
            // first: the conventional roman numeral analysis
            // second: the function of the scale degree, lowercase
            // (note: these are dynamic; see examples below)
            title1: "i. tonic",
    
            // next, the stem of the path for an SVG of the triad of this mode
            svg: "assets/svg/spectrawhorl/AEOLIAN_",
    
            // finally, the name of the mode, mode quality
            title2: "Aeolian (Minor)",
        },
        2: {
            title1: "ii°. supertonic",
            svg: "assets/svg/spectrawhorl/LOCRIAN_",
            title2: "Locrian (dim)",
        },
        3: {
            title1: "♭III. mediant",
            svg: "assets/svg/spectrawhorl/IONIAN_",
            title2: "Ionian (Major)",
        },
        4: {
            title1: "iv. subdominant",
            svg: "assets/svg/spectrawhorl/DORIAN_",
            title2: "Dorian (minor)",
        },
        5: {
            title1: "v. dominant",
            svg: "assets/svg/spectrawhorl/PHRYGIAN_",
            title2: "Phrygian (minor)",
        },
        6: {
            title1: "♭VI. submediant",
            svg: "assets/svg/spectrawhorl/LYDIAN_",
            title2: "Lydian (Major)",
        },
        7: {
            title1: "♭VII. subtonic",
            svg: "assets/svg/spectrawhorl/MIXOLYDIAN_",
            title2: "Mixolydian (Major)",
        },
    },
    
    7: {
        // LOCRIAN
    
        1: {
            // title 1 contains 2 parts:
            // first: the conventional roman numeral analysis
            // second: the function of the scale degree, lowercase
            // (note: these are dynamic; see examples below)
            title1: "i°. tonic",
    
            // next, the stem of the path for an SVG of the triad of this mode
            svg: "assets/svg/spectrawhorl/LOCRIAN_",
    
            // finally, the name of the mode, mode quality
            title2: "Locrian (dim)",
        },
        2: {
            title1: "♭II. supertonic",
            svg: "assets/svg/spectrawhorl/IONIAN_",
            title2: "Ionian (Major)",
        },
        3: {
            title1: "♭iii. mediant",
            svg: "assets/svg/spectrawhorl/DORIAN_",
            title2: "Dorian (minor)",
        },
        4: {
            title1: "iv. subdominant",
            svg: "assets/svg/spectrawhorl/PHRYGIAN_",
            title2: "Phrygian (minor)",
        },
        5: {
            title1: "♭V. dominant",
            svg: "assets/svg/spectrawhorl/LYDIAN_",
            title2: "Lydian (Major)",
        },
        6: {
            title1: "♭VI. submediant",
            svg: "assets/svg/spectrawhorl/MIXOLYDIAN_",
            title2: "Mixolydian (Major)",
        },
        7: {
            title1: "♭vii. subtonic",
            svg: "assets/svg/spectrawhorl/AEOLIAN_",
            title2: "Aeolian (Minor)",
        },
    },
    

};

//console.log("Scale degree data loaded.");
