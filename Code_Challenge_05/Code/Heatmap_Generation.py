import arcpy
arcpy.env.overwriteOutput = True

# Set environment settings
arcpy.env.workspace = r"C:\GitHub\NRS_528\Code Challenge 05\Final_05"

# 1. Convert Step_3_Cepphus_grylle.csv to a shapefile.
in_Table = r"Step_3_Cepphus_grylle.csv"
x_coords = "lon"
y_coords = "lat"
out_Layer = "cepphus"
saved_Layer = r"Step_3_Cepphus_Output.shp"

# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, "")

# Print the total rows
print(arcpy.GetCount_management(out_Layer))

# Save to a layer file
arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print("Created file successfully!")

# 2. Extract the Extent, i.e. XMin, XMax, YMin, YMax of the generated shapefile
desc = arcpy.Describe(saved_Layer)
XMin = (-83.5869)
XMax = (-83.5869)
YMin = (+35.9181)
YMax = (60.3661 + 1)

# Set coordinate system of the output fishnet
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

outFeatureClass = "Step_3_Fishnet.shp"  # Name of output fishnet

# Set the origin of the fishnet
originCoordinate = str(XMin) + " " + str(YMin)  # Left bottom of our point data
yAxisCoordinate = str(XMax) + " " + str(YMax)   # This sets the orientation on the y-axis, so we head north
cellSizeWidth = "0.25"
cellSizeHeight = "0.25"
numRows = ""
numColumns = ""
oppositeCorner = str(-48.371) + " " + str(61.231)  # i.e. max x and max y coordinate
labels = "NO_LABELS"
templateExtent = "#"
geometryType = "POLYGON"  # Create a polygon, could be POLYLINE

arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                               cellSizeWidth, cellSizeHeight, numRows, numColumns,
                               oppositeCorner, labels, templateExtent, geometryType)

if arcpy.Exists(outFeatureClass):
    print("Created Fishnet file successfully!")

# 4. Undertake a Spatial Join to join the fishnet to the observed points.
target_features = "Step_3_Fishnet.shp"
join_features = "Step_3_Cepphus_Output.shp"
out_feature_class = "Step_3_HeatMap.shp"
join_operation = "JOIN_ONE_TO_ONE"
join_type = "KEEP_ALL"
field_mapping = ""
match_option = "INTERSECT"
search_radius = ""
distance_field_name = ""

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                           join_operation, join_type, field_mapping, match_option,
                           search_radius, distance_field_name)

# 5. Delete the intermediate files (e.g. species shapefile and fishnet).
intermediate_files = [saved_Layer, outFeatureClass]
for intermediate_file in intermediate_files:
    if arcpy.Exists(intermediate_file):
        arcpy.Delete_management(intermediate_file)
        print(f"Deleted intermediate file: {intermediate_file}")
