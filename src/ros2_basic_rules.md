# ROS2 basic command from packages

```bash
ros2 pkg create --build-type ament_cmake package_name
```

Створюйте окремі компоненти для дуже окремих задач модуля:
  - {module_name}_control/
  - {module_name}_kinematics/


rover_description - пакет, де мають лежати всі 3d моделі ровера, в папці meshes, з підпапками по модулях
rover_bringup - пакет, де будуть лежати всі загальні файли конфігурації


Щоб збілдити весь проєкт:
```bash
colcon build --symlink-install
```

Щоб збілдити конкретний пакет:
```bash
colcon build --packages-select package_name
```
