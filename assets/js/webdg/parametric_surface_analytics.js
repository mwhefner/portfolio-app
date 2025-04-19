
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};


/** Computes the analytics for parametric surfaces */
window.dash_clientside.differential_geometry.render_surface_analytics = function(surface_data) {
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

};

// specifies the plotly plots for surfaces */
window.dash_clientside.differential_geometry.makeSurfaceCurvaturePlot = function(surface_data, light, c) {

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
};

/** Make the plot above for each surface curvature:*/

window.dash_clientside.differential_geometry.makeSurfaceCurvaturePlot_K = function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'K');
};

window.dash_clientside.differential_geometry.makeSurfaceCurvaturePlot_H = function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'H');
};

window.dash_clientside.differential_geometry.makeSurfaceCurvaturePlot_k_1 = function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'k_1');
};

window.dash_clientside.differential_geometry.makeSurfaceCurvaturePlot_k_2 = function(surface_data, light) {
    return this.makeSurfaceCurvaturePlot(surface_data, light, 'k_2');
};
