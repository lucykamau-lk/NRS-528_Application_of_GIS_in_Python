import arcpy
import os
import json
import tempfile

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
        self.label = "Convert TIFF to Shapefile: Step 1"
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

        # Create a temporary folder for intermediate outputs
        temp_dir = tempfile.mkdtemp()

        # Check if the input TIFF file exists and is valid
        if not arcpy.Exists(in_tiff):
            arcpy.AddError("Input TIFF file does not exist or is invalid.")
            return

        try:
            # Describe the input TIFF file
            desc_tiff = arcpy.Describe(in_tiff)
            if desc_tiff.dataType != "RasterDataset":
                arcpy.AddError("Input is not a valid raster TIFF file.")
                return

            # Define a common coordinate system (e.g., WGS 1984)
            coord_system = arcpy.SpatialReference(4326)  # WGS 1984

            # Project the raster to the common coordinate system
            projected_tiff = os.path.join(temp_dir, "projected_tiff.tif")
            arcpy.ProjectRaster_management(in_tiff, projected_tiff, coord_system)

            # Convert the projected raster to polygon (Shapefile)
            arcpy.RasterToPolygon_conversion(projected_tiff, out_shapefile, "NO_SIMPLIFY", "VALUE")
            arcpy.AddMessage("Conversion complete: " + out_shapefile)
        except arcpy.ExecuteError as e:
            arcpy.AddError(f"Error during conversion: {e}")
            arcpy.AddError(arcpy.GetMessages())

class AddXY(object):
    def __init__(self):
        """Tool for adding XY coordinates to each point in the shapefile"""
        self.label = "Add XY Coordinates: Step 2"
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

        # Create a temporary folder for intermediate outputs
        temp_dir = tempfile.mkdtemp()

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError("Input Shapefile does not exist or is invalid.")
            return

        try:
            # Define a common coordinate system (e.g., WGS 1984)
            coord_system = arcpy.SpatialReference(4326)  # WGS 1984

            # Project the shapefile to the common coordinate system
            projected_shapefile = os.path.join(temp_dir, "projected_shapefile.shp")
            arcpy.Project_management(in_shapefile, projected_shapefile, coord_system)

            temp_points = os.path.join(temp_dir, "temp_points.shp")
            arcpy.FeatureToPoint_management(projected_shapefile, temp_points)
            arcpy.AddXY_management(temp_points)
            arcpy.CopyFeatures_management(temp_points, out_shapefile)

            # Output message
            arcpy.AddMessage(f"XY coordinates added. Output shapefile saved as: {out_shapefile}")
        except arcpy.ExecuteError as e:
            arcpy.AddError(f"Error during adding XY coordinates: {e}")
            arcpy.AddError(arcpy.GetMessages())

class IntersectShapefiles(object):
    def __init__(self):
        """Tool for intersecting two shapefiles"""
        self.label = "Intersect Shapefiles: Step 3"
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

        # Create a temporary folder for intermediate outputs
        temp_dir = tempfile.mkdtemp()

        # Check if the input shapefiles exist and are valid
        if not arcpy.Exists(in_shapefile1):
            arcpy.AddError("Input Shapefile 1 does not exist or is invalid.")
            return
        if not arcpy.Exists(in_shapefile2):
            arcpy.AddError("Input Shapefile 2 does not exist or is invalid.")
            return

        try:
            # Define a common coordinate system (e.g., WGS 1984)
            coord_system = arcpy.SpatialReference(4326)  # WGS 1984

            # Project the shapefiles to the common coordinate system
            projected_shapefile1 = os.path.join(temp_dir, "projected_shapefile1.shp")
            projected_shapefile2 = os.path.join(temp_dir, "projected_shapefile2.shp")
            arcpy.Project_management(in_shapefile1, projected_shapefile1, coord_system)
            arcpy.Project_management(in_shapefile2, projected_shapefile2, coord_system)

            arcpy.Intersect_analysis([projected_shapefile1, projected_shapefile2], out_shapefile)
            arcpy.AddMessage("Intersection complete: " + out_shapefile)
        except arcpy.ExecuteError as e:
            arcpy.AddError(f"Error during intersection: {e}")
            arcpy.AddError(arcpy.GetMessages())

