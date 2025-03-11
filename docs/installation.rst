============
Installation
============

This section provides detailed instructions for installing and configuring the Vibration Monitoring System.

Prerequisites
============

Hardware Requirements
--------------------

* **Server/Computer System**:
* Processor: Intel Core i7 or equivalent (8+ cores recommended)
* RAM: Minimum 16GB (32GB recommended)
* Storage: 500GB SSD (for operating system and application)
* Additional storage: 2TB+ for video recordings storage
* Network: Gigabit Ethernet connection

* **Camera System**:
* Network cameras with RTSP support
* Minimum resolution: 1920x1080 (Full HD)
* Frame rate: 30fps minimum
* Multiple camera mounting points with clear view of monitoring areas
* Ethernet connectivity to server

* **PLC System**:
* Compatible Modbus ASCII PLC
* Serial connection capability (COM port)
* Available register addresses for integration

* **Network Infrastructure**:
* Gigabit network switches
* Stable network connection between cameras and server
* Sufficient bandwidth for multiple camera feeds

Software Requirements
--------------------

* **Operating System**:
* Windows 10 64-bit or Windows Server 2016/2019
* .NET Framework 4.7.2+

* **Python Environment**:
* Python 3.8+ (64-bit)
* Virtual environment management (Anaconda or venv)

* **Database**:
* PostgreSQL 12.0+

* **Additional Software**:
* Git (for version control)
* Visual Studio Code or similar IDE (recommended for code editing)

Installation Process
===================

1. System Preparation
--------------------

1.1 Operating System Setup
^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure your system meets all hardware requirements before beginning:

.. code-block:: bash

# Check system specifications on Windows
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type" /C:"Total Physical Memory"

1.2 Install PostgreSQL
^^^^^^^^^^^^^^^^^^^^^

1. Download PostgreSQL installer from https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Installation configuration:
 
 * Use default installation directory
 * Set password for 'postgres' user to 'root'
 * Keep default port (5432)
 * Set locale to 'English, United States'

4. Complete installation with pgAdmin (included in the installer)
5. Verify installation by connecting to the server through pgAdmin

1.3 Install Python and Setup Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Download Python 3.8+ from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Create a virtual environment for the project:

.. code-block:: bash

# Create a directory for your project
mkdir -p D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development
cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development

# Create and activate virtual environment
python -m venv vms
call vms\Scripts\activate

# Verify Python version
python --version

2. Application Installation
--------------------------

2.1 Get the Application Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Option 1: Clone from Git repository (if available):

.. code-block:: bash

# Navigate to Development directory
cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development

# Clone the repository
git clone https://your-repository-url.git VMS_BF2_07_12_2024

# Enter project directory
cd VMS_BF2_07_12_2024

Option 2: Manual installation:

1. Create the application directory structure:

.. code-block:: bash

# Create application directory
mkdir -p D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024
cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024

# Create subdirectories
mkdir data logs results\videos PLC_Related Recorder_PC

2. Copy application files (app.py, cam.py, plc.py, database.py, etc.) to the application directory

2.2 Install Dependencies
^^^^^^^^^^^^^^^^^^^^^^

Install required Python packages using the requirements.txt file:

.. code-block:: bash

# Activate virtual environment if not already activated
call D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\vms\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installations
pip list

3. Configuration
--------------

3.1 Camera Configuration
^^^^^^^^^^^^^^^^^^^^^^

Create or edit the camera configuration file:

1. Navigate to the data directory:

.. code-block:: bash

cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024\data

2. Create a `cameras.json` file with the following format:

.. code-block:: json

{
"camera_serial_number_1": "rtsp://username:password@camera-ip-address:port/stream",
"camera_serial_number_2": "rtsp://username:password@camera-ip-address:port/stream"
}

Replace `camera_serial_number_X` with your actual camera identifiers and update the RTSP URLs with your camera credentials and IP addresses.

3.2 System Configuration
^^^^^^^^^^^^^^^^^^^^^^

Create or edit the main configuration file:

1. Navigate to the data directory:

.. code-block:: bash

cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024\data

2. Create a `config.json` file with the following format:

.. code-block:: json

{
"mes_score": 50,
"fps": 20,
"video_duration": 180,
"stable_threshold": 5,
"motion_blur": true
}

Adjust these values according to your requirements:

