#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import sensor_msgs_py.point_cloud2 as pc2
import struct
import time
import random

class FilterTestNode(Node):
    def __init__(self):
        super().__init__('filter_test_node')
        
        self.publisher_ = self.create_publisher(PointCloud2, '/camera/points', 10)
        self.subscriber_ = self.create_subscription(PointCloud2, '/perception/obstacle_points', self.listener_callback, 10)
        
        self.min_z = 0.10
        self.max_z = 1.50
        self.num_points = 50000
        self.expected_count = 0
        
        self.timer = self.create_timer(1.0, self.publish_mock_cloud)

    def generate_random_points(self, n):
        points = []
        valid_count = 0
        for _ in range(n):
            x = random.uniform(-5.0, 5.0)
            y = random.uniform(-5.0, 5.0)
            z = random.uniform(-0.5, 2.5)
            points.append([x, y, z])
            if self.min_z <= z <= self.max_z:
                valid_count += 1
        return points, valid_count
        
    def publish_mock_cloud(self):
        points, self.expected_count = self.generate_random_points(self.num_points)
        
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = 'camera_depth_optical_frame'
        
        cloud_msg = pc2.create_cloud_xyz32(header, points)
        
        self.get_logger().info(f'Publishing test point cloud with {self.num_points} points.')
        self.publisher_.publish(cloud_msg)
        
    def listener_callback(self, msg):
        cloud_data = list(pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))
        
        self.get_logger().info(f'Received filtered point cloud with {len(cloud_data)} points.')
        
        errors = 0
        for p in cloud_data:
            if not (self.min_z <= p[2] <= self.max_z):
                errors += 1
                
        if errors == 0 and len(cloud_data) == self.expected_count:
            self.get_logger().info('Validation passed: all points are within bounds and the count matches the expected value.')
        else:
            self.get_logger().error(f'Validation failed. Errors: {errors}. Expected count: {self.expected_count}, received: {len(cloud_data)}.')
            
        raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    test_node = FilterTestNode()
    
    try:
        rclpy.spin(test_node)
    except SystemExit:
        pass
    finally:
        test_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
