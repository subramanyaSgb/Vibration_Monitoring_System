from cx_Freeze import setup, Executable
import os

# Define the base options for the executable
base = None
# if os.name == "nt":
#     base = "Win32GUI"  # Use "Win32GUI" for a Windows GUI application

# Define the executable
executables = [Executable("app.py", base=base)]

# Define the options for the build
build_options = {
    "packages": ["cv2", "time", "numpy", "os", "datetime", "json", "traceback"],
    "includes": ["cam", "logging_config", "database", "plc", "file_verifier"],
    "include_files": [
        ("data/storage_limit.json", "data/storage_limit.json"),
        ("data/roi.json", "data/roi.json"),
        ("data/logo.png", "data/logo.png"),
        ("data/config.json", "data/config.json"),
        ("data/cameras.json", "data/cameras.json")
    ],
    "excludes": [],
    "optimize": 2
}

# Setup the cx_Freeze configuration
setup(
    name="VibrationDetectionSystem",
    version="1.0",
    description="Vibration Detection System",
    options={"build_exe": build_options},
    executables=executables
)
