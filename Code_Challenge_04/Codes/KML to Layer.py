import arcpy
import os

def convert_data(kml_file, output_folder):
    try:
        arcpy.env.workspace = output_folder
        os.path.join(output_folder, "output_layer.lyr")
        arcpy.KMLToLayer_conversion(kml_file, output_folder)
        
        print("Conversion completed successfully.")
    except arcpy.ExecuteError as e:
        print("An ArcPy error occurred:", e)
    except Exception as e:
        print("An error occurred during conversion:", e)

if __name__ == "__main__":
    # Example input KML file path - replace with your actual file path
    kml_file_path = r"C:\GitHub\NRS_528\Trial_04\Watershed.kml"
    # Output layer file path - replace with your desired output layer path
    output_folder_path = r"C:\GitHub\NRS_528\Trial_04\KML to Layer"

    # Call the conversion function
    convert_data(kml_file_path, output_folder_path)
