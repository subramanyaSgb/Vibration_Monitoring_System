===========
Maintenance
===========

This section provides detailed information about maintaining the Vibration Monitoring System to ensure optimal performance and longevity.

Routine Maintenance Tasks
========================

Daily Checks
-----------

* **Log Review**: Review application logs in the ``logs/`` directory for any errors or warnings.
* **Camera Feed Verification**: Verify all camera feeds are operational and providing clear images.
* **Disk Space Check**: Ensure sufficient disk space is available for video recordings.
* **PLC Communication**: Confirm stable communication with the PLC system.

Weekly Tasks
-----------

* **Database Size Check**: Monitor the growth of the PostgreSQL database.
* **Temporary File Cleanup**: Remove temporary files that may accumulate in the system.
* **Camera Lens Inspection**: Physically inspect and clean camera lenses if necessary.
* **System Performance Check**: Review system resource usage (CPU, memory, network).

Monthly Tasks
------------

* **Configuration Backup**: Create backups of all configuration files in the ``data/`` directory.
* **Database Maintenance**: Run PostgreSQL VACUUM operations to optimize database performance.
* **System Updates**: Apply any pending system updates (see System Updates section).
* **Hardware Inspection**: Inspect all hardware components for signs of wear or damage.

Quarterly Tasks
--------------

* **Comprehensive System Backup**: Perform a full system backup including code, configurations, and database.
* **Network Infrastructure Check**: Verify all network components are functioning correctly.
* **Camera Calibration**: Recalibrate cameras if vibration detection accuracy has decreased.
* **Performance Optimization**: Review and optimize system performance based on historical data.

System Updates
=============

Software Update Procedure
------------------------

1. **Preparation**:
   
   * Create a complete backup of the current system.
   * Schedule maintenance window during non-critical operational hours.
   * Review the changelog of the new version.

2. **Update Process**:

   .. code-block:: bash

      # Navigate to the system directory
      cd D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024
      
      # Activate the virtual environment
      call activate vms
      
      # Update Python dependencies
      pip install -r requirements.txt --upgrade
      
      # Apply any database migrations if provided with the update
      python db_migrate.py  # if applicable

3. **Testing**:
   
   * Restart the application using run.bat
   * Verify all camera feeds are operational
   * Test PLC communication
   * Verify vibration detection is functioning correctly
   * Review logs for any errors or warnings

4. **Rollback Procedure** (if needed):
   
   * Stop the application
   * Restore from backup
   * Restart the application
   * Verify system functionality

Python Environment Updates
-------------------------

To update the Python virtual environment:

.. code-block:: bash

   # Activate the virtual environment
   call activate vms
   
   # Update pip itself
   pip install --upgrade pip
   
   # Update all packages
   pip install --upgrade -r requirements.txt

Operating System Updates
-----------------------

When applying Windows updates:

1. Schedule updates during maintenance windows
2. Ensure all system services are properly stopped
3. Backup system before major updates
4. After updates, verify all services restart correctly
5. Test system functionality comprehensively

Backup Procedures
===============

Database Backup
--------------

Perform regular PostgreSQL database backups:

.. code-block:: bash

   # Navigate to PostgreSQL bin directory
   cd "C:\Program Files\PostgreSQL\13\bin"
   
   # Backup the database
   pg_dump -U postgres deevia_vms > D:\Backups\db_backup_YYYY_MM_DD.sql

Configuration Backup
-------------------

Backup all configuration files:

.. code-block:: bash

   # Create backup directory with date
   $backupDir = "D:\Backups\Config_$(Get-Date -Format 'yyyy_MM_dd')"
   New-Item -Path $backupDir -ItemType Directory -Force
   
   # Copy configuration files
   Copy-Item -Path "D:\Projects\JSW_Bellary\BF2\Vibration_Monitoring_System\Development\VMS_BF2_07_12_2024\data\*" -Destination $backupDir -Recurse

Full System Backup
----------------

For complete system backup:

