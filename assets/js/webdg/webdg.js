
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};

/** The current sketch */
window.dash_clientside.differential_geometry.sketch = null;

/** These variables are manipulated by clienside callbacks in the settings */

window.dash_clientside.differential_geometry.showAxis = true;
window.dash_clientside.differential_geometry.showFocalPoint = true;
window.dash_clientside.differential_geometry.movementSpeed = 1;
window.dash_clientside.differential_geometry.TNB_data = null;
window.dash_clientside.differential_geometry.TNB_select = null;
window.dash_clientside.differential_geometry.TNB_anchor_slider = null;
window.dash_clientside.differential_geometry.TNB_speed_slider = null;
window.dash_clientside.differential_geometry.TNB_select_disabled = true;
window.dash_clientside.differential_geometry.scaler = 100;
window.dash_clientside.differential_geometry.strokeW = 4;
window.dash_clientside.differential_geometry.animation_position = 0;
window.dash_clientside.differential_geometry.showBackground = true;
window.dash_clientside.differential_geometry.backgroundColor = "#2e2e2e"; // "middle gray" https://en.wikipedia.org/wiki/Middle_gray
window.dash_clientside.differential_geometry.orbitControlled = true;
window.dash_clientside.differential_geometry.surfaceShine = 10;
window.dash_clientside.differential_geometry.ambient_light = [100, 100, 100];
window.dash_clientside.differential_geometry.x_light = [255, 0, 0];
window.dash_clientside.differential_geometry.y_light = [0, 255, 0];
window.dash_clientside.differential_geometry.z_light = [0, 0, 255];
window.dash_clientside.differential_geometry.rotate_toggle = false;
window.dash_clientside.differential_geometry.rotation_speed = 5;
window.dash_clientside.differential_geometry.orbit_sensitivity = 1;

/** Essential utility functions */

/** Used as a color processing utility */
window.dash_clientside.differential_geometry.hexToRGB = function(hex) {
    // Remove the hash (#) if it exists
    hex = hex.replace('#', '');

    // Parse the RGB values from the hex string
    let r = parseInt(hex.substring(0, 2), 16);
    let g = parseInt(hex.substring(2, 4), 16);
    let b = parseInt(hex.substring(4, 6), 16);

    return [r, g, b];
};

/** Safe setup is useful for setup needs for all sketches */
window.dash_clientside.differential_geometry.safe_setup = function (p) {

    // A little pointless for now, but useful as a stub
    // for future expansion
    p.createCanvas(window.innerWidth, window.innerHeight, p.WEBGL);

};

/** A wrapper function to show the background only if so set */
window.dash_clientside.differential_geometry.drawBackground = function(p) {
    if (this.showBackground) {
        p.background(this.backgroundColor);
    } else {
        p.clear(0, 0, 0, 0); // transparent background
    }
};

/** Draw axes only if so set */
window.dash_clientside.differential_geometry.drawAxes = function(p) {
}

/** Parses what should ostensibly be a constant (includes e, pi) */
window.dash_clientside.differential_geometry.parse_constant = function(pre, value) {
    if (!value) {
        return ["Please enter a valid value in the input form to parse.", 0];
    }

    try {

        value = String(value);

        // Ensure math.js is loaded
        if (typeof math === 'undefined') {
            throw new Error("math.js is not loaded");
        }

        let parsed = math.parse(value);
        let evaluated = parsed.evaluate({ pi: Math.PI, e: Math.E });

        // Ensure the result is a finite number
        if (!isFinite(evaluated)) {
            throw new Error("Expression must evaluate to a finite constant.");
        }

        // Format as LaTeX
        return ["$$" + pre + " " + parsed.toTex() + "$$", evaluated];

    } catch (e) {
        
        return ["Input could not be parsed. Please try again.", 0];
    }
};

/** Safely parses mathematical expressions of specified variables */
window.dash_clientside.differential_geometry.parse_math= function(pre, value, accepted_variables) {
    if (!value) {
        return "No value in form input to parse.";
    }
    
    try {
        // Ensure math.js is loaded
        if (typeof math === 'undefined') {
            throw new Error("math.js is not loaded");
        }

        let parsed = math.parse(value);

        // Extract variables from the parsed expression
        let variables = new Set();
        parsed.traverse(function (node) {
            if (node.isSymbolNode) {
                // Only add if the node is not a built-in function
                if (!math[node.name]) {
                    variables.add(node.name);
                }
            }
        });

        // Check if all variables are in the accepted list
        for (let variable of variables) {
            if (!accepted_variables.includes(variable)) {
                return `Invalid variable detected: '${variable}'. Only allowed variables are: ${accepted_variables.join(", ")}.`;
            }
        }

        // Convert to LaTeX
        return "$$" + pre + parsed.toTex() + "$$";
        
    } catch (e) {
        return "Input could not be parsed. Please try again.";
    }
};

/** makes the appropriate render outcome alert appear */
window.dash_clientside.differential_geometry.render_result_alert = function(success, error = "Unspecified error.") {

    // Close rendering alert by setting to 'display: none'
    rendering_alert = document.getElementById('rendering_alert');
    
    if (rendering_alert) {
        rendering_alert.style.display = 'none';
    }
    
    // success or failure
    if (success) {
        
        // Success alert
        const success_alert = document.getElementById('success_alert');
        if (success_alert) { // i.e. if it has not yet been dismissed
            success_alert.style.display = 'block';
        }
        
        
    } else {

        // Failure alert
        const failure_alert = document.getElementById('failure_alert');
        const failure_alert_inner = document.getElementById('failure_alert_inner');
        if (failure_alert) {
            failure_alert.style.display = 'block';
            failure_alert_inner.innerText = error;
            setTimeout(function() {
                failure_alert.style.display = 'none';
            }, 10000); // 5000 ms = 5 second timeout for failure
        }
        
        
    }
};

/** This function is burning to find you 
 * https://open.spotify.com/track/6zKF4293k44ItKWJJgrhXv?si=94490fae15e94719
 * (and any instance of a p5.js sketch from webdg and kills it if the
 * user has navigated away from the webdg page) */
window.dash_clientside.differential_geometry.killswitch_engage = function(path) {
    //console.log("Killswitch engaged.", path);
    document.querySelectorAll('.p5Canvas').forEach(el => el.remove());
};
