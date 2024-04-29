
# Advanced Conversion Toolbox. 
## This toolbox includes several tool classes for different conversion tasks. They include;
## TIFF to Shapefile.
This tool converts raster TIFF data to vector Shapefile format, facilitating further analysis and visualization in GIS applications.
## Adding XY coordinates to a Shapefile.
This tool facilitates the addition of XY coordinates to a point Shapefile, which can be crucial for spatial analysis and visualization tasks in GIS applications.
## Intersecting two Shapefiles.
This tool is designed to facilitate detailed spatial analysis by allowing users to easily identify and analyze the intersections between two spatial datasets.
## Converting Shapefile to GeoJSON.
This tool enables the integration of spatial data with applications,facilitating broader accessibility and usability of geographical information.
## Cleaning GeoJSON for Flutter.
This tool is to use GeoJSON files for use in mobile app development with Flutter, focusing on optimizing file size and data structure for better performance on mobile platforms.

*Overally, Each tool class has methods for parameter definition and execution, execute method of each tool performs the specified operation on the input data, checking the validity of input files using (arcpy.Describe and arcpy.Exists.), temporary files created during execution are deleted using (arcpy.Delete_management), the main function tests each tool's functionality with mock data paths, Print messages are printed during tool execution to provide feedback to the user*

# The results are as below:
![Image](https://i.imgur.com/wdWMqFhl.jpg)