1. Stop all running application instances
2. Backup the entire application directory
3. Backup the PostgreSQL database
4. Document the current system state including:
   * Camera configurations
   * PLC settings
   * Hardware configurations
   * Network settings

Backup Retention Policy
---------------------

Implement the following backup retention schedule:

* Daily backups: Retain for 7 days
* Weekly backups: Retain for 4 weeks
* Monthly backups: Retain for 12 months
* Quarterly backups: Retain for 5 years

Health Monitoring
===============

System Health Indicators
----------------------

Monitor the following indicators for system health:

1. **CPU Usage**: Should remain below 70% during normal operation
2. **Memory Usage**: Should remain below 80% of available RAM
3. **Disk Space**: Maintain at least 20% free space on all drives
4. **Network Latency**: Camera feed latency should be < 500ms
5. **Database Response Time**: Queries should complete within 1 second
6. **Log Error Rate**: Sudden increases in error logs may indicate issues

Monitoring Tools
--------------

Use the following tools for system health monitoring:

1. **Windows Performance Monitor**:
   * Set up custom data collector sets for CPU, memory, disk, and network metrics
   * Configure alerts for threshold violations

2. **PostgreSQL Monitoring**:
   * Use pg_stat_statements to monitor query performance
   * Monitor database size growth over time
   * Set up alerts for slow queries

3. **Application Logs**:
   * Use a log analyzer to identify patterns and anomalies
   * Set up email alerts for critical errors

Preventive Maintenance
--------------------

1. **Regular System Reboots**:
   * Schedule weekly reboots during non-operational hours
   * Verify system comes up correctly after each reboot

2. **Database Optimization**:
   * Run VACUUM ANALYZE weekly to optimize database performance
   * Reindex tables monthly to maintain query performance

3. **Log Rotation**:
   * Ensure log rotation is functioning as configured
   * Verify logs are not consuming excessive disk space

Emergency Recovery
----------------

1. **Create Recovery Documentation**:
   * Document step-by-step recovery procedures
   * Include contact information for support personnel
   * Keep printed copies accessible to operators

2. **Recovery Testing**:
   * Conduct quarterly recovery drills
   * Validate backup integrity by performing test restores
   * Update recovery procedures based on test results

Troubleshooting Common Maintenance Issues
=======================================

Storage Space Issues
------------------

If disk space becomes critically low:

1. Check the videos directory and remove oldest recordings if appropriate
2. Verify log rotation is working correctly
3. Run disk cleanup utilities on the server
4. Consider increasing storage capacity if this is a recurring issue

Database Performance Degradation
------------------------------

If database performance degrades:

1. Run VACUUM ANALYZE on the database
2. Check for long-running queries and optimize if necessary
3. Verify index health and rebuild indexes if needed
4. Consider increasing database server resources if necessary

Camera Connection Issues
---------------------

If cameras become disconnected:

1. Verify network connectivity to the camera
2. Check RTSP URL configuration
3. Restart the camera if possible
4. Verify power supply to the camera
5. Replace the camera if hardware failure is confirmed

PLC Communication Failures
------------------------

If PLC communication fails:

1. Check serial port connections
2. Verify PLC is powered on and operational
3. Reset the serial connection
4. Run diagnostics on the PLC
5. Update PLC firmware if necessary

Maintenance Record Keeping
========================

Maintenance Log
-------------

Maintain a detailed maintenance log including:

* Date and time of maintenance
* Type of maintenance performed
* Issues discovered
* Actions taken
* Results of maintenance
* Name of personnel performing maintenance

This log should be stored both electronically and in hard copy.

System Documentation Updates
--------------------------

Update system documentation when:

* New hardware is installed
* Software is upgraded
* Configuration changes are made
* Operational procedures are modified

Ensure all documentation references the correct versions and includes the date of last update.

Conclusion
=========

Regular and systematic maintenance is essential for the reliable operation of the  Vibration Monitoring System. By following these guidelines, system administrators can ensure optimal performance, minimize downtime, and extend the service life of the system.

