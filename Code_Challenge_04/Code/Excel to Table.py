import arcpy

def excel_to_table(input_excel, output_gdb, output_table_name):
    """
    Converts an Excel file to a table file in a geodatabase.

    Args:
    input_excel (str): Path to the input Excel file.
    output_gdb (str): Path to the output geodatabase.
    output_table_name (str): Name of the output table in the geodatabase.
    """
    try:
        # Check out the ArcGIS Spatial Analyst extension license
        arcpy.CheckOutExtension("Spatial")

        # Convert Excel to table in the geodatabase
        arcpy.TableToTable_conversion(input_excel, output_gdb, output_table_name)

        print("Conversion completed successfully.")
    except arcpy.ExecuteError:
        print("ArcPy execution error occurred.")
    except arcpy.ExecuteError as e:
        print("An ArcPy specific error occurred:", str(e))
    except Exception as e:
        print("An error occurred during conversion:", str(e))

if __name__ == "__main__":
    # Example input Excel file path - replace with your actual file path
    input_excel_path = r"C:\GitHub\NRS_528\Code Challenge 04\Meshanticut Precipitation Data.csv"

    # Example output geodatabase path - replace with your desired output geodatabase path
    output_gdb_path = r"C:\GitHub\NRS_528\Code Challenge 04\Final"

    # Name of the output table in the geodatabase
    output_table_name = "output_table"

    # Call the excel_to_table function
    excel_to_table(input_excel_path, output_gdb_path, output_table_name)
