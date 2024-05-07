
import arcpy
import os
import json

# Set up environment to allow overwriting output files
arcpy.env.overwriteOutput = True

class Toolbox(object):
    def __init__(self):
        """Toolbox definition with a list of tools"""
        self.label = "Advanced Conversion Toolbox"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [TifftoShapefile, AddXY, IntersectShapefiles, CleanShapefile, ShapefileToGeoJSON, StructuredGeoJSON]

class TifftoShapefile(object):
    def __init__(self):
        """Tool for converting TIFF to Shapefile"""
        self.label = "Convert TIFF to Shapefile"
        self.description = "Converts a raster TIFF file to a vector Shapefile by raster to polygon conversion."

    def getParameterInfo(self):
        """Parameter definitions for the tool"""
        params = [arcpy.Parameter(displayName="Input TIFF File",
                                  name="in_tiff",
                                  datatype="DERasterDataset",
                                  parameterType="Required",
                                  direction="Input"),
                  arcpy.Parameter(displayName="Output Shapefile",
                                  name="out_shapefile",
                                  datatype="DEShapefile",
                                  parameterType="Required",
                                  direction="Output")]
        return params

    def execute(self, parameters, messages):
        """Execution of converting TIFF to Shapefile"""
        in_tiff = parameters[0].valueAsText
        out_shapefile = parameters[1].valueAsText

        # Check if the input TIFF file exists and is valid
        if not arcpy.Exists(in_tiff):
            arcpy.AddError("Input TIFF file does not exist or is invalid.")
            return

        # Describe the input TIFF file
        desc_tiff = arcpy.Describe(in_tiff)
        if desc_tiff.dataType != "RasterDataset":
            arcpy.AddError("Input is not a valid raster TIFF file.")
            return

        arcpy.RasterToPolygon_conversion(in_tiff, out_shapefile, "NO_SIMPLIFY", "VALUE")
        print("Conversion complete: " + out_shapefile)

class AddXY(object):
    def __init__(self):
        """Tool for adding XY coordinates to each point in the shapefile"""
        self.label = "Add XY Coordinates"
        self.description = "Adds XY coordinates to each point in the shapefile."

    def getParameterInfo(self):
        """Parameter definitions for the tool"""
        params = [
            arcpy.Parameter(
                displayName="Input Shapefile",
                name="in_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Output Shapefile",
                name="out_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Output"
            )
        ]
        return params

    def execute(self, parameters, messages):
        """Execution of adding XY coordinates"""
        in_shapefile = parameters[0].valueAsText
        out_shapefile = parameters[1].valueAsText

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError("Input Shapefile does not exist or is invalid.")
            return

        temp_points = "in_memory/temp_points"
        arcpy.FeatureToPoint_management(in_shapefile, temp_points)
        arcpy.AddXY_management(temp_points)
        arcpy.CopyFeatures_management(temp_points, out_shapefile)

        # Output message
        arcpy.AddMessage(f"XY coordinates added. Output shapefile saved as: {out_shapefile}")

class IntersectShapefiles(object):
    def __init__(self):
        """Tool for intersecting two shapefiles"""
        self.label = "Intersect Shapefiles"
        self.description = "Intersects two Shapefiles."

    def getParameterInfo(self):
        """Parameter definitions for the tool"""
        params = [arcpy.Parameter(displayName="Input Shapefile 1",
                                  name="in_shapefile1",
                                  datatype="DEShapefile",
                                  parameterType="Required",
                                  direction="Input"),
                  arcpy.Parameter(displayName="Input Shapefile 2",
                                  name="in_shapefile2",
                                  datatype="DEShapefile",
                                  parameterType="Required",
                                  direction="Input"),
                  arcpy.Parameter(displayName="Output Shapefile",
                                  name="out_shapefile",
                                  datatype="DEShapefile",
                                  parameterType="Required",
                                  direction="Output")]
        return params

    def execute(self, parameters, messages):
        """Execution of intersecting shapefiles"""
        print("Running tool: " + self.label)  # Print statement
        in_shapefile1 = parameters[0].valueAsText
        in_shapefile2 = parameters[1].valueAsText
        out_shapefile = parameters[2].valueAsText

        # Check if the input shapefiles exist and are valid
        if not arcpy.Exists(in_shapefile1):
            arcpy.AddError("Input Shapefile 1 does not exist or is invalid.")
            return
        if not arcpy.Exists(in_shapefile2):
            arcpy.AddError("Input Shapefile 2 does not exist or is invalid.")
            return

        arcpy.Intersect_analysis([in_shapefile1, in_shapefile2], out_shapefile)
        print("Intersection complete: " + out_shapefile)

