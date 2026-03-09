import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    rover_description_share = get_package_share_directory('indomitus_rover_description')
    
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.environ.get('GZ_SIM_RESOURCE_PATH', ''),
            ':',
            os.path.dirname(rover_description_share),
        ]
    )

    rover_sim_share = get_package_share_directory('indomitus_rover_sim')

    sdf_model_file = os.path.join(
        rover_sim_share,
        'sdf',
        'indomitus_rover_s1.sdf'
    )

    world_file = os.path.join(
        rover_sim_share,
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
        rover_sim_share,
        'parameters',
        'bridge_parameters_sdf.yaml'
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

    rocker_soft_mimic = Node(
        package='indomitus_rover_sim',
        executable='rocker_soft_mimic',
        output='screen',
    )


    return LaunchDescription([
        gz_resource_path,
        gazebo_launch,
        ros_gz_bridge,
        spawn_model_node,
        icr_controller_node,
        rocker_soft_mimic,
    ])