* `mes_score`: Motion energy score threshold (default: 50)
* `fps`: Processing frames per second (default: 20)
* `video_duration`: Video recording duration in seconds (default: 180)
* `stable_threshold`: Time in seconds to determine stability (default: 5)
* `motion_blur`: Enable/disable motion blur detection (default: true)

3.3 Region of Interest (ROI) Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create or edit the ROI configuration file:

1. Navigate to the data directory:

.. code-block:: bash

cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024\data

2. Create a `roi.json` file with the following format:

.. code-block:: json

{
"x": 100,
"y": 100,
"width": 500,
"height": 300
}

Adjust these values to define the region in the camera frame where vibration will be monitored.

3.4 Storage Configuration
^^^^^^^^^^^^^^^^^^^^^^^

Create or edit the storage limit configuration file:

1. Navigate to the data directory:

.. code-block:: bash

cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024\data

2. Create a `storage_limit.json` file with the following format:

.. code-block:: json

{
"storage_limit": 30
}

This defines the storage limit in GB for video recordings (default: 30GB).

3.5 PLC Configuration
^^^^^^^^^^^^^^^^^^^

The PLC connection parameters are defined in the plc.py file:

* Port: COM7 (default)
* Baud rate: 9600
* Parity: Even
* Stop bits: 1
* Data bits: 7
* Protocol: Modbus ASCII

If you need to modify these settings, edit the relevant sections in the plc.py file.

4. Database Setup
---------------

The system automatically creates the required database and tables on first run. However, you can manually set up the database with the following steps:

1. Open pgAdmin
2. Connect to the PostgreSQL server
3. Create a new database named "deevia_vms"
4. Run the following SQL query to create the vibration events table:

.. code-block:: sql

CREATE TABLE IF NOT EXISTS vms (
id SERIAL PRIMARY KEY,
vibration_stopped_date_time TIMESTAMP NOT NULL
);

5. System Verification
--------------------

Before running the application, verify all components are properly configured:

1. Check PostgreSQL is running:

.. code-block:: bash

# On Windows
sc query postgresql-x64-12

2. Verify camera connectivity:

.. code-block:: bash

# Test RTSP connection using VLC or similar tool
# Open network stream with your camera's RTSP URL

3. Verify PLC connectivity:
 
 * Ensure the PLC is powered on and accessible
 * Check serial port connection (COM7 by default)

6. Running the Application
------------------------

6.1 Using the Batch File
^^^^^^^^^^^^^^^^^^^^^^^

The simplest way to start the application is using the provided batch file:

.. code-block:: bash

# Navigate to application directory
cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024

# Run the application
run.bat

6.2 Manual Start
^^^^^^^^^^^^^^

Alternatively, you can start the application manually:

.. code-block:: bash

# Navigate to application directory
cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024

# Activate virtual environment
call D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\vms\Scripts\activate

# Run the application
python app.py

Troubleshooting Installation Issues
==================================

Camera Connection Issues
----------------------

* **Problem**: Cannot connect to cameras
**Solution**: 
- Verify camera IP addresses and credentials
- Check network connectivity between server and cameras
- Ensure cameras support RTSP protocol
- Test RTSP URLs with VLC or similar tools

PLC Connection Issues
-------------------

* **Problem**: Cannot communicate with PLC
**Solution**:
- Verify COM port settings
- Check physical connection between server and PLC
- Ensure PLC is configured for Modbus ASCII communication
- Test with a Modbus diagnostic tool

Database Connection Issues
------------------------

* **Problem**: Application fails to connect to database
**Solution**:
- Verify PostgreSQL service is running
- Check database credentials (user: postgres, password: root)
- Ensure PostgreSQL is accessible on localhost:5432
- Manually test connection with pgAdmin

Python Environment Issues
-----------------------

* **Problem**: Missing dependencies or packages
**Solution**:
- Verify virtual environment is activated
- Reinstall all dependencies: `pip install -r requirements.txt`
- Check for any error messages during installation
- Verify Python version (3.8+)

Storage Issues
------------

* **Problem**: Running out of disk space
**Solution**:
- Adjust storage_limit.json to a lower value
- Add additional storage
- Implement a data retention policy for older recordings

Upgrading the System
==================

For system upgrades:

1. Back up all configuration files
2. Back up the database
3. Update application files
4. Run `pip install -r requirements.txt` to update dependencies
5. Restart the application

Conclusion
=========

After following these installation steps, your Vibration Monitoring System should be successfully installed and configured. If you encounter any issues not covered in the troubleshooting section, please refer to the project documentation or contact the development team.

