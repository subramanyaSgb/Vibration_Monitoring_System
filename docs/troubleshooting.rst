=======================
Troubleshooting Guide
=======================

This guide provides solutions for common issues you may encounter with the Vibration Monitoring System.

Camera Connection Issues
------------------------

Camera Feed Not Displaying
^^^^^^^^^^^^^^^^^^^^^^^^^

**Issue**: Camera feed is not visible in the monitoring interface.

**Possible Causes**:
- Network connectivity issues
- Incorrect RTSP URL
- Camera power issues
- Camera in use by another application

**Solutions**:

1. **Check Network Connectivity**:
   
   .. code-block:: none
   
      ping [camera_ip_address]
   
   If the ping fails, check the network connections and ensure the camera is on the same network.

2. **Verify RTSP URL**:
   
   Open the ``data/cameras.json`` file and verify the RTSP URL for the problematic camera:
   
   .. code-block:: json
   
      {
        "camera_serial_number": "rtsp://username:password@camera_ip:554/stream"
      }
   
   Ensure the IP address, username, password, and stream path are correct.

3. **Restart Camera**:
   
   Power cycle the camera by disconnecting and reconnecting its power supply.

4. **Check Camera in Device Manager**:
   
   Ensure no other applications are using the camera.

5. **Adjust Reconnection Settings**:
   
   In ``cam.py``, you can modify the ``RECONNECTION_PERIOD`` attribute to adjust how quickly the system attempts to reconnect:
   
   .. code-block:: python
   
      self.RECONNECTION_PERIOD = 0.5  # seconds

Poor Video Quality
^^^^^^^^^^^^^^^^^

**Issue**: Camera feed is displaying but with poor quality or high latency.

**Solutions**:

1. **Check Network Bandwidth**:
   
   Ensure sufficient bandwidth is available for the video stream. Consider using a dedicated network for cameras.

2. **Adjust Camera Settings**:
   
   Access the camera's web interface and reduce resolution or frame rate if bandwidth is limited.

3. **Update Camera Firmware**:
   
   Check for and install any available firmware updates for your camera model.

PLC Communication Issues
-----------------------

PLC Connection Failures
^^^^^^^^^^^^^^^^^^^^^^

**Issue**: System cannot connect to the PLC or loses connection frequently.

**Possible Causes**:
- Incorrect COM port
- Serial cable issues
- Incorrect communication parameters
- PLC in faulty state

**Solutions**:

1. **Verify COM Port**:
   
   In ``plc.py``, check the COM port configuration:
   
   .. code-block:: python
   
      self.instrument = minimalmodbus.Instrument('COM7', 1)
   
   Ensure COM7 is the correct port. You can check available ports using:
   
   .. code-block:: python
   
      import serial.tools.list_ports
      ports = list(serial.tools.list_ports.comports())
      for p in ports:
          print(p)
   
2. **Check Serial Cable**:
   
   Inspect the serial cable for damage and ensure it's securely connected at both ends.

3. **Verify Communication Parameters**:
   
   Confirm the PLC communication parameters match those in the code:
   
   .. code-block:: python
   
      self.instrument.serial.baudrate = 9600
      self.instrument.serial.bytesize = 7
      self.instrument.serial.parity = serial.PARITY_EVEN
      self.instrument.serial.stopbits = 1
      self.instrument.mode = minimalmodbus.MODE_ASCII

4. **Restart PLC**:
   
   If possible, restart the PLC to reset its communication state.

5. **Check PLC Address**:
   
   Verify the PLC address in the code matches the actual PLC address:
   
   .. code-block:: python
   
      self.instrument = minimalmodbus.Instrument('COM7', 1)  # 1 is the slave address

PLC Not Responding to Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Issue**: System connects to PLC but the PLC doesn't respond to commands.

**Solutions**:

1. **Check Register Addresses**:
   
   Verify the register addresses used in read_bit and write_bit functions:
   
   .. code-block:: python
   
      def read_bit(self, address):
          try:
              return self.instrument.read_register(address)
          except Exception as e:
              logger.error(f"Failed to read bit: {str(e)}")
              return None
   
   Ensure the addresses match those in the PLC documentation.

