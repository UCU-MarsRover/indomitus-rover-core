#include <cmath>
#include "indomitus_rover_sim/icr_controller_node.hpp"

ICRController::ICRController()
: Node("icr_controller")
{
    cmd_vel_sub_ = create_subscription<geometry_msgs::msg::Twist>(
        "/cmd_vel", 10,
        std::bind(&ICRController::cmdVelCallback, this, std::placeholders::_1));

    steer_pub_ = create_publisher<std_msgs::msg::Float64MultiArray>(
        "/steering_controller/commands", 10);

    drive_pub_ = create_publisher<std_msgs::msg::Float64MultiArray>(
        "/drive_controller/commands", 10);
}

void ICRController::cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg)
{
    double vel_x   = msg->linear.x;
    double vel_y   = msg->linear.y;
    double ang_vel = msg->angular.z;

    std_msgs::msg::Float64MultiArray steer_msg, drive_msg;
    steer_msg.data.resize(4);
    drive_msg.data.resize(4);

    for (int i = 0; i < 4; i++) {
        auto [x_i, y_i] = wheel_positions[i];

        double Vx = vel_x - ang_vel * y_i;
        double Vy = vel_y + ang_vel * x_i;

        double angle = std::atan2(Vy, Vx);
        double vel   = std::hypot(Vx, Vy) / WHEEL_RADIUS;

        if (angle > M_PI_2) {
            angle -= M_PI;
            vel = -vel;
        } else if (angle < -M_PI_2) {
            angle += M_PI;
            vel = -vel;
        }

        steer_msg.data[i] = std::clamp(angle, -STEER_MAX, STEER_MAX);
        drive_msg.data[i] = vel;
    }

    steer_pub_->publish(steer_msg);
    drive_pub_->publish(drive_msg);
}

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ICRController>());
    rclcpp::shutdown();
    return 0;
}