# Details
University project for my Computer Science GIS course.

My task is to generalize building shapes on an input ESRI Shapefile, and generate an output SHP file.
Generalization in this case means finding the rotated minimal bounding boxes for each building.

I've created several versions for this programme, using different features of the OGR module!

# Installation
1) Install Pixi: https://pixi.prefix.dev/latest/installation/
2) Download the project and navigate into the source folder.
3) Run ``` pixi install ``` in terminal.
4) Get the Shapefile you would like to generalize. E.g: https://extract.bbbike.org/ 
5) Copy the input Shapefile into the input folder! Don't forget to copy any dependencies of the SHP file as well! Rename the files to: ``` buildings.<extension> ```
6) Run ``` pixi run python <file.py> ```
7) Check the output files (e.g. in QGIS).

# Versions

## convexhull.py
Generalizing the buildings with the built in ConvexHull function.

Not an acceptable solution, as the shapes are still not always rectangular. It only forces convexivity.

## envelope.py
Generalizing the building with the minimum bounding boxes using the GetEnvelope() function.
I convert the enveloping coordinates into a polygon.

Not an acceptable solution, as the shapes are not rotated to the original dimension of the buildings. 

## mrr.py
Generalizing is happening with a custom minimal rotated rectangle algorithm.
Although the plots look a little weird on each other, it solves the original task.

# Credits
Using pixi package management tool: https://pixi.prefix.dev/latest/
Using Python GDAL: https://gdal.org/en/stable/api/python/index.html
Using BBBike for the maps: https://extract.bbbike.org/