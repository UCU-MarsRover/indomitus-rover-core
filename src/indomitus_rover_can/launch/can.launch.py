from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_sim = LaunchConfiguration('use_sim', default='true')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim',
            default_value='true',
            description='use simulation mode (no CAN)'
        ),

        Node(
            package='indomitus_rover_can',
            executable='can_bridge_node',
            name='sican_bridge_nodem',
            arguments=['--ros-args', '--log-level', 'info'],
            parameters=[{
                'use_sim': use_sim,
                'can_interface': 'can0',
            }],
            output='screen',
        )
    ])