
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = {

// visibility booleans
showAxis : true,

scaler : 100,
strokeW : 10,

getAxisLimits : function(vertices) {
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    let minZ = Infinity, maxZ = -Infinity;

    for (let v of vertices) {
        minX = math.min(minX, v[0]);
        maxX = math.max(maxX, v[0]);
        minY = math.min(minY, v[1]);
        maxY = math.max(maxY, v[1]);
        minZ = math.min(minZ, v[2]);
        maxZ = math.max(maxZ, v[2]);
    }

    let maxAbsX = math.max(math.abs(minX), math.abs(maxX));
    let maxAbsY = math.max(math.abs(minY), math.abs(maxY));
    let maxAbsZ = math.max(math.abs(minZ), math.abs(maxZ));
    let axisLimit = math.max(maxAbsX, maxAbsY, maxAbsZ) * 1.2; // 20% buffer

    return axisLimit;
},

drawAxes : function (limit, p, sw) {

    p.strokeWeight(sw);

    // X-Axis (Red)
    p.stroke(255, 0, 0);
    p.line(-limit, 0, 0, limit, 0, 0);

    // Y-Axis (Green)
    p.stroke(0, 255, 0);
    p.line(0, -limit, 0, 0, limit, 0);

    // Z-Axis (Blue)
    p.stroke(0, 0, 255);
    p.line(0, 0, -limit, 0, 0, limit);
},

parse_constant: function(pre, value) {
    if (!value) {
        return "Please enter a valid value in the input form to parse.";
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
        return "$$" + pre + " " + parsed.toTex() + "$$";

    } catch (e) {
        
        return "Input could not be parsed. Please try again.";
    }
},
    

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


safe_setup : function (p) {

    p.createCanvas(window.innerWidth, window.innerHeight, p.WEBGL);

},

// The function ran when the refresh button is pressed.
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

            console.log("Setting up landing page sketch.");
            
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
        console.log("Existing WebDG instance destroyed. cya");
    }

    console.log("A new WebDG instance is being created.");

    WebDG_Sketch = new p5(landing_sketch);

    return "Completed sketch setup.";

}, // This ends the refresh function

// The function ran to build a sketch around a curve
curve_sketch : function (curveData) {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let sketch_function = function (p) {

    p.preload = function () {
        console.log("Preloading, if need be.");
    };

    p.setup = function () {
        console.log("Setting up the subject sketch of:", curveData);
            
        // Run the safe setup function
        dg.safe_setup(p);

        p.setAttributes('antialias', true);

    };
    
    p.draw = function () {

        p.clear(0, 0, 0, 0); // transparent background

        let axisLimit = dg.getAxisLimits(curveData.vertices) * dg.scaler; // Scale factor

        // Draw the XYZ axes
        if (dg.showAxis) {
            dg.drawAxes(axisLimit, p, dg.strokeW);
        }
        
        // Orbit control to allow mouse interaction
        // Only allow orbit control when no modal is open
        p.orbitControl();

        // account for y pointing down at the start
        p.rotateX(p.PI);

        // Set lighting
        p.ambientLight(100); // Ambient light with moderate intensity
        p.directionalLight(255, 255, 255, 1, 0, 0);
        p.directionalLight(255, 255, 255, 0, 1, 0);
        p.directionalLight(255, 255, 255, 0, 0, 1);

    
        // Draw text at the origin
        p.push(); // Save the current transformation matrix

        // TODO: translate to focus

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

    };

    p.windowResized = function () {

    };

    p.keyPressed = function () {
        // arrow keys will move focus according to movement mode
        // in subject settings
    };
    
    } // This ends the sketch function

    if (typeof WebDG_Sketch !== "undefined") {
        WebDG_Sketch.remove(); // This properly disposes of the old instance
        console.log("Existing WebDG instance destroyed. cya");
    }

    console.log("A new WebDG instance is being created.");

    WebDG_Sketch = new p5(sketch_function);

    return "Completed sketch setup.";

}, // This ends create_sketch

