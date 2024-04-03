import arcpy

def describe_shp(input_shapefile):

    # Initialize variables
    shapetype = ""
    sprefname = ""
    spreftype = ""
    extent = None

    # Check if the input shapefile exists
    if arcpy.Exists(input_shapefile):
        # Get the description of the shapefile
        desc = arcpy.Describe(input_shapefile)
        print("Describing: " + str(input_shapefile))
        # Check if the data type is a ShapeFile
        if desc.dataType == "ShapeFile":
            # Get shape type, spatial reference name, and spatial reference type
            shapetype = desc.shapeType
            sprefname = desc.spatialReference.name
            spreftype = desc.spatialReference.type
            # Get the extent of the shapefile
            extent = desc.extent
        else:
            print("Input data not ShapeFile..")
    else:
        print("Dataset not found, please check the file path..")

    # Return shape type, spatial reference name, spatial reference type, and extent
    return shapetype, sprefname, spreftype, extent

def print_shapefile_info(shapetype, sprefname, spreftype, extent):

    # Print shape type, spatial reference name, spatial reference type, and extent
    print("Shape Type:", shapetype)
    print("Spatial Reference Name:", sprefname)
    print("Spatial Reference Type:", spreftype)
    print("Extent:", extent)

if __name__ == "__main__":
    # Example usage
    input_shapefile = r"C:\Users\Student\Desktop\Risk Maps\Risk Maps\Risk_022624_Kenya.shp"
    # Describe the shapefile and get its properties
    shapetype, sprefname, spreftype, extent = describe_shp(input_shapefile)
    # Print the properties of the shapefile
    print_shapefile_info(shapetype, sprefname, spreftype, extent)
