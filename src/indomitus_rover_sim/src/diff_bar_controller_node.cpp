#include "indomitus_rover_sim/diff_bar_controller_node.hpp"

DiffBarController ::DiffBarController() : Node("diff_bar_controller") {
    joint_state_sub_ = create_subscription<sensor_msgs::msg::JointState>(
        "/joint_states", 10,
        std::bind(&DiffBarController::jointStateCallback, this, std::placeholders::_1));

    base_axii_pub_ = create_publisher<std_msgs::msg::Float64>(
        "/base_axii/angle", 10);
}

void DiffBarController::jointStateCallback(const sensor_msgs::msg::JointState::SharedPtr msg) {
    double l_angle = 0.0, r_angle = 0.0;
    bool l_found = false, r_found = false;

    for (size_t i = 0; i < msg->name.size(); i++) {
        if (msg->name[i] == "l_rocker_joint") {
            l_angle = msg->position[i];
            l_found = true;
        }
        if (msg->name[i] == "r_rocker_joint") {
            r_angle = msg->position[i];
            r_found = true;
        }
    }

    if (l_found && r_found) {
        std_msgs::msg::Float64 cmd;
        cmd.data = (l_angle + r_angle) / 2.0;
        base_axii_pub_->publish(cmd);
    }
}


int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<DiffBarController>());
    rclcpp::shutdown();
}