// © 2024. All rights reserved.  DO NOT DUPLICATE OR REDISTRIBUTE.

// _decodeWorker.js
self.onmessage = function (e) {
    const base64String = e.data;
    const contentType = base64String.split(',')[0].split(':')[1].split(';')[0];
    const fileContent = base64String.split(',')[1];

    // Decode base64 content
    const byteCharacters = atob(fileContent);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);

    // Create a Blob from the byte array
    const blob = new Blob([byteArray], { type: contentType });
    const url = URL.createObjectURL(blob);

    // Send the blob URL back to the main thread
    self.postMessage({ url: url, contentType: contentType });
};