// The function ran to build a sketch around a surface
surface_sketch : function (obj_file) {


    const subject_model = obj_file;

    //subject
    let subject;

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let sketch_function = function (p) {

    p.preload = function () {
        console.log("Preloading, if need be.");
    };

    p.setup = function () {
        // console.log("Setting up the subject sketch of:", obj_file);
    
        // Run the safe setup function
        dg.safe_setup(p);
    
        p.setAttributes('antialias', true);
    
        p.camera(0, -500, 500, 0, 0, 0, 0, 1, 0);

        subject = p.createModel(subject_model, '.obj');
    };
    
    p.draw = function () {

        p.clear(0, 0, 0, 0);

        p.orbitControl();
    
        // Set lighting
        p.ambientLight(128);
        p.directionalLight(255, 0, 0, 1, 0, 0);
        p.directionalLight(0, 255, 0, 0, 1, 0);
        p.directionalLight(0, 0, 255, 0, 0, 1);
        p.ambientMaterial(255); // Ensure the model reacts to lighting
        p.shininess(10);       // Make highlights pop
        p.specularMaterial(255);
    
        p.push(); 
        p.rotateX(p.PI);
        
        p.fill(255);
        p.strokeWeight(0);

        p.scale(dg.scaler);
        
    
        p.model(subject);
    
        p.pop();
    };
    

    p.windowResized = function () {

    };

    p.keyPressed = function () {
        // arrow keys will move focus according to movement mode
        // in subject settings
    };
    
    } // This ends the sketch function

    if (typeof WebDG_Sketch !== "undefined") {
        WebDG_Sketch.remove(); // This properly disposes of the old instance
        console.log("Existing WebDG instance destroyed. cya");
    }

    console.log("A new WebDG instance is being created.");

    WebDG_Sketch = new p5(sketch_function);

    return "Completed sketch setup.";

}, // This ends create_sketch

