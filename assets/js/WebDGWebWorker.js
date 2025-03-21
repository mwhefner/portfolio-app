onmessage = function (e) {

    // Ignore React DevTools messages
    if (!e.data.from_webdg) {
        console.warn("Ignoring nonsense sent to webworker. This is normal with some developer browser extensions.");
        return;
    }

    try {
        let obj;

        if (e.data.subject === "render_embbeded_curve") {
            obj = createEmbeddedCurveOBJ(e.data.ec_params);
        } else if (e.data.subject === "render_surface") {
            obj = createSurfaceOBJ(e.data.s_params);
        } else if (e.data.subject === "render_curve") {
            obj = createCurveJSON(e.data.c_params);
        } else {
            console.warn("The webworker was called with an ambiguous context.", e.data.subject);
            postMessage({ success: false});
            return;
        }

        postMessage({ success: true, obj_file: obj});

    } catch (error) {
        console.error("An error occurred:", error);
        postMessage({ success: false, error: error.message});
    }
};



function createCurveJSON(params) {
    importScripts('https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js');

    // Parse numeric params
    const nt = Math.max(2, params.nt);
    const t_start = math.evaluate(params.t_start);
    const t_end = math.evaluate(params.t_end);

    if (t_start > t_end) {
        [t_start, t_end] = [t_end, t_start]; // Swap if needed
    }

    const color_by = params.color_by;
    const color_hex = params.color_picker || "#FFFFFF";  // Default to white if no color is provided

    function hexToRGB(hex) {
        const bigint = parseInt(hex.slice(1), 16);
        return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
    }
    
    const solidColor = hexToRGB(color_hex);
    

    // Define the input for alpha (t)
    const alphaCompiled = [
        math.parse(params.x),
        math.parse(params.y),
        math.parse(params.z)
    ];

    // Derivatives for alpha', alpha'', alpha'''
    const alphaPrimeCompiled = [
        math.derivative(params.x, 't'),
        math.derivative(params.y, 't'),
        math.derivative(params.z, 't')
    ];

    const alphaDoublePrimeCompiled = [
        math.derivative(alphaPrimeCompiled[0].toString(), 't'),
        math.derivative(alphaPrimeCompiled[1].toString(), 't'),
        math.derivative(alphaPrimeCompiled[2].toString(), 't')
    ];

    const alphaTripplePrimeCompiled = [
        math.derivative(alphaDoublePrimeCompiled[0].toString(), 't'),
        math.derivative(alphaDoublePrimeCompiled[1].toString(), 't'),
        math.derivative(alphaDoublePrimeCompiled[2].toString(), 't')
    ];

    // Speed
    const speed = math.parse(
        `norm([${alphaPrimeCompiled[0]}, ${alphaPrimeCompiled[1]}, ${alphaPrimeCompiled[2]}]) / 1`
    );
    
    // Curvature :(
    const curvature = math.parse("norm(cross([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "], [" + alphaDoublePrimeCompiled[0] + ", " + alphaDoublePrimeCompiled[1] + ", " + alphaDoublePrimeCompiled[2] + "])) / (norm([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "]) ^ 3)");

    // Torsion :((
    const torsion = math.parse(
        "dot(cross([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "], [" + alphaDoublePrimeCompiled[0] + ", " + alphaDoublePrimeCompiled[1] + ", " + alphaDoublePrimeCompiled[2] + "]), [" + alphaTripplePrimeCompiled[0] + ", " + alphaTripplePrimeCompiled[1] + ", " + alphaTripplePrimeCompiled[2] + "]) / (norm(cross([" + alphaPrimeCompiled[0] + ", " + alphaPrimeCompiled[1] + ", " + alphaPrimeCompiled[2] + "], [" + alphaDoublePrimeCompiled[0] + ", " + alphaDoublePrimeCompiled[1] + ", " + alphaDoublePrimeCompiled[2] + "])) ^ 2)"
        );

    // Prepare for curvature and torsion calculations
    let curveData = {
        vertices: [],
        colors: [],
        speed: [],
        curvature: [],
        torsion: [],
        alpha : alphaCompiled.toString(),
        alphaPrime : alphaPrimeCompiled.toString(),
        alphaDoublePrime : alphaDoublePrimeCompiled.toString(),
        curvature_expression : curvature,
        torsion_expression : torsion
    };

    // Loop over the parameter t to calculate curvature and torsion
    for (let i = 0; i <= nt; i++) {
        const t = t_start + (i / nt) * (t_end - t_start);
        const scope = { t };

        // Evaluate position (alpha)
        const x = alphaCompiled[0].evaluate(scope);
        const y = alphaCompiled[1].evaluate(scope);
        const z = alphaCompiled[2].evaluate(scope);
        curveData.vertices.push([x, y, z]);

        // Evaluate curvature and torsion
        const spe = speed.evaluate(scope);  // Evaluate curvature
        const cur = curvature.evaluate(scope);  // Evaluate curvature
        const tor = torsion.evaluate(scope);    // Evaluate torsion
        
        // Store the results
        curveData.speed.push(spe);
        curveData.curvature.push(cur);
        curveData.torsion.push(tor);

        // Assign colors based on the selected mode
        let color;
        if (color_by === "Solid Color") {
            color = solidColor;
        } else if (color_by === "xyz") {
            color = [(255 * x) % 255,(255 * y) % 255,(255 * z) % 255]; 
        } else if (color_by === "Speed") {
            color = [speed];  // Color based on speed (simplified)
        } else if (color_by === "Curvature") {
            color = [curvature];  // Color based on curvature (simplified)
        } else if (color_by === "Torsion") {
            color = [torsion];  // Color based on torsion (simplified)
        } else {
            color = [1, 1, 1]; // Default to white
        }

        curveData.colors.push(color);
    }


    // Find the min and max of the speed, curvature and torsion arrays
    const minSpeed = Math.min(...curveData.speed);
    const maxSpeed = Math.max(...curveData.speed);

    const minCurvature = Math.min(...curveData.curvature);
    const maxCurvature = Math.max(...curveData.curvature);

    const minTorsion = Math.min(...curveData.torsion);
    const maxTorsion = Math.max(...curveData.torsion);

    function interpolateColor(value, colorScale) {
        value = Math.min(1, Math.max(0, value)); // Clamp value to [0,1]
        
        let scaledIndex = value * (colorScale.length - 1);
        let index = Math.floor(scaledIndex);
        let t = scaledIndex - index;
    
        if (index >= colorScale.length - 1) return colorScale[colorScale.length - 1];
    
        let c0 = colorScale[index], c1 = colorScale[index + 1];
    
        return [
            Math.round(c0[0] + t * (c1[0] - c0[0])),
            Math.round(c0[1] + t * (c1[1] - c0[1])),
            Math.round(c0[2] + t * (c1[2] - c0[2]))
        ];
    }
    
    function getDivergingColor(value) {
            const colorScale = [
                [48, 18, 59],   // Deep Blue (Low)
                [70, 107, 190], // Blue (Middle-Low)
                [255, 216, 53], // Yellow (Middle-High)
                [189, 28, 33]   // Red (High)
            ];
            return interpolateColor(value, colorScale);
        }
        
    

    // Normalize and scale color values after the loop
    curveData.colors = curveData.colors.map((color, index) => {
        let spe = curveData.speed[index]; // Get the corresponding curvature value
        let cur = curveData.curvature[index]; // Get the corresponding curvature value
        let tor = curveData.torsion[index];   // Get the corresponding torsion value

        if (color_by === "Curvature") {
            // Handle division by zero case
            if (maxCurvature - minCurvature === 0 || maxCurvature - minCurvature < 0.00001) {
                return getDivergingColor(0.5); // Or you can return 0, depending on your preference
            }
            // Map the curvature value from min-max to 0-255
            let normalizedCurvature = ((cur - minCurvature) / (maxCurvature - minCurvature));
            return getDivergingColor(normalizedCurvature);
        } else if (color_by === "Torsion") {
            // Handle division by zero case
            if (maxTorsion - minTorsion === 0 || maxTorsion - minTorsion < 0.00001) {
                return getDivergingColor(0.5); // Or you can return 0, depending on your preference
            }
            // Map the torsion value from min-max to 0-255
            let normalizedTorsion = ((tor - minTorsion) / (maxTorsion - minTorsion));
            return getDivergingColor(normalizedTorsion);
        } else if (color_by === "Speed") {
            // Handle division by zero case
            if (maxSpeed - minSpeed === 0 || maxSpeed - minSpeed < 0.00001) {
                return getDivergingColor(0.5); // Or you can return 0, depending on your preference
            }
            // Map the Speed value from min-max to 0-255
            let normalizedSpeed = ((spe - minSpeed) / (maxSpeed - minSpeed));

            return getDivergingColor(normalizedSpeed);
        }

        return color;  // If not Speed, Curvature or Torsion, return the original color
    });




    return curveData;
}

