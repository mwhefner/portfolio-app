
// differential geometry sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = window.dash_clientside.differential_geometry || {};

/** 
 * This creates a p5.js sketch of a viewer inside a sphere
 * as a red, green, and blue light wander in brownian
 * motion around the sphere with one constant white light
 * in the user's focus. "I just think they're neat" 
 * */
window.dash_clientside.differential_geometry.landing_sketch = function () {

    // Get the subnamespace to refer to variables more efficiently
    let dg = window.dash_clientside.differential_geometry;

    let sketch_function = function (p) {

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

            //console.log("Setting up landing page sketch.");
            
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

    return sketch_function;

};

/** 
 * The function ran when the refresh button is pressed.
 * */
window.dash_clientside.differential_geometry.refresh = function () {
    // Get rid of current sketch(es)
    document.querySelectorAll('.p5Canvas').forEach(el => el.remove());
    window.dash_clientside.differential_geometry.sketch = new p5_v2(window.dash_clientside.differential_geometry.landing_sketch());
}
