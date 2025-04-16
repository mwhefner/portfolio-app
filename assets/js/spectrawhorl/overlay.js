window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** spectrawhorl overlay variables w/ defaults */
window.spectrawhorl_namespace.noteOverlayColor = "#ffffff";
window.spectrawhorl_namespace.harmonicSeriesOverlayColor = "#ffffff";

window.spectrawhorl_namespace.overlayOnTop = false;
window.spectrawhorl_namespace.showNoteOverlay = true;
window.spectrawhorl_namespace.overlayWidthPercent = 100;
window.spectrawhorl_namespace.overlayStrokeWidth = 2;
window.spectrawhorl_namespace.overlayWidth; // Calculated in init & update.
window.spectrawhorl_namespace.overlayOpacity = 64;

// NOTE OVERLAY SPECIFIC
window.spectrawhorl_namespace.noteOverlayLetterPercent = 0.1;
window.spectrawhorl_namespace.noteOverlayType = "ALL"; // "NONE", "ALL", "KEY", or "TRIAD"

// HARMONIC SERIES OVERLAY
window.spectrawhorl_namespace.harmonicSeriesOverlayType = "FREE"; // Whether and how to show the harmonic series overlay. "NONE", "FREE", or snap to "NOTE"
window.spectrawhorl_namespace.seriesFundamental = 60;

window.spectrawhorl_namespace.chordFactorsToShow = "ALL"; // "NONE", "ALL", "KEY", or "TRIAD"


window.spectrawhorl_namespace.initOverlay = function(p) {

    window.spectrawhorl_namespace.overlayWidth = (window.spectrawhorl_namespace.overlayWidthPercent / 100) * Math.min(p.width, p.height);

}

window.spectrawhorl_namespace.drawOverlay = function(p) {

    // NOTE OVERLAY
    if (window.spectrawhorl_namespace.showNoteOverlay) {
        const overlayNoteColor = window.spectrawhorl_namespace.hexToRgbCached(window.spectrawhorl_namespace.noteOverlayColor);

        // Shuffle through Octave 1 MIDI 
        for (let i = 24; i < 36; i++) {
            
            if (
                (window.spectrawhorl_namespace.noteOverlayType === "ALL") ||
                (window.spectrawhorl_namespace.noteOverlayType === "KEY" && window.spectrawhorl_namespace.overlayKeyNotes.includes(i)) ||
                (window.spectrawhorl_namespace.noteOverlayType === "TRIAD" && window.spectrawhorl_namespace.overlayTriadNotes.includes(i))
            ) {

                let angle = (2 * Math.PI * i) / 12;
                let radius = window.spectrawhorl_namespace.overlayWidth / 2;
                let center_x = p.width / 2;
                let center_y = p.height / 2;

                let rLine = radius * (1 - window.spectrawhorl_namespace.noteOverlayLetterPercent * 2);
                let rxLine = rLine * Math.cos(angle) + center_x;
                let ryLine = center_y - rLine * Math.sin(angle);

                let rLetter = radius * (1 - window.spectrawhorl_namespace.noteOverlayLetterPercent);
                let rxLetter = rLetter * Math.cos(angle) + center_x;
                let ryLetter = center_y - rLetter * Math.sin(angle);

                p.stroke(overlayNoteColor[0], overlayNoteColor[1], overlayNoteColor[2], window.spectrawhorl_namespace.overlayOpacity);
                p.fill(overlayNoteColor[0], overlayNoteColor[1], overlayNoteColor[2], window.spectrawhorl_namespace.overlayOpacity);

                p.strokeWeight(window.spectrawhorl_namespace.overlayStrokeWidth);

                p.line(center_x, center_y, rxLine, ryLine);

                p.noStroke();

                p.textAlign(p.CENTER, p.CENTER);

                p.textSize(radius * window.spectrawhorl_namespace.noteOverlayLetterPercent);

                p.text(window.spectrawhorl_namespace.midiNoteToString(i)[0], rxLetter, ryLetter);

            }
        }
    }

    if (window.spectrawhorl_namespace.harmonicSeriesOverlayType !== "NONE") {
    
    const harmonicSeriesOverlayColor = window.spectrawhorl_namespace.hexToRgbCached(window.spectrawhorl_namespace.harmonicSeriesOverlayColor);
    // HARMONIC SERIES OVERLAY

    let frequencyToUse = window.spectrawhorl_namespace.seriesFundamental;

    if (window.spectrawhorl_namespace.harmonicSeriesOverlayType === "NOTE") {
        frequencyToUse = Math.round(frequencyToUse);
    }


    for (let i = 1, harmonicFrequency = window.spectrawhorl_namespace.noteToFreq(frequencyToUse); 
        harmonicFrequency <= p.sampleRate() / 2; 
        i++, harmonicFrequency = i * window.spectrawhorl_namespace.noteToFreq(frequencyToUse)) {
    
        let note = window.spectrawhorl_namespace.freqToNote(harmonicFrequency);

        let octave = Math.floor(note / 12) - 1;
        let angle = (2 * Math.PI * note) / 12;

        let lx1 = p.width / 2;
        let ly1 = p.height / 2;
        let lx2 = p.width / 2;
        let ly2 = p.height / 2;

        p.stroke(harmonicSeriesOverlayColor[0], harmonicSeriesOverlayColor[1], harmonicSeriesOverlayColor[2], window.spectrawhorl_namespace.overlayOpacity);
        p.fill(harmonicSeriesOverlayColor[0], harmonicSeriesOverlayColor[1], harmonicSeriesOverlayColor[2], window.spectrawhorl_namespace.overlayOpacity);

        p.strokeWeight(window.spectrawhorl_namespace.overlayStrokeWidth);

        if (window.spectrawhorl_namespace.spectrogramType === "CIRCLES") {
            lx1 = lx1 + (((octave - 1) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(angle);
            ly1 = ly1 - (((octave - 1) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(angle);

            lx2 = lx1 + (window.spectrawhorl_namespace.canvasSize / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(angle);
            ly2 = ly1 - (window.spectrawhorl_namespace.canvasSize / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(angle);

            p.line(lx1, ly1, lx2, ly2);

        } else if (window.spectrawhorl_namespace.spectrogramType === "SPIRAL") {
            lx1 = lx1 + ((((note - 24) / 12) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(angle);
            ly1 = ly1 - ((((note - 24) / 12) * window.spectrawhorl_namespace.canvasSize) / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(angle);

            lx2 = lx1 + (window.spectrawhorl_namespace.canvasSize / 20) * window.spectrawhorl_namespace.octaveWidth * Math.cos(angle);
            ly2 = ly1 - (window.spectrawhorl_namespace.canvasSize / 20) * window.spectrawhorl_namespace.octaveWidth * Math.sin(angle);

            p.line(lx1, ly1, lx2, ly2);
        } else {

            lx2 = lx1 + (window.spectrawhorl_namespace.canvasSize / 2) * window.spectrawhorl_namespace.octaveWidth * Math.cos(angle);
            ly2 = ly1 - (window.spectrawhorl_namespace.canvasSize / 2) * window.spectrawhorl_namespace.octaveWidth * Math.sin(angle);

            p.line(lx1, ly1, lx2, ly2);
        }

    }
    }

}


//console.log("Overlay variables initialized.")