class CleanShapefile(object):
    def __init__(self):
        """Tool for cleaning a shapefile"""
        self.label = "Clean Shapefile: Step 4"
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
        fields_to_delete = parameters[1].values
        out_shapefile = parameters[2].valueAsText

        # Create a temporary folder for intermediate outputs
        temp_dir = tempfile.mkdtemp()

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError("Input Shapefile does not exist or is invalid.")
            return

        try:
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

            # Define a common coordinate system (e.g., WGS 1984)
            coord_system = arcpy.SpatialReference(4326)  # WGS 1984

            # Project the shapefile to the common coordinate system
            projected_shapefile = os.path.join(temp_dir, "projected_shapefile.shp")
            arcpy.Project_management(in_shapefile, projected_shapefile, coord_system)

            try:
                # Delete the specified fields from the attribute table
                arcpy.DeleteField_management(projected_shapefile, fields_to_delete)
                arcpy.AddMessage("Fields deleted successfully from: " + projected_shapefile)

                # Copy the cleaned shapefile to the output location
                arcpy.CopyFeatures_management(projected_shapefile, out_shapefile)
                arcpy.AddMessage("Cleaned shapefile saved as: " + out_shapefile)
            except arcpy.ExecuteError as e:
                arcpy.AddError(f"Error during field deletion: {e}")
                arcpy.AddError(arcpy.GetMessages())
        except arcpy.ExecuteError as e:
            arcpy.AddError(f"Error during processing: {e}")
            arcpy.AddError(arcpy.GetMessages())

class ShapefileToGeoJSON(object):
    def __init__(self):
        """Tool for converting Shapefile to GeoJSON"""
        self.label = "Convert Shapefile to GeoJSON: Step 5"
        self.description = "Converts a Shapefile to a GeoJSON file."

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
                displayName="Output GeoJSON",
                name="out_geojson",
                datatype="DEFile",
                parameterType="Required",
                direction="Output"
            )
        ]
        return params

    def execute(self, parameters, messages):
        print("Running tool: " + self.label)  # Print statement
        in_shapefile = parameters[0].valueAsText
        out_geojson = parameters[1].valueAsText

        # Create a temporary folder for intermediate outputs
        temp_dir = tempfile.mkdtemp()

        # Check if the input shapefile exists and is valid
        if not arcpy.Exists(in_shapefile):
            arcpy.AddError("Input Shapefile does not exist or is invalid.")
            return

        try:
            # Define a common coordinate system (e.g., WGS 1984)
            coord_system = arcpy.SpatialReference(4326)  # WGS 1984

            # Project the shapefile to the common coordinate system
            projected_shapefile = os.path.join(temp_dir, "projected_shapefile.shp")
            arcpy.Project_management(in_shapefile, projected_shapefile, coord_system)

            # Describe the input shapefile
            desc_shapefile = arcpy.Describe(projected_shapefile)
            if desc_shapefile.shapeType not in ["Point", "Polyline", "Polygon"]:
                arcpy.AddError("Input shapefile must be a point, polyline, or polygon shapefile.")
                return

            # Perform the conversion to GeoJSON
            temp_geojson = os.path.join(temp_dir, "temp_geojson.json")
            arcpy.FeaturesToJSON_conversion(in_features=projected_shapefile, out_json_file=temp_geojson, format_json="FORMATTED")

            # Save the GeoJSON to the output file
            arcpy.Copy_management(temp_geojson, out_geojson)

            arcpy.AddMessage("Shapefile converted to GeoJSON: " + out_geojson)
        except arcpy.ExecuteError as e:
            arcpy.AddError(f"Error during conversion: {e}")
            arcpy.AddError(arcpy.GetMessages())
        except Exception as e:
            arcpy.AddError(f"Unexpected error: {e}")


