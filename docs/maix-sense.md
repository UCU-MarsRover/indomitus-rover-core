1. Setup & Launch

To run the camera driver along with the necessary coordinate transforms and visualization, follow these steps:
Hardware Preparation

    Connect the MaixSense A010 to a USB 3.0 port.

    Grant serial permissions on your host machine:
    Bash

        sudo chmod 666 /dev/ttyUSB0
        assuming you're running ttyUSB0 on Linux. Otherwise change it in docker-compose

Running the Stack

Use the custom launch file to start the driver, the static transform (to fix frame errors), and RViz2 simultaneously:
Bash
```bash
ros2 launch sipeed_tof_ms_a010 tof_test_launch.py
```
and in second terminal
```bash
source /opt/ros/humble/setup.sh
rviz2
```
On the left upper corner: File -> Open config -> /work/rviz2_conf.rviz


2. Common Problems & Solutions
Problem A: Docker Hardware Isolation

Symptoms: path for serial can't open or Error: failed to configure serial device.

    Cause: Docker containers do not see host hardware by default.

    Fix: Add the device mapping to your docker-compose.yml:
    YAML

    devices:
      - "/dev/ttyUSB0:/dev/ttyUSB0"
    group_add:
      - dialout

Problem B: Segmentation Fault on Startup

Symptoms: The node crashes immediately with [ros2run]: Segmentation fault.

    Cause: The C++ driver attempted to access the serial port, failed, and tried to perform operations on a null pointer.

    Fix: Ensure the device is mapped (Problem A) and power-cycle the camera (unplug/replug) to reset its internal state.

Problem C: "Frame [tof] does not exist" in RViz

Symptoms: RViz opens, but the PointCloud2 display shows a red error: No tf data.

    Cause: ROS 2 requires a Transform (TF) tree to know where the sensor is in 3D space. The driver publishes data but doesn't define the camera's position.

    Fix: Run a static_transform_publisher to bridge the map frame to the tof frame:
    Bash

    ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map tof
That line is in launch script, so should be good

Problem D: Launch File Not Found

Symptoms: file 'tof_test_launch.py' was not found in the share directory.

    Cause: Creating the file in src/ isn't enough; the build system (CMake) must be told to install it.

    Fix: Add an install rule to CMakeLists.txt:
    CMake

    install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})

    Then rebuild with colcon build --symlink-install.