render_webdg : function(n_clicks, n_2, c_x_validated, c_y_validated,  c_z_validated, c_tstart_validated, c_tend_validated, c_nt_validated, c_colorby, c_colorpicker, s_x_validated, s_y_validated, s_z_validated, s_ustart_validated, s_uend_validated, s_nu_validated, s_vstart_validated, s_vend_validated, s_nv_validated, s_colorby) {

    if (n_clicks > 0 || n_2 > 0) {
        
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
        let worker = new Worker('/assets/js/WebDGWebWorker.js');
        
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
                
        };
        
        // Pass to the obj rendering web worker
        worker.postMessage(dataToSend);
        
        // Open rendering alert by setting to 'display: block'
        
        let rendering_alert = document.getElementById('rendering_alert');
        
        if (alert) {
            console.log('explicitly showing rendering_alert!');
            rendering_alert.style.display = 'block';
        } else {
            console.log('rendering_alert not found!');
        }
        
        // Listen for the result from the worker------------------
        worker.onmessage = function(e) {

            console.log('The worker is done! She says:', e.data);



            // At this point, the OBJ is built. We need to:



            // Close rendering alert by setting to 'display: none'
            
            rendering_alert = document.getElementById('rendering_alert');
            
            if (alert) {
                console.log('hide rendering_alert!');
                rendering_alert.style.display = 'none';
            } else {
                console.log('rendering_alert not found!');
            }
            

            
            // success or failure
            
            if (e.data.success) {
                
                // Success alert
                const success_alert = document.getElementById('success_alert');
                
                if (success_alert) {
                    success_alert.style.display = 'block';
                } else {
                    console.log('success_alert not found!  (may be normal)');
                }
                
                
                // Build P5.js Sketch around recieved data
                
                if (triggered_id === "render_curve") {
                    // Curves are rendered in real time since they're
                    // far less computationally intense and do not involve lighting
                    dg.curve_sketch(e.data.obj_file);    
                } else if (triggered_id === "render_surface") {
                    dg.surface_sketch(e.data.obj_file); 
                } else if (triggered_id === "render_surface") {
                    dg.embedded_curve_sketch(e.data.obj_file); 
                } 
                
            } else {
                
                // Failure alert
                const failure_alert = document.getElementById('failure_alert');
                if (failure_alert) {
                    failure_alert.style.display = 'block';
                    setTimeout(function() {
                        failure_alert.style.display = 'none';
                    }, 5000); // 5000 ms = 5 second timeout for failure
                } else {
                    console.log('failure_alert not found!');
                }
                
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

        console.log("Updating store_math with: ", math_store_data);
        
        return [{ display: 'block'}, math_store_data];
    }
    
    // Default behavior: Hide the alert if no button is clicked
    return [{ display: 'none' }, {rendered: false}];
},

render_curve_analytics: function(curve_data) {

    console.log("I've been asked to render analytics of: ", curve_data);

    // Get the math expressions
    const x_expr = curve_data['c_x_validated'];
    const y_expr = curve_data['c_y_validated'];
    const z_expr = curve_data['c_z_validated'];

    // Convert expressions to LaTeX
    const x_latex = math.parse(x_expr).toTex();
    const y_latex = math.parse(y_expr).toTex();
    const z_latex = math.parse(z_expr).toTex();

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
    const T_x = math.simplify(`${dx_dt} / ${speed_expr}`);
    const T_y = math.simplify(`${dy_dt} / ${speed_expr}`);
    const T_z = math.simplify(`${dz_dt} / ${speed_expr}`);

    // Compute derivative of T
    const dT_x = math.derivative(T_x, 't');
    const dT_y = math.derivative(T_y, 't');
    const dT_z = math.derivative(T_z, 't');

    // Compute unit normal vector (N)
    const normal_magnitude_expr = math.simplify(`sqrt(${dT_x}^2 + ${dT_y}^2 + ${dT_z}^2)`);
    const N_x = math.simplify(`${dT_x} / ${normal_magnitude_expr}`);
    const N_y = math.simplify(`${dT_y} / ${normal_magnitude_expr}`);
    const N_z = math.simplify(`${dT_z} / ${normal_magnitude_expr}`);

    // Compute binormal vector (B)
    const B_x = math.simplify(`(${T_y} * ${N_z}) - (${T_z} * ${N_y})`);
    const B_y = math.simplify(`(${T_z} * ${N_x}) - (${T_x} * ${N_z})`);
    const B_z = math.simplify(`(${T_x} * ${N_y}) - (${T_y} * ${N_x})`);

    // Compute Darboux vector 
    const curvature_expr = math.simplify(
        `norm(cross([${dx_dt}, ${dy_dt}, ${dz_dt}], [${d2x_dt2}, ${d2y_dt2}, ${d2z_dt2}])) / (norm([${dx_dt}, ${dy_dt}, ${dz_dt}]) ^ 3)`
    );

    const torsion_expr = math.simplify(
        `dot(cross([${dx_dt}, ${dy_dt}, ${dz_dt}], [${d2x_dt2}, ${d2y_dt2}, ${d2z_dt2}]), [${d3x_dt3}, ${d3y_dt3}, ${d3z_dt3}]) / (norm(cross([${dx_dt}, ${dy_dt}, ${dz_dt}], [${d2x_dt2}, ${d2y_dt2}, ${d2z_dt2}])) ^ 2)`
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

    t_values.forEach(t => {
        let speed = speed_expr.evaluate({ t });
        let curv = curvature_expr.evaluate({ t });
        let tors = torsion_expr.evaluate({ t });

        let T_t = [T_x.evaluate({ t }), T_y.evaluate({ t }), T_z.evaluate({ t })];
        let N_t = [N_x.evaluate({ t }), N_y.evaluate({ t }), N_z.evaluate({ t })];
        let B_t = [B_x.evaluate({ t }), B_y.evaluate({ t }), B_z.evaluate({ t })];

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
    });

    // Create the data dictionary
    let data = {
        "speed" : speed_values,
        "curvature": curvature_values,
        "torsion": torsion_values,
        "Tangent": T_values,
        "Normal": N_values,
        "Binormal": B_values,
        "Darboux": D_values,
        "t_values" : t_values
    };

    console.log("Computed Curvature, Torsion, and Frenet-Serret Data:", data);

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

        data  
    ];
}

}; // This ends the namespace
