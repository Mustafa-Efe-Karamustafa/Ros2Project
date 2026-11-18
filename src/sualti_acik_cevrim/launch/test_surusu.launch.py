from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler, Shutdown
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from sualti_acik_cevrim.surus import FORCE_TOPIC, CLEAR_TOPIC


def generate_launch_description():
    world = Path(get_package_share_directory('sualti_acik_cevrim')) / 'worlds' / 'pool.sdf'
    server = ExecuteProcess(cmd=['ign', 'gazebo', '-s', '-r', str(world)], output='screen')
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        RegisterEventHandler(OnProcessExit(target_action=server, on_exit=[Shutdown()])),
        server,
        ExecuteProcess(cmd=['ign', 'gazebo', '-g'], condition=IfCondition(LaunchConfiguration('gui'))),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                f'{FORCE_TOPIC}@ros_gz_interfaces/msg/EntityWrench]ignition.msgs.EntityWrench',
                f'{CLEAR_TOPIC}@ros_gz_interfaces/msg/Entity]ignition.msgs.Entity',
            ],
            output='screen',
        ),
        Node(
            package='sualti_acik_cevrim',
            executable='test_surusu',
            parameters=[{'use_sim_time': True}],
            output='screen',
        ),
    ])
