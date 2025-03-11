API Reference
============

This section provides detailed information about the code structure, modules, and APIs of the JSW Bellary BF2 Vibration Monitoring System.

.. contents:: Table of Contents
   :local:
   :depth: 2

System Architecture
------------------

The Vibration Monitoring System consists of multiple interconnected modules, each responsible for specific functionality:

.. code-block:: text
            +---------------------------------------------+
            v                                             |
    +---------------+      +---------------+      +---------------+
    |               |      |               |      |               |
    |    app.py     |<---->|    cam.py     |      |    plc.py     |
    | (Main Module) |      | (Camera Mgmt) |      | (PLC Comms)   |
    |               |      |               |      |               |
    +-------+-------+      +---------------+      +-------+-------+
            |                                             |
            |                                             |
            v                                             v
    +---------------+                           +-------------------+
    |               |                           |                   |
    |  database.py  |                           |  logging_config.py|
    | (Data Storage)|                           |  (Logging System) |
    |               |                           |                   |
    +---------------+                           +-------------------+

Module: app.py
-------------

The main application module that coordinates all components and implements the core vibration detection algorithm.

Class: VideoProcessor
~~~~~~~~~~~~~~~~~~~

.. py:class:: VideoProcessor(mes_score=50, fps=10, video_duration=180, stable_threshold=1, motion_blur=True)

   Main class for processing video frames and detecting vibrations.

   :param mes_score: Threshold for motion energy score to detect vibrations
   :type mes_score: int
   :param fps: Frames per second for video processing
   :type fps: int
   :param video_duration: Duration of recorded video in seconds
   :type video_duration: int
   :param stable_threshold: Threshold for determining stability in seconds
   :type stable_threshold: int
   :param motion_blur: Enable/disable motion blur detection
   :type motion_blur: bool

Methods
^^^^^^^

.. py:method:: load_storage_limit(self)

   Loads storage limit from configuration file.

   :return: Storage limit in GB (default: 30GB)
   :rtype: int

   **Example:**

   .. code-block:: python

       storage_limit = processor.load_storage_limit()
       print(f"Storage limit: {storage_limit} GB")

.. py:method:: check_storage(self)

   Checks available disk space against the configured limit.

   :return: True if sufficient space, False if below limit
   :rtype: bool

   **Example:**

   .. code-block:: python

       if processor.check_storage():
           # Proceed with recording
       else:
           # Display warning or stop recording

.. py:method:: load_roi(self)

   Loads Region of Interest (ROI) configuration from file.

   :return: ROI configuration as dictionary
   :rtype: dict

   **Example:**

   .. code-block:: python

       roi = processor.load_roi()
       if roi:
           x, y, width, height = roi['x'], roi['y'], roi['width'], roi['height']

.. py:method:: add_camera(self, cam_serial_num, rtsp_path)

   Adds and initializes a camera connection.

   :param cam_serial_num: Camera serial number identifier
   :type cam_serial_num: str
   :param rtsp_path: RTSP URL for camera connection
   :type rtsp_path: str

   **Example:**

   .. code-block:: python

       processor.add_camera("CAM001", "rtsp://192.168.1.100:554/stream")

.. py:method:: create_video_writer(self, output_path)

   Creates a video writer object for recording.

   :param output_path: Path where video will be saved
   :type output_path: str
   :return: OpenCV VideoWriter object
   :rtype: cv2.VideoWriter

   **Example:**

   .. code-block:: python

       writer = processor.create_video_writer("path/to/output.avi")

.. py:method:: mse(self, image_a, image_b)

   Calculates Mean Squared Error between two images.

   :param image_a: First image for comparison
   :type image_a: numpy.ndarray
   :param image_b: Second image for comparison
   :type image_b: numpy.ndarray
   :return: MSE value
   :rtype: float

   **Example:**

   .. code-block:: python

       error = processor.mse(gray_frame1, gray_frame2)
       if error > threshold:
           print("Motion detected")

.. py:method:: lighting_compensation(self, frame)

   Applies histogram equalization to compensate for lighting variations.

   :param frame: Input BGR image
   :type frame: numpy.ndarray
   :return: Histogram equalized grayscale image
   :rtype: numpy.ndarray

   **Example:**

   .. code-block:: python

       compensated = processor.lighting_compensation(frame)

