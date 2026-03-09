import os
from typing import List

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description() -> LaunchDescription:
    rover_description_share = get_package_share_directory('indomitus_rover_description')
    rover_sim_share = get_package_share_directory('indomitus_rover_sim')

    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.environ.get('GZ_SIM_RESOURCE_PATH', ''),
            ':',
            os.path.dirname(rover_description_share),
        ]
    )

    pathModelFile = os.path.join(rover_sim_share,
                                 'urdf', 'indomitus_rover_gazebo.urdf.xacro')

    robotDescription = xacro.process_file(pathModelFile).toxml()

    # this is the launch file from gazebo_ros package, it will launch Gazebo and load the world file
    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'),
                                                                        'launch', 'gz_sim.launch.py'))

    world_file = os.path.join(
        rover_sim_share,
        'worlds',
        'rover_world.sdf'
    )

    gazeboLaunch = IncludeLaunchDescription(
        gazebo_rosPackageLaunch,
        launch_arguments={
            'gz_args': f'-r -v -v4 {world_file}',
            'on_exit_shutdown': 'True'
        }.items()
    )

    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robotDescription,
                     'use_sim_time': True}]
    )

    bridge_params = os.path.join(
        rover_sim_share,
        'parameters',
        'bridge_parameters_urdf.yaml'
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

    # publics all joints states in /joint_states
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
    )

    # angle of wheel_mount joints (position)
    steering_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['steering_controller'],
        output='screen',
    )

    # speed of wheel joints (velocity)
    drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['drive_controller'],
        output='screen',
    )


    icr_controller_node = Node(
        package='indomitus_rover_sim',
        executable='icr_controller_node',
        output='screen',
    )

    r_rocker_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['r_rocker_position_controller'],
        output='screen',
    )

    rocker_soft_mimic_node = Node(
        package='indomitus_rover_sim',
        executable='rocker_soft_mimic',
        output='screen',
    )

    return LaunchDescription([
        gz_resource_path,
        gazeboLaunch,
        nodeRobotStatePublisher,
        start_gazebo_ros_bridge_cmd,
        spawnModelNodeGazebo,
        joint_state_broadcaster_spawner,
        steering_controller_spawner,
        drive_controller_spawner,
        icr_controller_node,
        r_rocker_spawner,
        rocker_soft_mimic_node,
    ])

