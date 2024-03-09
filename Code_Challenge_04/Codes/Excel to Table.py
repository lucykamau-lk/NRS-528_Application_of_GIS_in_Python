import arcpy
import os

def excel_to_table(input_excel, output_gdb, output_table_name):
    pass
    try:
        arcpy.env.workspace = os.getcwd()
        arcpy.CheckOutExtension("Spatial")
        arcpy.TableToTable_conversion(input_excel, output_gdb, output_table_name)

        print("Conversion completed successfully.")
    except arcpy.ExecuteError:
        print("ArcPy execution error occurred.")
    except arcpy.ExecuteError as e:
        print("An ArcPy specific error occurred:", str(e))
    except Exception as e:
        print("An error occurred during conversion:", str(e))

if __name__ == "__main__":
    input_excel_path = r"C:\GitHub\NRS_528\Trial_04\Meshanticut Precipitation Data.csv"

    output_gdb_path = r"C:\GitHub\NRS_528\Trial_04\Excel to table"

    output_table_name = "output_table"

    excel_to_table(input_excel_path, output_gdb_path, output_table_name)
