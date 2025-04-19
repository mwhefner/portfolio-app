// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};

/** Creates a web worker to process the subject
 * then calls the sketch rendering function with the results */
window.dash_clientside.differential_geometry.render_webdg = function(n_clicks, n_2, n_3, c_x_validated, c_y_validated,  c_z_validated, c_tstart_validated, c_tend_validated, c_nt_validated, c_colorby, c_colorpicker, s_x_validated, s_y_validated, s_z_validated, s_ustart_validated, s_uend_validated, s_nu_validated, s_vstart_validated, s_vend_validated, s_nv_validated, s_colorby, ls_f_validated, ls_xstart_validated, ls_xend_validated, ls_nx_validated, ls_ystart_validated, ls_yend_validated, ls_ny_validated, ls_zstart_validated, ls_zend_validated, ls_nz_validated, ls_colorby) {

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
        let worker = new Worker('/assets/js/webdg/async_renderer.js');
        
        // The necessary rendering information to the async renderer
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
        
        // on result from the worker
        worker.onmessage = function(e) {

            // success or failure
            if (e.data.success) {

                document.querySelectorAll('.p5Canvas').forEach(el => el.remove());

                // Create new sketch
                if (triggered_id === "render_curve") {
                    dg.sketch = new p5_v2(dg.curve_sketch(e.data.obj_file));    
                } else if (triggered_id === "render_surface") {
                    dg.sketch = new p5_v2(dg.surface_sketch(e.data.obj_file, e.data.colorJSON, s_nu_validated, s_nv_validated, s_colorby)); 
                } else if (triggered_id === "render_level_surface") {
                    dg.sketch = new p5_v2(dg.level_surface_sketch(e.data.obj_file, ls_colorby)); 
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
};