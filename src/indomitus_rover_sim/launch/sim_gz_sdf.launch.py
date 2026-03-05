import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    sdf_model_file = os.path.join(
        get_package_share_directory('indomitus_rover_description'),
        'sdf',
        'indomitus_rover_s1.sdf'
    )

    world_file = os.path.join(
        get_package_share_directory('indomitus_rover_sim'),
        'worlds',
        'rover_world.sdf'
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'),
            'launch', 'gz_sim.launch.py'
        )),
        launch_arguments={
            'gz_args': f'-r -v 4 {world_file}',
            'on_exit_shutdown': 'True'
        }.items()
    )

    spawn_model_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', sdf_model_file,
            '-name', 'indomitus_rover',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '4.0',
        ],
        output='screen',
    )

    bridge_params = os.path.join(
        get_package_share_directory('indomitus_rover_sim'),
        'parameters',
        'sdf_bridge_parameters.yaml'
    )
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}'],
        output='screen'
    )

    icr_controller_node = Node(
        package='indomitus_rover_sim',
        executable='icr_controller_node',
        output='screen',
    )

    diff_bar_controller_node = Node(
        package='indomitus_rover_sim',
        executable='diff_bar_controller_node',
        output='screen',
    )


    return LaunchDescription([
        gazebo_launch,
        ros_gz_bridge,
        TimerAction(period=2.0, actions=[spawn_model_node]),
        TimerAction(period=3.0, actions=[
            icr_controller_node,
            diff_bar_controller_node,
            ]),
    ])