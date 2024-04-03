import arcpy
import os

def convert_kml_to_layer(kml_file, output_folder, layer_name="output_layer"):

    try:
        # Set workspace to output folder
        arcpy.env.workspace = output_folder
        # Define output layer file path
        output_layer = os.path.join(output_folder, f"{layer_name}.lyr")
        # Convert KML to layer
        arcpy.KMLToLayer_conversion(kml_file, output_folder)
        # Print success message
        print("Conversion completed successfully.")
        # Return path to output layer
        return output_layer
    except arcpy.ExecuteError as e:
        # Print ArcPy error
        print("ArcPy error:", e)
    except Exception as e:
        # Print other error during conversion
        print("Error during conversion:", e)

def print_layer_info(layer_file):

    # Get layer description
    desc = arcpy.Describe(layer_file)
    # Print layer information
    print("Layer Name:", desc.name)
    print("Data Type:", desc.dataType)
    print("Data Source:", desc.dataSource)
    print("Spatial Reference Name:", desc.spatialReference.name)

if __name__ == "__main__":
    # Example input KML file path
    kml_file_path = r"C:\GitHub\NRS_528\Application of Python in GIS Classes\Class_08\Code Challenge 08\Watershed.kml"
    # Output folder path
    output_folder_path = r"C:\GitHub\NRS_528\Application of Python in GIS Classes\Class_08\Code Challenge 08\Output"
    # Output layer name
    layer_name = "watershed_layer"

    # Convert KML to layer
    layer_file_path = convert_kml_to_layer(kml_file_path, output_folder_path, layer_name)


