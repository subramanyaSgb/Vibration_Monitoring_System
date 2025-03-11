=====
Usage
=====

User Interface
=============

Main Interface
-------------

The main interface of the JSW Bellary BF2 Vibration Monitoring System displays:

1. **Camera Feed**: The primary view shows the live camera feed with vibration monitoring.
2. **Region of Interest (ROI)**: A highlighted rectangle showing the area being monitored for vibrations.
3. **Status Bar**: Shows the current vibration status (vibration detected or no vibration).
4. **FPS Counter**: Displays the current frames per second being processed.
5. **JSW Logo**: Company branding in the upper corner.

.. figure:: _static/interface_diagram.png
   :width: 80%
   :align: center
   :alt: Main interface of the Vibration Monitoring System

   *Main interface of the Vibration Monitoring System*

Status Indicators
----------------

The system uses color-coded text overlays to indicate vibration status:

* **Green Text**: "Vibration Detected!" - Indicates active vibration in the monitored area.
* **Red Text**: "No Vibration detected" - Indicates stable conditions with no vibration.

The system also maintains a constant display of the current processing frame rate (FPS) to help monitor system performance.

Monitoring Techniques
====================

ROI Selection
------------

The Region of Interest (ROI) is a critical component for accurate vibration detection:

1. **Default ROI**: The system loads the ROI configuration from ``data/roi.json``.
2. **Optimal Placement**: Place the ROI over structural elements where vibration is most likely to be visible.
3. **Size Considerations**: The ROI should be large enough to capture meaningful movement but small enough to avoid including irrelevant motion.

.. note::
   The ROI configuration can be adjusted by modifying the ``data/roi.json`` file. Changes require application restart to take effect.

Vibration Detection Parameters
-----------------------------

Several parameters affect vibration detection sensitivity:

* **Motion Energy Score (MES)**: Threshold for detecting vibration (default: 50)
* **Stable Threshold**: Time in seconds the system must observe stability before declaring vibration has stopped (default: 1 second)
* **Motion Blur**: Enable/disable motion blur detection for different lighting conditions

These parameters can be adjusted in the ``data/config.json`` file to tune the system for specific monitoring requirements:

.. code-block:: json

   {
     "mes_score": 50,
     "fps": 10,
     "video_duration": 180,
     "stable_threshold": 1,
     "motion_blur": true
   }

Daily Operations
===============

Startup Procedure
----------------

1. **System Boot**: Start the computer system and log in.
2. **Network Check**: Ensure all cameras are online and accessible on the network.
3. **Launch Application**: Execute the ``run.bat`` file by double-clicking it or running it from the command prompt.
4. **Verification**: Confirm the system interface appears and camera feeds are visible.
5. **PLC Communication**: Verify PLC connection status in the application logs (check logs directory).

.. warning::
   Ensure that the application is launched from the correct directory to avoid path-related errors.

Shutdown Procedure
-----------------

1. **Close Application**: Press 'q' key while the application window is in focus.
2. **Verify PLC Reset**: Ensure the PLC signal is reset to the default state (the application does this automatically).
3. **Check Logs**: Review the day's log files for any warnings or errors that may require attention.

Monitoring Best Practices
------------------------

1. **Regular Checks**: Perform visual checks of the camera feeds at least once per shift.
2. **Storage Management**: Monitor available disk space - the system requires minimum free space as configured in ``data/storage_limit.json``.
3. **Vibration Event Review**: Review recorded vibration events daily for unusual patterns.
4. **Camera Alignment**: Periodically verify camera positioning hasn't changed and the ROI is still properly aligned.
5. **PLC Signal Testing**: Conduct monthly tests of the PLC signaling by simulating vibration events.

Data Management
--------------

Recorded vibration events are stored in two places:

1. **Video Files**: Located in ``results/videos/YYYY-MM-DD/`` with HH-MM-SS.avi format
2. **Database Records**: Stored in the PostgreSQL database with timestamps

**Video File Management:**

* Videos are automatically organized by date
* Older videos can be archived based on company retention policies
* Video duration is configurable in ``data/config.json``

**Database Management:**

* The system automatically records vibration stop times in the database
* Use standard PostgreSQL tools for database backup and maintenance
* Connect to the database using:
  - Host: localhost
  - Port: 5432
  - User: postgres
  - Database name: deevia_vms
  - Table: vms

Remote Monitoring
----------------

The system can be monitored remotely through:

1. **Remote Desktop**: Connect to the monitoring PC via Remote Desktop Protocol (RDP)
2. **Database Queries**: Connect to the PostgreSQL database remotely (requires network configuration)
3. **Log File Access**: Access log files through shared network folders

Maintenance Tasks
----------------

**Daily Maintenance:**
* Review system logs for errors
* Verify camera feeds are clear and properly positioned
* Check available disk space

**Weekly Maintenance:**
* Review recorded video samples for quality issues
* Verify database connectivity
* Check PLC communication status

**Monthly Maintenance:**
* Test emergency response procedures
* Back up configuration files
* Verify ROI positioning is still optimal
* Clean camera lenses if accessible

