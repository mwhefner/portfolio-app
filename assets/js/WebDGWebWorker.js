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
            postMessage({ success: true, obj_file: obj});
        } else if (e.data.subject === "render_surface") {
            let S = createSurfaceOBJ(e.data.s_params);
            obj = S[0];
            vertexColorJSON = S[1];
            postMessage({ success: true, obj_file: obj, colorJSON : vertexColorJSON});
        } else if (e.data.subject === "render_curve") {
            obj = createCurveJSON(e.data.c_params);
            postMessage({ success: true, obj_file: obj});
        } else {
            console.warn("The webworker was called with an ambiguous context.", e.data.subject);
            postMessage({ success: false});
            return;
        }

       

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
            color = [(255 * math.abs(x)) % 255,(255 * math.abs(y)) % 255,(255 * math.abs(z)) % 255]; 
        } else if (color_by === "Speed") {
            color = [speed];  // Color based on speed (simplified)
        } else if (color_by === "Curvature") {
            color = [curvature];  // Color based on curvature (simplified)
        } else if (color_by === "Torsion") {
            color = [torsion];  // Color based on torsion (simplified)
        } else if (color_by === "t") {
            color = [255 * i / nt, 255 * i / nt, 255 * i / nt];  // Color based on torsion (simplified)
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
        if (!Array.isArray(colorScale) || colorScale.length === 0) {
            throw new Error("colorScale must be a non-empty array.");
        }
    
        value = Math.min(1, Math.max(0, value)); // Clamp value to [0, 1]
    
        let scaledIndex = value * (colorScale.length - 1);
        let index = Math.floor(scaledIndex);
        let t = scaledIndex - index;
    
        // Ensure we don't go out of bounds
        if (index >= colorScale.length - 1) {
            return colorScale[colorScale.length - 1];
        }
    
        let c0 = colorScale[index];
        let c1 = colorScale[index + 1];
    
        // Check if c0 or c1 is undefined
        if (!c0 || !c1) {
            throw new Error("Invalid color value at index " + index);
        }
    
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

function mapToCividis(value) {
    // Ensure value is within the expected range [-1, 1]
    value = Math.max(-1, Math.min(1, value));

    // Define the Cividis color scale manually (from Plotly's colormap)
    const cividisScale = [
        [0, "#313695"],
        [0.1, "#4575b4"],
        [0.2, "#74add1"],
        [0.3, "#abd9e9"],
        [0.4, "#e0f3f8"],
        [0.5, "#ffffbf"],
        [0.6, "#fee090"],
        [0.7, "#fdae61"],
        [0.8, "#f46d43"],
        [0.9, "#d73027"],
        [1.0, "#A50026"]
    ];

    // Normalize value from [-1, 1] to [0, 1] (since Plotly scales work in [0,1])
    let normalizedValue = (value + 1) / 2;

    // Find the two closest points in the scale
    for (let i = 0; i < cividisScale.length - 1; i++) {
        let [t1, color1] = cividisScale[i];
        let [t2, color2] = cividisScale[i + 1];

        if (normalizedValue >= t1 && normalizedValue <= t2) {
            // Compute interpolation factor
            let factor = (normalizedValue - t1) / (t2 - t1);

            // Interpolate between colors
            return interpolateColor(color1, color2, factor);
        }
    }

    // Default return (shouldn't be reached)
    return [0, 0, 0];
}

// Helper function to interpolate between two hex colors
function interpolateColor(color1, color2, factor) {
    let c1 = hexToRgb(color1);
    let c2 = hexToRgb(color2);

    let r = Math.round(c1.r + factor * (c2.r - c1.r));
    let g = Math.round(c1.g + factor * (c2.g - c1.g));
    let b = Math.round(c1.b + factor * (c2.b - c1.b));

    return [r,g,b];
}

// Convert hex color to RGB
function hexToRgb(hex) {
    let bigint = parseInt(hex.slice(1), 16);
    return {
        r: (bigint >> 16) & 255,
        g: (bigint >> 8) & 255,
        b: bigint & 255
    };
}

// SURFACE-----------------------------------------------------

function createSurfaceOBJ(params) {

    //console.log("The validated: ", params);

    importScripts('https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js');

    //console.log("All the params made a");

    const { s_nu_validated, s_nv_validated, s_uend_validated, s_ustart_validated, s_vend_validated, s_vstart_validated, s_x_validated, s_y_validated, s_z_validated, s_colorby } = params;

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

    let minCurvature = 0;
    let maxCurvature = 0;
    let vertexCurvature = 0;

    let x_expr, y_expr, z_expr;
    let dx_du, dy_du, dz_du;
    let dx_dv, dy_dv, dz_dv;
    let d2x_du2, d2y_du2, d2z_du2;
    let d2x_dudv, d2y_dudv, d2z_dudv;
    let d2x_dv2, d2y_dv2, d2z_dv2;

    let E, F, G, L, M, N, K, H, k_1, k_2;
    

    if (s_colorby === "gaussian" || s_colorby === "mean" || s_colorby === "k1" || s_colorby === "k2") {
        // Get the math expressions
        x_expr = s_x_validated;
        y_expr = s_y_validated;
        z_expr = s_z_validated;
        
        // Compute derivatives
        dx_du = math.derivative(x_expr, 'u');
        dy_du = math.derivative(y_expr, 'u');
        dz_du = math.derivative(z_expr, 'u');
        
        dx_dv = math.derivative(x_expr, 'v');
        dy_dv = math.derivative(y_expr, 'v');
        dz_dv = math.derivative(z_expr, 'v');
        
        d2x_du2 = math.derivative(dx_du, 'u');
        d2y_du2 = math.derivative(dy_du, 'u');
        d2z_du2 = math.derivative(dz_du, 'u');
        
        d2x_dudv = math.derivative(dx_du, 'v');
        d2y_dudv = math.derivative(dy_du, 'v');
        d2z_dudv = math.derivative(dz_du, 'v');
        
        d2x_dv2 = math.derivative(dx_dv, 'v');
        d2y_dv2 = math.derivative(dy_dv, 'v');
        d2z_dv2 = math.derivative(dz_dv, 'v');

        // Compute the first fundamental form matrix (E, F, G)
        E = math.simplify(`(${dx_du})^2 + (${dy_du})^2 + (${dz_du})^2`);
        
        F = math.simplify(`(${dx_du}) * (${dx_dv}) + (${dy_du}) * (${dy_dv}) + (${dz_du}) * (${dz_dv})`);

        G = math.simplify(`(${dx_dv})^2 + (${dy_dv})^2 + (${dz_dv})^2`);

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
        L = math.simplify(`(${d2x_du2}) * (${n_x}) + (${d2y_du2}) * (${n_y}) + (${d2z_du2}) * (${n_z})`);
        M = math.simplify(`(${d2x_dudv}) * (${n_x}) + (${d2y_dudv}) * (${n_y}) + (${d2z_dudv}) * (${n_z})`);
        N = math.simplify(`(${d2x_dv2}) * (${n_x}) + (${d2y_dv2}) * (${n_y}) + (${d2z_dv2}) * (${n_z})`);

        let maxK = -Infinity, minK = Infinity;
        let maxH = -Infinity, minH = Infinity;
        let maxk1 = -Infinity, mink1 = Infinity;
        let maxk2 = -Infinity, mink2 = Infinity;

        //console.log("Fundamental forms calculated");

        if (s_colorby === "gaussian") {

            K = math.simplify(`((${L}) * (${N}) - (${M})^2) / ((${E}) * (${G}) - (${F})^2)`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {

                    const u = uStart + i * du;
                    const v = vStart + j * dv;
            
                    let K_value = K.evaluate({ u, v });

                    maxK = Math.max(maxK, K_value);
                    minK = Math.min(minK, K_value);

                }
            }

            maxCurvature = maxK;
            minCurvature = minK;

        } else if (s_colorby === "mean") {

            H = math.simplify(`((${E}) * (${N}) - 2 * (${F}) * (${M}) + (${G}) * (${L})) / (2 * ((${E}) * (${G}) - (${F})^2))`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {

                    const u = uStart + i * du;
                    const v = vStart + j * dv;
            
                    let H_value = H.evaluate({ u, v });

                    maxH = Math.max(maxH, H_value);
                    minH = Math.min(minH, H_value);

                }
            }

            maxCurvature = maxH;
            minCurvature = minH;

        } else if (s_colorby === "k1") {
            K = math.simplify(`((${L}) * (${N}) - (${M})^2) / ((${E}) * (${G}) - (${F})^2)`);
            H = math.simplify(`((${E}) * (${N}) - 2 * (${F}) * (${M}) + (${G}) * (${L})) / (2 * ((${E}) * (${G}) - (${F})^2))`);
            k_1 = math.simplify(`(${H}) + sqrt((${H})^2 - (${K}))`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {

                    const u = uStart + i * du;
                    const v = vStart + j * dv;

                    let k_1_value = k_1.evaluate({ u, v });
                    
                    maxk1 = Math.max(maxk1, k_1_value);
                    mink1 = Math.min(mink1, k_1_value);

                }
            }

            maxCurvature = maxk1;
            minCurvature = mink1;
        } else if (s_colorby === "k2") {
            K = math.simplify(`((${L}) * (${N}) - (${M})^2) / ((${E}) * (${G}) - (${F})^2)`);
            H = math.simplify(`((${E}) * (${N}) - 2 * (${F}) * (${M}) + (${G}) * (${L})) / (2 * ((${E}) * (${G}) - (${F})^2))`);
            k_2 = math.simplify(`(${H}) - sqrt((${H})^2 - (${K}))`);

            for (let i = 0; i <= uSteps; i++) {
                for (let j = 0; j <= vSteps; j++) {
                    const u = uStart + i * du;
                    const v = vStart + j * dv;
            
                    let k_2_value = k_2.evaluate({ u, v });
                    
                    maxk2 = Math.max(maxk2, k_2_value);
                    mink2 = Math.min(mink2, k_2_value);
                }
            }

            maxCurvature = maxk2;
            minCurvature = mink2;
        }

        //console.log("Calculated curvature bounds of type ", s_colorby, minCurvature, maxCurvature);
        
        
    }

    function vertexColor(u,v,uNorm, vNorm, x, y, z) {

        if (s_colorby === "uv") {

            const r = 255 * uNorm;  
            const g = 255 * vNorm;  
            const b = 0; 
        
            return { r, g, b };

        } else if (s_colorby === "xyz") {

            const r = math.abs(x * 255) %  255;  
            const g = math.abs(y * 255) %  255;  
            const b = math.abs(z * 255) %  255; 
        
            return { r, g, b };

        } else if (s_colorby === "normal" || s_colorby === "lighting") {

            const r = 255;  
            const g = 255;  
            const b = 255; 

            // there modes are handled directly in p5
            // so just return white
        
            return { r, g, b };

        } else {

            if (s_colorby === "gaussian") {

                let K_value = K.evaluate({ u, v });
                vertexCurvature = K_value;

            } else if (s_colorby === "mean") {

                let H_value = H.evaluate({ u, v });
                vertexCurvature = H_value;

            } else if (s_colorby === "k1") {

                let k_1_value = k_1.evaluate({ u, v });
                vertexCurvature = k_1_value;

            } else if (s_colorby === "k2") {

                let k_2_value = k_2.evaluate({ u, v });
                vertexCurvature = k_2_value;

            }

        } 

        

        let vertexCurvature_normalized = 0;

        if (maxCurvature - minCurvature !== 0) {
            let maxAbsCurvature = Math.max(Math.abs(minCurvature), Math.abs(maxCurvature));
            
            if (vertexCurvature !== 0) {
                vertexCurvature_normalized = vertexCurvature / maxAbsCurvature;
            }
        }
        else {
            // If min and max curvatures are the same, set the normalized value to a default (e.g., 0.5)
            vertexCurvature_normalized = 0;
        }

        //console.log(vertexCurvature_normalized);

        let vertexColor = mapToCividis(vertexCurvature_normalized);

        //console.log(mapToCividis(vertexCurvature_normalized));

        const r = vertexColor[0];  
        const g = vertexColor[1];  
        const b = vertexColor[2]; 
    
        return { r, g, b };
    }

    let vertexColors = [];  // Stores colors for each vertex

    // Create vertices & texture coordinates
    for (let i = 0; i <= uSteps; i++) {
        for (let j = 0; j <= vSteps; j++) {
            const u = uStart + i * du;
            const v = vStart + j * dv;

            const p = evalXYZ(u, v);
            const uNorm = i / uSteps;  // Normalize U (0 to 1)
            const vNorm = j / vSteps;  // Normalize V (0 to 1)

            objString += `v ${p.x} ${p.y} ${p.z}\n`;
            objString += `vt ${uNorm} ${vNorm}\n`;  // Texture coordinates

            // push the color for this vertex to a
            // dataframe to be passed to p5js to be read
            // to make a pixels graphics buffer
            // that is then applied as a texture

            // Compute color based on (u, v)
            const color = vertexColor(u,v,uNorm, vNorm, p.x, p.y,p.z);  // Replace with your function

            // Store color data (normalized to 0-255)
            vertexColors.push({ u: uNorm, v: vNorm, r: color.r, g: color.g, b: color.b, u_index : i, v_index : j});
        }
    }

    const vertexColorJSON = JSON.stringify(vertexColors);

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

            objString += `f ${p1}/${p1}/${p1} ${p2}/${p2}/${p2} ${p3}/${p3}/${p3}\n`;
            objString += `f ${p1}/${p1}/${p1} ${p3}/${p3}/${p3} ${p4}/${p4}/${p4}\n`;
        }
    }

    //console.log("OBJ file with normals has been created.");

    return [objString, vertexColorJSON];
}




// EMBEDDED CURE------------------------------------------------

function createEmbeddedCurveOBJ(params) {

    //console.log("OBJ of the embedded curve has been created.");

    return "I'm the embedded curve obj.";
}