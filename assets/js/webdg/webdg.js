
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = {

// These variables are manipulated back clienside callbacks in the settings
showAxis : true,
showFocalPoint : true,
movementSpeed : 1,

TNB_data : null,
TNB_select : null,
TNB_anchor_slider : null,
TNB_speed_slider : null,
TNB_select_disabled : true,

scaler : 100,
strokeW : 4,

animation_position : 0,

showBackground : true,
backgroundColor : "#2e2e2e", // "middle gray" https://en.wikipedia.org/wiki/Middle_gray

orbitControlled : true,

surfaceShine : 10,
ambient_light : [100, 100, 100],
x_light : [255, 0, 0],
y_light : [0, 255, 0],
z_light : [0, 0, 255],

rotate_toggle : false,
rotation_speed : 5,
orbit_sensitivity : 1,

// Used as a color processing utility
hexToRGB : function(hex) {
    // Remove the hash (#) if it exists
    hex = hex.replace('#', '');

    // Parse the RGB values from the hex string
    let r = parseInt(hex.substring(0, 2), 16);
    let g = parseInt(hex.substring(2, 4), 16);
    let b = parseInt(hex.substring(4, 6), 16);

    return [r, g, b];
},

// Get the TNB frame at a given index
getDataAtIndex : function(index, TNB_data) {
    return {
        position: TNB_data.position[index],
        Tangent: TNB_data.Tangent[index],
        Normal: TNB_data.Normal[index],
        Binormal: TNB_data.Binormal[index],
        curvature: TNB_data.curvature[index],
        torsion: TNB_data.torsion[index],
        speed: TNB_data.speed[index]
    };
},

// Get the TNB frame at a given t value
getDataAtT : function(t, TNB_data) {

    let index = TNB_data.t_values.findIndex(val => Math.abs(val - t) < 1e-6);
    if (index === -1) return null; // Return null if t is not found
    
    return this.getDataAtIndex(index, TNB_data);
},

// (3) Plot T, N, and B vectors at a given t value using p5.js
plotTNB : function(t, TNB_data, p, index = null) {

    let data = this.getDataAtT(t, TNB_data);

    if (index || index === 0) {
        data = this.getDataAtIndex(index, TNB_data);
    }

    if (!data) return;
    
    let pos = data.position;
    let T = data.Tangent;
    let N = data.Normal;
    let B = data.Binormal;

    p.strokeWeight(this.strokeW);
    
    p.push();
    p.translate(pos[0] * this.scaler, pos[1] * this.scaler, pos[2] * this.scaler);
    
    // Draw Tangent vector (YELLOW)
    p.stroke(255, 255, 0);
    p.line(0, 0, 0, T[0] * this.scaler, T[1] * this.scaler, T[2] * this.scaler);
    
    // Draw Normal vector (CYAN)
    p.stroke(0, 255, 255);
    p.line(0, 0, 0, N[0] * this.scaler, N[1] * this.scaler, N[2] * this.scaler);
    
    // Draw Binormal vector (MAGENTA)
    p.stroke(255, 0, 255);
    p.line(0, 0, 0, B[0] * this.scaler, B[1] * this.scaler, B[2] * this.scaler);
    
    p.pop();
},

// A wrapper function to show the background only if so set
drawBackground : function(p) {
    if (this.showBackground) {
        p.background(this.backgroundColor);
    } else {
        p.clear(0, 0, 0, 0); // transparent background
    }
},

// Parses what should ostensibly be a constant (includes e, pi)
// e.g. param bounds
parse_constant: function(pre, value) {
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
},

// safely parses mathematical expressions of specified variables
parse_math: function(pre, value, accepted_variables) {
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
},

// Safe setup is useful for setup needs for all sketches
safe_setup : function (p) {

    // A little pointless for now, but useful as a stub
    // for future expansion
    p.createCanvas(window.innerWidth, window.innerHeight, p.WEBGL);

},

// The function ran when the refresh button is pressed.
// This creates a p5.js sketch of a viewer inside a sphere
// as a red, green, and blue light wander in brownian
// motion around the sphere with one constant white light
// in the user's focus. "I just think they're neat"
refresh : function () {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let landing_sketch = function (p) {

        let t = 0; // Global time variable for noise

        let radius = 500; // Fixed radius for the light positions
        
        // Brownian motion variables for the light rotation angles
        let phiRed = 0, thetaRed = 0;
        let phiGreen = Math.PI / 2, thetaGreen = Math.PI / 2; // Different initial positions
        let phiBlue = Math.PI, thetaBlue = Math.PI / 2;
        
        let vel_phiRed = 0, vel_thetaRed = 0;
        let vel_phiGreen = 0, vel_thetaGreen = 0;
        let vel_phiBlue = 0, vel_thetaBlue = 0;
        
        let maxSpeed = 0.01; // Max speed for the rotation of the lights

        p.setup = function () {

            //console.log("Setting up landing page sketch.");
            
            // Run the safe setup function
            dg.safe_setup(p);

            p.setAttributes('antialias', true);

        };

        p.draw = function() {

            p.clear(0, 0, 0, 0);
    
            t += 0.001; // Increment time for noise evolution
    
            // Use noise for smooth Brownian-like motion for light rotation (phi and theta)
            let acc_phiRed = p.map(p.noise(t, 0), 0, 1, -0.0001, 0.0001);
            let acc_thetaRed = p.map(p.noise(t, 1), 0, 1, -0.0001, 0.0001);
    
            let acc_phiGreen = p.map(p.noise(t, 2), 0, 1, -0.0001, 0.0001);
            let acc_thetaGreen = p.map(p.noise(t, 3), 0, 1, -0.0001, 0.0001);
    
            let acc_phiBlue = p.map(p.noise(t, 4), 0, 1, -0.0001, 0.0001);
            let acc_thetaBlue = p.map(p.noise(t, 5), 0, 1, -0.0001, 0.0001);
    
            // Update velocities for light rotation angles
            vel_phiRed = p.constrain(vel_phiRed + acc_phiRed, -maxSpeed, maxSpeed);
            vel_thetaRed = p.constrain(vel_thetaRed + acc_thetaRed, -maxSpeed, maxSpeed);
    
            vel_phiGreen = p.constrain(vel_phiGreen + acc_phiGreen, -maxSpeed, maxSpeed);
            vel_thetaGreen = p.constrain(vel_thetaGreen + acc_thetaGreen, -maxSpeed, maxSpeed);
    
            vel_phiBlue = p.constrain(vel_phiBlue + acc_phiBlue, -maxSpeed, maxSpeed);
            vel_thetaBlue = p.constrain(vel_thetaBlue + acc_thetaBlue, -maxSpeed, maxSpeed);
    
            // Apply velocity to the angles
            phiRed += vel_phiRed;
            thetaRed += vel_thetaRed;
    
            phiGreen += vel_phiGreen;
            thetaGreen += vel_thetaGreen;
    
            phiBlue += vel_phiBlue;
            thetaBlue += vel_thetaBlue;
    
            // Apply base lighting
            p.lights(); // base lighting (looks cooler with)
    
            // Calculate the positions of the lights using spherical coordinates
            let xRed = radius * p.sin(thetaRed) * p.cos(phiRed);
            let yRed = radius * p.sin(thetaRed) * p.sin(phiRed);
            let zRed = radius * p.cos(thetaRed);
            
            let xGreen = radius * p.sin(thetaGreen) * p.cos(phiGreen);
            let yGreen = radius * p.sin(thetaGreen) * p.sin(phiGreen);
            let zGreen = radius * p.cos(thetaGreen);
            
            let xBlue = radius * p.sin(thetaBlue) * p.cos(phiBlue);
            let yBlue = radius * p.sin(thetaBlue) * p.sin(phiBlue);
            let zBlue = radius * p.cos(thetaBlue);
    
            // Apply the rotating directional lights
            p.directionalLight(255, 0, 0, xRed, yRed, zRed);  // Red light
            p.directionalLight(0, 255, 0, xGreen, yGreen, zGreen); // Green light
            p.directionalLight(0, 0, 255, xBlue, yBlue, zBlue);  // Blue light
    
            p.ambientMaterial(255); // Ensure the model reacts to lighting
            p.shininess(10);       // Make highlights pop
            p.specularMaterial(255);
    
            // Draw a white sphere at the origin
            p.fill(255); // White color for the sphere
            p.noStroke(); // No stroke for the sphere
            p.sphere(800, 100, 100); // The sphere size can be adjusted as needed

        };


    }

    if (typeof WebDG_Sketch !== "undefined") {
        WebDG_Sketch.remove(); // This properly disposes of the old instance
        //console.log("Existing WebDG instance destroyed. cya");
    }

    //console.log("A new WebDG instance is being created.");

    WebDG_Sketch = new p5(landing_sketch);

    return "Completed sketch setup.";

}, // This ends the refresh function

// The function ran to build a sketch around a curve
curve_sketch : function (curveData) {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let cam;

    let sketch_function = function (p) {


    p.setup = function () {
        // //console.log("Setting up the subject sketch of:", curveData);
            
        // Run the safe setup function
        dg.safe_setup(p);

        p.setAttributes('antialias', true);

        cam = p.createCamera();

        // Place the camera at the top-right.
        cam.setPosition(400, -400, 800);
      
        // Point it at the origin.
        cam.lookAt(0, 0, 0);

        document.addEventListener('wheel', function(event) {
            //console.log(event);
            if (event.ctrlKey && event.deltaY !== 0) {
              event.preventDefault();
            }
          }, { passive: false });

    };
    
    p.draw = function () {

        if (p.frameCount === 1 && curveData) {
            dg.render_result_alert(true);
        } else if (!curveData) {
            dg.render_result_alert(false);
        }

        dg.drawBackground(p);

        // Draw the XYZ axes
        if (dg.showAxis) {
            p.strokeWeight(1);
            p.stroke(128);
            p.debugMode(dg.scaler * 100, 100, 0, 0, 0);
        } else {
            p.noDebugMode();
        }


        
        // Orbit control to allow mouse interaction
        // Only allow orbit control when no modal is open
        if (dg.orbitControlled) {
            p.orbitControl(dg.orbit_sensitivity, dg.orbit_sensitivity, dg.orbit_sensitivity);
        }

        // Draw a gray dot at the focal point of the camera
        if (dg.showFocalPoint) {
            p.push();
            p.translate(cam.centerX, cam.centerY, cam.centerZ);
            p.fill(255, 255, 255);
            p.noStroke();
            p.sphere(3); // Adjust size as needed
            p.pop();
        }


        // account for y pointing down at the start
        p.rotateX(p.PI);
    
        if (dg.rotate_toggle) {
            p.rotateY(p.frameCount * dg.rotation_speed);
        }

        // Draw text at the origin
        p.push(); // Save the current transformation matrix

        if (!dg.TNB_select_disabled && dg.TNB_select === "anchor") {
            dg.plotTNB(dg.TNB_anchor_slider, dg.TNB_data, p);
        } else if (!dg.TNB_select_disabled && dg.TNB_select === "animated") {

            if (dg.animation_position >= dg.TNB_data.position.length) {
                dg.animation_position = 0;
            }

            dg.plotTNB(dg.TNB_anchor_slider, dg.TNB_data, p, dg.animation_position);

            if (p.frameCount % (11 - dg.TNB_speed_slider) == 0) {
                dg.animation_position += 1;
            }
            
        }

        p.strokeWeight(dg.strokeW);
        p.noFill();



        p.beginShape();
        for (let i = 0; i < curveData.vertices.length; i++) {
            let v = curveData.vertices[i];
            let c = curveData.colors[i];
            p.stroke(c[0], c[1], c[2]);
            p.vertex(v[0] * dg.scaler, v[1] * dg.scaler, v[2] * dg.scaler);
        }
        p.endShape(p.OPEN);
        
        p.pop(); // Restore the previous transformation matrix
        

        
        p.strokeWeight(1);

        if (dg.orbitControlled) {
            if (p.keyIsDown(p.LEFT_ARROW) === true) {
                cam.move(-dg.movementSpeed, 0, 0);
            }
        
            if (p.keyIsDown(p.RIGHT_ARROW) === true) {
                cam.move(dg.movementSpeed, 0, 0);
            }
        
            if (p.keyIsDown(p.UP_ARROW) === true) {
    
                if (p.keyIsDown(p.SHIFT)) {
                    cam.move(0, 0, -dg.movementSpeed);
                } else {
                    cam.move(0, -dg.movementSpeed, 0);
                }
                
            }
        
            if (p.keyIsDown(p.DOWN_ARROW) === true) {
    
                if (p.keyIsDown(p.SHIFT)) {
                    cam.move(0, 0, dg.movementSpeed);
                } else {
                    cam.move(0, dg.movementSpeed, 0);
                }
    
            }
        }

    };

    p.keyPressed = function () {

    };
    
    } // This ends the sketch function

    if (typeof WebDG_Sketch !== "undefined") {
        WebDG_Sketch.remove(); // This properly disposes of the old instance
        //console.log("Existing WebDG instance destroyed. cya");
    }

    //console.log("A new WebDG instance is being created.");

    WebDG_Sketch = new p5(sketch_function);

    return "Completed sketch setup.";

}, // This ends create_sketch

// The function ran to build a sketch around a surface
surface_sketch : function (obj_file, colorsJSON, s_nu_validated, s_nv_validated, colorby) {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let sketch_function = function (p) {

    //subject
    let subject;
    let cam;
    let graphicsBuffer;
    if (typeof colorsJSON === 'string') {
        try {
            vertexColors = JSON.parse(colorsJSON);  // Parse the string into an object
        } catch (e) {
            console.error('Error parsing colorsJSON:', e);
        }
    } else {
        vertexColors = colorsJSON;  // If it's already an object, use it as is
    }

    p.setup = function () {
        // //console.log("Setting up the subject sketch of:", obj_file);
    
        // Run the safe setup function
        dg.safe_setup(p);
    
        p.setAttributes('antialias', true);

        cam = p.createCamera();
    
        // Place the camera at the top-right.
        cam.setPosition(400, -400, 800);
      
        // Point it at the origin.
        cam.lookAt(0, 0, 0);

        subject = p.createModel(obj_file, '.obj');

        if (typeof obj_file !== "undefined") {
            //console.log("Getting rid of obj to clear up mem.");
            obj_file = null;
        }

        //console.log("I'm inside the setup of the p5js sketch and I have the colors right here man:", s_nu_validated, s_nv_validated);

        graphicsBuffer = p.createGraphics(s_nu_validated, s_nv_validated);

        // Load the pixels array to initialize it for manipulation
        graphicsBuffer.loadPixels();

        // Map colors to texture pixels graphics buffer
        for (let i = 0; i < vertexColors.length; i++) {

            let { u, v, r, g, b, u_index, v_index } = vertexColors[i];

            let index = (u_index - 1 + v_index * graphicsBuffer.width) * 4;

            graphicsBuffer.pixels[index] = r;
            graphicsBuffer.pixels[index + 1] = g;
            graphicsBuffer.pixels[index + 2] = b;
            graphicsBuffer.pixels[index + 3] = 255;  // Alpha

        }

        graphicsBuffer.updatePixels();

        document.addEventListener('wheel', function(event) {
            if (event.ctrlKey && event.deltaY !== 0) {
              event.preventDefault();
            }
          }, { passive: false });

    };
    
    p.draw = function () {

        if (p.frameCount === 1 && subject) {
            dg.render_result_alert(true);
        } else if (!subject) {
            dg.render_result_alert(false, "Either the GPU is out of memory or the subject generated a malformed 3D object that cannot be displayed.");
        }

        dg.drawBackground(p);

        // Draw the XYZ axes
        if (dg.showAxis) {
            p.strokeWeight(1);
            p.stroke(128);
            p.debugMode(dg.scaler * 100, 100, 0, 0, 0);
        } else {
            p.noDebugMode();
        }

        // Orbit control to allow mouse interaction
        // Only allow orbit control when no modal is open
        if (dg.orbitControlled) {
            p.orbitControl(dg.orbit_sensitivity, dg.orbit_sensitivity, dg.orbit_sensitivity);
        }

        // Draw a gray dot at the focal point of the camera
        if (dg.showFocalPoint) {
            p.push();
            p.translate(cam.centerX, cam.centerY, cam.centerZ);
            p.fill(255, 255, 255);
            p.noStroke();
            p.sphere(3); // Adjust size as needed
            p.pop();
        }


        //  LIGHTING AND COLOR BY
        if (colorby === "normal") {

            p.normalMaterial();
            //p.ambientLight(255);

        } else if (colorby === "lighting") {

            // scene lighting
            p.ambientLight(dg.ambient_light[0], dg.ambient_light[1], dg.ambient_light[2]); // Ambient light with moderate intensity


            p.directionalLight(dg.x_light[0], dg.x_light[1], dg.x_light[2], 1, 0, 0);
            p.directionalLight(dg.y_light[0], dg.y_light[1], dg.y_light[2], 0, 1, 0);
            p.directionalLight(dg.z_light[0], dg.z_light[1], dg.z_light[2], 0, 0, 1);

            p.shininess(dg.surfaceShine);       // Make highlights pop
            p.specularMaterial(255);

        } else {

            p.texture(graphicsBuffer);
            p.ambientLight(255);

        }

        p.push(); 

        p.rotateX(p.PI);
        
        p.strokeWeight(0);

        p.scale(dg.scaler);

        if (dg.rotate_toggle) {
            p.rotateY(p.frameCount * dg.rotation_speed);
        }

        p.model(subject);

        p.pop();

        p.strokeWeight(1);

        if (dg.orbitControlled) {
            if (p.keyIsDown(p.LEFT_ARROW) === true) {
                cam.move(-dg.movementSpeed, 0, 0);
            }
        
            if (p.keyIsDown(p.RIGHT_ARROW) === true) {
                cam.move(dg.movementSpeed, 0, 0);
            }
        
            if (p.keyIsDown(p.UP_ARROW) === true) {
    
                if (p.keyIsDown(p.SHIFT)) {
                    cam.move(0, 0, -dg.movementSpeed);
                } else {
                    cam.move(0, -dg.movementSpeed, 0);
                }
                
            }
        
            if (p.keyIsDown(p.DOWN_ARROW) === true) {
    
                if (p.keyIsDown(p.SHIFT)) {
                    cam.move(0, 0, dg.movementSpeed);
                } else {
                    cam.move(0, dg.movementSpeed, 0);
                }
    
            }
        }
    };
    
    } // This ends the sketch function

    if (typeof WebDG_Sketch !== "undefined") {
        WebDG_Sketch.remove(); // This properly disposes of the old instance
        //console.log("Existing WebDG instance destroyed. cya");
    }

    //console.log("A new WebDG instance is being created.");

    WebDG_Sketch = new p5(sketch_function);

    return "Completed sketch setup.";

}, // This ends create_sketch

// the function ran to build a sketch around a level surface
level_surface_sketch : function(obj_file, colorby) {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let sketch_function = function (p) {

    //subject
    let subject;
    let cam;

    p.setup = function () {
    
        // Run the safe setup function
        dg.safe_setup(p);
    
        p.setAttributes('antialias', true);

        cam = p.createCamera();
    
        // Place the camera at the top-right.
        cam.setPosition(400, -400, 800);
      
        // Point it at the origin.
        cam.lookAt(0, 0, 0);

        subject = p.createModel(obj_file, '.obj');

        if (typeof obj_file !== "undefined") {
            //console.log("Getting rid of obj to clear up mem.");
            obj_file = null;
        }

        document.addEventListener('wheel', function(event) {
            if (event.ctrlKey && event.deltaY !== 0) {
              event.preventDefault();
            }
          }, { passive: false });

    };
    
    p.draw = function () {

        if (p.frameCount === 1 && subject) {
            dg.render_result_alert(true);
        } else if (!subject) {
            dg.render_result_alert(false, "Either the GPU is out of memory or the subject generated a malformed 3D object that cannot be displayed.");
        }

        dg.drawBackground(p);

        // Draw the XYZ axes
        if (dg.showAxis) {
            p.strokeWeight(1);
            p.stroke(128);
            p.debugMode(dg.scaler * 100, 100, 0, 0, 0);
        } else {
            p.noDebugMode();
        }

        // Orbit control to allow mouse interaction
        // Only allow orbit control when no modal is open
        if (dg.orbitControlled) {
            p.orbitControl(dg.orbit_sensitivity, dg.orbit_sensitivity, dg.orbit_sensitivity);
        }

        // Draw a gray dot at the focal point of the camera
        if (dg.showFocalPoint) {
            p.push();
            p.translate(cam.centerX, cam.centerY, cam.centerZ);
            p.fill(255, 255, 255);
            p.noStroke();
            p.sphere(3); // Adjust size as needed
            p.pop();
        }


        //  LIGHTING AND COLOR BY
        if (colorby === "normal") {

            p.normalMaterial();
            //p.ambientLight(255);

        } else {

            // scene lighting
            p.ambientLight(dg.ambient_light[0], dg.ambient_light[1], dg.ambient_light[2]); // Ambient light with moderate intensity


            p.directionalLight(dg.x_light[0], dg.x_light[1], dg.x_light[2], 1, 0, 0);
            p.directionalLight(dg.y_light[0], dg.y_light[1], dg.y_light[2], 0, 1, 0);
            p.directionalLight(dg.z_light[0], dg.z_light[1], dg.z_light[2], 0, 0, 1);

            p.shininess(dg.surfaceShine);       // Make highlights pop
            p.specularMaterial(255);

        }

        p.push(); 

        p.rotateX(p.PI);

        if (dg.rotate_toggle) {
            p.rotateY(p.frameCount * dg.rotation_speed);
        }
        
        p.strokeWeight(0);

        p.scale(dg.scaler);

        p.model(subject);

        p.pop();

        p.strokeWeight(1);

        if (dg.orbitControlled) {
            if (p.keyIsDown(p.LEFT_ARROW) === true) {
                cam.move(-dg.movementSpeed, 0, 0);
            }
        
            if (p.keyIsDown(p.RIGHT_ARROW) === true) {
                cam.move(dg.movementSpeed, 0, 0);
            }
        
            if (p.keyIsDown(p.UP_ARROW) === true) {
    
                if (p.keyIsDown(p.SHIFT)) {
                    cam.move(0, 0, -dg.movementSpeed);
                } else {
                    cam.move(0, -dg.movementSpeed, 0);
                }
                
            }
        
            if (p.keyIsDown(p.DOWN_ARROW) === true) {
    
                if (p.keyIsDown(p.SHIFT)) {
                    cam.move(0, 0, dg.movementSpeed);
                } else {
                    cam.move(0, dg.movementSpeed, 0);
                }
    
            }
        }
    };
    
    } // This ends the sketch function

    if (typeof WebDG_Sketch !== "undefined") {
        WebDG_Sketch.remove(); // This properly disposes of the old instance
        //console.log("Existing WebDG instance destroyed. cya");
    }

    //console.log("A new WebDG instance is being created.");

    WebDG_Sketch = new p5(sketch_function);

    return "Completed sketch setup.";
},

// makes the appropriate render outcome alert appear
render_result_alert : function(success, error = "Unspecified error.") {

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
},

// Creates a web worker to process the subject
// then calls the sketch rendering function with the results
render_webdg : function(n_clicks, n_2, n_3, c_x_validated, c_y_validated,  c_z_validated, c_tstart_validated, c_tend_validated, c_nt_validated, c_colorby, c_colorpicker, s_x_validated, s_y_validated, s_z_validated, s_ustart_validated, s_uend_validated, s_nu_validated, s_vstart_validated, s_vend_validated, s_nv_validated, s_colorby, ls_f_validated, ls_xstart_validated, ls_xend_validated, ls_nx_validated, ls_ystart_validated, ls_yend_validated, ls_ny_validated, ls_zstart_validated, ls_zend_validated, ls_nz_validated, ls_colorby
    ) {

    // EASY TO MISS!! LOOK AT ME!!!
    // When new render buttons are added, be sure to include it here
    if (n_clicks > 0 || n_2 > 0 || n_3 > 0) {
        
        // Access Dash's callback context to find 
        // which button was clicked-----------------------------
        let ctx = window.dash_clientside.callback_context;
        
        if (!ctx) {
            return { display: 'none' };  // No input received, hide the alert
        }
        
        // Get the ID of the triggered component
        const triggered_id = ctx.triggered[0].prop_id.split('.')[0]; // Get the ID of the button
        
        
        
        // Refresh the WebDG engine while rendering ------------
        let dg = window.dash_clientside.differential_geometry;
        dg.refresh();



        // Initialize the Web Worker------------------------
        let worker = new Worker('/assets/js/webdg/webdg_renderer.js');
        
        // The necessary rendering information
        // from the dcc.Stores that contain the validated config
        
        let dataToSend = {

            from_webdg : true,
            
            subject: triggered_id,
            
            c_params: {
                
                x : c_x_validated,
                y : c_y_validated,
                z : c_z_validated,
                
                t_start : c_tstart_validated,
                t_end : c_tend_validated,
                nt : c_nt_validated,
                
                color_by : c_colorby,
                color_picker : c_colorpicker
                
                },
                
            s_params: {
                
                s_x_validated, 
                s_y_validated, 
                s_z_validated, 

                s_ustart_validated, 
                s_uend_validated, 
                s_nu_validated, 

                s_vstart_validated, 
                s_vend_validated, 
                s_nv_validated, 

                s_colorby
                
                },

            ls_params: {
            
                ls_f_validated,
                ls_xstart_validated,
                ls_xend_validated,
                ls_nx_validated,
                ls_ystart_validated,
                ls_yend_validated,
                ls_ny_validated,
                ls_zstart_validated,
                ls_zend_validated,
                ls_nz_validated,
                ls_colorby
                
                }
                
        };
        
        // Pass to the web worker
        worker.postMessage(dataToSend);
        
        // Open rendering alert by setting style to 'display: block'
        let rendering_alert = document.getElementById('rendering_alert');
        
        if (alert) {
            rendering_alert.style.display = 'block';
        }
        
        // Listen for the result from the worker
        worker.onmessage = function(e) {

            // success or failure
            if (e.data.success) {
                
                if (triggered_id === "render_curve") {
                    // Curves are rendered in real time since they're
                    // far less computationally intense and do not involve lighting
                    dg.curve_sketch(e.data.obj_file);    
                } else if (triggered_id === "render_surface") {
                    dg.surface_sketch(e.data.obj_file, e.data.colorJSON, s_nu_validated, s_nv_validated, s_colorby); 
                } else if (triggered_id === "render_level_surface") {
                    dg.level_surface_sketch(e.data.obj_file, ls_colorby); 
                } 
                
            } else {

                dg.render_result_alert(false, "A failure occurred in the subject rendering process: " +  e.data.error);
            }
            
            // End of worker message receipt action
            
        };

        // Open the rendering alert initially and 
        // populate the math_store so the analytics
        // callbacks can access the validated values
        
        var math_store_data = {
            rendered: true,
            subject: triggered_id,
            "c_x_validated": c_x_validated,
            "c_y_validated": c_y_validated,
            "c_z_validated": c_z_validated,
            "c_tstart_validated": c_tstart_validated,
            "c_tend_validated": c_tend_validated,
            "c_nt_validated": c_nt_validated,
            "c_colorby": c_colorby,
            "c_colorpicker": c_colorpicker,
            "s_x_validated" : s_x_validated, 
            "s_y_validated" : s_y_validated, 
            "s_z_validated" : s_z_validated, 
            "s_ustart_validated" : s_ustart_validated, 
            "s_uend_validated" : s_uend_validated, 
            "s_nu_validated" : s_nu_validated, 
            "s_vstart_validated" : s_vstart_validated, 
            "s_vend_validated" : s_vend_validated, 
            "s_nv_validated" : s_nv_validated, 
            "s_colorby" : s_colorby
        };

        //console.log("Updating store_math with: ", math_store_data);
        
        return [{ display: 'block'}, math_store_data];
    }
    
    // Default behavior: Hide the alert if no button is clicked
    return [{ display: 'none' }, {rendered: false}];
},

// Computes the analytics for curves
render_curve_analytics: function(curve_data) {

    //console.log("I've been asked to render analytics of: ", curve_data);

    // Get the math expressions
    const x_expr = math.parse(curve_data['c_x_validated']);
    const y_expr = math.parse(curve_data['c_y_validated']);
    const z_expr = math.parse(curve_data['c_z_validated']);

    // Convert expressions to LaTeX
    const x_latex = x_expr.toTex();
    const y_latex = y_expr.toTex();
    const z_latex = z_expr.toTex();

    // Compute derivatives
    const dx_dt = math.derivative(x_expr, 't');
    const dy_dt = math.derivative(y_expr, 't');
    const dz_dt = math.derivative(z_expr, 't');

    const d2x_dt2 = math.derivative(dx_dt, 't');
    const d2y_dt2 = math.derivative(dy_dt, 't');
    const d2z_dt2 = math.derivative(dz_dt, 't');

    const d3x_dt3 = math.derivative(d2x_dt2, 't');
    const d3y_dt3 = math.derivative(d2y_dt2, 't');
    const d3z_dt3 = math.derivative(d2z_dt2, 't');

    // Compute unit tangent vector (T)
    const speed_expr = math.simplify(`sqrt((${dx_dt})^2 + (${dy_dt})^2 + (${dz_dt})^2)`);
    const T_x = math.simplify(`(${dx_dt}) / (${speed_expr})`);
    const T_y = math.simplify(`(${dy_dt}) / (${speed_expr})`);
    const T_z = math.simplify(`(${dz_dt}) / (${speed_expr})`);

    // Compute derivative of T
    const dT_x = math.derivative(T_x, 't');
    const dT_y = math.derivative(T_y, 't');
    const dT_z = math.derivative(T_z, 't');

    // Compute unit normal vector (N)
    const normal_magnitude_expr = math.simplify(`sqrt((${dT_x})^2 + (${dT_y})^2 + (${dT_z})^2)`);
    const N_x = math.simplify(`(${dT_x}) / (${normal_magnitude_expr})`);
    const N_y = math.simplify(`(${dT_y}) / (${normal_magnitude_expr})`);
    const N_z = math.simplify(`(${dT_z}) / (${normal_magnitude_expr})`);

    // Compute binormal vector (B)
    const B_x = math.simplify(`((${T_y}) * (${N_z})) - ((${T_z}) * (${N_y}))`);
    const B_y = math.simplify(`((${T_z}) * (${N_x})) - ((${T_x}) * (${N_z}))`);
    const B_z = math.simplify(`((${T_x}) * (${N_y})) - ((${T_y}) * (${N_x}))`);

    // Compute Darboux vector 
    const curvature_expr = math.simplify(
        `norm(cross([(${dx_dt}), (${dy_dt}), (${dz_dt})], [(${d2x_dt2}), (${d2y_dt2}), (${d2z_dt2})])) / (norm([(${dx_dt}), (${dy_dt}), (${dz_dt})]) ^ 3)`
    );

    const torsion_expr = math.simplify(
        `dot(cross([(${dx_dt}), (${dy_dt}), (${dz_dt})], [(${d2x_dt2}), (${d2y_dt2}), (${d2z_dt2})]), [(${d3x_dt3}), (${d3y_dt3}), (${d3z_dt3})]) / (norm(cross([(${dx_dt}), (${dy_dt}), (${dz_dt})], [(${d2x_dt2}), (${d2y_dt2}), (${d2z_dt2})])) ^ 2)`
    );

    // Compute LaTeX representations
    const T_latex = `\\mathbf{T}(t) = \\left( ${T_x.toTex()}, ${T_y.toTex()}, ${T_z.toTex()} \\right)`;
    const N_latex = `\\mathbf{N}(t) = \\left( ${N_x.toTex()}, ${N_y.toTex()}, ${N_z.toTex()} \\right)`;
    const B_latex = `\\mathbf{B}(t) = \\left( ${B_x.toTex()}, ${B_y.toTex()}, ${B_z.toTex()} \\right)`;
    
    let speed_latex = speed_expr.toTex();
    let curvature_latex = curvature_expr.toTex();
    let torsion_latex = torsion_expr.toTex();

    if (speed_latex.includes("\\infty")) {
        speed_latex = "\\text{Not well defined. Will show zero on plot.}";
    } 

    if (curvature_latex.includes("\\infty")) {
        curvature_latex = "\\text{Not well defined. Will show zero on plot.}";
    } 
    
    if (torsion_latex.includes("\\infty")) {
        torsion_latex = "\\text{Not well defined. Will show zero on plot.}";
    } 

    // Evaluate the bounds
    const t_start = math.evaluate(curve_data["c_tstart_validated"]);
    const t_end = math.evaluate(curve_data["c_tend_validated"]);
    const n_steps = curve_data["c_nt_validated"];

    const t_step = (t_end - t_start) / (n_steps - 1);
    const t_values = math.range(t_start, t_end, t_step, true).toArray();

    // Compute speed, curvature, torsion, and vectors for each t
    let speed_values = [];
    let curvature_values = [];
    let torsion_values = [];
    let T_values = [], N_values = [], B_values = [], D_values = [];
    let positions = [];

    t_values.forEach(t => {
        let speed = speed_expr.evaluate({ t });
        let curv = curvature_expr.evaluate({ t });
        let tors = torsion_expr.evaluate({ t });

        let T_t = [T_x.evaluate({ t }), T_y.evaluate({ t }), T_z.evaluate({ t })];
        let N_t = [N_x.evaluate({ t }), N_y.evaluate({ t }), N_z.evaluate({ t })];
        let B_t = [B_x.evaluate({ t }), B_y.evaluate({ t }), B_z.evaluate({ t })];
        let position = [x_expr.evaluate({ t }), y_expr.evaluate({ t }), z_expr.evaluate({ t })];

        // Handle infinity values
        if (!isFinite(speed)) speed = 0;
        if (!isFinite(curv)) curv = 0;
        if (!isFinite(tors)) tors = 0;

        speed_values.push(speed);
        curvature_values.push(curv);
        torsion_values.push(tors);
        T_values.push(T_t);
        N_values.push(N_t);
        B_values.push(B_t);
        positions.push(position);
    });

    // Create the data dictionary
    let data = {
        "speed" : speed_values,
        "curvature": curvature_values,
        "torsion": torsion_values,
        "Tangent": T_values,
        "Normal": N_values,
        "Binormal": B_values,
        "t_values" : t_values,
        "position" : positions
    };

    //console.log("Computed Curvature, Torsion, and Frenet-Serret Data:", data);

    return [
        `\n\n $X(t)=${x_latex}$\n\n$Y(t)=${y_latex}$\n\n$Z(t)=${z_latex}$`,
        `$X(t)=${x_latex}$    $Y(t)=${y_latex}$    $Z(t)=${z_latex}$`,

        `\n\n $X'(t)=${dx_dt.toTex()}$\n\n$Y'(t)=${dy_dt.toTex()}$\n\n$Z'(t)=${dz_dt.toTex()}$`,
        `$X'(t)=${dx_dt.toTex()}$    $Y'(t)=${dy_dt.toTex()}$    $Z'(t)=${dz_dt.toTex()}$`,

        `\n\n $X''(t)=${d2x_dt2.toTex()}$\n\n$Y''(t)=${d2y_dt2.toTex()}$\n\n$Z''(t)=${d2z_dt2.toTex()}$`,
        `$X''(t)=${d2x_dt2.toTex()}$    $Y''(t)=${d2y_dt2.toTex()}$    $Z''(t)=${d2z_dt2.toTex()}$`,

        `\n\n $X'''(t)=${d3x_dt3.toTex()}$\n\n$Y'''(t)=${d3y_dt3.toTex()}$\n\n$Z'''(t)=${d3z_dt3.toTex()}$`,
        `$X'''(t)=${d3x_dt3.toTex()}$    $Y'''(t)=${d3y_dt3.toTex()}$    $Z'''(t)=${d3z_dt3.toTex()}$`,

        `\n\n $$||\\alpha'(t)|| = ${speed_latex}$$ \n\n $$\\kappa(t) = ${curvature_latex}$$ \n\n $$\\tau(t) = ${torsion_latex}$$`,
        `$$||\\alpha'(t)|| = ${speed_latex}$$    $$\\kappa(t) = ${curvature_latex}$$    $$\\tau(t) = ${torsion_latex}$$`,

        `\n\n $$${T_latex}$$ \n\n $$${N_latex}$$ \n\n $$${B_latex}$$`,
        `$$${T_latex}$$  $$${N_latex}$$  $$${B_latex}$$`,

        data,

        t_start,
        t_end,
        t_step,
        t_start
    ];
},

render_surface_analytics: function(surface_data) {
    //console.log("I've been asked to render analytics of: ", surface_data);

    // Get the math expressions
    const x_expr = surface_data['s_x_validated'];
    const y_expr = surface_data['s_y_validated'];
    const z_expr = surface_data['s_z_validated'];

    // Convert expressions to LaTeX
    const x_latex = math.parse(x_expr).toTex();
    const y_latex = math.parse(y_expr).toTex();
    const z_latex = math.parse(z_expr).toTex();


    // Compute derivatives
    const dx_du = math.derivative(x_expr, 'u');
    const dy_du = math.derivative(y_expr, 'u');
    const dz_du = math.derivative(z_expr, 'u');

    const dx_dv = math.derivative(x_expr, 'v');
    const dy_dv = math.derivative(y_expr, 'v');
    const dz_dv = math.derivative(z_expr, 'v');

    const d2x_du2 = math.derivative(dx_du, 'u');
    const d2y_du2 = math.derivative(dy_du, 'u');
    const d2z_du2 = math.derivative(dz_du, 'u');

    const d2x_dudv = math.derivative(dx_du, 'v');
    const d2y_dudv = math.derivative(dy_du, 'v');
    const d2z_dudv = math.derivative(dz_du, 'v');

    const d2x_dv2 = math.derivative(dx_dv, 'v');
    const d2y_dv2 = math.derivative(dy_dv, 'v');
    const d2z_dv2 = math.derivative(dz_dv, 'v');


    // Compute the Jacobian matrix
    const J_11 = " $$\\frac{\\partial X(u,v)}{\\partial u}=" + math.simplify(`${dx_du}`).toTex() + "$$";

    const J_12 = " $$\\frac{\\partial X(u,v)}{\\partial v}=" + math.simplify(`${dx_dv}`).toTex() + "$$";

    const J_21 = " $$\\frac{\\partial Y(u,v)}{\\partial u}=" + math.simplify(`${dy_du}`).toTex() + "$$";

    const J_22 = " $$\\frac{\\partial Y(u,v)}{\\partial v}=" + math.simplify(`${dy_dv}`).toTex() + "$$";

    const J_31 = " $$\\frac{\\partial Z(u,v)}{\\partial u}=" + math.simplify(`${dz_du}`).toTex() + "$$";

    const J_32 = " $$\\frac{\\partial Z(u,v)}{\\partial v}=" + math.simplify(`${dz_dv}`).toTex() + "$$";

    const jacobian = J_11 + "\n\n" + J_12 + "\n\n" + J_21 + "\n\n" + J_22 + "\n\n" + J_31 + "\n\n" + J_32;

    const jacobian_tex = J_11 + "    " + J_12 + "    " + J_21 + "    " + J_22 + "    " + J_31 + "    " + J_32;


    // Compute the Hessian matricies
    const H_X_11 = " $$\\frac{\\partial^2 X(u,v)}{\\partial u^2}=" + math.simplify(`${d2x_du2}`).toTex() + "$$";
    const H_X_12 = " $$\\frac{\\partial^2 X(u,v)}{\\partial u \\partial v}=\\frac{\\partial^2 X(u,v)}{\\partial v \\partial u}=" + math.simplify(`${d2x_dudv}`).toTex() + "$$";
    const H_X_22 = " $$\\frac{\\partial^2 X(u,v)}{\\partial v^2}=" + math.simplify(`${d2x_dv2}`).toTex() + "$$";

    const H_Y_11 = " $$\\frac{\\partial^2 Y(u,v)}{\\partial u^2}=" + math.simplify(`${d2x_du2}`).toTex() + "$$";
    const H_Y_12 = " $$\\frac{\\partial^2 Y(u,v)}{\\partial u \\partial v}=\\frac{\\partial^2 Y(u,v)}{\\partial v \\partial u}=" + math.simplify(`${d2x_dudv}`).toTex() + "$$";
    const H_Y_22 = " $$\\frac{\\partial^2 Y(u,v)}{\\partial v^2}=" + math.simplify(`${d2x_dv2}`).toTex() + "$$";

    const H_Z_11 = " $$\\frac{\\partial^2 Z(u,v)}{\\partial u^2}=" + math.simplify(`${d2x_du2}`).toTex() + "$$";
    const H_Z_12 = " $$\\frac{\\partial^2 Z(u,v)}{\\partial u \\partial v}=\\frac{\\partial^2 Z(u,v)}{\\partial v \\partial u}=" + math.simplify(`${d2x_dudv}`).toTex() + "$$";
    const H_Z_22 = " $$\\frac{\\partial^2 Z(u,v)}{\\partial v^2}=" + math.simplify(`${d2x_dv2}`).toTex() + "$$";

    const hessian = H_X_11 + "\n\n" + H_X_12 + "\n\n" + H_X_22 + "\n\n" + H_Y_11 + "\n\n" + H_Y_12 + "\n\n" + H_Y_22 + "\n\n" + H_Z_11 + "\n\n" + H_Z_12 + "\n\n" + H_Z_22;

    const hessian_tex = H_X_11 + "    " + H_X_12 + "    " + H_X_22 + "    " + H_Y_11 + "    " + H_Y_12 + "    " + H_Y_22 + "    " + H_Z_11 + "    " + H_Z_12 + "    " + H_Z_22;

    // Compute the first fundamental form matrix (E, F, G)
    const E = math.simplify(`(${dx_du})^2 + (${dy_du})^2 + (${dz_du})^2`);
    const E_tex = "$$E(u,v)=" +  E.toTex() + "$$";

    const F = math.simplify(`(${dx_du}) * (${dx_dv}) + (${dy_du}) * (${dy_dv}) + (${dz_du}) * (${dz_dv})`);
    const F_tex = "$$F(u,v)=" +  F.toTex() + "$$";

    const G = math.simplify(`(${dx_dv})^2 + (${dy_dv})^2 + (${dz_dv})^2`);
    const G_tex = "$$G(u,v)=" +  G.toTex() + "$$";

    const FFF = E_tex + "\n\n" + F_tex + "\n\n" + G_tex;
    const FFF_tex = E_tex + "    " + F_tex + "    " + G_tex;


    // Compute the cross product (normal vector n)
    let n_x = math.simplify(`(${dy_du}) * (${dz_dv}) - (${dz_du}) * (${dy_dv})`);
    let n_y = math.simplify(`(${dz_du}) * (${dx_dv}) - (${dx_du}) * (${dz_dv})`);
    let n_z = math.simplify(`(${dx_du}) * (${dy_dv}) - (${dy_du}) * (${dx_dv})`);

    // Compute the magnitude of the normal vector
    const magnitude = math.simplify(`sqrt((${n_x})^2 + (${n_y})^2 + (${n_z})^2)`);

    // Normalize the normal vector
    n_x = math.simplify(`(${n_x}) / (${magnitude})`);
    n_y = math.simplify(`(${n_y}) / (${magnitude})`);
    n_z = math.simplify(`(${n_z}) / (${magnitude})`);

    // Compute the second fundamental form components (L, M, N)
    let L = math.simplify(`(${d2x_du2}) * (${n_x}) + (${d2y_du2}) * (${n_y}) + (${d2z_du2}) * (${n_z})`);
    let M = math.simplify(`(${d2x_dudv}) * (${n_x}) + (${d2y_dudv}) * (${n_y}) + (${d2z_dudv}) * (${n_z})`);
    let N = math.simplify(`(${d2x_dv2}) * (${n_x}) + (${d2y_dv2}) * (${n_y}) + (${d2z_dv2}) * (${n_z})`);


    const L_tex = "$$L(u,v)=" + L.toTex() + "$$";
    const M_tex = "$$M(u,v)=" + M.toTex() + "$$";
    const N_tex = "$$N(u,v)=" + N.toTex() + "$$";

    const SFF = L_tex + "\n\n" + M_tex + "\n\n" + N_tex;
    const SFF_tex = L_tex + "    " + M_tex + "    " + N_tex;


    // Compute Gaussian and Mean Curvature
    const K = math.simplify(`((${L}) * (${N}) - (${M})^2) / ((${E}) * (${G}) - (${F})^2)`);
    const K_tex = "$$K(u,v)=" + K.toTex() + "$$";

    const H = math.simplify(`((${E}) * (${N}) - 2 * (${F}) * (${M}) + (${G}) * (${L})) / (2 * ((${E}) * (${G}) - (${F})^2))`);
    const H_tex = "$$H(u,v)=" + H.toTex() + "$$";

    const k_1 = math.simplify(`(${H}) + sqrt((${H})^2 - (${K}))`);
    const k_1_tex = "$$\\kappa_1(u,v)=" + k_1.toTex() + "$$";

    const k_2 = math.simplify(`(${H}) - sqrt((${H})^2 - (${K}))`);
    const k_2_tex = "$$\\kappa_2(u,v)=" + k_2.toTex() + "$$";

    const surface_curvatures = K_tex + "\n\n" + H_tex + "\n\n" + k_1_tex + "\n\n" + k_2_tex;
    const surface_curvatures_tex = K_tex + "    " + H_tex + "    " + k_1_tex + "    " + k_2_tex;

    // Evaluate the u,v mesh
    const u_start = math.evaluate(surface_data["s_ustart_validated"]);
    const u_end = math.evaluate(surface_data["s_uend_validated"]);
    const nu_steps = surface_data["s_nu_validated"];
    const u_step = (u_end - u_start) / (nu_steps - 1);
    const u_values = math.range(u_start, u_end, u_step, true).toArray();

    const v_start = math.evaluate(surface_data["s_vstart_validated"]);
    const v_end = math.evaluate(surface_data["s_vend_validated"]);
    const nv_steps = surface_data["s_nv_validated"];
    const v_step = (v_end - v_start) / (nv_steps - 1);
    const v_values = math.range(v_start, v_end, v_step, true).toArray();

    // Create arrays to store curvature values
    let H_values = [], K_values = [], k_1_values = [], k_2_values = [];

    // Loop over u and v values to calculate the curvatures
    u_values.forEach(u => {
        let H_row = [], K_row = [], k_1_row = [], k_2_row = [];  // To store curvature values for each v

        v_values.forEach(v => {
            let H_value = H.evaluate({ u, v });
            let K_value = K.evaluate({ u, v });
            let k_1_value = k_1.evaluate({ u, v });
            let k_2_value = k_2.evaluate({ u, v });

            // Handle infinity values
            if (!isFinite(H_value)) H_value = 0;
            if (!isFinite(K_value)) K_value = 0;
            if (!isFinite(k_1_value)) k_1_value = 0;
            if (!isFinite(k_2_value)) k_2_value = 0;

            H_value = Math.round(H_value * 10**7) / 10**7;
            K_value = Math.round(K_value * 10**7) / 10**7;
            k_1_value = Math.round(k_1_value * 10**7) / 10**7;
            k_2_value = Math.round(k_2_value * 10**7) / 10**7;

            // Store the values for this (u, v) pair
            H_row.push(H_value);
            K_row.push(K_value);
            k_1_row.push(k_1_value);
            k_2_row.push(k_2_value);
        });

        // Add the row for this u value to the overall arrays
        H_values.push(H_row);
        K_values.push(K_row);
        k_1_values.push(k_1_row);
        k_2_values.push(k_2_row);
    });

    // Prepare the data dictionary to return to Python
    let data = {
        "H": H_values,
        "K": K_values,
        "k_1": k_1_values,
        "k_2": k_2_values,
        "u" : u_values,
        "v" : v_values
    };

    //console.log(data);


    return [
        `\n\n $X(u,v)=${x_latex}$\n\n$Y(u,v)=${y_latex}$\n\n$Z(u,v)=${z_latex}$`,
        `$X(u,v)=${x_latex}$    $Y(u,v)=${y_latex}$    $Z(u,v)=${z_latex}$`,

        jacobian,
        jacobian_tex,

        hessian,
        hessian_tex,

        FFF,
        FFF_tex,

        SFF,
        SFF_tex,

        surface_curvatures,
        surface_curvatures_tex,

        data

    ];

},

// This function is burning to find you https://open.spotify.com/track/6zKF4293k44ItKWJJgrhXv?si=94490fae15e94719
// and any instance of a p5.js sketch from webdg and kills it if the
// user has navigated away from the webdg page
killswitch_engage : function(path) {
    //console.log("Killswitch engaged.", path);
    if (typeof WebDG_Sketch !== "undefined" && path !== "/webdg") {
        WebDG_Sketch.remove(); // This properly disposes of the old instance
        //console.log("Existing WebDG instance destroyed. cya");
    }
},

// specifies the plotly plots for curves
plot_c_kappa_tau: function(curve_data, light) {
    if (!curve_data) {
        return {
            data: [],
            layout: {}
        };
    }

    // Function to round values to 5 decimal places
    function roundArray(arr) {
        return arr.map(val => Math.round(val * 1e8) / 1e8);
    }

    // Extract and round values
    let speed_values = roundArray(curve_data["speed"]);
    let curvature_values = roundArray(curve_data["curvature"]);
    let torsion_values = roundArray(curve_data["torsion"]);
    let t_values = roundArray(curve_data["t_values"]);

    let theme = light ? "plotly_white" : "plotly_dark";

    // Create traces
    let traces = [
        {
            x: t_values,
            y: speed_values,
            mode: "lines+markers",
            name: "Speed",
            line: { color: "green" }
        },
        {
            x: t_values,
            y: curvature_values,
            mode: "lines+markers",
            name: "Curvature (κ)",
            line: { color: "blue" }
        },
        {
            x: t_values,
            y: torsion_values,
            mode: "lines+markers",
            name: "Torsion (τ)",
            line: { color: "red" }
        }
    ];

    // Return figure
    return {
        data: traces,
        layout: {
            xaxis: { title: "t" },
            yaxis: { title: "Metric" },
            legend: { title: { text: "Metrics" } },
            template: theme,
            hovermode: "closest"
        }
    };
},

// specifies the plotly plots for surfaces
makeSurfaceCurvaturePlot: function(surface_data, light, c) {

    //console.log(surface_data, light, c);

    if (!surface_data) {
        return { data: [], layout: {} };
    }

    let theme = light ? "plotly_white" : "plotly_dark";
    let u = surface_data["u"];
    let v = surface_data["v"];
    let z = surface_data[c];

    // Create the Heatmap trace
    let trace = {
        x: v,
        y: u,
        z: z,
        type: "heatmap",
        colorscale: "Cividis",
        zmid: 0,
        hovertemplate: 
            `u: %{x}<br>` +
            `v: %{y}<br>` +
            `${c}: %{z:.2f}<extra></extra>`
    };

    // Return the Plotly figure
    return {
        data: [trace],
        layout: {
            template: theme,
            margin: { t: 0, b: 0, l: 0, r: 0 },
            xaxis: {
                title: "v",
                range: [Math.min(...v), Math.max(...v)],
                scaleanchor: "y"
            },
            yaxis: {
                title: "u",
                range: [Math.min(...u), Math.max(...u)],
                scaleanchor: "x",
                autorange: "reversed"
            },
            autosize: true
        }
    };
},

// Make the plot above for each surface curvature:

makeSurfaceCurvaturePlot_K: function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'K');
},

makeSurfaceCurvaturePlot_H: function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'H');
},

makeSurfaceCurvaturePlot_k_1: function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'k_1');
},

makeSurfaceCurvaturePlot_k_2: function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'k_2');
},

}; // This ends the namespace
