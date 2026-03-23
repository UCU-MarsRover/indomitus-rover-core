#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
from sensor_msgs_py.point_cloud2 import create_cloud

class PointCloudFilterNode(Node):
    def __init__(self):
        super().__init__('point_cloud_filter')
        
        # Declare parameters
        self.declare_parameter('min_z', 0.1)
        self.declare_parameter('max_z', 1.5)
        self.declare_parameter('frame_id', 'camera_depth_optical_frame')
        self.declare_parameter('input_topic', '/camera/points')
        self.declare_parameter('output_topic', '/perception/obstacle_points')
        
        # Get parameters
        self.min_z = self.get_parameter('min_z').value
        self.max_z = self.get_parameter('max_z').value
        self.target_frame = self.get_parameter('frame_id').value
        input_topic = self.get_parameter('input_topic').value
        output_topic = self.get_parameter('output_topic').value
        
        # Subscriptions and Publishers
        self.subscription = self.create_subscription(PointCloud2, input_topic, self.pc_callback, 10)
        self.publisher = self.create_publisher(PointCloud2, output_topic, 10)
        
        self.get_logger().info(f"Point Cloud Filter started.")

    def pc_callback(self, msg):
        # Read the point cloud into an iterable
        cloud_data = list(pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))
        
        # Filter points based on the Z axis (height)
        filtered_points = [
            point for point in cloud_data 
            if self.min_z <= point[2] <= self.max_z
        ]
        
        # Create a new PointCloud2 message with the filtered points
        header = msg.header
        header.frame_id = self.target_frame
        
        filtered_msg = create_cloud(header, msg.fields, filtered_points)
        
        # Publish the filtered point cloud
        self.publisher.publish(filtered_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudFilterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()