import arcpy
import os
def convert_data(input_excel_file, output_folder):
    try:
        arcpy.env.workspace = output_folder
        arcpy.CheckOutExtension("Spatial")
        arcpy.TableToTable_conversion(input_excel_file, output_folder, "output_table")

        print("Conversion completed successfully.")
    except arcpy.ExecuteError:
        print("ArcPy execution error occurred.")
    except arcpy.ExecuteError as e:
        print("An ArcPy specific error occurred:", str(e))
    except Exception as e:
        print("An error occurred during conversion:", str(e))

if __name__ == "__main__":
    input_excel_path = r"C:\GitHub\NRS_528\Trial_04\Meshanticut Precipitation Data.csv"
    output_folder_path = r"C:\GitHub\NRS_528\Trial_04\Excel to table"

    convert_data(input_excel_path, output_folder_path)
