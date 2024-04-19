import os
import arcpy

# Setup
arcpy.env.overwriteOutput = True
data_directory = r'C:\GitHub\NRS_528\Code Challenge 10\Landsat_data_Ifs'
output_directory = os.path.join(data_directory, 'output')

# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Print available folders
list_input = os.listdir(data_directory)
print("Folders available: " + str(list_input))

# Iterate over each subfolder
for data in list_input:
    folder_path = os.path.join(data_directory, data)
    arcpy.env.workspace = folder_path
    list_raster = arcpy.ListRasters("*", "TIF")

    print(f"Gathering all raster files in {arcpy.env.workspace}...")
    if not list_raster:
        print("No raster files found in the directory.")
        continue

    print("Searching for Band 4 and Band 5...")
    band_4_rasters = [x for x in list_raster if "B4" in x]
    band_5_rasters = [x for x in list_raster if "B5" in x]

    if not band_4_rasters or not band_5_rasters:
        print("Required bands are not found in the folder.")
        continue

    try:
        # Assume one band 4 and band 5 per folder
        band_4_raster = band_4_rasters[0]
        band_5_raster = band_5_rasters[0]
        band_4 = arcpy.Raster(band_4_raster)
        band_5 = arcpy.Raster(band_5_raster)

        print("Calculating NDVI...")
        NDVI = (band_5 - band_4) / (band_5 + band_4)
        output_path = os.path.join(output_directory, f"output_{data}.tif")
        NDVI.save(output_path)

        if arcpy.Exists(output_path):
            print(f"NDVI Calculated Successfully for {output_path}")
        else:
            print("Failed to save the NDVI raster.")

        # Delete unwanted files
        print("Deleting unwanted files...")
        arcpy.Delete_management(band_4_raster)
        arcpy.Delete_management(band_5_raster)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
