import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO

point = (320, 290)

class Camera:
    def __init__(self, width=640, height=480, FPS=60):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, width, height, rs.format.z16, FPS)
        self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, FPS)
        self.config.enable_stream(rs.stream.accel)  # Enable accelerometer stream
        self.config.enable_stream(rs.stream.gyro)   # Enable gyroscope stream
        self.pipeline.start(self.config)

    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            return None, None
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        return depth_image, color_image

    def get_imu_data(self):
        frames = self.pipeline.wait_for_frames()
        accel_frame = frames.first_or_default(rs.stream.accel)
        gyro_frame = frames.first_or_default(rs.stream.gyro)

        if accel_frame and gyro_frame:
            accel_data = accel_frame.as_motion_frame().get_motion_data()
            gyro_data = gyro_frame.as_motion_frame().get_motion_data()
            return {
                'acceleration': {
                    'x': accel_data.x,
                    'y': accel_data.y,
                    'z': accel_data.z,
                },
                'gyroscope': {
                    'x': gyro_data.x,
                    'y': gyro_data.y,
                    'z': gyro_data.z,
                }
            }
        return None

    def stop(self):
        self.pipeline.stop()


# Initialize the camera and YOLO model
camera = Camera()
model = YOLO('yolov10n.pt')

try:
    while True:
        # Get depth and color frames
        depth_image, color_image = camera.get_frames()
        if depth_image is None or color_image is None:
            continue

        # Retrieve IMU data
        imu_data = camera.get_imu_data()
        if imu_data:
            print(f"Acceleration: {imu_data['acceleration']}")
            print(f"Gyroscope: {imu_data['gyroscope']}")

        # Run YOLO model on the color image
        results = model(color_image)
        annotated_image = results[0].plot()  # Plot annotations directly on the image

        # Display the RGB image
        cv2.imshow('RGB', color_image)

        # Display the depth image (normalize for better visualization)
        normalized_depth = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        depth_colormap = cv2.applyColorMap(normalized_depth, cv2.COLORMAP_JET)
        cv2.imshow('Depth', depth_colormap)

        # Display the YOLO output
        cv2.imshow('YOLO Output', annotated_image)

        # Check the depth at the specified point
        if depth_image[point[1], point[0]] > 1219:
            print("Move out the way")
            print(f"Depth at {point}: {depth_image[point[1], point[0]]}")

finally:
    camera.stop()
    cv2.destroyAllWindows()
