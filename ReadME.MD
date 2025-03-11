# JSW Bellary BF2 Vibration Monitoring System

## Table of Contents
1. [Introduction](#introduction)
   - [Project Overview](#project-overview)
   - [System Architecture](#system-architecture)
2. [Requirements](#requirements)
   - [Hardware Requirements](#hardware-requirements)
   - [Software Requirements](#software-requirements)
   - [Dependencies](#dependencies)
3. [Setup and Installation](#setup-and-installation)
   - [Environment Setup](#environment-setup)
   - [Configuration](#configuration)
   - [Running the Application](#running-the-application)
4. [File Structure](#file-structure)
5. [Module Documentation](#module-documentation)
   - [app.py (Main Application)](#apppy-main-application)
   - [cam.py (Camera Module)](#campy-camera-module)
   - [plc.py (PLC Communication Module)](#plcpy-plc-communication-module)
   - [database.py (Database Operations)](#databasepy-database-operations)
   - [logging_config.py (Logging Configuration)](#logging_configpy-logging-configuration)
   - [file_verifier.py (File Verification)](#file_verifierpy-file-verification)
6. [Configuration Files](#configuration-files)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)
9. [References](#references)

## Introduction

### Project Overview

The JSW Bellary BF2 Vibration Monitoring System is designed to monitor and detect vibrations in Blast Furnace 2 at JSW Bellary Steel Plant. The system utilizes camera-based vibration detection techniques to identify abnormal vibration patterns, which may indicate potential issues in the blast furnace operation. When vibrations are detected or when they stop, the system interacts with Programmable Logic Controllers (PLCs) to signal control systems and logs these events in a PostgreSQL database for historical analysis and reporting.

The system provides a real-time monitoring interface that displays camera feeds with visual indicators for vibration status. It also records video footage during vibration events for later analysis, with a configurable storage management system to handle disk space constraints.

### System Architecture

The Vibration Monitoring System is built with a modular architecture consisting of the following core components:

1. **Camera Monitoring**: Utilizes RTSP camera feeds with OpenCV to capture and process video streams.
2. **Vibration Detection Algorithm**: Analyzes frame-to-frame differences within configured Regions of Interest (ROI) to detect vibration patterns.
3. **PLC Interface**: Communicates with industrial PLCs via Modbus ASCII protocol to signal control systems.
4. **Database System**: PostgreSQL database for storing vibration event data, including timestamps of when vibrations stop.
5. **Logging System**: Comprehensive logging with automatic rotation for system monitoring and diagnostics.
6. **Video Recording**: Automatically captures and organizes video recordings of vibration events.

The system's modular design allows for easy maintenance, configuration, and extension of functionality.

## Requirements

### Hardware Requirements

- Server/PC with:
  - Intel Core i5 processor or better
  - Minimum 8GB RAM
  - At least 100GB of available disk space
  - Network interface card for camera connectivity
  - Serial port (COM port) for PLC communication
- Network cameras with RTSP stream capability
- PLC system with Modbus ASCII protocol support
- Network infrastructure for camera and system connectivity

### Software Requirements

- Windows 10 or later (64-bit)
- Python 3.7 or later
- PostgreSQL database server
- OpenCV 4.x
- Appropriate camera firmware with RTSP support

### Dependencies

The system relies on the following Python packages:
- OpenCV (`cv2`): For camera operations and image processing
- NumPy: For numerical operations and array handling
- minimalmodbus: For PLC communication via Modbus ASCII protocol
- psycopg2: For PostgreSQL database connectivity
- Standard Python libraries:
  - datetime: For timestamp management
  - threading: For multi-threaded camera handling
  - json: For configuration file parsing
  - os, shutil: For file system operations
  - time: For timing operations
  - logging: For system-wide logging

All dependencies are listed in the `requirements.txt` file.

## Setup and Installation

### Environment Setup

1. **Install Python 3.7 or later**
   ```
   # Download from https://www.python.org/downloads/
   ```

2. **Create a virtual environment named "vms"**
   ```bash
   python -m venv vms
   ```

3. **Activate the virtual environment**
   - Windows:
     ```
     vms\Scripts\activate
     ```
   - Linux/MacOS:
     ```
     source vms/bin/activate
     ```

4. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install PostgreSQL**
   - Download from https://www.postgresql.org/download/
   - Install with default settings
   - Create a user with username "postgres" and password "root"

### Configuration

1. **Camera Configuration**
   - Create/edit `data/cameras.json` with the following format:
     ```json
     {
       "camera_serial_number_1": "rtsp://camera_ip_1:port/stream",
       "camera_serial_number_2": "rtsp://camera_ip_2:port/stream"
     }
     ```

2. **ROI Configuration**
   - Create/edit `data/roi.json` with the following format:
     ```json
     {
       "x": 100,
       "y": 100,
       "width": 500,
       "height": 300
     }
     ```

3. **System Configuration**
   - Create/edit `data/config.json` with the following format:
     ```json
     {
       "mes_score": 50,
       "fps": 20,
       "video_duration": 180,
       "stable_threshold": 5,
       "motion_blur": true
     }
     ```

4. **Storage Limit Configuration**
   - Create/edit `data/storage_limit.json` with the following format:
     ```json
     {
       "limit_gb": 30
     }
     ```

5. **PLC Configuration**
   - The PLC connection is configured in `plc.py` with the following default settings:
     - Serial port: COM7
     - Baud rate: 9600
     - Data bits: 7
     - Parity: Even
     - Stop bits: 1
   - Modify these settings in the `connectToPLC` method if needed

### Running the Application

1. **Using run.bat (recommended)**
   - Simply double-click the `run.bat` file
   - This activates the "vms" environment and runs app.py

2. **Manual execution**
   ```bash
   call activate vms
   python app.py
   ```

3. **Exit the application**
   - Press 'q' key when the application window is in focus to exit cleanly

## File Structure

```
VMS_BF2_07_12_2024/
│
├── app.py                  # Main application entry point
├── cam.py                  # Camera connection and management
├── plc.py                  # PLC communication module
├── database.py             # Database operations
├── logging_config.py       # Logging system configuration
├── file_verifier.py        # File and directory verification
├── requirements.txt        # Python dependencies
├── run.bat                 # Application launcher script
│
├── data/                   # Configuration files
│   ├── cameras.json        # Camera RTSP URLs
│   ├── config.json         # System configuration
│   ├── roi.json            # Region of Interest settings
│   └── storage_limit.json  # Storage management settings
│
├── logs/                   # Application logs (created at runtime)
│   └── VMS_YYYY-MM-DD.log  # Daily log files
│
└── results/                # Recorded videos (created at runtime)
    └── videos/
        └── YYYY-MM-DD/     # Date-organized folders
            └── HH-MM-SS.avi # Time-stamped video files
```

## Module Documentation

### app.py (Main Application)

This is the primary entry point for the application that coordinates all subsystems.

#### Class: `VideoProcessor`

##### `__init__(self, mes_score=50, fps=10, video_duration=180, stable_threshold=1, motion_blur=True)`
- **Purpose**: Initializes the Vibration Detection System with configuration parameters
- **Parameters**:
  - `mes_score` (int, default=50): Threshold for motion energy score to detect vibrations
  - `fps` (int, default=10): Frames per second for video processing
  - `video_duration` (int, default=180): Duration of recorded video in seconds
  - `stable_threshold` (int, default=1): Threshold for determining stability in seconds
  - `motion_blur` (bool, default=True): Enable/disable motion blur detection
- **Attributes**:
  - `MOTION_BLUR`: Flag to enable/disable motion blur detection
  - `FPS`: Frames per second for video processing
  - `VIDEO_DURATION`: Duration of video recording in seconds
  - `stable_time`: Counter for tracking stable duration before detecting vibration
  - `STABLE_THRESHOLD`: Threshold in seconds to determine if an object is stable
  - `mes_score`: Motion energy score threshold for vibration detection
  - `cnt_frame`: Counter for processed frames
  - `fps`: Current processing frames per second
  - `frame_dict`: Dictionary to store frames from cameras
  - `camera_threads`: List storing active camera threads
  - `video_writer`: Video writer object for saving recordings
  - `start_time`: Timestamp when system was initialized
  - `video_start_time`: Timestamp when video recording started
  - `frame_gray_p`: Previous grayscale frame for comparison
  - `title`: System interface title
  - `last_saved_time`: Timestamp of last saved video/frame
  - `roi`: Region of interest configuration
  - `fps_for_frame`: FPS counter for individual frames
  - `last_plc_signal_time`: Timestamp of last PLC signal
- **Database Initialization**: Calls `create_db_if_not_exists()` and `create_table_if_not_exists()`
- **Usage**:
  ```python
  processor = VideoProcessor(mes_score=30, fps=15, video_duration=300, stable_threshold=2)
  ```

##### `load_storage_limit(self)`
- **Purpose**: Loads storage limit from configuration file
- **Returns**: Storage limit in GB (default: 30GB)
- **File Source**: 'data/storage_limit.json'
- **Process**:
  1. Attempts to read and parse JSON from storage_limit.json
  2. Extracts the 'limit_gb' value
- **Exception Handling**: Returns default value (30GB) if file is missing or corrupt
- **Usage**:
  ```python
  storage_limit = processor.load_storage_limit()
  print(f"Current storage limit is {storage_limit} GB")
  ```

##### `check_storage(self)`
- **Purpose**: Checks available disk space against the configured limit
- **Returns**: Boolean (True if sufficient space, False if below limit)
- **Process**: 
  1. Loads storage limit from configuration
  2. Checks available disk space using shutil.disk_usage
  3. Compares available space to limit
  4. Logs warning if space is low
- **Usage**:
  ```python
  if processor.check_storage():
      # Proceed with recording
  else:
      # Display warning or stop recording
  ```

##### `load_roi(self)`
- **Purpose**: Loads Region of Interest (ROI) configuration from file
- **Returns**: ROI configuration as dictionary with keys 'x', 'y', 'width', 'height'
- **File Source**: 'data/roi.json'
- **Process**:
  1. Attempts to read and parse JSON from roi.json
  2. Validates that required keys exist
- **Exception Handling**: Logs error and returns None if file is missing or invalid
- **Usage**:
  ```python
  roi = processor.load_roi()
  if roi:
      x, y, width, height = roi['x'], roi['y'], roi['width'], roi['height']
      cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
  ```

##### `add_camera(self, cam_serial_num, rtsp_path)`
- **Purpose**: Adds and initializes a camera connection
- **Parameters**:
  - `cam_serial_num`: Camera serial number identifier
  - `rtsp_path`: RTSP URL for camera connection
- **Process**:
  1. Creates a CameraThread with given serial number and RTSP path
  2. Adds thread to camera_threads list
  3. Starts the thread for capturing frames
- **Exception Handling**: Logs error if camera addition fails
- **Usage**:
  ```python
  processor.add_camera("CAM001", "rtsp://192.168.1.100:554/stream")
  ```

##### `create_video_writer(self, output_path)`
- **Purpose**: Creates a video writer object for recording
- **Parameters**:
  - `output_path`: Path where video will be saved
- **Returns**: OpenCV VideoWriter object
- **Configuration**:
  - Codec: XVID
  - Frame size: 1920x1080
  - FPS: Uses the configured FPS value
- **Exception Handling**: Logs error and re-raises if creation fails
- **Usage**:
  ```python
  writer = processor.create_video_writer("path/to/output.avi")
  ```

##### `mse(self, image_a, image_b)`
- **Purpose**: Calculates Mean Squared Error between two images
- **Parameters**:
  - `image_a`: First image for comparison
  - `image_b`: Second image for comparison
- **Returns**: MSE value (float)
- **Process**:
  1. Calculates squared difference between pixel values
  2. Averages the differences
- **Used For**: Detecting vibration by comparing consecutive frames
- **Exception Handling**: Logs error and re-raises if calculation fails
- **Usage**:
  ```python
  error = processor.mse(gray_frame1, gray_frame2)
  if error > threshold:
      print("Motion detected")
  ```

##### `lighting_compensation(self, frame)`
- **Purpose**: Applies histogram equalization to compensate for lighting variations
- **Parameters**:
  - `frame`: Input BGR image
- **Returns**: Histogram equalized grayscale image
- **Process**:
  1. Converts frame to grayscale
  2. Applies histogram equalization
- **Why It's Used**: To normalize lighting conditions for more reliable motion detection
- **Exception Handling**: Logs error and re-raises if processing fails
- **Usage**:
  ```python
  compensated = processor.lighting_compensation(frame)
  ```

##### `overlay_logo(self, frame, logo, position=(10, 10))`
- **Purpose**: Overlays a logo on the frame
- **Parameters**:
  - `frame`: Target frame to overlay logo on
  - `logo`: Logo image (with or without alpha channel)
  - `position`: Tuple of (x, y) coordinates for logo placement
- **Returns**: Frame with overlaid logo
- **Process**:
  1. Positions logo at specified coordinates (adjusts to right side)
  2. Handles alpha channel if present for transparent overlay
  3. Directly overlays if no alpha channel
- **Exception Handling**: Logs error and re-raises if overlay fails
- **Usage**:
  ```python
  frame_with_logo = processor.overlay_logo(frame, logo_img, (20, 20))
  ```

##### `put_title(self, frame, title)`
- **Purpose**: Adds a title text to the frame
- **Parameters**:
  - `frame`: Target frame to add title to
  - `title`: Text to display as title
- **Process**:
  1. Calculates text size and position for centered alignment
  2. Draws background rectangle
  3. Adds title text with white color
- **Configuration**:
  - Font: FONT_HERSHEY_SIMPLEX
  - Scale: 1
  - Color: White (255, 255, 255)
  - Thickness: 2
- **Exception Handling**: Logs error and re-raises if text placement fails
- **Usage**:
  ```python
  processor.put_title(frame, "Vibration Monitoring System")
  ```

##### `put_motion_notification(self, frame, text)`
- **Purpose**: Adds vibration status notification text to the frame
- **Parameters**:
  - `frame`: Target frame to add notification to
  - `text`: Notification text (e.g., "Vibration Detected!" or "No Vibration detected")
- **Process**:
  1. Calculates text size and position for centered alignment at bottom
  2. Draws background rectangle
  3. Adds notification text with color based on content
- **Color Coding**:
  - "Vibration Detected!": Green (0, 255, 0)
  - Other text: Red (0, 0, 255)
- **Exception Handling**: Logs error and re-raises if text placement fails
- **Usage**:
  ```python
  processor.put_motion_notification(frame, "Vibration Detected!")
  ```

##### `show(self, name, frame)`
- **Purpose**: Displays frame in a window
- **Parameters**:
  - `name`: Window name
  - `frame`: Frame to display
- **Process**:
  1. Creates named window with WINDOW_NORMAL flag
  2. Displays the frame in that window
- **Exception Handling**: Logs error and re-raises if display fails
- **Usage**:
  ```python
  processor.show("Camera Feed", frame)
  ```

##### `start_video_recording(self, video_writer, frame_raw)`
- **Purpose**: Writes a frame to video recording
- **Parameters**:
  - `video_writer`: OpenCV VideoWriter object
  - `frame_raw`: Frame to write to video
- **Process**: Writes the frame to the video file
- **Exception Handling**: Logs error and re-raises if recording fails
- **Usage**:
  ```python
  processor.start_video_recording(writer, frame)
  ```

##### `process_frame(self, frame_raw, logo, frame_gray)`
- **Purpose**: Core function for processing each frame for vibration detection
- **Parameters**:
  - `frame_raw`: Original unprocessed frame
  - `logo`: Logo image to overlay
  - `frame_gray`: Grayscale version of frame
- **Process**:
  1. Checks storage availability
  2. Loads ROI configuration
  3. Extracts ROI region from frame
  4. Applies optional motion blur
  5. Applies lighting compensation
  6. Overlays logo and title
  7. Draws ROI rectangle on display frame
  8. Calculates MSE between current and previous ROI
  9. Detects vibration if MSE exceeds threshold
  10. Manages PLC signaling based on vibration state
  11. Updates frame with notifications and FPS
  12. Displays the processed frame
  13. Stores current grayscale frame for next comparison
- **PLC Interaction**:
  - Sends signal to PLC when vibration stops
  - Writes bit 200 to address 4106 when vibration detected
  - Writes bit 100 to address 4106 when stable
- **Exception Handling**: Logs error and re-raises if processing fails
- **Usage**:
  ```python
  processor.process_frame(frame, logo, gray_frame)
  ```

##### `manage_video(self)`
- **Purpose**: Manages video recording file creation and path
- **Returns**: Current time string in format "HH:MM:SS"
- **Process**:
  1. Checks if video_writer exists
  2. If not, creates required directories with date-based structure
  3. Names video files with time-based filenames (HH-MM-SS.avi)
  4. Creates a new video writer
- **Path Structure**: "results/videos/YYYY-MM-DD/HH-MM-SS.avi"
- **Exception Handling**: Logs error and re-raises if video management fails
- **Usage**:
  ```python
  current_time = processor.manage_video()
  ```

##### `process(self)`
- **Purpose**: Main processing loop for the application
- **Process**:
  1. Loads logo image
  2. Loads camera configuration and initializes cameras
  3. Enters main processing loop:
     - Gets frames from camera threads
     - Adds timestamp to frame
     - Manages video recording
     - Processes frame for vibration detection
     - Records video if storage is sufficient
     - Handles video duration and creates new files as needed
     - Calculates and tracks FPS
     - Checks for keyboard interrupts
  4. Cleanup on exit:
     - Releases video writer
     - Resets PLC signal
     - Closes OpenCV windows
- **Exit Condition**: Press 'q' key to exit
- **Exception Handling**: Logs errors and ensures cleanup
- **Usage**:
  ```python
  processor.process()
  ```

#### Function: `load_config()`
- **Purpose**: Loads application configuration from file
- **Returns**: Tuple of (mes_score, fps, video_duration, stable_threshold, motion_blur)
- **File Source**: 'data/config.json'
- **Default Values**:
  - mes_score: 50
  - fps: 20
  - video_duration: 180
  - stable_threshold: 5
  - motion_blur: True
- **Process**:
  1. Attempts to read and parse JSON from config.json
  2. Extracts configuration values with defaults if keys are missing
- **Exception Handling**: Returns default values if file is missing or invalid
- **Usage**:
  ```python
  mes_score, fps, video_duration, stable_threshold, motion_blur = load_config()
  ```

#### Main Block
- **Purpose**: Entry point for the application
- **Process**:
  1. Loads configuration using load_config()
  2. Creates VideoProcessor instance with loaded configuration
  3. Calls process() to start the main application loop
- **Usage**: Run the script directly with `python app.py`

### cam.py (Camera Module)

This module handles camera connections and video frame acquisition.

#### Class: `CamConnect`

##### `__init__(self, cam_address)`
- **Purpose**: Initializes connection to camera via RTSP
- **Parameters**:
  - `cam_address`: RTSP URL for camera connection
- **Attributes**:
  - `cam_address`: Stored RTSP URL
  - `capture`: OpenCV VideoCapture object
  - `RECONNECTION_PERIOD`: Wait time between reconnection attempts (0.5 seconds)
  - `frame`: Current frame from camera
- **Process**: 
  1. Stores camera address
  2. Initializes VideoCapture with the RTSP URL
  3. Creates and starts frame grabbing thread
- **Exception Handling**: Initializes with default error frame if connection fails
- **Usage**:
  ```python
  camera = CamConnect("rtsp://192.168.1.100:554/stream")
  ```

##### `grab_frame(self)`
- **Purpose**: Thread function to continuously grab frames from camera
- **Process**:
  1. Runs in infinite loop while connection exists
  2. Continuously attempts to read frames using capture.read()
  3. Stores latest frame in self.frame
  4. If connection fails (ret is False), attempts reconnection
  5. Uses error frame if reconnection fails
- **Thread Safety**: Uses try-except to handle thread interruptions
- **Usage**: Called internally by `__init__` in a separate thread

##### `reconnect_camera(self)`
- **Purpose**: Attempts to reconnect to camera after connection loss
- **Returns**: Boolean - True if reconnection successful, False otherwise
- **Process**:
  1. Releases current VideoCapture if it exists
  2. Tries to connect up to 3 times
  3. Creates new VideoCapture with stored RTSP URL
  4. Tests connection by reading a frame
  5. Waits RECONNECTION_PERIOD (0.5s) between attempts
- **Usage**: Called automatically by `grab_frame` when connection fails

##### `read(self)`
- **Purpose**: Returns the current frame from camera
- **Returns**: Current frame or error image if unavailable
- **Process**: Simply returns the most recent frame grabbed by the background thread
- **Thread Safety**: Designed to be called from main thread while grab_frame runs in background
- **Usage**:
  ```python
  frame = camera.read()
  cv2.imshow("Camera Feed", frame)
  ```

##### `release(self)`
- **Purpose**: Releases camera resources
- **Process**:
  1. Releases the VideoCapture object if it exists
- **Usage**: Call when done with camera to free resources
  ```python
  camera.release()
  ```

#### Class: `CameraThread`

##### `__init__(self, camera_serial_number, rtsp_link, frame_dictionary)`
- **Purpose**: Initializes thread for camera operations
- **Parameters**:
  - `camera_serial_number`: Serial number identifier for camera
  - `rtsp_link`: RTSP URL for camera connection
  - `frame_dictionary`: Shared dictionary to store frames from multiple cameras
- **Attributes**:
  - `cam_serial_num`: Stored serial number
  - `rtsp_url`: Stored RTSP URL
  - `frame`: Current frame from camera
  - `running`: Boolean flag to control thread execution
  - `frame_dict`: Reference to shared frame dictionary
- **Process**: Sets up thread attributes but doesn't start the thread
- **Usage**:
  ```python
  frame_dict = {}
  cam_thread = CameraThread("CAM001", "rtsp://192.168.1.100:554/stream", frame_dict)
  cam_thread.start()
  ```

##### `run(self)`
- **Purpose**: Main thread function that continuously captures frames
- **Process**:
  1. Creates CamConnect instance with rtsp_url
  2. Continually reads frames while running flag is True
  3. Stores frames in the shared frame_dict with camera serial number as key
  4. Includes timestamp overlay on each frame
  5. Handles exceptions to prevent thread crashes
- **Used By**: Thread system when thread is started
- **Usage**: Not called directly, invoked via thread.start()

##### `stop(self)`
- **Purpose**: Stops the thread execution safely
- **Process**:
  1. Sets running flag to False, which terminates the run loop
- **Usage**:
  ```python
  cam_thread.stop()
  cam_thread.join()  # Wait for thread to finish
  ```

#### Function: `load_camera_config()`
- **Purpose**: Loads camera configuration from file
- **Returns**: Dictionary mapping camera serial numbers to RTSP URLs
- **File Source**: 'data/cameras.json'
- **Process**:
  1. Opens and reads cameras.json file
  2. Parses JSON into dictionary
- **Exception Handling**:
  - Returns empty dictionary if file not found
  - Logs error and returns empty dictionary for other exceptions
- **Usage**:
  ```python
  cameras = load_camera_config()
  for serial_num, rtsp_url in cameras.items():
      add_camera(serial_num, rtsp_url)
  ```

### plc.py (PLC Communication Module)

This module handles communication with the Programmable Logic Controller via Modbus ASCII protocol.

#### Class: `PLC`

##### `__init__(self)`
- **Purpose**: Initializes PLC object and connects to the physical PLC
- **Attributes**:
  - `isPLCConnected`: Boolean indicating PLC connection status
  - `instrument`: MinimalModbus instrument object
- **Process**:
  1. Sets initial connection status to False
  2. Attempts to connect to PLC by calling connectToPLC()
- **Exception Handling**: Logs connection failures but doesn't raise exceptions
- **Usage**:
  ```python
  plc = PLC()
  if plc.isPLCConnected:
      # Perform PLC operations
  ```

##### `convert_ma_to_percentage(self, ma)`
- **Purpose**: Converts milliamp readings to percentage
- **Parameters**:
  - `ma`: Current in milliamps (float)
- **Returns**: Percentage value (float)
- **Conversion**: Maps range -12mA to 20mA → 0% to 100%
- **Process**:
  1. Applies linear conversion formula
  2. Clamps result to 0-100 range
- **Usage**:
  ```python
  current_ma = 4.0
  percentage = plc.convert_ma_to_percentage(current_ma)
  print(f"Current: {current_ma}mA, Percentage: {percentage}%")  # Example: 4.0mA → 50%
  ```

##### `connectToPLC(self)`
- **Purpose**: Establishes connection to PLC via Modbus ASCII protocol
- **Returns**: Boolean - True if connection successful, False otherwise
- **Process**:
  1. Creates MinimalModbus instrument on COM7
  2. Configures communication parameters:
     - Baud rate: 9600
     - Byte size: 7 bits
     - Parity: Even
     - Stop bits: 1
     - Mode: ASCII
  3. Tests connection by reading a register
- **Configuration**:
  - Serial port: COM7 (hardware-dependent)
  - Slave address: 1
- **Exception Handling**: Catches and logs connection errors
- **Usage**: Called automatically by `__init__` but can be called manually to reconnect
  ```python
  if not plc.isPLCConnected:
      success = plc.connectToPLC()
      if success:
          print("PLC reconnected successfully")
  ```

##### `read_bit(self, address)`
- **Purpose**: Reads a value from the specified PLC register
- **Parameters**:
  - `address`: Register address to read from (int)
- **Returns**: Value read from register or None if failed
- **Process**:
  1. Checks if PLC is connected
  2. Uses MinimalModbus to read register value
  3. Returns value if successful
- **Exception Handling**: 
  - Logs errors but doesn't raise exceptions
  - Attempts to reconnect on communication failure
- **Usage**:
  ```python
  value = plc.read_bit(4106)
  if value is not None:
      print(f"Register 4106 value: {value}")
  ```

##### `write_bit(self, address, data)`
- **Purpose**: Writes a value to the specified PLC register
- **Parameters**:
  - `address`: Register address to write to (int)
  - `data`: Value to write to register (typically int)
- **Returns**: Boolean - True if write successful, False otherwise
- **Process**:
  1. Checks if PLC is connected
  2. Uses MinimalModbus to write value to register
  3. Returns success status
- **Exception Handling**: 
  - Logs errors but doesn't raise exceptions
  - Attempts to reconnect on communication failure
- **Usage**:
  ```python
  success = plc.write_bit(4106, 200)  # Signal vibration detected
  if success:
      print("Successfully wrote value to PLC")
  ```

### database.py (Database Operations)

This module handles database operations for storing vibration events.

#### Function: `create_db_if_not_exists()`
- **Purpose**: Creates the database if it doesn't exist
- **Returns**: None
- **Process**:
  1. Connects to PostgreSQL server using psycopg2
  2. Checks if database "deevia_vms" exists by querying pg_database
  3. If not exists, creates the database
  4. Closes connection
- **Configuration**:
  - Host: localhost
  - Port: 5432
  - User: postgres
  - Password: root
  - Initial database: postgres (for connection)
  - Target database: deevia_vms (to create)
- **Exception Handling**: Logs errors but doesn't raise exceptions
- **Usage**:
  ```python
  create_db_if_not_exists()  # Ensures database exists before attempting operations
  ```

#### Function: `create_table_if_not_exists()`
- **Purpose**: Creates the required table if it doesn't exist
- **Returns**: None
- **Process**:
  1. Connects to the "deevia_vms" database
  2. Executes SQL CREATE TABLE IF NOT EXISTS statement
  3. Creates "vms" table with column for vibration stopped timestamp
  4. Closes connection
- **Configuration**:
  - Table: vms
  - Columns: id (serial), vibration_stopped_date_time (timestamp)
- **Exception Handling**: Logs errors but doesn't raise exceptions
- **Usage**:
  ```python
  create_table_if_not_exists()  # Call after database creation
  ```

#### Function: `store_vibration_stopped_time()`
- **Purpose**: Records the timestamp when vibration stops
- **Returns**: None
- **Process**:
  1. Connects to the "deevia_vms" database
  2. Gets current timestamp
  3. Inserts timestamp into vms table
  4. Commits transaction and closes connection
- **Database Impact**: Creates a new record with current timestamp
- **Exception Handling**: Logs errors but doesn't raise exceptions
- **Usage**:
  ```python
  # When vibration stops after being detected
  store_vibration_stopped_time()  # Records the event time
  ```

### logging_config.py (Logging Configuration)

This module configures the application-wide logging system.

#### Function: `setup_logger()`
- **Purpose**: Configures and returns a logger with file rotation
- **Returns**: Configured logger object
- **Process**:
  1. Creates logs directory if it doesn't exist
  2. Creates a logger instance
  3. Sets log level to INFO
  4. Configures TimedRotatingFileHandler:
     - Base filename: logs/VMS_{date}.log
     - When: midnight (daily rotation)
     - Backups: 1 (keeps one previous log file)
  5. Sets formatter with timestamp, filename, thread name, and log level
  6. Adds handler to logger
- **Log Format**: `%(asctime)s - %(filename)s - %(threadName)s - %(levelname)s - %(message)s`
- **Exception Handling**: Creates fallback console logger if file setup fails
- **Usage**:
  ```python
  logger = setup_logger()
  logger.info("Application started")
  logger.error("Error occurred: %s", error_message)
  ```

#### Variable: `logger`
- **Purpose**: Global logger instance for use throughout the application
- **Type**: logging.Logger
- **Initialization**: Created by calling setup_logger()
- **Usage**:
  ```python
  from logging_config import logger
  
  logger.info("Function called")
  logger.warning("Potential issue: %s", warning_message)
  ```

### file_verifier.py (File Verification)

This module handles verification of required files and creation of necessary directories.

#### Function: `verify_config_files()`
- **Purpose**: Checks for the existence of required configuration files
- **Returns**: Boolean - True if all required files exist, False otherwise
- **Files Checked**:
  - data/cameras.json: Camera RTSP URLs
  - data/roi.json: Region of interest settings
  - data/config.json: System configuration
  - data/storage_limit.json: Storage management settings
- **Process**:
  1. Checks each file path using os.path.exists()
  2. Returns True only if all required files exist
- **Usage**:
  ```python
  if not verify_config_files():
      print("Missing configuration files. Please check data directory.")
      # Handle missing files situation
  ```

#### Function: `create_directories()`
- **Purpose**: Creates necessary directories if they don't exist
- **Returns**: None
- **Directories Created**:
  - data: For configuration files
  - logs: For application logs
  - results/videos: For recorded video files
- **Process**:
  1. Uses os.makedirs() with exist_ok=True to create directories
  2. Creates nested directory structure as needed
- **Usage**:
  ```python
  create_directories()  # Call at application startup
  ```

#### Function: `check_and_create_files()`
- **Purpose**: Main function that combines verification and directory creation
- **Returns**: Boolean - True if all checks pass, False otherwise
- **Process**:
  1. Calls create_directories() to ensure directories exist
  2. Calls verify_config_files() to check for required files
  3. Returns result of verification
- **Usage**:
  ```python
  success = check_and_create_files()
  if not success:
      print("Configuration issue detected. Please check data files.")
  ```

## Configuration Files

The system relies on several JSON configuration files located in the `data` directory:

### cameras.json
- **Purpose**: Defines camera connections with their serial numbers and RTSP URLs
- **Format**:
  ```json
  {
    "camera_serial_number_1": "rtsp://camera_ip_1:port/stream",
    "camera_serial_number_2": "rtsp://camera_ip_2:port/stream"
  }
  ```
- **Required Fields**:
  - Camera serial number (key): Unique identifier for each camera
  - RTSP URL (value): Full RTSP stream URL including protocol, IP, port, and path
- **Example**:
  ```json
  {
    "CAM001": "rtsp://192.168.1.100:554/main/stream",
    "CAM002": "rtsp://192.168.1.101:554/main/stream"
  }
  ```

### roi.json
- **Purpose**: Defines Region of Interest for vibration detection
- **Format**:
  ```json
  {
    "x": integer,
    "y": integer,
    "width": integer,
    "height": integer
  }
  ```
- **Required Fields**:
  - x: X-coordinate of top-left corner (pixels)
  - y: Y-coordinate of top-left corner (pixels)
  - width: Width of ROI (pixels)
  - height: Height of ROI (pixels)
- **Example**:
  ```json
  {
    "x": 500,
    "y": 300,
    "width": 800,
    "height": 600
  }
  ```

### config.json
- **Purpose**: General system configuration parameters
- **Format**:
  ```json
  {
    "mes_score": integer,
    "fps": integer,
    "video_duration": integer,
    "stable_threshold": integer,
    "motion_blur": boolean
  }
  ```
- **Required Fields**:
  - mes_score: Motion energy score threshold (default: 50)
  - fps: Frames per second for processing (default: 20)
  - video_duration: Duration of recorded videos in seconds (default: 180)
  - stable_threshold: Time in seconds before declaring stability (default: 5)
  - motion_blur: Whether to use motion blur detection (default: true)
- **Example**:
  ```json
  {
    "mes_score": 30,
    "fps": 15,
    "video_duration": 300,
    "stable_threshold": 3,
    "motion_blur": true
  }
  ```

### storage_limit.json
- **Purpose**: Defines disk space limit for video recordings
- **Format**:
  ```json
  {
    "limit_gb": integer
  }
  ```
- **Required Fields**:
  - limit_gb: Storage limit in gigabytes (default: 30)
- **Example**:
  ```json
  {
    "limit_gb": 50
  }
  ```

## Troubleshooting

This section provides guidance for troubleshooting common issues.

### Camera Connection Issues

#### Symptoms:
- Black screen or error message in camera feed
- "Camera disconnected" error in logs

#### Possible Causes:
- Incorrect RTSP URL in cameras.json
- Network connectivity issues
- Camera power or hardware failure
- Camera bandwidth limitations

#### Solutions:
1. **Verify RTSP URL**:
   - Check cameras.json for correct URLs
   - Test URLs with VLC or similar player
   - Ensure proper authentication is included if required

2. **Check Network Connectivity**:
   - Ping camera IP addresses
   - Verify that cameras are on the same network as the monitoring system
   - Check network switches and routers

3. **Camera Hardware Check**:
   - Verify power supply to cameras
   - Check camera status LEDs
   - Restart cameras if possible

4. **Bandwidth Considerations**:
   - Lower camera resolution or framerate if network is congested
   - Ensure sufficient network capacity for all cameras

### PLC Communication Issues

#### Symptoms:
- "PLC connection failed" error in logs
- System unable to signal vibration events

#### Possible Causes:
- Incorrect COM port configuration
- PLC not powered on or in fault state
- Serial cable disconnected or damaged
- PLC communication parameters mismatch
- Invalid PLC addresses used

#### Solutions:
1. **Verify COM Port Settings**:
   - Check that COM7 is the correct port (use Device Manager)
   - Ensure no other software is using the same COM port
   - Try changing the COM port in the `connectToPLC()` method if necessary

2. **Check PLC Configuration**:
   - Verify PLC is powered on and operational
   - Check that Modbus ASCII protocol is enabled on the PLC
   - Ensure communication parameters match (9600 baud, 7 data bits, even parity, 1 stop bit)

3. **Test Serial Connection**:
   - Inspect physical connections between PC and PLC
   - Try a different serial cable
   - Use a diagnostic tool like Modbus Poll to test the connection

4. **Address Verification**:
   - Confirm that register addresses (e.g., 4106) are correct for your PLC model
   - Check PLC documentation for valid register ranges

### Database Issues

#### Symptoms:
- "Failed to connect to database" error in logs
- Vibration events not being recorded

#### Possible Causes:
- PostgreSQL service not running
- Incorrect database credentials
- Database structure issues

#### Solutions:
1. **Check PostgreSQL Service**:
   - Verify PostgreSQL service is running (Services app in Windows)
   - Restart service if necessary

2. **Verify Credentials**:
   - Ensure the username "postgres" and password "root" are set correctly
   - Try connecting with pgAdmin or other PostgreSQL client

3. **Database Structure**:
   - Run the application with clean database to allow auto-creation
   - If issues persist, manually create database and table:
     ```sql
     CREATE DATABASE deevia_vms;
     \c deevia_vms
     CREATE TABLE vms (
         id SERIAL PRIMARY KEY,
         vibration_stopped_date_time TIMESTAMP NOT NULL
     );
     ```

### Video Recording Issues

#### Symptoms:
- Videos not being saved
- "Low disk space" warnings
- Poor video quality

#### Possible Causes:
- Insufficient disk space
- File permission issues
- OpenCV codec issues

#### Solutions:
1. **Disk Space Management**:
   - Check available disk space
   - Adjust storage_limit.json to a lower value
   - Manually clear old videos if necessary

2. **File Permissions**:
   - Ensure the application has write permissions to the results directory
   - Run the application as administrator if needed

3. **Codec Issues**:
   - Install the required codecs (XVID) for OpenCV
   - Try changing the codec in create_video_writer method if issues persist

## Maintenance

This section provides guidelines for regular maintenance tasks to ensure the system runs optimally.

### Regular Maintenance Tasks

#### Daily

1. **Log Review**:
   - Check log files in the logs directory for any errors or warnings
   - Look for patterns of connection failures or system issues

2. **System Monitor**:
   - Verify the application is running and detecting vibrations correctly
   - Ensure all cameras are connected and streaming

#### Weekly

1. **Disk Space Management**:
   - Review disk usage and available space
   - Archive or delete old video recordings if necessary
   - Adjust storage_limit.json if needed

2. **Camera Verification**:
   - Verify camera positioning has not changed
   - Clean camera lenses if accessible
   - Check video quality and adjust ROI if necessary

3. **Database Maintenance**:
   - Backup the PostgreSQL database
   - Run VACUUM command to optimize database performance:
     ```sql
     VACUUM ANALYZE deevia_vms;
     ```

#### Monthly

1. **System Restart**:
   - Perform a controlled restart of the system
   - Update PostgreSQL if new security patches are available

2. **Configuration Review**:
   - Review and adjust system parameters based on performance
   - Check mes_score threshold and adjust if vibration detection is too sensitive or not sensitive enough
   - Update ROI settings if blast furnace conditions have changed

3. **PLC Connection Test**:
   - Verify PLC communication is functioning correctly
   - Test the full signal chain from vibration detection to PLC notification

### System Upgrade Procedures

1. **Before Upgrading**:
   - Backup all configuration files from the data directory
   - Backup the PostgreSQL database
   - Document current performance and settings

2. **Software Update Process**:
   - Stop the running application
   - Create a backup of the entire application directory
   - Replace files with new versions
   - Update requirements if needed:
     ```bash
     call activate vms
     pip install -r requirements.txt
     ```

3. **After Upgrade**:
   - Restore configuration files if they were overwritten
   - Run the application and verify all components are working
   - Compare performance metrics with pre-upgrade documentation

## References

### Technical References

1. **Python Libraries**:
   - [OpenCV Documentation](https://docs.opencv.org/4.x/)
   - [NumPy Documentation](https://numpy.org/doc/stable/)
   - [Psycopg2 Documentation](https://www.psycopg.org/docs/)
   - [MinimalModbus Documentation](https://minimalmodbus.readthedocs.io/)

2. **Protocols**:
   - [Modbus Protocol Specification](https://modbus.org/specs.php)
   - [RTSP Protocol Documentation](https://tools.ietf.org/html/rfc7826)

3. **Database**:
   - [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Internal References

1. **System Design Documents**:
   - JSW Bellary BF2 Monitoring System Requirements Specification
   - Vibration Detection Algorithm Design Document

2. **Equipment Manuals**:
   - Camera System Installation and Operation Manual
   - PLC Programming and Communication Guide

3. **Contact Information**:
   - Technical Support: subramanya.b@deevia.pw
---

**Document Version**: 1.0  
**Last Updated**: December 7, 2024  
**Author**: Subramanya Gopal Bellary | Software Engineer | DEEVIA Software India Pvt Ltd
