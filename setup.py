from setuptools import find_packages, setup

package_name = 'gesture_safety_stop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/gesture_demo.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abc',
    maintainer_email='jaskeeratsingh1299@gmail.com',
    description='Gesture-triggered safety stop demo for ROS2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_publisher = gesture_safety_stop.camera_publisher:main',
            'gesture_detector = gesture_safety_stop.gesture_detector:main',
            'turtle_reactor = gesture_safety_stop.turtle_reactor:main',
        ],
    },
)