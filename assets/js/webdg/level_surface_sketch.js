
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};


/** the function ran to build a sketch around a level surface */
window.dash_clientside.differential_geometry.level_surface_sketch = function(obj_file, colorby, x_spacing, y_spacing, z_spacing) {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let sketch_function = function (p) {

    //generator
    let subject
    let cam;
    let instancingShader;

    p.setup = async function () {
    
        // Run the safe setup function
        dg.safe_setup(p);

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

        let instancingCallback = {





        };

        instancingShader = p.baseMaterialShader().modify({

            declarations: 'vec3 myNormal;',

            'Vertex getObjectInputs': `(Vertex inputs) {
                int id = gl_InstanceID;
                int size = 3; // 10 per axis
                float spacing = 6.283184;
                float halfGrid = float(size - 1) * spacing * 0.5;

                int x = id % size;
                int y = (id / size) % size;
                int z = id / (size * size);

                vec3 offset = vec3(
                float(x) * spacing,
                float(y) * spacing,
                float(z) * spacing
                );

                inputs.position.xyz += offset - vec3(halfGrid);

                return inputs;
            }`,

            'Inputs getPixelInputs': `(Inputs inputs) {
                myNormal = inputs.normal;
                return inputs;
            }`,
  
            'vec4 getFinalColor': `(vec4 color) {
                return mix(
                vec4(1.0, 1.0, 1.0, 1.0),
                color,
                abs(dot(myNormal, vec3(0.0, 0.0, 1.0))));
            }`

        });

        //p.ortho(-p.width/2, p.width/2, -p.height/2, p.height/2, 0, 50000);

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
            // scene lighting
            dg.sceneLighting(p, dg);
        }

        p.push(); 
        
        p.strokeWeight(0);

        p.scale(dg.scaler);

        p.shader(instancingShader);
        
        p.model(subject, 27);

        p.pop();

        p.strokeWeight(1);

        dg.movement(p, cam);

    };
    
    }

    return sketch_function;
};
