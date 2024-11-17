from setuptools import find_packages, setup

package_name = 'vision'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'opencv-python'],
    zip_safe=True,
    maintainer='ros_bumperbot',
    maintainer_email='ros_bumperbot@todo.todo',
    description='ROS 2 package for streaming camera images using OpenCV and publishing them as ROS messages.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
             'camera_streamer = camera_streamer.camera_streamer:main',
        ],
    },
)
