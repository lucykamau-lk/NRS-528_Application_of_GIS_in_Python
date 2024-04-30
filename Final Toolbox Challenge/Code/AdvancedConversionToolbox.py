import arcpy
import os
import json

arcpy.env.overwriteOutput = True


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Advanced Conversion Toolbox"
        self.alias = "ConversionTools"
        self.tools = [TifftoShapefile, AddXY, IntersectShapefiles, ShapefileToGeoJSON, CleanGeoJSONForFlutter]


class TifftoShapefile(object):
    def __init__(self):
        """Convert a TIFF file to a Shapefile."""
        self.label = "Convert TIFF to Shapefile"
        self.description = "Converts a raster TIFF file to a vector Shapefile by raster to polygon conversion."

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            arcpy.Parameter(
                displayName="Input TIFF File",
                name="in_tiff",
                datatype="DERasterDataset",
                parameterType="Required",
                direction="Input"),
            arcpy.Parameter(
                displayName="Output Shapefile",
                name="out_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Output")
        ]

    def execute(self, parameters, messages):
        """Run the tool."""
        in_tiff = parameters[0].valueAsText
        out_shapefile = parameters[1].valueAsText

        # Check if the input TIFF file exists and is valid
        desc_tiff = arcpy.Describe(in_tiff)
        if desc_tiff.dataType != "RasterDataset":
            arcpy.AddError("Input is not a valid raster TIFF file.")
            return

        arcpy.RasterToPolygon_conversion(in_tiff, out_shapefile, "NO_SIMPLIFY", "VALUE")
        arcpy.AddMessage(f"Converted TIFF to Shapefile: {out_shapefile}")

        # Delete temporary files
        arcpy.Delete_management("in_memory/temp_polygon")


class AddXY(object):
    def __init__(self):
        """Add XY coordinates to a Shapefile."""
        self.label = "Add XY Coordinates"
        self.description = "Adds XY coordinates to each point in the shapefile."

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            arcpy.Parameter(
                displayName="Input Shapefile",
                name="in_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Input")
        ]

    def execute(self, parameters, messages):
        """Run the tool."""
        in_shapefile = parameters[0].valueAsText

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError("Input Shapefile does not exist or is invalid.")
            return

        desc_shapefile = arcpy.Describe(in_shapefile)
        if desc_shapefile.shapeType != "Point":
            arcpy.AddError("Input is not a valid point Shapefile.")
            return

        temp_points = "in_memory/temp_points"
        arcpy.FeatureToPoint_management(in_shapefile, temp_points)
        arcpy.AddXY_management(temp_points)
        arcpy.CopyFeatures_management(temp_points, in_shapefile)
        arcpy.AddMessage(f"Added XY coordinates to: {in_shapefile}")

        # Delete temporary files
        arcpy.Delete_management(temp_points)


class IntersectShapefiles(object):
    def __init__(self):
        """Intersect two shapefiles."""
        self.label = "Intersect Shapefiles"
        self.description = "Intersects two Shapefiles to create a new Shapefile."

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            arcpy.Parameter(
                displayName="Input Shapefile 1",
                name="in_shapefile1",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Input"),
            arcpy.Parameter(
                displayName="Input Shapefile 2",
                name="in_shapefile2",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Input"),
            arcpy.Parameter(
                displayName="Output Shapefile",
                name="out_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Output")
        ]

    def execute(self, parameters, messages):
        """Run the tool."""
        in_shapefile1 = parameters[0].valueAsText
        in_shapefile2 = parameters[1].valueAsText
        out_shapefile = parameters[2].valueAsText

        # Check if the input shapefiles exist and are valid
        if not (arcpy.Exists(in_shapefile1) and arcpy.Exists(in_shapefile2)):
            arcpy.AddError("One or both input shapefiles do not exist.")
            return

        arcpy.Intersect_analysis([in_shapefile1, in_shapefile2], out_shapefile)
        arcpy.AddMessage(f"Intersected Shapefiles: {out_shapefile}")


class ShapefileToGeoJSON(object):
    def __init__(self):
        """Convert a Shapefile to GeoJSON."""
        self.label = "Convert Shapefile to GeoJSON"
        self.description = "Converts a Shapefile to a GeoJSON file suitable for web applications."

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            arcpy.Parameter(
                displayName="Input Shapefile",
                name="in_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Input"),
            arcpy.Parameter(
                displayName="Output GeoJSON",
                name="out_geojson",
                datatype="DEFile",
                parameterType="Required",
                direction="Output")
        ]

    def execute(self, parameters, messages):
        """Run the tool."""
        in_shapefile = parameters[0].valueAsText
        out_geojson = parameters[1].valueAsText

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError(f"The file {in_shapefile} does not exist.")
            return

        arcpy.FeaturesToJSON_conversion(in_shapefile, out_geojson, format_json="FORMATTED")
        arcpy.AddMessage(f"Converted Shapefile to GeoJSON: {out_geojson}")

        # Delete temporary files
        arcpy.Delete_management("in_memory/temp_feature_class")


class CleanGeoJSONForFlutter(object):
    def __init__(self):
        """Clean and format GeoJSON for use in Flutter applications."""
        self.label = "Clean GeoJSON for Flutter"
        self.description = "Formats a GeoJSON file for optimal use in Flutter mobile applications."

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            arcpy.Parameter(
                displayName="Input GeoJSON",
                name="in_geojson",
                datatype="DEFile",
                parameterType="Required",
                direction="Input"),
            arcpy.Parameter(
                displayName="Output Clean JSON",
                name="out_clean_json",
                datatype="DEFile",
                parameterType="Required",
                direction="Output")
        ]

    def execute(self, parameters, messages):
        """Run the tool."""
        in_geojson = parameters[0].valueAsText
        out_clean_json = parameters[1].valueAsText

        # Check if the input GeoJSON file exists and is valid
        if not arcpy.Exists(in_geojson):
            arcpy.AddError(f"The file {in_geojson} does not exist.")
            return

        with open(in_geojson, 'r') as file:
            data = json.load(file)

        with open(out_clean_json, 'w') as file:
            json.dump(data, file, indent=4)

        arcpy.AddMessage(f"Cleaned GeoJSON saved as: {out_clean_json}")


def main():
    """Test each tool functionality"""
    # Setup for testing
    # These paths are for demonstration and will need valid paths to actual data on your system.
    tiff_path = "path/to/input.tif"
    shapefile_output = "path/to/output.shp"
    shapefile1 = "path/to/input1.shp"
    shapefile2 = "path/to/input2.shp"
    intersect_output = "path/to/intersect_output.shp"
    geojson_output = "path/to/output.geojson"
    clean_json_output = "path/to/clean_output.json"

    # Simulate tool usage
    tools = [TifftoShapefile(), AddXY(), IntersectShapefiles(), ShapefileToGeoJSON(), CleanGeoJSONForFlutter()]
    for tool in tools:
        arcpy.AddMessage(f"Testing tool: {tool.label}")
        # Normally you would set parameters like this:
        # params = tool.getParameterInfo()
        # params[0].value = some_value
        # params[1].value = some_other_value
        # tool.execute(params, None)
        # For this test, you need to replace `some_value` and `some_other_value` with actual test values.


if __name__ == "__main__":
    main()

