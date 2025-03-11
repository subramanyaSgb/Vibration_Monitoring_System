import os
import json
from PIL import Image

# Default data for the files
default_data = {
    "cameras.json": {
        "CAM1": 0
    },
    "config.json": {
        "mes_score":100,
        "fps": 20,
        "video_duration": 180,
        "stable_threshold": 5,
        "motion_blur": True
    },
    "roi.json": {
        "roi": {
            "x": 150,
            "y": 250,
            "width": 400,
            "height": 300
        }
    },
    "storage_limit.json": {
        "storage_limit": 30
    }
}

def create_placeholder_logo(path):
    # Create a blank white image as a placeholder for the logo
    img = Image.new('RGB', (100, 100), color='white')  # You can change size and color
    img.save(path)
    print(f"logo.png created as a placeholder.")

def check_and_create_files():
    # Path to the 'data' folder
    data_folder = "data"
    
    # Check if the 'data' folder exists, if not, create it
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Iterate over each file and check if it exists
    for filename, data in default_data.items():
        file_path = os.path.join(data_folder, filename)
        
        # If the file doesn't exist, create it with the default data
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"{filename} created with default data.")
        else:
            print(f"{filename} already exists.")
    
    # Check and create logo.png if it doesn't exist
    logo_path = os.path.join(data_folder, "logo.png")
    if not os.path.exists(logo_path):
        create_placeholder_logo(logo_path)
    else:
        print("logo.png already exists.")

if __name__ == "__main__":
    # Run the function
    check_and_create_files()