.. py:method:: overlay_logo(self, frame, logo, position=(10, 10))

   Overlays a logo on the frame.

   :param frame: Target frame to overlay logo on
   :type frame: numpy.ndarray
   :param logo: Logo image
   :type logo: numpy.ndarray
   :param position: Tuple of (x, y) coordinates for logo placement
   :type position: tuple
   :return: Frame with overlaid logo
   :rtype: numpy.ndarray

   **Example:**

   .. code-block:: python

       frame_with_logo = processor.overlay_logo(frame, logo_img, (20, 20))

.. py:method:: put_title(self, frame, title)

   Adds a title text to the frame.

   :param frame: Target frame to add title to
   :type frame: numpy.ndarray
   :param title: Text to display as title
   :type title: str
   :return: Frame with title
   :rtype: numpy.ndarray

   **Example:**

   .. code-block:: python

       processor.put_title(frame, "Vibration Monitoring System")

.. py:method:: put_motion_notification(self, frame, text)

   Adds vibration status notification text to the frame.

   :param frame: Target frame to add notification to
   :type frame: numpy.ndarray
   :param text: Notification text
   :type text: str
   :return: Frame with notification
   :rtype: numpy.ndarray

   **Example:**

   .. code-block:: python

       processor.put_motion_notification(frame, "Vibration Detected!")

.. py:method:: show(self, name, frame)

   Displays frame in a window.

   :param name: Window name
   :type name: str
   :param frame: Frame to display
   :type frame: numpy.ndarray

   **Example:**

   .. code-block:: python

       processor.show("Camera Feed", frame)

.. py:method:: start_video_recording(self, video_writer, frame_raw)

   Writes a frame to video recording.

   :param video_writer: OpenCV VideoWriter object
   :type video_writer: cv2.VideoWriter
   :param frame_raw: Frame to write to video
   :type frame_raw: numpy.ndarray

   **Example:**

   .. code-block:: python

       processor.start_video_recording(writer, frame)

.. py:method:: process_frame(self, frame_raw, logo, frame_gray)

   Core function for processing each frame for vibration detection.

   :param frame_raw: Original unprocessed frame
   :type frame_raw: numpy.ndarray
   :param logo: Logo image to overlay
   :type logo: numpy.ndarray
   :param frame_gray: Grayscale version of frame
   :type frame_gray: numpy.ndarray
   :return: Processed frame
   :rtype: numpy.ndarray

   **Example:**

   .. code-block:: python

       processed_frame = processor.process_frame(frame, logo, gray_frame)

.. py:method:: manage_video(self)

   Manages video recording file creation and path.

   :return: Current time string in format "HH:MM:SS"
   :rtype: str

   **Example:**

   .. code-block:: python

       current_time = processor.manage_video()

.. py:method:: process(self)

   Main processing loop for the application.

   **Example:**

   .. code-block:: python

       processor.process()

Functions
^^^^^^^^^

.. py:function:: load_config()

   Loads application configuration from file.

   :return: Tuple of (mes_score, fps, video_duration, stable_threshold, motion_blur)
   :rtype: tuple

   **Example:**

   .. code-block:: python

       mes_score, fps, video_duration, stable_threshold, motion_blur = load_config()

Module: cam.py
-------------

This module handles camera connections and frame acquisition.

Class: CamConnect
~~~~~~~~~~~~~~~~

.. py:class:: CamConnect(cam_address)

   Manages connection to a camera via RTSP.

   :param cam_address: RTSP URL for camera connection
   :type cam_address: str

Methods
^^^^^^^

.. py:method:: grab_frame(self)

   Thread function to continuously grab frames from camera.

   **Example:**

   .. code-block:: python

       # Called internally
       import threading
       thread = threading.Thread(target=camera.grab_frame)
       thread.start()

.. py:method:: reconnect_camera(self)

   Attempts to reconnect to camera after connection loss.

   :return: True if reconnection successful, False otherwise
   :rtype: bool

   **Example:**

   .. code-block:: python

       if not camera.reconnect_camera():
           print("Failed to reconnect to camera")

.. py:method:: read(self)

   Returns the current frame from camera.

   :return: Current frame or error image if unavailable
   :rtype: numpy.ndarray

   **Example:**

   .. code-block:: python

       frame = camera.read()
       cv2.imshow("Frame", frame)

.. py:method:: release(self)

   Releases the camera connection.

   **Example:**

   .. code-block:: python

       camera.release()

Class: CameraThread
~~~~~~~~~~~~~~~~~

.. py:class:: CameraThread(camera_serial_number, rtsp_link, frame_dictionary)

   Thread class for handling camera operations in parallel.

   :param camera_serial_number: Serial number identifier for camera
   :type camera_serial_number: str
   :param rtsp_link: RTSP URL for camera connection
   :type rtsp_link: str
   :param frame_dictionary: Shared dictionary to store frames from multiple cameras
   :type frame_dictionary: dict

