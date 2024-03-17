import os
from arcpy import env
from arcpy.sa import *

# Set environment settings
base_path_directory = r"C:\GitHub\NRS_528\Midterm Challenge\Modelling"
output_folder = r"C:\GitHub\NRS_528\Midterm Challenge\Modelling\Output"
env.workspace = base_path_directory
env.overwriteOutput = True

# Define input DEM file
dem_file = "Park_DEM.dt2"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Flow direction analysis
flow_dir = FlowDirection(os.path.join(env.workspace, dem_file))
print("Flow direction analysis successful.")

# Flow accumulation analysis
flow_acc = FlowAccumulation(flow_dir)
print("Flow accumulation analysis successful.")

# Save Flow Accumulation result in the output folder
flow_acc.save(os.path.join(output_folder, "FlowAcc_FlowDir1.tif"))

print("Flow accumulation result saved in the output folder.")

# Stream network delineation
stream_threshold = Con(flow_acc > 1000, 1)
stream_network = StreamLink(stream_threshold, flow_dir)
print("Stream network delineation successful.")

# Watershed delineation
out_watershed = Watershed(flow_dir, stream_network)
print("Watershed delineation successful.")

# Calculate slope and aspect
slope = Slope(dem_file)
aspect = Aspect(dem_file)
print("Slope and aspect calculations successful.")

# Identify drainage basins
basins = RegionGroup(out_watershed, "FOUR", "WITHIN", "NO_LINK")
print("Drainage basins identified.")

# Stream order analysis
stream_order = StreamOrder(stream_network, flow_dir)
print("Stream order analysis successful.")

# Floodplain mapping
floodplain = Con(IsNull(stream_network), 1, 0)
print("Floodplain mapping successful.")

# Save outputs in the output folder
flow_dir.save(os.path.join(output_folder, "flow_direction.tif"))
flow_acc.save(os.path.join(output_folder, "flow_accumulation.tif"))
stream_network.save(os.path.join(output_folder, "stream_network.tif"))
out_watershed.save(os.path.join(output_folder, "watershed.tif"))
slope.save(os.path.join(output_folder, "slope.tif"))
aspect.save(os.path.join(output_folder, "aspect.tif"))
basins.save(os.path.join(output_folder, "drainage_basins.tif"))
stream_order.save(os.path.join(output_folder, "stream_order.tif"))
floodplain.save(os.path.join(output_folder, "floodplain.tif"))

print("Hydrological modelling analysis completed, and files are saved.")
