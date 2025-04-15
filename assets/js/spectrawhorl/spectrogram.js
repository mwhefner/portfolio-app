window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** spectrawhorl spectrogram variables w/ defaults */

window.spectrawhorl_namespace.spectrogramType = "SPIRAL";
window.spectrawhorl_namespace.palette = [
    "rgb(165,0,38)",
    "rgb(215,48,39)",
    "rgb(244,109,67)",
    "rgb(253,174,97)",
    "rgb(254,224,144)",
    "rgb(255,255,191)",
    "rgb(224,243,248)",
    "rgb(171,217,233)",
    "rgb(116,173,209)",
    "rgb(69,117,180)",
    "rgb(49,54,149)",
];
window.spectrawhorl_namespace.REINIT_SPECTROGRAM = false;
window.spectrawhorl_namespace.FREQUENCIES = null;
window.spectrawhorl_namespace.NOTES = null;
window.spectrawhorl_namespace.OCTAVES = null;
window.spectrawhorl_namespace.ANGLES = null;
window.spectrawhorl_namespace.Cx = null;
window.spectrawhorl_namespace.Cy = null;
window.spectrawhorl_namespace.COLORS = null;
window.spectrawhorl_namespace.max_amplitude = null;
window.spectrawhorl_namespace.radii = null;
window.spectrawhorl_namespace.x = null;
window.spectrawhorl_namespace.y = null;

window.spectrawhorl_namespace.canvasSize = null;
window.spectrawhorl_namespace.octaveHeight = 5;
window.spectrawhorl_namespace.octaveWidth = 1;
window.spectrawhorl_namespace.peakAccentuation = 4;
window.spectrawhorl_namespace.fade = 0.1; 

window.spectrawhorl_namespace.spectrogramLineWidth = 10;
window.spectrawhorl_namespace.threshold = 0;

