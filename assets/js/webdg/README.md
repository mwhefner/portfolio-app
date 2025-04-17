# JavaScript Development Log: WebDG

Last updated version 1.0.4

## Plans :bigplans:

- Gather naive event handling in the draw functions and refactor as even listeners for the namespace.
- Camera projection adjustment (perspective and orthogonal)

### Algo & Optimization

I've hit the optimization asymptote for returns on surface resolution for the current CPU-built GPU-displayed approach for level surfaces. Honestly, imho, it's pretty good. If you zoom in / look real close, there's a mesh texture, but all in all, it's great for classroom use. But it can be a lot better. 

**Building:** Two parts of the algorithm grow fast: (1) function evaluation - you have to evaluate the arbitrary math.js-parsed function at every point in the grid and (2) the marching cubes algorithm (march through that grid 8 vertices at a time [as a little cube in space] and use the signs of vertices to index a lookup table for triangles to match the surface in that cube... think about that! lol). Both could be done on the CPU with webworkers in parallel, depending on the number of threads the operating system allocates to the browser. That said, both are embarrassingly parallel, so at least some of it should hopefully be offloaded to the GPU with a graphics buffer... when it's worth it.

**Displaying:** All of that is moot for now because the largest bottleneck by magnitudes is the size of the surface's OBJ (vertex/face/normal definitions) string in memory. With these periodic (triply periodic to be exact) shapes, it would be a lot better if I could instead focus that memory on just a single "generator" unit of, say, a Gyroid or a Schwarz-P surface, and then just instance render (or "tile space with") that with the GPU. 

I tried this with p5.js, and it's just super hacky and randomly crashes. The change will ultimately probably require a refactor to three.js from p5.js, which is sort of the more industrial 3D web graphics library. I've just avoided it because it's... another thing to learn, and the app currently "ain't broke..."
