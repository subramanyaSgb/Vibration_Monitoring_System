import cv2
import time
import threading
import numpy as np
from logging_config import logger
import json
import traceback

thread_count_lock = threading.Lock()
lock = threading.Lock()
error_image = np.zeros((1080, 1920, 3), dtype="uint8")  # Adjusted to 3 channels for color image
# Define the text and its properties
text = "Camera Not Connected"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 3
font_thickness = 10
text_color = (255, 255, 255)  # White color

# Get the text size to position it in the center
text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
text_x = (error_image.shape[1] - text_size[0]) // 2
text_y = (error_image.shape[0] + text_size[1]) // 2

# Put the text on the image
cv2.putText(error_image, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)


class CamConnect:
    def __init__(self, cam_address):
        self.cam_address = cam_address
        self.capture = None
        self.RECONNECTION_PERIOD = 0.5
        self.reconnect_camera()
        self.frame = error_image
        self.grab_thread = None

    def grab_frame(self):
        while True:
            ret, self.frame = self.capture.read()
            if ret is False:
                self.reconnect_camera()
                self.frame = error_image
                break
            time.sleep(0.01)

    def reconnect_camera(self):
        attempts = 0
        while attempts < 3:  # Limit reconnection attempts
            try:
                self.capture = cv2.VideoCapture(self.cam_address)
                if not self.capture.isOpened():
                    raise Exception(f"Could not connect to a camera: {self.cam_address}")

                logger.info(f"Connected to camera: {self.cam_address}")
                self.grab_thread = threading.Thread(target=self.grab_frame, daemon=True)
                self.grab_thread.start()
                break
            except Exception as e:
                logger.error(f"Error in reconnect_camera: {e}")
                logger.error(traceback.format_exc())
                attempts += 1
                time.sleep(self.RECONNECTION_PERIOD)

    def read(self):
        return self.frame

    def release(self):
        if self.capture is not None:
            self.capture.release()


class CameraThread(threading.Thread):
    def __init__(self, camera_serial_number, rtsp_link, frame_dictionary):
        super(CameraThread, self).__init__()
        self.cam_serial_num = camera_serial_number
        self.rtsp_url = rtsp_link
        self.frame = error_image
        self.running = True
        self.frame_dict = frame_dictionary

    def run(self):
        try:
            cap = CamConnect(self.rtsp_url)
            while self.running:
                frame = cap.read()
                with lock:
                    self.frame_dict[self.cam_serial_num] = frame
                self.frame = frame
                time.sleep(0.01)
        except Exception as e:
            logger.error(f"Error in CameraThread run(): {e}")
            logger.error(traceback.format_exc())

    def stop(self):
        self.running = False


def load_camera_config():
    try:
        with open('data/cameras.json', 'r') as f:
            config = json.load(f)
        logger.info("Camera configuration loaded successfully.")
        return config
    except FileNotFoundError:
        logger.error("Config file 'cameras.json' not found.")
        return {}
    except Exception as e:
        logger.error(f"Error loading camera configuration: {e}")
        logger.error(traceback.format_exc())
        return {}


if __name__ == "__main__":
    frame_dict = {}
    camera_threads = []

    camera_config = load_camera_config()

    for cam_serial_num, rtsp_path in camera_config.items():
        try:
            thread = CameraThread(cam_serial_num, rtsp_path, frame_dict)
            camera_threads.append(thread)
            thread.start()
            cv2.namedWindow(f'Camera {thread.cam_serial_num} Feed', cv2.WINDOW_NORMAL)
        except Exception as e:
            logger.error(f"Error starting camera thread for {cam_serial_num}: {e}")
            logger.error(traceback.format_exc())

    while True:
        for thread in camera_threads:
            latest_frame = frame_dict.get(thread.cam_serial_num, error_image)
            with lock:
                cv2.imshow(f'Camera {thread.cam_serial_num} Feed', latest_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01)

    # Stop all camera threads
    for thread in camera_threads:
        thread.stop()
        thread.join()

    cv2.destroyAllWindows()
