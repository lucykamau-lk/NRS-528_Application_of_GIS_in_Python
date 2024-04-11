import arcpy

# Set workspace environment
arcpy.env.workspace = r"C:\GitHub\NRS_528\Code Challenge 09"

# Input dataset and fields
input_dataset = "RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp"
fields = ["Photo", "Species"]

# Queries to filter records
queries = {
    "with_photo": f"{fields[0]} IS NOT NULL AND {fields[0]} <> ''",
    "without_photo": f"{fields[0]} IS NULL OR {fields[0]} = ''"
}

# Initialize counter for records and a set for unique species
counters = {"with_photo": 0, "without_photo": 0}
unique_species = set()

# Process records based on photo presence and update counters and species set
for key, query in queries.items():
    with arcpy.da.SearchCursor(input_dataset, fields, query) as cursor:
        for row in cursor:
            counters[key] += 1
            unique_species.add(row[1])
    arcpy.Select_analysis(input_dataset, key, query)

# Print results
print(f"Records with Photos: {counters['with_photo']}")
print(f"Records Without Photos: {counters['without_photo']}")
print(f"Unique species in the dataset: {len(unique_species)}")

# Export shapefiles for records
output_dir = r"C:\GitHub\NRS_528\Code Challenge 09\Results"
arcpy.FeatureClassToShapefile_conversion(["with_photo", "without_photo"], output_dir)

print("Shapefiles generated for records with and without photos.")

