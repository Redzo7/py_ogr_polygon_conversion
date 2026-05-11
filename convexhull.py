from osgeo import ogr
import datetime
import os

input_file = "input/buildings.shp"
output_file = "output/result_chull.shp"

# Driver setup
driver = ogr.GetDriverByName("ESRI Shapefile")
data_source = driver.Open(input_file, 0)

input_layer = data_source.GetLayer()
input_layer_defn = input_layer.GetLayerDefn()

# Create output shapefile
if os.path.exists(output_file):
    driver.DeleteDataSource(output_file)

output_data_source = driver.CreateDataSource(output_file)
output_layer = output_data_source.CreateLayer("result", geom_type=ogr.wkbPolygon)

for i in range(input_layer_defn.GetFieldCount()):
    field_defn = input_layer_defn.GetFieldDefn(i)
    output_layer.CreateField(field_defn)

for feature in input_layer:
    feature_geom = feature.GetGeometryRef()

    if feature_geom is not None and feature_geom.GetGeometryType() == ogr.wkbPolygon:
        mrr_geom = feature_geom.ConvexHull()

        output_feature = ogr.Feature(output_layer.GetLayerDefn())
        output_feature.SetGeometry(mrr_geom)

        for i in range(input_layer_defn.GetFieldCount()):
            field_defn = input_layer_defn.GetFieldDefn(i)
            field_name = field_defn.GetNameRef()
            output_feature.SetField(field_name, feature.GetField(i))

        output_layer.CreateFeature(output_feature)
        output_feature = None
    else:
        print("Unsupported geometry type: {}".format(feature_geom.GetGeometryType()))


data_source = None
output_data_source = None

print("Processing completed.")