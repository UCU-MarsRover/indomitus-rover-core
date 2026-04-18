from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. The Camera Driver Node
        Node(
            package='sipeed_tof_ms_a010',
            executable='publisher',
            name='tof_publisher',
            parameters=[{'device': '/dev/ttyUSB0'}],
            output='screen'
        ),
        # 2. The Static Transform Node (Fixes the Frame Error)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_pub',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'tof'],
            output='screen'
        )
    ])