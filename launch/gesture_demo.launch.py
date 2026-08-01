from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),
        Node(package='gesture_safety_stop', executable='camera_publisher', name='camera_publisher'),
        Node(package='gesture_safety_stop', executable='gesture_detector', name='gesture_detector'),
        Node(package='gesture_safety_stop', executable='turtle_reactor', name='turtle_reactor'),
    ])