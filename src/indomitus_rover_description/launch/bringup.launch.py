import os
from typing import List

import launch.actions
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.utilities import perform_substitutions
from launch_ros.actions import Node


args_descriptions = {
    "name": "Name of the robot used as a tf prefix"
}


def urdf(name: str = '') -> str:
    # Тільки модель S1
    urdf_xacro = os.path.join(get_package_share_directory('indomitus_rover_description'),
                              'urdf', 'indomitus_rover_s1.urdf.xacro')
    
    # Формуємо аргументи для xacro
    xacro_args = [f'name:={name}']
    
    opts, input_file_name = xacro.process_args([urdf_xacro] + xacro_args)
    try:
        doc = xacro.process_file(input_file_name, **vars(opts))
        return doc.toprettyxml(indent='  ')
    except Exception as e:
        print(f"Error processing URDF for S1: {e}")
        return ''


def robot_state_publisher(context: LaunchContext,
                          **substitutions: launch.substitutions.LaunchConfiguration
                          ) -> List[Node]:
    kwargs = {k: perform_substitutions(context, [v]) for k, v in substitutions.items()}
    params = {'robot_description': urdf(**kwargs), 'publish_frequency': 100.0}
    # with open('test.urdf', 'w+') as f:
    #     f.write(params['robot_description'])
    node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[params], output='screen',
        arguments=["--ros-args", "--log-level", "warn"])
    return [node]


def generate_launch_description() -> None:
    arguments = [
        launch.actions.DeclareLaunchArgument(
            k, default_value=str(urdf.__defaults__[i]), description=args_descriptions.get(k, ''))
        for i, (k, _) in enumerate(urdf.__annotations__.items()) if k != 'return']
    kwargs = {k: launch.substitutions.LaunchConfiguration(k)
              for (k, _) in urdf.__annotations__.items() if k != 'return'}
    return LaunchDescription(
        arguments + [
            # launch.actions.LogInfo(msg=launch.substitutions.LaunchConfiguration('name')),
            # launch.actions.LogInfo(msg=launch.substitutions.LaunchConfiguration('publish_ground_truth')),
            launch.actions.OpaqueFunction(
                function=robot_state_publisher,
                kwargs=kwargs),
        ])