import arcpy
import os

def convert_data(kml_file, output_folder):
    """
    Converts a KML file to a layer file in ArcGIS.

    Args:
    kml_file (str): Path to the input KML file.
    output_layer (str): Path to save the output layer file.
    """
    # Set up the workspace environment
    arcpy.env.workspace = output_folder

    # Output layer file name
    output_layer = os.path.join(output_folder, "output_layer.lyr")

    try:
        # Perform data conversion
        arcpy.KMLToLayer_conversion(kml_file,output_folder)

        print("Conversion completed successfully.")
    except arcpy.ExecuteError:
        print("ArcPy execution error occurred.")
    except arcpy.ExecuteError as e:
        print("An ArcPy specific error occurred:", str(e))
    except Exception as e:
        print("An error occurred during conversion:", str(e))


if __name__ == "__main__":
    # Example input KML file path - replace with your actual file path
    kml_file_path = r"C:\GitHub\NRS_528\Code Challenge 04\Watershed.kml"

    # Output layer file path - replace with your desired output layer path
    output_folder_path = r"C:\GitHub\NRS_528\Code Challenge 04\Results"


    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Call the conversion function
    convert_data(kml_file_path, output_folder_path)
