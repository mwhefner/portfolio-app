

// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};


/** Computes the analytics for curves */
window.dash_clientside.differential_geometry.render_curve_analytics = function(curve_data) {

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
};

// specifies the plotly plots for curves */
window.dash_clientside.differential_geometry.plot_c_kappa_tau = function(curve_data, light) {
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
};
