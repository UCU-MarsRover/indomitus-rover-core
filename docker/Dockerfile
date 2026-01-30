FROM ros:humble
MAINTAINER Yurii Fitio "fito.pn@ucu.edu.ua"

RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    python3-pip \
    libopus-dev \
    && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

SHELL ["/bin/bash", "-c"]

# RUN mkdir -p /ros_ws/src \
#     && cd /ros_ws \
#     && git clone https://github.com/ros/urdfdom.git --branch humble src/urdfdom \
#     && git clone https://github.com/berndpfrommer/ffmpeg_image_transport_msgs.git \
#     && source /ros_entrypoint.sh \
#     && colcon build --install-base /opt/ros/ws --merge-install \
#     && rm -r /ros_ws

RUN python3 -m pip install -U numpy numpy-quaternion PyYaml av

# RUN mkdir -p /ros_ws/src \
#     && cd /ros_ws \
#     && git clone https://github.com/jeguzzi/robomaster_ros.git src/robomaster_ros \
#     && source /ros_entrypoint.sh \
#     && colcon build --install-base /opt/ros/ws --merge-install \
#     && rm -r /ros_ws
