window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** spectrawhorl spectrogram variables w/ defaults */

window.spectrawhorl_namespace.spectrogramType = "SPIRAL";

// 1. VIBRANT MUSIC PALETTE (Neon Synthwave/Cyberpunk Theme)
window.spectrawhorl_namespace.palette = [
    "#FF007F", // Neon Pink (Sub-bass)
    "#9D00FF", // Intense Violet
    "#7000FF", // Deep Purple
    "#0019FF", // Electric Blue
    "#0088FF", // Bright Blue
    "#00FFFF", // Cyan (Mids)
    "#00FFAA", // Mint Green
    "#00FF55", // Bright Green
    "#AAFF00", // Lime
    "#FFFF00", // Neon Yellow
    "#FFAA00", // Neon Orange (Highs)
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
window.spectrawhorl_namespace.octaveWidth = 1.2; // Slightly widened for better spiral spread
window.spectrawhorl_namespace.peakAccentuation = 2.5; // Lowered from 4 to show more fluid harmonic movement
window.spectrawhorl_namespace.fade = 0.15; 

window.spectrawhorl_namespace.spectrogramLineWidth = 4; // Thinner base lines look cleaner and sharper
window.spectrawhorl_namespace.threshold = 0.05; // Raised slightly to ignore muddy background noise

window.spectrawhorl_namespace.initSpectrogram = function (p) {
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

    window.spectrawhorl_namespace.canvasSize = Math.min(p.width, p.height);

    // Calculating Cx and Cy based on spectrogramType
    if (window.spectrawhorl_namespace.spectrogramType === "CIRCLES") {
        window.spectrawhorl_namespace.Cx = window.spectrawhorl_namespace.OCTAVES.map(
            (octave, i) =>
                center_x + (((octave - 1) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(window.spectrawhorl_namespace.ANGLES[i])
        );
        window.spectrawhorl_namespace.Cy = window.spectrawhorl_namespace.OCTAVES.map(
            (octave, i) =>
                center_y - (((octave - 1) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(window.spectrawhorl_namespace.ANGLES[i])
        );
    } else if (window.spectrawhorl_namespace.spectrogramType === "SPIRAL") {
        window.spectrawhorl_namespace.Cx = window.spectrawhorl_namespace.NOTES.map(
            (note, i) =>
                center_x +
                ((((note - 24) / 12) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(window.spectrawhorl_namespace.ANGLES[i])
        );
        window.spectrawhorl_namespace.Cy = window.spectrawhorl_namespace.NOTES.map(
            (note, i) =>
                center_y -
                ((((note - 24) / 12) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(window.spectrawhorl_namespace.ANGLES[i])
        );
    } else {
        window.spectrawhorl_namespace.Cx = window.spectrawhorl_namespace.FREQUENCIES.map(() => center_x);
        window.spectrawhorl_namespace.Cy = window.spectrawhorl_namespace.FREQUENCIES.map(() => center_y);
    }

    // COLORS calculation
    window.spectrawhorl_namespace.COLORS = window.spectrawhorl_namespace.OCTAVES.map((octave) => {
        let idx = Math.abs(octave) % window.spectrawhorl_namespace.palette.length;
        return window.spectrawhorl_namespace.palette[idx];
    });

    // max_amplitude calculation
    window.spectrawhorl_namespace.max_amplitude = Math.max.apply(null, spectrum.map(Math.abs)) || 1;

    // radii calculation
    window.spectrawhorl_namespace.radii = spectrum.map(
        (amp) =>
            (window.spectrawhorl_namespace.octaveHeight * window.spectrawhorl_namespace.canvasSize / 20) * Math.pow(Math.abs(amp) / window.spectrawhorl_namespace.max_amplitude, window.spectrawhorl_namespace.peakAccentuation)
    );

    // x and y calculation
    window.spectrawhorl_namespace.x = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.cos(window.spectrawhorl_namespace.ANGLES[i]));
    window.spectrawhorl_namespace.y = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.sin(window.spectrawhorl_namespace.ANGLES[i]));
};

window.spectrawhorl_namespace.lines = [];
window.spectrawhorl_namespace.spectrum = null;
window.spectrawhorl_namespace.colorCache = {};

window.spectrawhorl_namespace.hexToRgbCached = function(hex) {
    if (window.spectrawhorl_namespace.colorCache[hex]) {
        return window.spectrawhorl_namespace.colorCache[hex];
    }
    hex = hex.replace(/^#/, '');
    let bigint = parseInt(hex, 16);
    let r = (bigint >> 16) & 255;
    let g = (bigint >> 8) & 255;
    let b = bigint & 255;
    window.spectrawhorl_namespace.colorCache[hex] = [r, g, b];
    return window.spectrawhorl_namespace.colorCache[hex];
}

window.spectrawhorl_namespace.drawSpectrogram = function (p) {
    if (window.spectrawhorl_namespace.fft) {
        window.spectrawhorl_namespace.spectrum = window.spectrawhorl_namespace.fft.analyze();
        window.spectrawhorl_namespace.max_amplitude = Math.max.apply(null, window.spectrawhorl_namespace.spectrum.map(Math.abs)) || 1;

        // radii calculation
        window.spectrawhorl_namespace.radii = window.spectrawhorl_namespace.spectrum.map(
            (amp) => ((window.spectrawhorl_namespace.octaveHeight * window.spectrawhorl_namespace.canvasSize / 20) * Math.pow(Math.abs(amp) / window.spectrawhorl_namespace.max_amplitude, window.spectrawhorl_namespace.peakAccentuation))
        );

        // x and y calculation
        window.spectrawhorl_namespace.x = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.cos(window.spectrawhorl_namespace.ANGLES[i]));
        window.spectrawhorl_namespace.y = window.spectrawhorl_namespace.radii.map((radius, i) => radius * Math.sin(window.spectrawhorl_namespace.ANGLES[i]));

        window.spectrawhorl_namespace.lines = [];
        let color;

        for (let i = 0; i < window.spectrawhorl_namespace.Cx.length; i++) {
            let currentAmp = window.spectrawhorl_namespace.spectrum[i];
            
            if (window.spectrawhorl_namespace.OCTAVES[i] > 0 && currentAmp > (window.spectrawhorl_namespace.threshold * window.spectrawhorl_namespace.max_amplitude)) {

                if (window.spectrawhorl_namespace.colorBy == "NOTE") {
                    color = window.spectrawhorl_namespace.palette[Math.floor(window.spectrawhorl_namespace.NOTES[i] + 0.5) % window.spectrawhorl_namespace.palette.length];
                } else {
                    color = window.spectrawhorl_namespace.palette[Math.abs(window.spectrawhorl_namespace.OCTAVES[i]) % window.spectrawhorl_namespace.palette.length];
                }

                if (!window.spectrawhorl_namespace.noteLegendPalette.includes(Math.floor(window.spectrawhorl_namespace.NOTES[i] + 0.5) % 12)) continue;
                if (!window.spectrawhorl_namespace.octaveLegendPalette.includes(Math.abs(window.spectrawhorl_namespace.OCTAVES[i]))) continue;

                let rgb = window.spectrawhorl_namespace.hexToRgbCached(color);
                
                // 2. DYNAMIC ALPHA MAPPING (Loud sounds are fully bright, quiet sounds glow softly)
                let intensity = currentAmp / window.spectrawhorl_namespace.max_amplitude;
                let alpha = p.map(intensity, window.spectrawhorl_namespace.threshold, 1, 30, 255);

                // 3. ENHANCED STROKE WEIGHTING (Gives a punchy, variable thickness to heavy beats)
                let dynamicWidth = window.spectrawhorl_namespace.spectrogramLineWidth * Math.pow(intensity, 0.5);

                window.spectrawhorl_namespace.lines.push({
                    x1: window.spectrawhorl_namespace.Cx[i],
                    y1: window.spectrawhorl_namespace.Cy[i],
                    x2: window.spectrawhorl_namespace.Cx[i] + window.spectrawhorl_namespace.x[i],
                    y2: window.spectrawhorl_namespace.Cy[i] - window.spectrawhorl_namespace.y[i],
                    octave: window.spectrawhorl_namespace.OCTAVES[i],
                    RGB: rgb,
                    A: alpha,
                    w: Math.max(1.5, dynamicWidth), // Never drop below a clean 1.5px line
                });
            }
        }

        // Sort lines based on their z-value
        window.spectrawhorl_namespace.lines.sort((a, b) => b.octave - a.octave);

        // Render pass with additive-like blending style
        for (let lineData of window.spectrawhorl_namespace.lines) {
            p.stroke(lineData.RGB[0], lineData.RGB[1], lineData.RGB[2], lineData.A);
            p.strokeWeight(lineData.w);
            p.line(lineData.x1, lineData.y1, lineData.x2, lineData.y2);
        }
    }
};