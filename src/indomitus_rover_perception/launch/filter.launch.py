import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('indomitus_rover_perception'),
        'config',
        'filter_params.yaml'
    )

    return LaunchDescription([
        Node(
            package='indomitus_rover_perception',
            executable='pc_filter_node.py',
            name='point_cloud_filter',
            output='screen',
            parameters=[config]
        )
    ])