2. **Test with PLC Programming Software**:
   
   Use the PLC manufacturer's programming software to test direct communication with the PLC.

3. **Check PLC Access Rights**:
   
   Ensure the PLC is configured to allow read/write access from external devices.

Database Issues
--------------

Database Connection Failures
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Issue**: System cannot connect to the PostgreSQL database.

**Possible Causes**:
- PostgreSQL service not running
- Incorrect connection parameters
- Database does not exist
- Permission issues

**Solutions**:

1. **Check PostgreSQL Service**:
   
   Verify the PostgreSQL service is running:
   
   .. code-block:: none
   
      services.msc
   
   Look for the PostgreSQL service and ensure it's started.

2. **Verify Connection Parameters**:
   
   In ``database.py``, check the connection parameters:
   
   .. code-block:: python
   
      conn = psycopg2.connect(
          host="localhost",
          port="5432",
          user="postgres",
          password="root",
          database="postgres"
      )
   
   Ensure these match your PostgreSQL installation.

3. **Create Database Manually**:
   
   If the automatic database creation fails, create it manually:
   
   .. code-block:: sql
   
      CREATE DATABASE deevia_vms;
   
4. **Check User Permissions**:
   
   Ensure the PostgreSQL user has appropriate permissions:
   
   .. code-block:: sql
   
      GRANT ALL PRIVILEGES ON DATABASE deevia_vms TO postgres;

Data Not Being Recorded
^^^^^^^^^^^^^^^^^^^^^^

**Issue**: Vibration events are detected but not recorded in the database.

**Solutions**:

1. **Check Table Creation**:
   
   Verify the vms table exists in the database:
   
   .. code-block:: sql
   
      \dt vms
   
   If it doesn't exist, the automatic table creation might have failed. Review the logs for errors.

2. **Check Database Disk Space**:
   
   Ensure sufficient disk space is available for the database.

3. **Check Database Logs**:
   
   Review PostgreSQL logs for any errors related to the database operations.

System Performance Issues
------------------------

High CPU Usage
^^^^^^^^^^^^^

**Issue**: System is using excessive CPU resources.

**Solutions**:

1. **Reduce Frame Rate**:
   
   In ``app.py``, modify the FPS setting in the config.json file:
   
   .. code-block:: json
   
      {
        "fps": 10
      }
   
   Lower values will reduce CPU usage.

2. **Optimize ROI Size**:
   
   In ``app.py``, adjust the Region of Interest size to process smaller areas:
   
   .. code-block:: json
   
      {
        "x": 100,
        "y": 100,
        "width": 300,
        "height": 300
      }
   
3. **Disable Motion Blur**:
   
   In ``app.py``, disable motion blur processing:
   
   .. code-block:: json
   
      {
        "motion_blur": false
      }

Disk Space Issues
^^^^^^^^^^^^^^^

**Issue**: System is rapidly filling available disk space with video recordings.

**Solutions**:

1. **Adjust Storage Limit**:
   
   In ``data/storage_limit.json``, modify the storage limit:
   
   .. code-block:: json
   
      {
        "limit_gb": 20
      }
   
2. **Reduce Video Duration**:
   
   In ``app.py``, modify the video duration setting:
   
   .. code-block:: json
   
      {
        "video_duration": 120
      }
   
   This will create smaller video files.

3. **Implement Automatic Cleanup**:
   
   Create a scheduled task to automatically delete older video files.

Vibration Detection Issues
-------------------------

False Positive Detections
^^^^^^^^^^^^^^^^^^^^^^^^

**Issue**: System detects vibrations when none are present.

**Solutions**:

1. **Adjust MES Score Threshold**:
   
   In ``app.py``, increase the mes_score threshold:
   
   .. code-block:: json
   
      {
        "mes_score": 75
      }
   
   Higher values require more significant movement to trigger detection.

