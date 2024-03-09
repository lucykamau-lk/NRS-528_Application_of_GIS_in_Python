import arcpy
arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"C:\GitHub\NRS_528\Code Challenge 05\Final_05"

in_Table = r"Step_3_Cepphus_grylle.csv"
x_coords = "lon"
y_coords = "lat"
out_Layer = "cepphus"
saved_Layer = r"Step_3_Cepphus_Output.shp"


spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, "")

print(arcpy.GetCount_management(out_Layer))

arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print("Created file successfully!")

desc = arcpy.Describe(saved_Layer)
XMin = desc.extent.XMin
XMax = desc.extent.XMax
YMin = desc.extent.YMin
YMax = desc.extent.YMax

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

outFeatureClass = "Step_3_Fishnet.shp"

originCoordinate = str(-83.5869) + " " + str(35.9181)
yAxisCoordinate = str(-83.5869) + " " + str(60.3661 + 1)
cellSizeWidth = "0.25"
cellSizeHeight = "0.25"
numRows = ""
numColumns = ""
oppositeCorner = str(-48.371) + " " + str(61.231)
labels = "NO_LABELS"
templateExtent = "#"
geometryType = "POLYGON"

arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                               cellSizeWidth, cellSizeHeight, numRows, numColumns,
                               oppositeCorner, labels, templateExtent, geometryType)

if arcpy.Exists(outFeatureClass):
    print("Created Fishnet file successfully!")


target_features="Step_3_Fishnet.shp"
join_features="Step_3_Cepphus_Output.shp"
out_feature_class="Step_3_HeatMap.shp"
join_operation="JOIN_ONE_TO_ONE"
join_type="KEEP_ALL"
field_mapping=""
match_option="INTERSECT"
search_radius=""
distance_field_name=""

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                           join_operation, join_type, field_mapping, match_option,
                           search_radius, distance_field_name)


if arcpy.Exists(out_feature_class):
    print("Created Heatmap file successfully!")
    print("Deleting intermediate files")
