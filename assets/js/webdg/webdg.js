
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};

/** The current sketch */
window.dash_clientside.differential_geometry.sketch = null;


/** For displaying the TNB frame of a curve */
window.dash_clientside.differential_geometry.TNB_data = null;
window.dash_clientside.differential_geometry.TNB_select = null;
window.dash_clientside.differential_geometry.TNB_anchor_slider = null;
window.dash_clientside.differential_geometry.TNB_speed_slider = null;
window.dash_clientside.differential_geometry.TNB_select_disabled = true;
window.dash_clientside.differential_geometry.animation_position = 0;

/** Contols controls (controls the controls) */
window.dash_clientside.differential_geometry.orbitControlled = true;
window.dash_clientside.differential_geometry.xVelocity = 0;
window.dash_clientside.differential_geometry.yVelocity = 0;
window.dash_clientside.differential_geometry.zVelocity = 0;


/** These variables are manipulated by clienside callbacks in the settings */
window.dash_clientside.differential_geometry.showAxis = true;
window.dash_clientside.differential_geometry.showFocalPoint = true;
window.dash_clientside.differential_geometry.movementSpeed = 1;
window.dash_clientside.differential_geometry.scaler = null;             // Initialized in Settings
window.dash_clientside.differential_geometry.strokeW = null;            // Initialized in Settings
window.dash_clientside.differential_geometry.showBackground = null;     // Initialized in Settings
window.dash_clientside.differential_geometry.backgroundColor = null;    // Initialized in Settings
window.dash_clientside.differential_geometry.surfaceShine = null;       // Initialized in Settings
window.dash_clientside.differential_geometry.ambient_light = null;      // Initialized in Settings
window.dash_clientside.differential_geometry.x_light = null;            // Initialized in Settings
window.dash_clientside.differential_geometry.y_light = null;            // Initialized in Settings
window.dash_clientside.differential_geometry.z_light = null;            // Initialized in Settings
window.dash_clientside.differential_geometry.neg_x_light = null;            // Initialized in Settings
window.dash_clientside.differential_geometry.neg_y_light = null;            // Initialized in Settings
window.dash_clientside.differential_geometry.neg_z_light = null;            // Initialized in Settings
window.dash_clientside.differential_geometry.rotate_toggle = null;      // Initialized in Settings
window.dash_clientside.differential_geometry.rotation_speed = null;     // Initialized in Settings
window.dash_clientside.differential_geometry.orbit_sensitivity = null;  // Initialized in Settings
window.dash_clientside.differential_geometry.fov = null;  // Initialized in Settings

/** Essential utility functions */

/** Used as a color processing utility */
window.dash_clientside.differential_geometry.hexToRGB = function(hex) {
    // Remove the hash (#) if it exists
    hex = hex.replace('#', '');
    return [parseInt(hex.substring(0, 2), 16), parseInt(hex.substring(2, 4), 16), parseInt(hex.substring(4, 6), 16)];
};

/** Safe setup is useful for setup needs for all sketches */
window.dash_clientside.differential_geometry.safe_setup = function (p) {

    // A little pointless for now, but useful as a stub
    // for future expansion
    p.createCanvas(window.innerWidth, window.innerHeight, p.WEBGL);

    p.setAttributes('antialias', true);

};

/** A wrapper function to show the background only if so set */
window.dash_clientside.differential_geometry.drawBackground = function(p) {
    if (this.showBackground) {
        p.background(this.backgroundColor);
    } else {
        p.clear(0, 0, 0, 0); // transparent background
    }
};

/** Draws the focal point */
window.dash_clientside.differential_geometry.drawFocalPoint = function(p) {
        // Draw a white dot at the focal point of the camera
        if (window.dash_clientside.differential_geometry.showFocalPoint) {
            //
            p.fill(255, 255, 255);
            p.noStroke();
            p.sphere(1); // Adjust size as needed
        }
        return "";
};

