import os
from typing import List

import yaml
import tempfile
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_bridge_config(context):
    world = LaunchConfiguration("world_name").perform(context)
    model = LaunchConfiguration("model_name").perform(context)

    config = [
        {
            "ros_topic_name": "/clock",
            "gz_topic_name": "/clock",
            "ros_type_name": "rosgraph_msgs/msg/Clock",
            "gz_type_name": "gz.msgs.Clock",
            "direction": "GZ_TO_ROS"
        },

        {
            "ros_topic_name": "/joint_states",
            "gz_topic_name": f"/world/{world}/model/{model}/joint_state",
            "ros_type_name": "sensor_msgs/msg/JointState",
            "gz_type_name": "gz.msgs.Model",
            "direction": "GZ_TO_ROS"
        },

        {
            "ros_topic_name": "/camera/image_raw",
            "gz_topic_name": f"/world/{world}/model/{model}/link/camera_link/sensor/camera_rgb/image",
            "ros_type_name": "sensor_msgs/msg/Image",
            "gz_type_name": "gz.msgs.Image",
            "direction": "GZ_TO_ROS"
        },

        {
            "ros_topic_name": "/camera/camera_info",
            "gz_topic_name": f"/world/{world}/model/{model}/link/camera_link/sensor/camera_rgb/camera_info",
            "ros_type_name": "sensor_msgs/msg/CameraInfo",
            "gz_type_name": "gz.msgs.CameraInfo",
            "direction": "GZ_TO_ROS"
        }
    ]

    path = os.path.join("/tmp", f"bridge_{world}_{model}.yaml")

    with open(path, "w") as f:
        yaml.dump(config, f)

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={path}',
        ],
        output='screen',
    )

    return [bridge_node]


def generate_launch_description() -> LaunchDescription:
    world = 'rover_world_demo'
    model = 'indomitus_rover'
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

    start_gazebo_ros_bridge_cmd = OpaqueFunction(
        function=generate_bridge_config
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

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
    )

    steering_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['steering_controller'],
        output='screen',
    )

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
        DeclareLaunchArgument(
            'world_name',
            default_value='indomitus_world_demo'
        ),

        DeclareLaunchArgument(
            'model_name',
            default_value='indomitus_rover'
        ),
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