Methods
^^^^^^^

.. py:method:: run(self)

   Main thread function that continuously captures frames.

   **Example:**

   .. code-block:: python

       # Called by starting the thread
       camera_thread.start()

.. py:method:: stop(self)

   Stops the thread execution.

   **Example:**

   .. code-block:: python

       camera_thread.stop()

Functions
^^^^^^^^^

.. py:function:: load_camera_config()

   Loads camera configuration from data/cameras.json.

   :return: Dictionary mapping camera serial numbers to RTSP URLs
   :rtype: dict

   **Example:**

   .. code-block:: python

       camera_config = load_camera_config()
       for serial, url in camera_config.items():
           print(f"Camera {serial}: {url}")

Module: plc.py
-------------

This module handles communication with the Programmable Logic Controller.

Class: PLC
~~~~~~~~~

.. py:class:: PLC()

   Manages connection and communication with the PLC.

Methods
^^^^^^^

.. py:method:: convert_ma_to_percentage(self, ma)

   Converts milliamp readings to percentage (range: -12mA to 20mA → 0% to 100%).

   :param ma: Current in milliamps
   :type ma: float
   :return: Percentage value
   :rtype: float

   **Example:**

   .. code-block:: python

       percentage = plc.convert_ma_to_percentage(15.5)
       print(f"Current percentage: {percentage}%")

.. py:method:: connectToPLC(self)

   Establishes connection to PLC via Modbus ASCII protocol on COM7.

   :return: True if connection established, False otherwise
   :rtype: bool

   **Example:**

   .. code-block:: python

       if plc.connectToPLC():
           print("Connected to PLC")
       else:
           print("Failed to connect to PLC")

.. py:method:: read_bit(self, address)

   Reads a value from the specified PLC register.

   :param address: Register address
   :type address: int
   :return: Value read from register
   :rtype: int

   **Example:**

   .. code-block:: python

       value = plc.read_bit(4106)
       print(f"Register value: {value}")

.. py:method:: write_bit(self, address, data)

   Writes a value to the specified PLC register.

   :param address: Register address
   :type address: int
   :param data: Value to write
   :type data: int
   :return: True if write successful, False otherwise
   :rtype: bool

   **Example:**

   .. code-block:: python

       success = plc.write_bit(4106, 200)
       if success:
           print("Value written successfully")

Module: database.py
-----------------

This module handles database operations for storing vibration events.

Functions
^^^^^^^^^

.. py:function:: create_db_if_not_exists()

   Creates the PostgreSQL database if it doesn't exist.

   **Example:**

   .. code-block:: python

       create_db_if_not_exists()

.. py:function:: create_table_if_not_exists()

   Creates the "vms" table if it doesn't exist.

   **Example:**

   .. code-block:: python

       create_table_if_not_exists()

.. py:function:: store_vibration_stopped_time()

   Records the timestamp when vibration stops.

   **Example:**

   .. code-block:: python

       store_vibration_stopped_time()

Module: logging_config.py
-----------------------

This module configures the application-wide logging system.

Functions
^^^^^^^^^

.. py:function:: setup_logger()

   Configures a logger with TimedRotatingFileHandler.

   :return: Configured logger object
   :rtype: logging.Logger

   **Example:**

   .. code-block:: python

       logger = setup_logger()
       logger.info("Application started")

Module: file_verifier.py
----------------------

This module handles file verification to ensure required files exist.

Functions
^^^^^^^^^

.. py:function:: verify_config_files()

   Checks for the existence of all required configuration files.

   :return: Boolean indicating if all required files are present
   :rtype: bool

   **Example:**

   .. code-block:: python

       if verify_config_files():
           print("All configuration files found")
       else:
           print("Missing configuration files")

.. py:function:: create_directories()

   Creates necessary directories if they don't exist.

   **Example:**

   .. code-block:: python

       create_directories()

API Usage Examples
----------------

Camera Initialization and Frame Capture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Initialize camera system
    camera_config = load_camera_config()
    frame_dict = {}
    camera_threads = []
    
    # Create camera threads
    for camera_serial, rtsp_url in camera_config.items():
        camera_thread = CameraThread(camera_serial, rtsp_url, frame_dict)
        camera_threads.append(camera_thread)
        camera_thread.start()
    
    # Process frames
    while True:
        for camera_serial in camera_config

