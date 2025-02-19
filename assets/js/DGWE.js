
// sub-namespace
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.differential_geometry = {

    // This function defines the sketch by the sketch_function below
    // Then, after, initialized the sketch with the p5 constructor

    create_sketch : function () {

        console.log("DGWE VIEWER FUNCTION CREATOR DEFINED.");

        // sketch_function is passed to the p5 constructor
        // This is a function that takes a p5 sketch instance (p)
        // and defines (overwrites) its functions (like setup and draw).

        let sketch_function = function (p) {

            console.log("CREATING DGWE VIEWER...");

            p.preload = function () {
                console.log("/t PRELOAD....");
            };

            p.setup = function () {

                console.log("/t SAFE SETUP....");
                // Define the safe setup function
                function initializeCanvas() {

                    // Get the parent element of the canvas
                    const parentElement = document.getElementById("DGWE_Canvas_Parent");

                    // Make sure the globalStorage exists
                    globalStorageElement = document.getElementById("DGWE_Store");

                    console.log(globalStorageElement);

                    // Get the dimensions of the parent and use them as the
                    // dimensions of the p5 canvas (if they change later, 
                    // that will be handled in p.windowResized.)
                    if (parentElement && globalStorageElement) {

                        // Get the width and the height of the sketch container
                        const w = parentElement.clientWidth;
                        const h = parentElement.clientHeight;

                        // Make sure there's an actual area
                        if (w > 0 && h > 0) {

                            // Set width and height of the p5 canvas
                            const canvas = p.createCanvas(w, h);

                            canvas.parent("DGWE_Canvas_Parent");

                        // Retry after a short delay if width or height is 0
                        } else {
                            setTimeout(initializeCanvas, 500);
                        }

                    // Retry after a short delay if parentElement is not found
                    } else {
                        setTimeout(initializeCanvas, 500);
                    }

                }

                // Run the safe setup function
                initializeCanvas();

                p.noLoop();
            };

            p.draw = function () {
                p.background(255, 0, 0);
            };

            p.windowResized = function () {

            };

            p.mousePressed = function () {
                p.background(255, 255, 0);
            };

            p.keyPressed = function () {

            };
            
        }

        DGWE = new p5(sketch_function);

        return "Completed sketch setup.";

    }


};