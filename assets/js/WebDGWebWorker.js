onmessage = function(e) {
    console.log("Received in worker:", e.data); // Print the full JSON object

    try {

        let obj;

        if (e.data.subject === "render_embbeded_curve") {
            obj = createEmbeddedCurveOBJ(e.data.ec_params);
        } else if (e.data.subject === "render_surface") {
            obj = createSurfaceOBJ(e.data.s_params);
        } else {
            obj = createCurveJSON(e.data.c_params);
        }
    
        postMessage({ success: true, obj_file: obj });

    } catch (error) {

        console.error("An error occurred:", error);
        postMessage({ success: false, error: error.message });

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
        const cur = curvature.evaluate(scope);  // Evaluate curvature
        const tor = torsion.evaluate(scope);    // Evaluate torsion
        
        // Store the results
        curveData.curvature.push(cur);
        curveData.torsion.push(tor);


        // Assign colors based on the selected mode
        let color;
        if (color_by === "Solid Color") {
            color = solidColor;
        } else if (color_by === "xyz") {
            color = [(255 * x) % 255,(255 * y) % 255,(255 * z) % 255]; // Normalize assuming [-1,1] range
        } else if (color_by === "Curvature") {
            color = [curvature];  // Color based on curvature (simplified)
        } else if (color_by === "Torsion") {
            color = [torsion];  // Color based on torsion (simplified)
        } else {
            color = [1, 1, 1]; // Default to white
        }

        curveData.colors.push(color);
    }


    // Find the min and max of the curvature and torsion arrays
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
        }

        return color;  // If not Curvature or Torsion, return the original color
    });




    return curveData;
}




// SURFACE-----------------------------------------------------

function createSurfaceOBJ(params) {

    console.log("The validated: ", params);

    console.log("OBJ of the surface has been created.");

    return "I'm the surface obj.";
}

// EMBEDDED CURE------------------------------------------------

function createEmbeddedCurveOBJ(params) {

    console.log("OBJ of the embedded curve has been created.");

    return "I'm the embedded curve obj.";
}