class StructuredGeoJSON(object):
    def __init__(self):
        self.label = "Structured GeoJSON: Step 6"
        self.description = "Formats a GeoJSON file to be easily readable by a Flutter application."

    def getParameterInfo(self):
        params = [
            arcpy.Parameter(displayName="Input GeoJSON",
                            name="in_geojson",
                            datatype="DEFile",
                            parameterType="Required",
                            direction="Input"),
            arcpy.Parameter(displayName="Output Structured JSON",
                            name="out_structured_json",
                            datatype="DEFile",
                            parameterType="Required",
                            direction="Output"),
            arcpy.Parameter(displayName="Decimal Points",
                            name="decimal_points",
                            datatype="GPLong",
                            parameterType="Required",
                            direction="Input")
        ]
        params[2].value = 7  # Default value for decimal points
        return params

    def execute(self, parameters, messages):
        print("Running tool: " + self.label)  # Print statement
        in_geojson = parameters[0].valueAsText
        out_structured_json = parameters[1].valueAsText
        decimal_points = parameters[2].valueAsText

        # Check if the input GeoJSON file exists and is valid
        if not arcpy.Exists(in_geojson):
            arcpy.AddError("Input GeoJSON file does not exist or is invalid.")
            return

        try:
            # Load GeoJSON data
            with open(in_geojson, 'r') as file:
                data = json.load(file)

            # Function to round coordinates to specified decimal points
            def round_coords(x, y):
                return round(x, decimal_points), round(y, decimal_points)

            # Round the coordinates in the GeoJSON to the specified decimal points
            for feature in data['features']:
                if 'geometry' not in feature:
                    arcpy.AddWarning("Feature without geometry found, skipping.")
                    continue
                geometry = feature['geometry']
                if 'x' in geometry and 'y' in geometry:
                    geometry['x'], geometry['y'] = round_coords(geometry['x'], geometry['y'])

            # Save structured JSON to output file
            with open(out_structured_json, 'w') as file:
                json.dump(data, file, indent=4)

            arcpy.AddMessage("Structured GeoJSON saved: " + out_structured_json)
        except Exception as e:
            arcpy.AddError(f"Unexpected error: {e}")

class StructuredGeoJSON(object):
    def __init__(self):
        self.label = "Structured GeoJSON: Step 6"
        self.description = "Formats a GeoJSON file to be easily readable by a Flutter application."

    def getParameterInfo(self):
        params = [
            arcpy.Parameter(displayName="Input GeoJSON",
                            name="in_geojson",
                            datatype="DEFile",
                            parameterType="Required",
                            direction="Input"),
            arcpy.Parameter(displayName="Output Structured JSON",
                            name="out_structured_json",
                            datatype="DEFile",
                            parameterType="Required",
                            direction="Output"),
            arcpy.Parameter(displayName="Decimal Points",
                            name="decimal_points",
                            datatype="GPLong",
                            parameterType="Required",
                            direction="Input")
        ]
        params[2].value = 7  # Default value for decimal points
        return params

    def execute(self, parameters, messages):
        print("Running tool: " + self.label)  # Print statement
        in_geojson = parameters[0].valueAsText
        out_structured_json = parameters[1].valueAsText
        decimal_points = int(parameters[2].valueAsText)  # Convert to integer

        # Check if the input GeoJSON file exists and is valid
        if not arcpy.Exists(in_geojson):
            arcpy.AddError("Input GeoJSON file does not exist or is invalid.")
            return

        try:
            # Load GeoJSON data
            with open(in_geojson, 'r') as file:
                data = json.load(file)

            # Function to round coordinates to specified decimal points
            def round_coords(x, y):
                return round(x, decimal_points), round(y, decimal_points)

            # Round the coordinates in the GeoJSON to the specified decimal points
            for feature in data['features']:
                if 'geometry' not in feature:
                    arcpy.AddWarning("Feature without geometry found, skipping.")
                    continue
                geometry = feature['geometry']
                if 'x' in geometry and 'y' in geometry:
                    geometry['x'], geometry['y'] = round_coords(geometry['x'], geometry['y'])
                if 'attributes' in feature and 'POINT_X' in feature['attributes'] and 'POINT_Y' in feature['attributes']:
                    feature['attributes']['POINT_X'], feature['attributes']['POINT_Y'] = round_coords(float(feature['attributes']['POINT_X']), float(feature['attributes']['POINT_Y']))

            # Save structured JSON to output file
            with open(out_structured_json, 'w') as file:
                json.dump(data, file, indent=4)

            arcpy.AddMessage("Structured GeoJSON saved: " + out_structured_json)
        except Exception as e:
            arcpy.AddError(f"Unexpected error: {e}")


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
