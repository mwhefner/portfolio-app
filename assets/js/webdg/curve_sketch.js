
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};


/** Get the TNB frame at a given index */
window.dash_clientside.differential_geometry.getDataAtIndex = function(index, TNB_data) {
    return {
        position: TNB_data.position[index],
        Tangent: TNB_data.Tangent[index],
        Normal: TNB_data.Normal[index],
        Binormal: TNB_data.Binormal[index],
        curvature: TNB_data.curvature[index],
        torsion: TNB_data.torsion[index],
        speed: TNB_data.speed[index]
    };
};

/** Get the TNB frame at a given t value */
window.dash_clientside.differential_geometry.getDataAtT = function(t, TNB_data) {

    let index = TNB_data.t_values.findIndex(val => Math.abs(val - t) < 1e-6);
    if (index === -1) return null; // Return null if t is not found
    
    return this.getDataAtIndex(index, TNB_data);
};

/** (3) Plot T, N, and B vectors at a given t value using p5.js */
window.dash_clientside.differential_geometry.plotTNB = function(t, TNB_data, p, index = null) {

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
};

/** The function ran to build a sketch around a curve */
window.dash_clientside.differential_geometry.curve_sketch = function (curveData) {

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

        p.setCamera(cam);

    };
    
    p.draw = function () {

        if (p.frameCount === 1 && curveData) {
            dg.render_result_alert(true);
        } else if (!curveData) {
            dg.render_result_alert(false);
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
    
    }

    return sketch_function;

};