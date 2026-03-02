#include <cmath>
#include "indomitus_rover_sim/icr_controller_node.hpp"

ICRController::ICRController()
: Node("icr_controller") {
    cmd_vel_sub_ = create_subscription<geometry_msgs::msg::Twist>(
        "/cmd_vel", 10,
        std::bind(&ICRController::cmdVelCallback, this, std::placeholders::_1));

    const std::vector<std::string> steer_topics = {
        "/steering/fl", "/steering/fr", "/steering/bl", "/steering/br"
    };
    const std::vector<std::string> drive_topics = {
        "/drive/fl_wheel", "/drive/fr_wheel", "/drive/bl_wheel", "/drive/br_wheel"
    };

    for (int i = 0; i < 4; i++) {
        steer_pubs_.push_back(
            create_publisher<std_msgs::msg::Float64>(steer_topics[i], 10));
        drive_pubs_.push_back(
            create_publisher<std_msgs::msg::Float64>(drive_topics[i], 10));
    }
}

void ICRController::cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
    double vel_x = msg->linear.x;   // forward
    double vel_y = msg->linear.y;   // left
    double ang_vel = msg->angular.z;

    for (int i = 0; i < 4; i++) {
        
        auto [x_i, y_i] = wheel_positions[i];

        // Velocity of wheel i in body frame
        double Vx = vel_x - ang_vel * y_i;
        double Vy = vel_y + ang_vel * x_i;

        double angle = std::atan2(Vy, Vx);
        double vel   = std::hypot(Vx, Vy) / WHEEL_RADIUS;

        if (angle > M_PI_2) {
            angle -= M_PI;
            vel = -vel;
        }
        else if (angle < -M_PI_2) {
            angle += M_PI;
            vel = -vel;
        }

        std_msgs::msg::Float64 steer_msg, drive_msg;
        steer_msg.data = std::clamp(angle, -STEER_MAX, STEER_MAX);
        drive_msg.data = vel;

        steer_pubs_[i]->publish(steer_msg);
        drive_pubs_[i]->publish(drive_msg);
    }
}


int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ICRController>());
    rclcpp::shutdown();
}
