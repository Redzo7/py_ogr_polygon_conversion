from osgeo import ogr
import datetime
import os

input_file = "input/oktogon_buildings.shp"
output_file = "output/oktogon_result.shp"

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
        env_coords = feature_geom.GetEnvelope()
        
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(env_coords[0], env_coords[2])
        ring.AddPoint(env_coords[1], env_coords[2])
        ring.AddPoint(env_coords[1], env_coords[3])
        ring.AddPoint(env_coords[0], env_coords[3])
        ring.AddPoint(env_coords[0], env_coords[2])

        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        output_feature = ogr.Feature(output_layer.GetLayerDefn())
        output_feature.SetGeometry(poly)

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