/** Draws the axes */
window.dash_clientside.differential_geometry.drawAxes = function(p) {
    const dg = window.dash_clientside.differential_geometry;
    if (!dg.showAxis) return;

    const x_max = 100, width = 1; 
    let x;



    p.noStroke();

    // Positive x
    p.push();
    // align with the x axis
    p.rotateZ(p.PI / 2);
    // offset to the edge of the marker rather than center
    p.translate(0, dg.scaler * (-0.5), 0);
    p.fill(255, 0, 0);
    for (x = 0; x < x_max; x += 2) {
        p.cylinder(width, dg.scaler, 6, 1);
        p.translate(0, -dg.scaler * 2, 0);
    }
    p.pop();

    // Negative x
    p.push();
    // align with the -x axis
    p.rotateZ(-p.PI / 2);
    // offset to the edge of the marker rather than center
    p.translate(0, dg.scaler * (-0.5), 0);
    p.fill(0, 255, 255);
    for (x = 0; x < x_max; x += 2) {
        p.cylinder(width, dg.scaler, 6, 1);
        p.translate(0, -dg.scaler * 2, 0);
    }
    p.pop();

    // Positive y
    p.push();
    // align with the y axis
    p.rotateZ(p.PI);
    // offset to the edge of the marker rather than center
    p.translate(0, dg.scaler * (-0.5), 0);
    p.fill(0, 255, 0);
    for (x = 0; x < x_max; x += 2) {
        p.cylinder(width, dg.scaler, 6, 1);
        p.translate(0, -dg.scaler * 2, 0);
    }
    p.pop();

    // Negative y
    p.push();
    // aligned with the y axis
    // offset to the edge of the marker rather than center
    p.translate(0, dg.scaler * (-0.5), 0);
    p.fill(255, 0, 255);
    for (x = 0; x < x_max; x += 2) {
        p.cylinder(width, dg.scaler, 6, 1);
        p.translate(0, -dg.scaler * 2, 0);
    }
    p.pop();

    // Positive z
    p.push();
    // align with the z axis
    p.rotateX(-p.PI / 2);
    // offset to the edge of the marker rather than center
    p.translate(0, dg.scaler * (-0.5), 0);
    p.fill(0, 0, 255);
    for (x = 0; x < x_max; x += 2) {
        p.cylinder(width, dg.scaler, 6, 1);
        p.translate(0, -dg.scaler * 2, 0);
    }
    p.pop();

    // Negative z
    p.push();
    // align with the z axis
    p.rotateX(p.PI / 2);
    // offset to the edge of the marker rather than center
    p.translate(0, dg.scaler * (-0.5), 0);
    p.fill(255, 255, 0);
    for (x = 0; x < x_max; x += 2) {
        p.cylinder(width, dg.scaler, 6, 1);
        p.translate(0, -dg.scaler * 2, 0);
    }
    p.pop();

};

/** Scene lighting */
window.dash_clientside.differential_geometry.sceneLighting = function(p, dg) {

    p.ambientLight(dg.ambient_light[0], dg.ambient_light[1], dg.ambient_light[2]); // Ambient light with moderate intensity

    if (dg.rotate_toggle) {
        let angle = p.frameCount * dg.rotation_speed;
        let cosA = Math.cos(angle);
        let sinA = Math.sin(angle);
        
        // Rotate around Y-axis: [x, z] → [x * cosA - z * sinA, x * sinA + z * cosA]
        function rotateY([x, y, z]) {
          return [
            x * cosA - z * sinA,
            y,
            x * sinA + z * cosA
          ];
        }
        
        // Apply to each light direction
        let dirs = {
          x: rotateY([-1, 0, 0]),
          y: rotateY([0, -1, 0]),
          z: rotateY([0, 0, -1]),
          neg_x: rotateY([1, 0, 0]),
          neg_y: rotateY([0, 1, 0]),
          neg_z: rotateY([0, 0, 1]),
        };
        
        // Then apply directional lights using the rotated directions
        p.directionalLight(...dg.x_light, ...dirs.x);
        p.directionalLight(...dg.y_light, ...dirs.y);
        p.directionalLight(...dg.z_light, ...dirs.z);             
    } else {
        p.directionalLight(dg.x_light[0], dg.x_light[1], dg.x_light[2], -1, 0, 0);
        p.directionalLight(dg.y_light[0], dg.y_light[1], dg.y_light[2], 0, -1, 0);
        p.directionalLight(dg.z_light[0], dg.z_light[1], dg.z_light[2], 0, 0, -1);
    }

    p.shininess(dg.surfaceShine);       // Make highlights pop

    p.specularMaterial(255);

    return "";
};

window.dash_clientside.differential_geometry.movement = function(p, cam) {

    const acc = window.dash_clientside.differential_geometry.movementSpeed * 0.001;

    if (window.dash_clientside.differential_geometry.orbitControlled) {
        if (p.keyIsDown(p.LEFT_ARROW) === true) {
            window.dash_clientside.differential_geometry.xVelocity -= acc;
        }
    
        if (p.keyIsDown(p.RIGHT_ARROW) === true) {
            window.dash_clientside.differential_geometry.xVelocity += acc;
        }
    
        if (p.keyIsDown(p.UP_ARROW) === true) {

            if (p.keyIsDown(p.SHIFT)) {
                window.dash_clientside.differential_geometry.zVelocity -= acc;
            } else {
                window.dash_clientside.differential_geometry.yVelocity -= acc;
            }
            
        }
    
        if (p.keyIsDown(p.DOWN_ARROW) === true) {

            if (p.keyIsDown(p.SHIFT)) {
                window.dash_clientside.differential_geometry.zVelocity += acc;
            } else {
                window.dash_clientside.differential_geometry.yVelocity += acc;
            }

        }

        //const decay = 0.001; //1 / (101 - window.dash_clientside.differential_geometry.movementSpeed);

        cam.move(window.dash_clientside.differential_geometry.xVelocity, 0, 0);
        //window.dash_clientside.differential_geometry.xVelocity *= decay;

        cam.move(0, window.dash_clientside.differential_geometry.yVelocity, 0);
        //window.dash_clientside.differential_geometry.yVelocity *= decay;

        cam.move(0, 0, window.dash_clientside.differential_geometry.zVelocity);
        //window.dash_clientside.differential_geometry.zVelocity *= decay;

    }
};

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
