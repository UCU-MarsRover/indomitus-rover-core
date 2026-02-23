import os
from typing import List

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import TimerAction


def generate_launch_description() -> LaunchDescription:
    pathModelFile = os.path.join(get_package_share_directory('indomitus_rover_sim'),
                                 'urdf', 'indomitus_rover_gazebo.urdf.xacro')

    robotDescription = xacro.process_file(pathModelFile).toxml()

    # this is the launch file from gazebo_ros package, it will launch Gazebo and load the world file
    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'),
                                                                        'launch', 'gz_sim.launch.py'))


    gazeboLaunch = IncludeLaunchDescription(gazebo_rosPackageLaunch,
                                            launch_arguments={
                                                'gz_args': '-r -v -v4 empty.sdf',
                                                'on_exit_shutdown': 'True'
                                            }.items())

    spawnModelNodeGazebo = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'indomitus_rover',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0', 
            '-z', '3.5',
        ],
        output='screen',
    )

    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robotDescription,
                     'use_sim_time': True}]
    )

    bridge_params = os.path.join(
        get_package_share_directory('indomitus_rover_sim'),
        'parameters',
        'bridge_parameters.yaml'
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen',
    )

    launchDescriptionObject = LaunchDescription()

    # launchDescriptionObject.add_action(spawnModelNodeGazebo)
    launchDescriptionObject.add_action(nodeRobotStatePublisher)
    launchDescriptionObject.add_action(start_gazebo_ros_bridge_cmd)
    launchDescriptionObject.add_action(TimerAction(period=1.0, actions=[spawnModelNodeGazebo]))

    return launchDescriptionObject
