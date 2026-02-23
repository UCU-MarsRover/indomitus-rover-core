#include <cmath>
#include "indomitus_rover_sim/icr_controller_node.hpp"

ICRController::ICRController()
: Node("icr_controller") {
    cmd_vel_sub_ = create_subscription<geometry_msgs::msg::Twist>(
        "/cmd_vel", 10,
        std::bind(&ICRController::cmdVelCallback, this, std::placeholders::_1));

    steering_pub_ = create_publisher<std_msgs::msg::Float64MultiArray>(
        "/steering_controller/commands", 10);
    drive_pub_ = create_publisher<std_msgs::msg::Float64MultiArray>(
        "/drive_controller/commands", 10);
}

void ICRController::cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
    double vx = msg->linear.x;
    double wz = msg->angular.z;

    std_msgs::msg::Float64MultiArray steer_cmd, drive_cmd;
    steer_cmd.data.resize(4);
    drive_cmd.data.resize(4);

    if (std::abs(wz) < 1e-6) {
      // Прямо
      for (int i = 0; i < 4; i++) {
        steer_cmd.data[i] = 0.0;
        drive_cmd.data[i] = vx / WHEEL_RADIUS;
      }
    } else if (std::abs(vx) < 1e-6) {
      // Обертання на місці
      for (int i = 0; i < 4; i++) {
        auto [wx, wy] = wheel_positions[i];
        double angle = std::atan2(wx, -wy);
        steer_cmd.data[i] = std::clamp(angle, STEER_MIN, STEER_MAX);
        double dist = std::hypot(wx, wy);
        drive_cmd.data[i] = wz * dist / WHEEL_RADIUS;
      }
    } else {
      // ICR розрахунок
      double R = vx / wz;
      for (int i = 0; i < 4; i++) {
        auto [wx, wy] = wheel_positions[i];
        double angle = std::atan2(wx, R - wy);
        steer_cmd.data[i] = std::clamp(angle, STEER_MIN, STEER_MAX);
        double dist = std::hypot(wx, R - wy);
        drive_cmd.data[i] = wz * dist / WHEEL_RADIUS;
      }
    }



    steering_pub_->publish(steer_cmd);
    drive_pub_->publish(drive_cmd);
}


int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ICRController>());
  rclcpp::shutdown();
}
