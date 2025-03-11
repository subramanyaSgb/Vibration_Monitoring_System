import cv2
import socket
import struct
import numpy as np
from datetime import datetime, timedelta
import os
import time

class VideoReceiver:
    def __init__(self, host, port, save_dir="recordings"):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        print("Waiting for connection...")
        self.connection, self.client_address = self.sock.accept()
        print(f"Connected to {self.client_address}")
        self.FPS = 20
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        print(f"Recording directory ready: {os.path.abspath(self.save_dir)}")
        self.video_writer = None
        self.frame_size = None
        self.current_filename = None
        self.frames_written = 0

    def create_video_writer(self, output_path, width, height):
        try:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            return cv2.VideoWriter(output_path, fourcc, self.FPS, (width, height))
        except Exception as e:
            raise e

    def start_video_recording(self, video_writer, frame_raw):
        try:
            video_writer.write(frame_raw)
        except Exception as e:
            raise e
    def receive_frame(self):
        try:
            data = self.connection.recv(4)
            if not data:
                return None
            size = struct.unpack(">L", data)[0]
            frame_data = b""
            while len(frame_data) < size:
                packet = self.connection.recv(size - len(frame_data))
                if not packet:
                    return None
                frame_data += packet

            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is not None:
                print(f"Frame received with shape: {frame.shape}")

                cv2.rectangle(frame, (20, 20), (350, 80), (0, 0, 0), -1)
                c_time = datetime.now()
                cv2.putText(frame, str(c_time)[:-7], (40,65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            else:
                print("Received a None frame. Skipping.")
            return frame
        except Exception as e:
            print(f"Error receiving frame: {e}")
            return None


    def manage_video(self, width, height):
        try:
            current_time = datetime.now().strftime("%H:%M:%S")

            if self.video_writer is None:
                output_dir = "results/videos"
                current_date = datetime.now().strftime("%Y-%m-%d")
                date_dir = os.path.join(output_dir, current_date)
                os.makedirs(date_dir, exist_ok=True)

                video_filename = datetime.now().strftime('%H-%M-%S') + '.avi'
                output_path = os.path.join(date_dir, video_filename)
                self.video_writer = self.create_video_writer(output_path, width, height)

            return current_time
        except Exception as e:
            raise e

if __name__ == "__main__":
    video_receiver = VideoReceiver(host="192.168.0.58", port=12345)

    try:
        start_time = time.time()
        while True:
            
            frame = video_receiver.receive_frame()
            if frame is None:
                print("No frame received, stopping.")
                break
            width, height = frame.shape[1], frame.shape[0]
            current_time = video_receiver.manage_video(width, height)
            video_receiver.start_video_recording(video_receiver.video_writer, frame)
            end_time = time.time()
            seconds = end_time - start_time
    
            if seconds >=360:
                video_receiver.video_writer.release()
                video_receiver.video_writer = None
                start_time = time.time()
            cv2.namedWindow("Received Video", cv2.WINDOW_NORMAL)
            cv2.imshow("Received Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit command received.")
                break

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # video_receiver.release()
        cv2.destroyAllWindows()
