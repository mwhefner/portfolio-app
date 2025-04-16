window.spectrawhorl_namespace = window.spectrawhorl_namespace || {};

/** spectrawhorl sound variables w/ defaults */
window.spectrawhorl_namespace.soundInitialized = false;
window.spectrawhorl_namespace.inputSource = "SAMPLE"; // "MICROPHONE", "SAMPLE", "UPLOAD", OR "GENERATOR"
window.spectrawhorl_namespace.currentSource = "soundfile"; // 'generator' 'mic' 'hold' or 'soundfile'
window.spectrawhorl_namespace.volume = 0.5; // 0-1
window.spectrawhorl_namespace.sampleMusic = "COSTE"; // "COSTE", "SCHUBERT", OR "BACH"
window.spectrawhorl_namespace.mediaPlayer = "STOP"; // "PLAY", "PAUSE", "STOP"
window.spectrawhorl_namespace.playRate = 1; // -4x - 4x
window.spectrawhorl_namespace.mic = null;
window.spectrawhorl_namespace.previousUploadFileContentData = "DEFAULT SUCCESS.";
window.spectrawhorl_namespace.uploadFileContentData = "DEFAULT SUCCESS.";
window.spectrawhorl_namespace.uploadFileName = "DEFAULT FILE NAME";
window.spectrawhorl_namespace.fileIsSuccessfullyUploaded = false;
window.spectrawhorl_namespace.soundFile = null; //  The actual sound file
window.spectrawhorl_namespace.soundFiles = []; //  The array of actual sound files
window.spectrawhorl_namespace.soundFileIndex = 0; // The index of said file in said array
window.spectrawhorl_namespace.recorder = null;
window.spectrawhorl_namespace.recordedSoundFile = null; 
window.spectrawhorl_namespace.recording = false; // a p5.SoundFile 
window.spectrawhorl_namespace.bassFilter = null; // p5 EQ filters
window.spectrawhorl_namespace.midFilter = null;
window.spectrawhorl_namespace.highFilter = null;
window.spectrawhorl_namespace.bassGain = 0;
window.spectrawhorl_namespace.middleGain = 0;
window.spectrawhorl_namespace.trebleGain = 0;
window.spectrawhorl_namespace.reverbTime = 0;
window.spectrawhorl_namespace.reverbDecay = 2;
window.spectrawhorl_namespace.fft = null;
window.spectrawhorl_namespace.timeSmoothing = 0;
window.spectrawhorl_namespace.fftSize = 32768 / 4;
window.spectrawhorl_namespace.reference_freq = 440;
window.spectrawhorl_namespace.cSubNeg1 = window.spectrawhorl_namespace.reference_freq * Math.pow(2, -69 / 12.0);

/** Freq  --> Note utility */
window.spectrawhorl_namespace.freqToNote = function (freq) {
    return 12 * (Math.log(freq / window.spectrawhorl_namespace.cSubNeg1) / Math.log(2));
};

/** Note --> Freq utility */
window.spectrawhorl_namespace.noteToFreq = function (freq) {
    return window.spectrawhorl_namespace.cSubNeg1 * Math.pow(2, freq / 12);
};

/** Initializes the FFT */
window.spectrawhorl_namespace.initFFT = function(input) {
    // Initialize FFT
    window.spectrawhorl_namespace.fft = new p5.FFT(window.spectrawhorl_namespace.timeSmoothing, window.spectrawhorl_namespace.fftSize);

    if (input) {
        window.spectrawhorl_namespace.fft.setInput(input);
    }
}

/** Stops all sources */
window.spectrawhorl_namespace.stopAllSources = function() {
    window.spectrawhorl_namespace.mic.stop();
    window.spectrawhorl_namespace.soundFiles.forEach((soundFile) => window.spectrawhorl_namespace.soundFile.stop());

    window.spectrawhorl_namespace.stopGenerator();
    window.spectrawhorl_namespace.stopSequence();
}

/** Switches to the generator */
window.spectrawhorl_namespace.switchToGenerator = function() {
    if (window.spectrawhorl_namespace.currentSource !== "generator") {
        window.spectrawhorl_namespace.stopAllSources();
        window.spectrawhorl_namespace.startGenerator();
        window.spectrawhorl_namespace.initFFT();
        window.spectrawhorl_namespace.currentSource = "generator";
        window.spectrawhorl_namespace.REINIT_SPECTROGRAM = true;
    }
}

/** Switch input to the microphone */
window.spectrawhorl_namespace.switchToMic = function() {
    if (window.spectrawhorl_namespace.currentSource !== "mic") {
        window.spectrawhorl_namespace.stopAllSources();
        window.spectrawhorl_namespace.mic.start();
        window.spectrawhorl_namespace.mic.disconnect();
        window.spectrawhorl_namespace.mic.connect(window.spectrawhorl_namespace.bassFilter);
        window.spectrawhorl_namespace.bassFilter.chain(window.spectrawhorl_namespace.midFilter, window.spectrawhorl_namespace.highFilter);
        window.spectrawhorl_namespace.initFFT(window.spectrawhorl_namespace.highFilter);
        window.spectrawhorl_namespace.currentSource = "mic";
        window.spectrawhorl_namespace.REINIT_SPECTROGRAM = true;
    }
}

