
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};


/** the function ran to build a sketch around a level surface */
window.dash_clientside.differential_geometry.level_surface_sketch = function(obj_file, colorby, x_spacing, y_spacing, z_spacing) {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let sketch_function = function (p) {

    //subject
    let subject;
    let cam;

    p.setup = async function () {
    
        // Run the safe setup function
        dg.safe_setup(p);
    
        p.setAttributes('antialias', true);

        cam = p.createCamera();
    
        // Place the camera at the top-right.
        cam.setPosition(800, -800, 800);
      
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

        p.setCamera(cam);

    };
    
    p.draw = function () {

        p.perspective(dg.fov, p.width / p.height, .8, 8000);

        p.rotateX(p.PI);

        if (dg.rotate_toggle) {
            p.rotateY(p.frameCount * dg.rotation_speed);
        }

        if (p.frameCount === 1 && subject) {
            dg.render_result_alert(true);
        } else if (!subject) {
            dg.render_result_alert(false, "Either the GPU is out of memory or the subject generated a malformed 3D object that cannot be displayed.");
        }

        dg.drawBackground(p);

        dg.drawAxes(p);

        p.push();
        p.translate(cam.centerX, -cam.centerY, -cam.centerZ);
        dg.drawFocalPoint(p);
        p.pop();

        // Orbit control to allow mouse interaction
        // Only allow orbit control when no modal is open
        if (dg.orbitControlled) {
            p.orbitControl(dg.orbit_sensitivity, dg.orbit_sensitivity, dg.orbit_sensitivity);
        }

        //  LIGHTING AND COLOR BY
        if (colorby === "normal") {
            p.normalMaterial();

        } else {
            dg.sceneLighting(p, dg);

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

        // For inertial movement (unused)
        //dg.movement(p, cam);

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
