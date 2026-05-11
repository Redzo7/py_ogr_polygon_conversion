# Details
University project for my Computer Science GIS course.

My task is to generalize building shapes on an input ESRI Shapefile, and generate an output SHP file.
Generalization in this case means finding the rotated minimal bounding boxes for each building.

I've created several versions for this programme, using different features of the OGR module!

# Versions

## convexhull.py
Generalizing the buildings with the built in ConvexHull function.

Not an acceptable solution, as the shapes are still not always rectangular. It only forces convexivity.

## envelope.py
Generalizing the building with the minimum bounding boxes using the GetEnvelope() function.
I convert the enveloping coordinates into a polygon.

Not an acceptable solution, as the shapes are not rotated to the original dimension of the buildings. 


# Credits
Using pixi package management tool: https://pixi.prefix.dev/latest/
Using Python GDAL: https://gdal.org/en/stable/api/python/index.html
Using BBBike for the maps: https://extract.bbbike.org/