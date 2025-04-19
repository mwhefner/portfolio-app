
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};

/** The function ran to build a sketch around a surface */
window.dash_clientside.differential_geometry.surface_sketch = function (obj_file, colorsJSON, s_nu_validated, s_nv_validated, colorby) {

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

        p.setCamera(cam);

    };
    
    p.draw = function () {

        if (p.frameCount === 1 && subject) {
            dg.render_result_alert(true);
        } else if (!subject) {
            dg.render_result_alert(false, "Either the GPU is out of memory or the subject generated a malformed 3D object that cannot be displayed.");
        }

        dg.drawBackground(p);

        dg.drawAxes();

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
    
    }

    return sketch_function;

};