/** Upload a sound file */
window.spectrawhorl_namespace.addSoundFile = function() {

    let p = window.spectrawhorl_namespace.sketch;

    // Create a web worker to decode the file
    worker = new Worker('assets/js/spectrawhorl/decodeWorker.js');

    return new Promise((resolve, reject) => {
        // Define the worker message handler
        worker.onmessage = function (e) {
            const { url } = e.data;

            // Load the sound file using p5.js into soundFiles' 4th index
            window.spectrawhorl_namespace.soundFile = p.loadSound(url, function () {
                //console.log('Sound file loaded');
                window.spectrawhorl_namespace.soundFiles[3] = window.spectrawhorl_namespace.soundFile;
                window.spectrawhorl_namespace.fileIsSuccessfullyUploaded = true;
                resolve(); // Resolve the promise when the sound file is successfully loaded
            }, function (err) {
                console.error('Failed to load sound file:', err);
                window.spectrawhorl_namespace.fileIsSuccessfullyUploaded = false;
                reject(); // Reject the promise if there's an error loading the sound file
            });
        };

        // Post the base64 string to the worker
        worker.postMessage(window.spectrawhorl_namespace.uploadFileContentData);
    });
}

/** Switch to a specified sound file index */
window.spectrawhorl_namespace.switchToSoundFile = function(index) {
    window.spectrawhorl_namespace.stopAllSources();
    window.spectrawhorl_namespace.soundFileIndex = index;
    window.spectrawhorl_namespace.soundFile = window.spectrawhorl_namespace.soundFiles[window.spectrawhorl_namespace.soundFileIndex];
    window.spectrawhorl_namespace.soundFile.disconnect();
    window.spectrawhorl_namespace.soundFile.connect(window.spectrawhorl_namespace.bassFilter);
    window.spectrawhorl_namespace.bassFilter.chain(window.spectrawhorl_namespace.midFilter, window.spectrawhorl_namespace.highFilter);
    window.spectrawhorl_namespace.initFFT();
    window.spectrawhorl_namespace.currentSource = "soundfile";
    window.spectrawhorl_namespace.REINIT_SPECTROGRAM = true;
}

/** Switch to the uploaded file as the input source */
window.spectrawhorl_namespace.switchToUploadedFile = function() {
    //console.log("This is me switching to the uploaded file, specifically index 3.");
    if (window.spectrawhorl_namespace.fileIsSuccessfullyUploaded) {
        window.spectrawhorl_namespace.switchToSoundFile(3);
    } else {
        //console.log("A problem was indicated with the file upload. This may be normal. Putting current source on hold.");
        window.spectrawhorl_namespace.stopAllSources();
        window.spectrawhorl_namespace.currentSource = "hold";
    }
}

/** Switched to upload as source only once a file is uploaded */
window.spectrawhorl_namespace.checkAndSwitchToUploadedFile = function() {
    // Check if the file is successfully uploaded and switch to it if so
    if (window.spectrawhorl_namespace.fileIsSuccessfullyUploaded) {
        window.spectrawhorl_namespace.switchToUploadedFile();
        document.getElementById("spectrawhorl-uploadIndicator").innerText = '"' + window.spectrawhorl_namespace.uploadFileName + '"' + " processing complete.";
    } else {
        // Retry after a short delay
        setTimeout(window.spectrawhorl_namespace.checkAndSwitchToUploadedFile, 500);
    }
}

window.spectrawhorl_namespace.initSound = function (p) {
    
    // Initialize mic
    window.spectrawhorl_namespace.mic = new p5.AudioIn();

    // Init the recorder for recording
    window.spectrawhorl_namespace.recorder = new p5.SoundRecorder();
    window.spectrawhorl_namespace.recorder.setInput();

    // Init the soundfile used for recording / downloading
    window.spectrawhorl_namespace.recordedSoundFile = new p5.SoundFile();

    window.spectrawhorl_namespace.bassFilter = new p5.Filter("lowshelf");
    window.spectrawhorl_namespace.midFilter = new p5.Filter("peaking");
    window.spectrawhorl_namespace.highFilter = new p5.Filter("highshelf");

    window.spectrawhorl_namespace.reverbEffect = new p5.Reverb();

    // Connect EQ filters
    window.spectrawhorl_namespace.bassFilter.freq(200);
    window.spectrawhorl_namespace.bassFilter.gain(window.spectrawhorl_namespace.bassGain);
    window.spectrawhorl_namespace.midFilter.freq(1000);
    window.spectrawhorl_namespace.midFilter.gain(window.spectrawhorl_namespace.middleGain);
    window.spectrawhorl_namespace.highFilter.freq(5000);
    window.spectrawhorl_namespace.highFilter.gain(window.spectrawhorl_namespace.trebleGain);

    // Default audio file is the first
    window.spectrawhorl_namespace.soundFileIndex = 0;
    window.spectrawhorl_namespace.soundFile = window.spectrawhorl_namespace.soundFiles[window.spectrawhorl_namespace.soundFileIndex];
    window.spectrawhorl_namespace.soundFile.disconnect();
    window.spectrawhorl_namespace.soundFile.connect(window.spectrawhorl_namespace.bassFilter);
    window.spectrawhorl_namespace.bassFilter.chain(window.spectrawhorl_namespace.midFilter, window.spectrawhorl_namespace.highFilter);

    window.spectrawhorl_namespace.initFFT();

    window.spectrawhorl_namespace.soundInitialized = true;

    //console.log("Sound initialized with the following audio context:", p.getAudioContext());
};

