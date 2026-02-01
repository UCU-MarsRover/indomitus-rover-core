ARG ROS_DISTRO=humble

FROM ros:${ROS_DISTRO}-ros-base

RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    git curl wget ca-certificates \
    build-essential python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    pkg-config \
    g++ make cmake \
    && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8


RUN rosdep init || true && rosdep update


ENV WS=/opt/ws
RUN mkdir -p ${WS}/src
WORKDIR ${WS}

ENV ROS_DISTRO=${ROS_DISTRO}

WORKDIR ${WS}


COPY docker/entrypoint.bash /entrypoint.bash
RUN chmod +x /entrypoint.bash
ENTRYPOINT ["/entrypoint.bash"]

CMD ["bash"]
