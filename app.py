import cv2
import time
import numpy as np
import os
from datetime import datetime
from cam import CameraThread, load_camera_config, error_image
from logging_config import logger
from database import create_db_if_not_exists, create_table_if_not_exists, store_vibration_stopped_time
from file_verifier import check_and_create_files
from plc import PLC
import json
import traceback
import sys
import shutil
from icecream import ic
from copy import deepcopy
ic.disable()
plc = PLC()

class VideoProcessor:
    def __init__(self, mes_score=50, fps=10, video_duration=180, stable_threshold=1, motion_blur=True):
        """
        Initializes the Vibration Detection System.

        Parameters:
        ----------
        mes_score : int, optional
            The motion energy score threshold for detecting vibrations (default is 50).
        fps : int, optional
            Frames per second for video processing (default is 10).
        video_duration : int, optional
            Duration of the recorded video in seconds (default is 180).
        stable_threshold : int, optional
            Threshold for determining stability in seconds (default is 1).
        motion_blur : bool, optional
            Flag to enable or disable motion blur detection (default is True).

        Attributes:
        ----------
        MOTION_BLUR : bool
            Indicates whether motion blur detection is enabled.
        FPS : int
            Frames per second for video capture.
        VIDEO_DURATION : int
            Duration of the video in seconds.
        stable_time : int
            Tracks the stable duration before detecting vibration.
        STABLE_THRESHOLD : int
            Threshold in seconds for determining if an object is stable.
        mes_score : int
            Motion energy score used for vibration detection.
        cnt_frame : int
            Counter for processed frames.
        fps : int
            Current frames per second.
        frame_dict : dict
            Dictionary to store frames and related metadata.
        camera_threads : list
            List to store active camera threads.
        video_writer : object or None
            Video writer object for saving video files.
        start_time : float
            Timestamp of when the system was initialized.
        video_start_time : float
            Timestamp of when video recording started.
        frame_gray_p : object or None
            Placeholder for storing the previous grayscale frame.
        title : str
            Title of the system interface or display.
        last_saved_time : float
            Timestamp of the last saved video or frame.
        roi : object
            Region of interest (ROI) configuration loaded from a file or database.
        fps_for_frame : int
            FPS counter for individual frames.
        last_plc_signal_time : float
            Timestamp of the last received PLC (Programmable Logic Controller) signal.

        Notes:
        -----
        - Calls `create_db_if_not_exists()` and `create_table_if_not_exists()` 
        to ensure the database and tables are initialized.
        - Loads the region of interest (ROI) using `load_roi()`.
        - Uses the `ic()` function for debugging initialization.
        """
        self.MOTION_BLUR = motion_blur
        self.FPS = fps
        self.VIDEO_DURATION = video_duration
        self.stable_time = 0  # Time in seconds
        self.STABLE_THRESHOLD = stable_threshold
        self.mes_score = mes_score
        ic("IN initialization :", self.mes_score)
        self.cnt_frame = 0
        self.fps = 0
        self.frame_dict = {}
        self.camera_threads = []
        self.video_writer = None
        self.start_time = time.time()
        self.video_start_time = self.start_time
        self.frame_gray_p = None
        self.title = "Vibration Detection System"
        self.last_saved_time = time.time()
        create_db_if_not_exists()
        create_table_if_not_exists()
        self.roi = self.load_roi()
        self.fps_for_frame = 0
        self.last_plc_signal_time = 0


    def load_storage_limit(self):
        """Load storage limit from the storage_limit.json file."""
        try:
            with open('data/storage_limit.json', 'r') as file:
                storage_data = json.load(file)
            return storage_data.get('storage_limit', 30)  # Default to 30 if the key doesn't exist
        except Exception as e:
            logger.error(f"Error loading storage limit from JSON: {e}")
            return 30  # Default to 30 GB if an error occurs
    
    def check_storage(self):
        """Check available disk space and return True if sufficient, False if less than the limit."""
        storage_limit = self.load_storage_limit()  # Get the storage limit from the JSON file
        total, used, free = shutil.disk_usage("/")  # Adjust the path if necessary
        free_gb = free // (2**30)  # Convert bytes to GB
        logger.info(f"Storage left: {free_gb} GB, Storage limit: {storage_limit} GB")

        if free_gb < storage_limit:
            logger.warning(f"Storage is low: {free_gb} GB left.")
            return False
        return True

    def load_roi(self):
        try:
            with open('data/roi.json', 'r') as file:
                roi_data = json.load(file)
            logger.info("ROI loaded successfully.")
            return roi_data['roi']
        except Exception as e:
            logger.error(f"Error reading ROI data: {e}")
            logger.error(traceback.format_exc())
            return None

    def add_camera(self, cam_serial_num, rtsp_path):
        try:
            thread = CameraThread(cam_serial_num, rtsp_path, self.frame_dict)
            self.camera_threads.append(thread)
            thread.start()
            logger.info(f"Camera with serial {cam_serial_num} added successfully.")
        except Exception as e:
            logger.error(f"Error adding camera {cam_serial_num}: {e}")
            logger.error(traceback.format_exc())

    def create_video_writer(self, output_path):
        try:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            return cv2.VideoWriter(output_path, fourcc, self.FPS, (1920, 1080))  # Adjust the frame size as needed
        except Exception as e:
            logger.error(f"Error creating video writer: {e}")
            logger.error(traceback.format_exc())
            raise e

    def mse(self, image_a, image_b):
        try:
            err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
            err /= float(image_a.shape[0] * image_a.shape[1])
            return err
        except Exception as e:
            logger.error(f"Error in MSE calculation: {e}")
            logger.error(traceback.format_exc())
            raise e

    def lighting_compensation(self, frame):
        try:
            logger.info("Performing lighting compensation...")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            compensated_frame = cv2.equalizeHist(gray)
            logger.info("Lighting compensation applied.")
            return compensated_frame
        except Exception as e:
            logger.error(f"Error in lighting compensation: {e}")
            logger.error(traceback.format_exc())
            raise e

    def overlay_logo(self, frame, logo, position=(10, 10)):
        try:
            logger.info("Overlaying logo...")
            h, w = logo.shape[:2]
            x, y = position
            x = frame.shape[1] - w  # Adjust position to overlay on the right side

            if logo.shape[2] == 4:  # RGBA
                alpha_logo = logo[:, :, 3] / 255.0  # Get the alpha channel
                alpha_frame = 1.0 - alpha_logo  # Inverse alpha for the frame

                for c in range(0, 3):
                    frame[y:y + h, x:x + w, c] = (alpha_logo * logo[:, :, c] + alpha_frame * frame[y:y + h, x:x + w, c])
            else:  # No alpha channel
                frame[y:y + h, x:x + w] = logo

            return frame
        except Exception as e:
            logger.error(f"Error in overlaying logo: {e}")
            logger.error(traceback.format_exc())
            raise e

    def put_title(self, frame, title):
        try:
            logger.info("Adding title to frame...")
            height, width, _ = frame.shape
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = (255, 255, 255)  # White color
            thickness = 2
            text_size = cv2.getTextSize(title, font, font_scale, thickness)[0]

            x = (width - text_size[0]) // 2
            y = 50  # Position near the top
            cv2.rectangle(frame, (x - 10, y - text_size[1] - 10), (x + text_size[0] + 10, y + 10), (0, 0, 0), -1)
            cv2.putText(frame, title, (x, y), font, font_scale, font_color, thickness)
            logger.info("Title added successfully.")
        except Exception as e:
            logger.error(f"Error in putting title on frame: {e}")
            logger.error(traceback.format_exc())
            raise e

    def put_motion_notification(self, frame, text):
        try:
            logger.info(f"Adding motion notification: {text}")
            height, width, _ = frame.shape
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = (0, 0, 255)  # Red color
            thickness = 2
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            x = (width - text_size[0]) // 2
            y = height - 30  # Position near the bottom

            # Draw a black rectangle for the background
            cv2.rectangle(frame, (x - 10, y - text_size[1] - 10), (x + text_size[0] + 10, y + 10), (0, 0, 0), -1)

            if text=="Vibration Detected!":
            # Put the text
                cv2.putText(frame, text, (x, y), font, font_scale, (0,255,0), thickness)
            else:    
                cv2.putText(frame, text, (x, y), font, font_scale, font_color, thickness)
            logger.info("Motion notification added successfully.")
        except Exception as e:
            logger.error(f"Error in putting motion notification: {e}")
            logger.error(traceback.format_exc())
            raise e

    def show(self, name, frame):
        try:
            logger.info(f"Displaying frame in window: {name}")
            cv2.namedWindow(name, cv2.WINDOW_NORMAL)
            cv2.imshow(name, frame)
        except Exception as e:
            logger.error(f"Error showing frame: {e}")
            logger.error(traceback.format_exc())
            raise e

    def start_video_recording(self, video_writer, frame_raw):
        try:
            logger.info("Starting video recording...")
            video_writer.write(frame_raw)
            logger.info(f"Frame written to video.\n{'='*100}")
        except Exception as e:
            logger.error(f"Error in starting video recording: {e}")
            logger.error(traceback.format_exc())
            raise e

    def process_frame(self, frame_raw, logo, frame_gray):
        try:
            ic.disable()
            logger.info(f"Processing frame {self.cnt_frame}...")

            # Check storage before continuing the recording
            if not self.check_storage():
                self.overlay_logo(frame_raw, logo, (10, 10))
                self.put_title(frame_raw, self.title)
                self.put_motion_notification(frame_raw, "Storage Full!")  # Show "Storage Full!" notification
                fps_text = f"FPS: {int(self.fps_for_frame)}"
                cv2.putText(frame_raw, fps_text, (10, frame_raw.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                self.show(f'Camera Feed', frame_raw)  # Display the frame with the notification
                return  # Stop further processing of frames, recording won't continue

            self.roi = self.load_roi()
            # Extract the ROI for vibration detection
            roi_x = self.roi['x']
            roi_y = self.roi['y']
            roi_width = self.roi['width']
            roi_height = self.roi['height']

            # Extract ROI region from the frame
            roi_frame = frame_raw[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
            logger.info("ROI extracted.")

            if self.MOTION_BLUR:
                logger.info("Applying motion blur...")
                frame = cv2.GaussianBlur(frame_raw, (3, 3), 0)
                logger.info("Motion blur applied.")
            else:
                frame = frame_raw

            # Lighting compensation
            compensated_frame = self.lighting_compensation(frame)

            # Overlay logo
            self.overlay_logo(frame, logo, (10, 10))

            # Put title
            self.put_title(frame, self.title)

            # Draw the ROI rectangle on the full frame (for display purposes)
            cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)  # Green color

            # Perform vibration detection only inside the ROI
            if self.cnt_frame > 0:
                mse_result = self.mse(cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY), self.frame_gray_p[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width])
                if mse_result > self.mes_score:  # Detect motion in ROI
                    ic("WHile checking condition of mse",self.mes_score)
                    ic(mse_result)
                    ic(mse_result > self.mes_score)
                    self.stable_time = 0  # Reset stable time when vibration is detected
                    self.video_start_time = time.time()
                    ic(self.stable_time, "vibration When mse is", mse_result)
                    logger.info('\n[Vibration Detected...!]\n')
                    self.put_motion_notification(frame, "Vibration Detected!")
                    plc.write_bit(4106, 200) # 4106 D10 # Send off signal to y0
                else:
                    # Increment stable time by the duration of the frame processing
                    self.stable_time += (time.time() - self.video_start_time)
                    ic(self.stable_time, "No vibration..... When mse is", mse_result)
                    logger.info(f"Logging self.stable_time - {self.stable_time} untill it reaches -Self.stable_theshold: {self.STABLE_THRESHOLD}")
                    if self.stable_time > self.STABLE_THRESHOLD:
                        logger.info(f"self.stable_time {self.stable_time} is now greater than self.stable_Threshold {self.STABLE_THRESHOLD} condition matched.....")
                        ic(self.stable_time > self.STABLE_THRESHOLD)
                        # If stable time exceeds the threshold, trigger the actions
                        logger.info('[Stable : No Vibration Detected....]\n')
                        ic('[Stable : No Vibration Detected....]\n')
                        self.put_motion_notification(frame, "No Vibration detected")  # Display stable notification    
                        # Check if 10 seconds have passed since the last PLC signal was sent
                        current_time = time.time()
                        plc.write_bit(4106, 100) # 4106 D10 send on signal to y0
                        if not hasattr(self, 'last_plc_signal_time') or current_time - self.last_plc_signal_time >= 10:
                            store_vibration_stopped_time()  # Save the time to the database
                            print("Send Signal TO PLC")
                            # Send signal to PLC
                            self.last_plc_signal_time = current_time  # Update the time of the last signal
                        else:
                            logger.info("Waiting to send PLC signal until 10 seconds have passed.")
                            # print(f'Waiting to send PLC signal until 10 seconds have passed. {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}')

                        # Send signal to plc
                        # plc.write_bit(4106, 100) # 4106 D10 send on signal to y0
                        # self.stable_time = 0  # Reset the stable time after sending notification
                        # self.video_start_time = time.time()
                    else:
                        self.put_motion_notification(frame, "Vibration Detected!")

            # Display FPS in the bottom-left corner
            fps_text = f"FPS: {int(self.fps_for_frame)}"
            cv2.putText(frame, fps_text, (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Display the frame
            self.show(f'Camera Feed', frame)
            logger.info(f"Frame {self.cnt_frame} processed successfully.")

            self.frame_gray_p = cv2.cvtColor(frame_raw, cv2.COLOR_BGR2GRAY)

        except Exception as e:
            logger.error(f"Error processing frame {self.cnt_frame}: {e}")
            logger.error(traceback.format_exc())
            raise e

    def manage_video(self):
        try:
            current_time = datetime.now().strftime("%H:%M:%S")

            if self.video_writer is None:
                output_dir = "results/videos"
                current_date = datetime.now().strftime("%Y-%m-%d")
                date_dir = os.path.join(output_dir, current_date)
                os.makedirs(date_dir, exist_ok=True)

                video_filename = datetime.now().strftime('%H-%M-%S') + '.avi'
                output_path = os.path.join(date_dir, video_filename)
                self.video_writer = self.create_video_writer(output_path)
                logger.info(f"Started recording: {output_path}")

            return current_time
        except Exception as e:
            logger.error(f"Error in managing video: {e}")
            logger.error(traceback.format_exc())
            raise e

    def process(self):
        try:
            logo_path = 'data/logo.png'  # Top left logo
            logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

            camera_config = load_camera_config()
            for cam_serial_num, rtsp_path in camera_config.items():
                self.add_camera(cam_serial_num, rtsp_path)
            # prev_frame_time = 0
            # new_frame_time = 0
            while True:
                prev_frame_time = time.time()
                for thread in self.camera_threads:
                    frame_raw = self.frame_dict.get(thread.cam_serial_num, error_image)
                if frame_raw is None:
                    frame_raw = error_image.copy()
                cv2.rectangle(frame_raw, (20,20), (600,100), (0,0,0), -1)
                c_time = datetime.now()
                cv2.putText(frame_raw, str(c_time)[:-7], (40,65), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2 )
                self.frame_for_video = frame_raw.copy()
                # frame_raw = cv2.resize(frame_raw, (1920, 1080))  # Resize the frame if necessary
                frame_gray = cv2.cvtColor(frame_raw, cv2.COLOR_BGR2GRAY)

                current_time = self.manage_video()
                frame_for_process = frame_raw.copy()
                self.process_frame(frame_for_process, logo, frame_gray)
                if self.check_storage():
                    self.start_video_recording(self.video_writer, self.frame_for_video)
                

                end_time = time.time()
                seconds = end_time - self.start_time
                self.fps = 1.0 / seconds
                self.cnt_frame += 1

                if seconds >= self.VIDEO_DURATION:
                    self.video_writer.release()
                    self.video_writer = None
                    self.start_time = time.time()  # Reset the start time for the next video

                if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' key is pressed
                    logger.info("Keyboard interrupt received. Exiting...")
                    break
                new_frame_time = time.time()
                self.fps_for_frame = 1/(new_frame_time-prev_frame_time) 
                # prev_frame_time = new_frame_time

        except Exception as e:
            logger.error(f"Error in main processing loop: {e}")
            logger.error(traceback.format_exc())

        finally:
            if self.video_writer is not None:
                self.video_writer.release()
            plc.write_bit(4106, 200)
            cv2.destroyAllWindows()
            sys.exit(0)

def load_config():
    """Load storage limit from the storage_limit.json file."""
    try:
        with open('data/config.json', 'r') as file:
            config_data = json.load(file)
        mes_score = config_data.get('mes_score', 50)
        fps = config_data.get('fps', 20)
        video_duration = config_data.get('video_duration', 180)
        stable_threshold = config_data.get('stable_threshold', 5)
        motion_blur = config_data.get('motion_blur', True)
        return mes_score, fps, video_duration, stable_threshold, motion_blur
    except Exception as e:
        logger.error(f"Error loading storage limit from JSON: {e}")
        mes_score, fps, video_duration, stable_threshold, motion_blur = 50, 20, 180, 5, True
        return mes_score, fps, video_duration, stable_threshold, motion_blur 

if __name__ == "__main__":
    # check_and_create_files() only use if you need to create files inside data folder
    mes_score, fps, video_duration, stable_threshold, motion_blur = load_config()
    ic(mes_score, fps, video_duration, stable_threshold, motion_blur)
    video_processor = VideoProcessor(mes_score, fps, video_duration, stable_threshold, motion_blur)
    video_processor.process()