// SURFACE-----------------------------------------------------

function createSurfaceOBJ(params) {

    console.log("The validated: ", params);

    importScripts('https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js');

    const { s_nu_validated, s_nv_validated, s_uend_validated, s_ustart_validated, s_vend_validated, s_vstart_validated, s_x_validated, s_y_validated, s_z_validated } = params;

    const uStart = math.evaluate(s_ustart_validated);
    const uEnd = math.evaluate(s_uend_validated);
    const vStart = math.evaluate(s_vstart_validated);
    const vEnd = math.evaluate(s_vend_validated);

    const uSteps = s_nu_validated;
    const vSteps = s_nv_validated;

    let objString = "# OBJ file with normals\n";

    function evalXYZ(u, v) {
        return {
            x: math.evaluate(s_x_validated, { u, v }),
            y: math.evaluate(s_y_validated, { u, v }),
            z: math.evaluate(s_z_validated, { u, v })
        };
    }

    function crossProduct(a, b) {
        return {
            x: a.y * b.z - a.z * b.y,
            y: a.z * b.x - a.x * b.z,
            z: a.x * b.y - a.y * b.x
        };
    }

    function normalize(v) {
        const length = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
        return { x: v.x / length, y: v.y / length, z: v.z / length };
    }

    const du = (uEnd - uStart) / uSteps;
    const dv = (vEnd - vStart) / vSteps;

    // Create vertices
    for (let i = 0; i <= uSteps; i++) {
        for (let j = 0; j <= vSteps; j++) {
            const u = uStart + i * du;
            const v = vStart + j * dv;

            const p = evalXYZ(u, v);
            objString += `v ${p.x} ${p.y} ${p.z}\n`;
        }
    }

    // Create normals (with boundary condition handling)
    for (let i = 0; i <= uSteps; i++) {
        for (let j = 0; j <= vSteps; j++) {
            const u = uStart + i * du;
            const v = vStart + j * dv;

            const p = evalXYZ(u, v);
            const pu = evalXYZ(u + 1e-5, v);
            const pv = evalXYZ(u, v + 1e-5);

            const duVec = { x: pu.x - p.x, y: pu.y - p.y, z: pu.z - p.z };
            const dvVec = { x: pv.x - p.x, y: pv.y - p.y, z: pv.z - p.z };

            const normal = normalize(crossProduct(duVec, dvVec));

            objString += `vn ${normal.x} ${normal.y} ${normal.z}\n`;
        }
    }

    // Create faces (fix boundary faces)
    for (let i = 0; i < uSteps; i++) {
        for (let j = 0; j < vSteps; j++) {
            const p1 = i * (vSteps + 1) + j + 1;
            const p2 = (i + 1) * (vSteps + 1) + j + 1;
            const p3 = (i + 1) * (vSteps + 1) + j + 2;
            const p4 = i * (vSteps + 1) + j + 2;

            objString += `f ${p1}//${p1} ${p2}//${p2} ${p3}//${p3}\n`;
            objString += `f ${p1}//${p1} ${p3}//${p3} ${p4}//${p4}\n`;
        }
    }

    console.log("OBJ file with normals has been created.");

    return objString;
}




// EMBEDDED CURE------------------------------------------------

function createEmbeddedCurveOBJ(params) {

    console.log("OBJ of the embedded curve has been created.");

    return "I'm the embedded curve obj.";
}