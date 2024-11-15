import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
point = (320, 290)
class Camera:
      def __init__(self, width=640, height=480, FPS=60):
            self.pipeline= rs.pipeline()
            self.config = rs.config()
            self.config.enable_stream(rs.stream.depth, width, height, rs.format.z16, FPS)
            self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, FPS)
            self.confgi.enable_stream(rs.stream.gyro)
           
      def ready_images(self):
            self.pipeline.start(self.config) 
            self.frame = self.pipeline.wait_for_frames()
            self.depth_frame = self.frame.get_depth_frame()
            self.color_frame = self.frame.get_color_frame()
            self.depth_image= np.asanyarray(self.depth_frame.get_data())
            self.color_image = np.asanyarray(self.color_frame.get_data())
            return self.depth_image, self.color_image
      def motion(self):
            pass
     
      def display(self):
            print(self.depth_image)
            # print(self.gyro_data)
while True:
        
        camera = Camera()
        depth_image, color_image = camera.ready_images()
        cv2.imshow('rgb', color_image)
        cv2.imshow('depth', depth_image)
        model = YOLO('yolov8n.pt')
        results = model(source=color_image, show=True, conf=0.4, save=False)
        if depth_image[point[1], point[0]] > 1219:
            print("Move out the way", type(depth_image))
            print(depth_image[point[1], point[0]])
        camera.display()
        key = cv2.waitKey(1)
        if key == 113:
              break
camera.pipeline.stop()