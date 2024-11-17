#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Header  # Import Header to create the header
import cv2
from cv_bridge import CvBridge

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_raw', 200)
        self.bridge = CvBridge()
        self.timer = self.create_timer(0.2, self.publish_frame)
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline(), cv2.CAP_GSTREAMER)

    def gstreamer_pipeline(self, capture_width=640, capture_height=480, display_width=640, display_height=480, framerate=15, flip_method=0):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (capture_width, capture_height, framerate, flip_method, display_width, display_height)
        )

    def publish_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Create a header for the image message
            header = Header()
            header.stamp = self.get_clock().now().to_msg()  # Set the current time
            header.frame_id = "camera_frame"  # Set a meaningful frame ID

            # Convert the frame to an Image message
            image_message = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            
            # Add the header to the image message
            image_message.header = header

            # Publish the image message
            self.publisher_.publish(image_message)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    rclpy.spin(camera_publisher)
    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
