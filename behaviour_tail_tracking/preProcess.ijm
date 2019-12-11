//test frame --> 1309 (Complex Swim 2.tif)
//Remove Stripes/Gratings
//run("Normalize Local Contrast", "block_radius_x=320 block_radius_y=10 standard_deviations=3 center stack");

waitForUser("Before clicking OK, Make a line selection \n Start at anterior and end at the posterior. ")
getSelectionCoordinates(x, y)
theta = atan2(y[1]-y[0], x[1]-x[0]) * 180 / PI
theta = -1 * theta - 180;
run("Rotate... ", "angle="+theta+" grid=1 interpolation=Bicubic enlarge stack");


//Smoothen
run("Gaussian Blur...", "sigma=1 stack");

//Enrich
run("Minimum...", "radius=1 stack")

run("Enhance Contrast...", "saturated=0 normalize equalize process_all");

//Threshold
setThreshold(0, 11036);
//run("Convert to Mask", "method=Default background=Light");
//-- For MAC
setOption("BlackBackground", false);
run("Convert to Mask", "stack");
//--

//Isolate fish larva
run("Fill Holes", "stack");
run("Analyze Particles...", "size=500-Infinity circularity=0.00-1.00 show=Masks exclude summarize stack");

//Skeletonize
run("Skeletonize", "stack");

//Dilate for the g-value-expand algo to work
run("Dilate", "stack");
