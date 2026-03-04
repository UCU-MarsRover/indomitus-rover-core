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