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
|-------------------------------|--------|---------------------------------------------|------------------|


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








# Gazebo

## Dependencies

Host:
```zsh
sudo apt install gz-harmonic
```

Distrobox:
```zsh
sudo rosdep init
rosdep update

sudo apt-get install -y curl
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install -y gz-harmonic

sudo apt-get install -y ros-humble-ros-gzharmonic

sudo apt install -y ros-humble-xacro ros-humble-robot-state-publisher ros-humble-joint-state-publisher

sudo rosdep init      # skip if already done
rosdep update
rosdep install -i --from-path src --rosdistro humble -y --skip-keys "ros_gzharmonic_bridge"



source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Preparation

Перед тим як все починати на хості:
```zsh
export GZ_PARTITION=rover
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/UCU/indomitus-rover-core/install/indomitus_rover_description/share
export ROS_DOMAIN_ID=0
export GZ_IP=127.0.0.1
```


В distrobox (мій випадок):
```zsh
export GZ_PARTITION=rover
export ROS_DOMAIN_ID=0
export GZ_IP=127.0.0.1
source /opt/ros/humble/setup.zsh
```


## Запуск gazebo: 
Я запускав gazebo harmonic на host OS, а ros2 і його топіки підіймав у distrobox

```zsh
❯ gz sim -r empty.sdf
```

```zsh
❯ ros2 launch indomitus_rover_sim sim_no_gazebo.launch.py
```
