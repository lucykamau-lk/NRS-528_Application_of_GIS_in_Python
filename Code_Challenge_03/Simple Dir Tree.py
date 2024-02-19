import os
import shutil

# Define the directory structure
directories = [
    "draft_code/pending",
    "draft_code/complete",
    "includes",
    "layouts/default",
    "layouts/post/posted",
    "site"
]

# Create directories
for directory in directories:
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno == os.errno.EEXIST:  # Directory already exists
            pass
        else:
            raise

print("Directory tree created successfully.")

# Delete directories
for directory in directories:
    try:
        shutil.rmtree(directory)
        print("Directory '{directory}' deleted successfully.")
    except OSError as e:
        print("Error: {e}")
