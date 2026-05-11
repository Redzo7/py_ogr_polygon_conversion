from osgeo import ogr
import datetime
import os
import math

def mrr(geom):
    cvxhull = geom.ConvexHull()
    path = cvxhull.GetGeometryRef(0)
    points = [path.GetPoint(i) for i in range(path.GetPointCount())]

    best_area = float('inf')
    best_rect = None

    # Find global minimum of area of bounding rectangle
    for i in range(len(points)-1):
        a = points[i]
        b = points[i+1]

        rot_angle = math.atan2(b[1] - a[1], b[0] - a[0])

        cos_angle = math.cos(-rot_angle)
        sin_angle = math.sin(-rot_angle)

        rotated = []
        for p in points: 
            x = p[0] * cos_angle - p[1] * sin_angle
            y = p[0] * sin_angle + p[1] * cos_angle
            rotated.append((x, y))

        min_x = min(p[0] for p in rotated)
        max_x = max(p[0] for p in rotated)
        min_y = min(p[1] for p in rotated)
        max_y = max(p[1] for p in rotated)

        area = (max_x - min_x) * (max_y - min_y)

        if(area < best_area):
            best_area = area
            
            cos_back = math.cos(rot_angle)
            sin_back = math.sin(rot_angle)

            rect_points = [
                (min_x, min_y), (max_x, min_y), 
                (max_x, max_y), (min_x, max_y),
                (min_x, min_y)
            ]

            final_path = ogr.Geometry(ogr.wkbLinearRing)
            for rp in rect_points:
                x = rp[0] * cos_back - rp[1] * sin_back
                y = rp[0] * sin_back + rp[1] * cos_back
                final_path.AddPoint(x, y)
            
            best_rect = ogr.Geometry(ogr.wkbPolygon)
            best_rect.AddGeometry(final_path)
    
    return best_rect



input_file = "input/buildings.shp"
output_file = "output/result_mrr.shp"

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
        mrr_geom = mrr(feature_geom)

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

