import pyrealsense2 as rs
import numpy as np
import cv2

point = (320, 290)
class Camera:
      def __init__(self, width=640, height=480, FPS=30):
            self.pipeline= rs.pipeline()
            self.config = rs.config()
            self.config.enable_stream(rs.stream.depth, width, height, rs.format.z16, FPS)
            self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, FPS)
      def show_camera(self):
            self.pipeline.start(self.config) 
            self.frame = self.pipeline.wait_for_frames()
            self.depth_frame = self.frame.get_depth_frame()
            self.color_frame = self.frame.get_color_frame()
while True:
        pipeline = rs.pipeline()
        config = rs.config()


        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        pipeline.start(config)
        frame = pipeline.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()
        depth_image= np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha=0.5), cv2.COLORMAP_JET)
        cv2.imshow('rgb', color_image)
        cv2.imshow('depth', depth_cm)

        if depth_image[point[1], point[0]] < 1219:
            print("Move out the way")
            print(depth_image[point[1], point[0]])
            # print(645//depth_image)
            pass
        key = cv2.waitKey(1)
        if key == 113:
              break
pipeline.stop()