window.spectrawhorl_namespace.initSpectrogram = function (p) {
    //console.log("Running spectrogram initialization.");

    // Assuming fft is properly initialized already
    let spectrum = window.spectrawhorl_namespace.fft.analyze();

    // Convert spectrum data to frequencies
    window.spectrawhorl_namespace.FREQUENCIES = spectrum.map(
        (value, index, array) => (index * window.spectrawhorl_namespace.fft.analyser.context.sampleRate) / (array.length * 2)
    );

    // NOTES and OCTAVES calculation
    window.spectrawhorl_namespace.NOTES = window.spectrawhorl_namespace.FREQUENCIES.map(
        (freq) => window.spectrawhorl_namespace.freqToNote(freq)
    );

    window.spectrawhorl_namespace.OCTAVES = window.spectrawhorl_namespace.NOTES.map((note) => Math.floor(note / 12) - 1);

    // ANGLES calculation
    window.spectrawhorl_namespace.ANGLES = window.spectrawhorl_namespace.NOTES.map((note) => (2 * Math.PI * note) / 12);

    let center_x = p.width / 2;
    let center_y = p.height / 2;

    window.spectrawhorl_namespace.canvasSize = p.height;

    if (p.width < p.height) {
        window.spectrawhorl_namespace.canvasSize = p.width;
    }

    // Calculating Cx and Cy based on spectrogramType
    if (window.spectrawhorl_namespace.spectrogramType === "CIRCLES") {
        window.spectrawhorl_namespace.Cx = window.spectrawhorl_namespace.OCTAVES.map(
            (octave, i) =>
                window.spectrawhorl_namespace.center_x + (((octave - 1) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(window.spectrawhorl_namespace.ANGLES[i])
        );
        window.spectrawhorl_namespace.Cy = window.spectrawhorl_namespace.OCTAVES.map(
            (octave, i) =>
                window.spectrawhorl_namespace.center_y - (((octave - 1) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(window.spectrawhorl_namespace.ANGLES[i])
        );
    } else if (window.spectrawhorl_namespace.spectrogramType === "SPIRAL") {
        window.spectrawhorl_namespace.Cx = window.spectrawhorl_namespace.NOTES.map(
            (note, i) =>
                window.spectrawhorl_namespace.center_x +
                ((((note - 24) / 12) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(window.spectrawhorl_namespace.ANGLES[i])
        );
        window.spectrawhorl_namespace.Cy = window.spectrawhorl_namespace.NOTES.map(
            (note, i) =>
                window.spectrawhorl_namespace.center_y -
                ((((note - 24) / 12) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(window.spectrawhorl_namespace.ANGLES[i])
        );
    } else {
        window.spectrawhorl_namespace.Cx = window.spectrawhorl_namespace.FREQUENCIES.map((freq) => window.spectrawhorl_namespace.center_x);
        window.spectrawhorl_namespace.Cy = window.spectrawhorl_namespace.FREQUENCIES.map((freq) => window.spectrawhorl_namespace.center_y);
    }

    // COLORS calculation
    window.spectrawhorl_namespace.COLORS = window.spectrawhorl_namespace.OCTAVES.map((octave) => {
        if (0 <= octave && octave < window.spectrawhorl_namespace.palette.length) return window.spectrawhorl_namespace.palette[octave];
        else return [255, 255, 255];
    });

    // max_amplitude calculation
    window.spectrawhorl_namespace.max_amplitude = Math.max.apply(null, spectrum.map(Math.abs));

    // radii calculation
    window.spectrawhorl_namespace.radii = spectrum.map(
        (amp) =>
            (window.spectrawhorl_namespace.octaveHeight * window.spectrawhorl_namespace.canvasSize / 20) * Math.pow(Math.abs(amp) / window.spectrawhorl_namespace.max_amplitude, window.spectrawhorl_namespace.peakAccentuation)
    );

    // x and y calculation
    window.spectrawhorl_namespace.x = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.cos(window.spectrawhorl_namespace.ANGLES[i]));
    window.spectrawhorl_namespace.y = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.sin(window.spectrawhorl_namespace.ANGLES[i]));

    //console.log("Spectrogram (re)initialized.");
};



window.spectrawhorl_namespace.lines = [];
window.spectrawhorl_namespace.spectrum = null;

// Cache object to store hex to RGB conversions
window.spectrawhorl_namespace.colorCache = {};

window.spectrawhorl_namespace.hexToRgbCached = function(hex) {
    // Check if the hex color is already in the cache
    if (window.spectrawhorl_namespace.colorCache[hex]) {
        return window.spectrawhorl_namespace.colorCache[hex];
    }

    // Remove the hash at the start if it's there
    hex = hex.replace(/^#/, '');
    
    // Parse r, g, b values
    let bigint = parseInt(hex, 16);
    let r = (bigint >> 16) & 255;
    let g = (bigint >> 8) & 255;
    let b = bigint & 255;

    // Store the result in the cache
    window.spectrawhorl_namespace.colorCache[hex] = [r, g, b];

    return window.spectrawhorl_namespace.colorCache[hex];
}

window.spectrawhorl_namespace.drawSpectrogram = function (p) {

    if (window.spectrawhorl_namespace.fft) {
        window.spectrawhorl_namespace.spectrum = window.spectrawhorl_namespace.fft.analyze();

        // max_amplitude calculation
        window.spectrawhorl_namespace.max_amplitude = Math.max.apply(null, window.spectrawhorl_namespace.spectrum.map(Math.abs));

        // radii calculation
        window.spectrawhorl_namespace.radii = window.spectrawhorl_namespace.spectrum.map(
            (amp) =>
                window.spectrawhorl_namespace.max_amplitude === 0 ? 0 : ((window.spectrawhorl_namespace.octaveHeight * window.spectrawhorl_namespace.canvasSize / 20) * Math.pow(Math.abs(amp) / window.spectrawhorl_namespace.max_amplitude, window.spectrawhorl_namespace.peakAccentuation))
        );

        // x and y calculation
        window.spectrawhorl_namespace.x = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.cos(window.spectrawhorl_namespace.ANGLES[i]));
        window.spectrawhorl_namespace.y = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.sin(window.spectrawhorl_namespace.ANGLES[i]));

        window.spectrawhorl_namespace.lines = [];

        let color;

        for (let i = 0; i < window.spectrawhorl_namespace.Cx.length; i++) {
            if (window.spectrawhorl_namespace.OCTAVES[i] > 0 && window.spectrawhorl_namespace.spectrum[i] > (window.spectrawhorl_namespace.threshold * window.spectrawhorl_namespace.max_amplitude)) {

                if (window.spectrawhorl_namespace.colorBy == "NOTE") {
                    
                    color = window.spectrawhorl_namespace.palette[Math.floor(window.spectrawhorl_namespace.NOTES[i] + 0.5) % 12];

                    if (
                        !window.spectrawhorl_namespace.legendPalette.includes(Math.floor(window.spectrawhorl_namespace.NOTES[i] + 0.5) % 12)
                    ) {
                        continue;
                    }
                } else {
                    color = window.spectrawhorl_namespace.palette[window.spectrawhorl_namespace.OCTAVES[i]];

                    if (!window.spectrawhorl_namespace.legendPalette.includes(window.spectrawhorl_namespace.OCTAVES[i])) {
                        continue;
                    }
                }

                let rgb = window.spectrawhorl_namespace.hexToRgbCached(color);
                let alpha = 256 * (1 - window.spectrawhorl_namespace.fade);

                // Add to lines
                window.spectrawhorl_namespace.lines.push({
                    x1: window.spectrawhorl_namespace.Cx[i],
                    y1: window.spectrawhorl_namespace.Cy[i],
                    x2: window.spectrawhorl_namespace.Cx[i] + window.spectrawhorl_namespace.x[i],
                    y2: window.spectrawhorl_namespace.Cy[i] - window.spectrawhorl_namespace.y[i],
                    octave: window.spectrawhorl_namespace.OCTAVES[i],
                    RGB: rgb,
                    A: alpha,
                    w: window.spectrawhorl_namespace.spectrogramLineWidth,
                });
            }
        }

        // Sort lines based on their z-value
        window.spectrawhorl_namespace.lines.sort((a, b) => b.octave - a.octave);

        // Actually draw the lines of the spectrogram, finally
        for (let lineData of window.spectrawhorl_namespace.lines) {
            p.stroke(lineData.RGB[0], lineData.RGB[1], lineData.RGB[2], lineData.A);
            p.strokeWeight(lineData.w);
            p.line(lineData.x1, lineData.y1, lineData.x2, lineData.y2);
        }
    }
};

//console.log("Spectrogram variables initialized.");
