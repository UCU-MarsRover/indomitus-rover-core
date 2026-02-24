# RViz Launch для марсохода Indomitus

## Мета

Цей launch-файл піднімає модель марсохода у ROS2 та дозволяє візуалізувати її в RViz2.
Він також запускає:

robot_state_publisher — транслює TF для всіх лінків робота

joint_state_publisher або joint_state_publisher_gui — для керування суглобами робота

## RViz2 — для візуалізації моделі

⚠️ rviz.launch.py в indomitus_rover_bringup не запускає реальні драйвери або контролери — тільки віртуальну модель.

#### 1. Підготовка

Перед запуском переконайтеся, що workspace зібраний:

```bash
cd ~/opt/ws
colcon build --symlink-install
source install/setup.bash
```

#### 2. Запуск launch-файлу
```bash
ros2 launch indomitus_rover_bringup rviz.launch.py
```

За замовчуванням запускається RViz і joint_state_publisher_gui.

### 3. Аргументи launch-файлу

| Аргумент | Тип Опис	За замовчуванням
name	string	Префікс TF для робота	''
use_rviz	bool	Чи запускати RViz2	true
use_joint_state_publisher_gui	bool	Використовувати GUI для керування суглобами	true

| Аргумент                      | Тип    | Опис                                        | За замовчуванням |
|-------------------------------|--------|---------------------------------------------|------------------|
| name                          | string | Префікс TF для робота2                      | ''               |
| use_rviz                      | bool   | Чи запускати RViz2                          | true             |
| use_joint_state_publisher_gui | bool   | Використовувати GUI для керування суглобами | true             |


Приклади використання

Запуск без RViz:
```bash
ros2 launch indomitus_rover_bringup rviz.launch.py use_rviz:=false
```

Запуск без GUI для суглобів:
```bash
ros2 launch indomitus_rover_bringup rviz.launch.py use_joint_state_publisher_gui:=false
```

Використання TF префіксу:
```bash
ros2 launch indomitus_rover_bringup rviz.launch.py name:=mars_rover
```

4. Що відбувається після запуску

Robot State Publisher читає URDF з пакета indomitus_rover_description і публікує TF для всіх лінків.

Joint State Publisher / GUI дозволяє рухати суглоби вручну.

RViz2 відкривається з конфігурацією robot.rviz і візуалізує модель робота та його TF дерево.

5. Примітки

Якщо URDF змінюється, переконайтеся, що RViz використовує актуальний файл.

Для швидкого тесту URDF без RViz можна використати:
```bash
ros2 launch indomitus_rover_description robot_state_publisher.launch.py
```


# Simulation Setup

DESCRIPTION FOR MY OS CONFIGURATION. DIDN'T test gazebo nativly on ubuntu 22
## Architecture
Gazebo runs on the **host OS** (Ubuntu 24), ROS2 runs inside **distrobox (Ubuntu 22)**.
Both communicate via gz-transport over shared network namespace.

## Installation

### Host
```bash
sudo apt install gz-harmonic
```

### Distrobox (Ubuntu 22 / ROS2 Humble)
```bash
# ROS2 tools
sudo apt install -y \
  ros-humble-xacro \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-teleop-twist-keyboard

# Gazebo Harmonic
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
  http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

sudo apt-get update
sudo apt-get install -y gz-harmonic ros-humble-ros-gzharmonic

# Project dependencies
rosdep update
rosdep install -i --from-path src --rosdistro humble -y
```

## Build
```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Running

### 1. Host — set env and launch Gazebo
```bash
export GZ_PARTITION=rover
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/UCU/ERC/indomitus-rover-core/install/indomitus_rover_description/share
gz sim -r src/indomitus_rover_sim/worlds/rover_world.sdf
```

### 2. Distrobox — set env and launch ROS2
```bash
export GZ_PARTITION=rover
export GZ_IP=127.0.0.1
source /opt/ros/humble/setup.zsh
source install/setup.bash
ros2 launch indomitus_rover_sim sim_no_gazebo.launch.py
```

> ⚠️ `GZ_PARTITION` must be identical on host and distrobox.


# For native Ubuntu 22:

Installation and setup are the same as described above.

The only difference: you don’t need to set `GZ_PARTITION` and `GZ_IP`, and you don’t need to run Gazebo separately

Don't run:
```bash
gz sim -r src/indomitus_rover_sim/worlds/rover_world.sdf

ros2 launch indomitus_rover_sim sim_no_gazebo.launch.py
```

Do run:
```bash
ros2 launch indomitus_rover_sim sim_gazebo.launch.py
```

# Camera on marsrover

To visualize camera streams from the rover, you can use `rqt_image_view`, a GUI tool that subscribes to image topics and displays them in real time

```bash
sudo apt update
sudo apt install ros-humble-rqt-image-view

ros2 run rqt_image_view rqt_image_view
```

# Driving rover with keyboard

To control the rover manually using your keyboard, use the `teleop_twist_keyboard` node. This publishes velocity commands to the robot

```bash
sudo apt update
sudo apt install ros-humble-teleop-twist-keyboard
```

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```