2. **Adjust Stable Threshold**:
   
   In ``app.py``, increase the stable_threshold:
   
   .. code-block:: json
   
      {
        "stable_threshold": 10
      }
   
   This requires the system to wait longer before declaring stability.

3. **Optimize ROI Placement**:
   
   Adjust the Region of Interest to exclude areas with normal movement:
   
   .. code-block:: json
   
      {
        "x": 200,
        "y": 200,
        "width": 400,
        "height": 400
      }

Missed Vibration Detections
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Issue**: System fails to detect actual vibrations.

**Solutions**:

1. **Decrease MES Score Threshold**:
   
   In ``app.py``, decrease the mes_score threshold:
   
   .. code-block:: json
   
      {
        "mes_score": 30
      }
   
   Lower values will make the system more sensitive.

2. **Optimize Camera Placement**:
   
   Ensure cameras have a clear view of the areas where vibration is expected.

3. **Improve Lighting**:
   
   Ensure consistent lighting in the monitored area to improve detection accuracy.

Logging Issues
-------------

Missing Log Files
^^^^^^^^^^^^^^^

**Issue**: Log files are not being created or are incomplete.

**Solutions**:

1. **Check Permissions**:
   
   Ensure the application has write permissions to the logs directory.

2. **Verify Logging Configuration**:
   
   In ``logging_config.py``, check the logging configuration:
   
   .. code-block:: python
   
      def setup_logger():
          if not os.path.exists('logs'):
              os.makedirs('logs')
          
          logger = logging.getLogger('vibration_monitoring')
          logger.setLevel(logging.INFO)
          
          handler = TimedRotatingFileHandler(
              'logs/app.log',
              when='midnight',
              backupCount=1
          )
          formatter = logging.Formatter('%(asctime)s - %(filename)s - %(threadName)s - %(levelname)s - %(message)s')
          handler.setFormatter(formatter)
          logger.addHandler(handler)
          
          return logger
   
   Ensure the path and configuration are correct.

3. **Free Disk Space**:
   
   Ensure sufficient disk space is available for log files.

Excessive Logging
^^^^^^^^^^^^^^^

**Issue**: Log files are growing too large too quickly.

**Solutions**:

1. **Adjust Log Level**:
   
   In ``logging_config.py``, change the log level to a less verbose setting:
   
   .. code-block:: python
   
      logger.setLevel(logging.WARNING)  # Change from INFO to WARNING
   
2. **Reduce Retention Period**:
   
   In ``logging_config.py``, reduce the backupCount parameter to retain fewer log files:
   
   .. code-block:: python
   
      handler = TimedRotatingFileHandler(
          'logs/app.log',
          when='midnight',
          backupCount=1  # Reduced from higher value
      )

System Not Starting
------------------

Application Crashes at Startup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Issue**: Application crashes immediately upon starting.

**Solutions**:

1. **Check Python Environment**:
   
   Ensure the correct Python environment is activated:
   
   .. code-block:: none
   
      call activate vms
   
2. **Verify Dependencies**:
   
   Ensure all required dependencies are installed:
   
   .. code-block:: none
   
      pip install -r requirements.txt
   
3. **Check Configuration Files**:
   
   Ensure all required configuration files exist and are valid JSON:
   
   - data/cameras.json
   - data/config.json
   - data/roi.json
   - data/storage_limit.json

4. **Check Log Files**:
   
   Review the log files for specific error messages:
   
   .. code-block:: none
   
      type logs\app.log
   
5. **Run with Debug Output**:
   
   Modify run.bat to show console output:
   
   .. code-block:: none
   
      call activate vms
      python app.py
      pause
   
   This will keep the console window open to display any error messages.

Contact Support
--------------

If you continue to experience issues after trying these troubleshooting steps, please contact Technical Support:

- Email: subramanya.b@deevia.pw
- Phone: +91-7892389809

When contacting support, please provide:

1. Detailed description of the issue
2. Steps to reproduce the problem
3. Any error messages from the logs
4. System configuration details
5. Screenshots of the issue if applicable