class CleanShapefile(object):
    def __init__(self):
        """Tool for cleaning a shapefile"""
        self.label = "Clean Shapefile"
        self.description = "Deletes specified fields from the attribute table of a shapefile."

    def getParameterInfo(self):
        """Parameter definitions for the tool"""
        params = [
            arcpy.Parameter(
                displayName="Input Shapefile",
                name="in_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Fields to Delete",
                name="fields_to_delete",
                datatype="GPString",
                parameterType="Required",
                direction="Input",
                multiValue=True
            ),
            arcpy.Parameter(
                displayName="Output Shapefile",
                name="out_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Output"
            )
        ]
        return params

    def execute(self, parameters, messages):
        """Execution of deleting fields from the attribute table"""
        in_shapefile = parameters[0].valueAsText
        fields_to_delete = parameters[1].values  # List of field names to delete
        out_shapefile = parameters[2].valueAsText  # Output shapefile path

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError("Input Shapefile does not exist or is invalid.")
            return

        # Describe the input shapefile
        desc_shapefile = arcpy.Describe(in_shapefile)
        field_names = [field.name for field in desc_shapefile.fields]

        # Check if any fields are selected for deletion
        if not fields_to_delete:
            arcpy.AddError("No fields selected for deletion.")
            return

        # Check if fields to delete exist in the input shapefile
        non_existing_fields = [field for field in fields_to_delete if field not in field_names]
        if non_existing_fields:
            arcpy.AddError(f"The following fields do not exist in the input shapefile: {', '.join(non_existing_fields)}")
            return

        try:
            # Delete the specified fields from the attribute table
            arcpy.DeleteField_management(in_shapefile, fields_to_delete)
            arcpy.AddMessage("Fields deleted successfully from: " + in_shapefile)

            # Copy the cleaned shapefile to the output location
            arcpy.CopyFeatures_management(in_shapefile, out_shapefile)
            arcpy.AddMessage("Cleaned shapefile saved as: " + out_shapefile)
        except arcpy.ExecuteError as e:
            arcpy.AddError(f"Error: {e}")

class ShapefileToGeoJSON(object):
    def __init__(self):
        """Tool for converting Shapefile to GeoJSON"""
        self.label = "Convert Shapefile to GeoJSON"
        self.description = "Converts a Shapefile to a GeoJSON file."

    def getParameterInfo(self):
        """Parameter definitions for the tool"""
        params = [arcpy.Parameter(displayName="Input Shapefile",
                                  name="in_shapefile",
                                  datatype="DEShapefile",
                                  parameterType="Required",
                                  direction="Input"),
                  arcpy.Parameter(displayName="Output GeoJSON",
                                  name="out_geojson",
                                  datatype="DEFile",
                                  parameterType="Required",
                                  direction="Output")]
        return params

    def execute(self, parameters, messages):
        print("Running tool: " + self.label)  # Print statement
        in_shapefile = parameters[0].valueAsText
        out_geojson = parameters[1].valueAsText

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError("Input Shapefile does not exist or is invalid.")
            return

        # Describe the input shapefile
        desc_shapefile = arcpy.Describe(in_shapefile)
        if desc_shapefile.shapeType not in ["Point", "Polyline", "Polygon"]:
            arcpy.AddError("Input shapefile must be a point, polyline, or polygon shapefile.")
            return

        # Perform the conversion
        arcpy.FeaturesToJSON_conversion(in_features=in_shapefile, out_json_file=out_geojson,
                                        format_json="FORMATTED")
        print("Shapefile converted to GeoJSON: " + out_geojson)

class StructuredGeoJSON(object):
    def __init__(self):
        self.label = "Structured GeoJSON"
        self.description = "Formats a GeoJSON file to be easily readable by a Flutter application."

    def getParameterInfo(self):
        params = [arcpy.Parameter(displayName="Input GeoJSON",
                                  name="in_geojson",
                                  datatype="DEFile",
                                  parameterType="Required",
                                  direction="Input"),
                  arcpy.Parameter(displayName="Output Structured JSON",
                                  name="out_structured_json",
                                  datatype="DEFile",
                                  parameterType="Required",
                                  direction="Output")]
        return params

    def execute(self, parameters, messages):
        print("Running tool: " + self.label)  # Print statement
        in_geojson = parameters[0].valueAsText
        out_structured_json = parameters[1].valueAsText

        # Check if the input GeoJSON file exists and is valid
        if not arcpy.Exists(in_geojson):
            arcpy.AddError("Input GeoJSON file does not exist or is invalid.")
            return

        # Load GeoJSON data
        with open(in_geojson, 'r') as file:
            data = json.load(file)

        # Perform structuring operations on the data

        # Save structured JSON to output file
        with open(out_structured_json, 'w') as file:
            json.dump(data, file, indent=4)


def main():
    """Main function to run the toolbox"""
    toolbox = Toolbox()
    for tool_class in toolbox.tools:
        tool = tool_class()
        print(f"Running tool: {tool.label}")
        params = tool.getParameterInfo()
        # Implement additional logic as needed for parameters

if __name__ == '__main__':
    main()

