=====================================
Vibration Monitoring System
=====================================

Introduction
===========

Project Overview
--------------

The Vibration Monitoring System is designed to monitor and detect vibrations in Steel Plant. The system utilizes camera-based vibration detection techniques to identify abnormal vibration patterns, which may indicate potential issues in the blast furnace operation. When vibrations are detected or when they stop, the system interacts with Programmable Logic Controllers (PLCs) to signal control systems and logs these events in a PostgreSQL database for historical analysis and reporting.

The system provides a real-time monitoring interface that displays camera feeds with visual indicators for vibration status. It also records video footage during vibration events for later analysis, with a configurable storage management system to handle disk space constraints.

Benefits
-------

* **Early Detection**: Identifies vibration anomalies before they lead to critical failures
* **Automated Monitoring**: Continuously monitors blast furnace operations without manual intervention
* **Historical Analysis**: Stores vibration events in a database for trend analysis and reporting
* **Real-time Alerts**: Interfaces with existing PLC systems to trigger appropriate actions when vibrations occur
* **Video Evidence**: Records video footage during vibration events for detailed analysis and troubleshooting
* **Flexible Configuration**: Customizable sensitivity settings and regions of interest
* **Resource Optimization**: Helps prevent unplanned downtime and extends equipment life

System Architecture
------------------

The Vibration Monitoring System is built with a modular architecture consisting of the following core components:

1. **Camera Monitoring**
   
   Utilizes RTSP camera feeds with OpenCV to capture and process video streams. The system supports multiple cameras simultaneously through multi-threaded processing.

2. **Vibration Detection Algorithm**
   
   Analyzes frame-to-frame differences within configured Regions of Interest (ROI) to detect vibration patterns. The algorithm employs Mean Squared Error (MSE) calculations and includes lighting compensation to handle varying environmental conditions.

3. **PLC Interface**
   
   Communicates with industrial PLCs via Modbus ASCII protocol to signal control systems. The interface allows bidirectional communication, sending signals when vibrations are detected or when stability returns.

4. **Database System**
   
   PostgreSQL database for storing vibration event data, including timestamps of when vibrations stop. This provides a historical record for analysis and reporting.

5. **Logging System**
   
   Comprehensive logging with automatic rotation for system monitoring and diagnostics. Logs are organized by date and provide detailed information about system operations and errors.

6. **Video Recording**
   
   Automatically captures and organizes video recordings of vibration events. The system includes storage management to prevent disk space issues.

The system's modular design allows for easy maintenance, configuration, and extension of functionality. Components are loosely coupled, making it possible to update or replace individual modules without affecting the entire system.

.. figure:: _static/system_architecture.png
   :alt: System Architecture Diagram
   :align: center
   
   *Figure 1: High-level architecture of the Vibration Monitoring System*

