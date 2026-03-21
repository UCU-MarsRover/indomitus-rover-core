#include "indomitus_rover_can/can_bridge_node.hpp"

namespace indomitus_rover_can {

CanBridgeNode::CanBridgeNode(const rclcpp::NodeOptions& options)
: Node("can_bridge_options", options) {
    this->declare_parameter("can_interface", "can0");
    this->declare_parameter("use_sim", false);

    can_interface_ = this->get_parameter("can_interface").as_string();
    use_sim_ = this->get_parameter("use_sim").as_bool();

    cmd_vel_sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
        "cmd_vel",
        rclcpp::QoS(10),
        std::bind(&CanBridgeNode::cmdVelCallback, this, std::placeholders::_1)
    );

    if (!use_sim_) {
        RCLCPP_ERROR(this->get_logger(),
            "CAN socket not implemented yet on interface '%s'", can_interface_.c_str());
        rclcpp::shutdown();
        return;
    } else {
        RCLCPP_INFO(this->get_logger(), "Running in SIM mode — CAN disabled");
    }

    RCLCPP_INFO(this->get_logger(), "can_bridge_node started, listening on /cmd_vel");
}

CanBridgeNode::~CanBridgeNode() {}

void CanBridgeNode::cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
    RCLCPP_DEBUG(this->get_logger(),
        "cmd_vel received: linear.x=%.3f  angular.z=%.3f",
        msg->linear.x, msg->angular.z);
    
    if (use_sim_) {
        return;
    }

    RCLCPP_ERROR(this->get_logger(),
        "CAN socket not implemented yet on interface '%s'", can_interface_.c_str());
    rclcpp::shutdown();
}

} // indomitus_rover_can

#include <rclcpp/rclcpp.hpp>
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<indomitus_rover_can::CanBridgeNode>(rclcpp::NodeOptions{}));
  rclcpp::shutdown();
  return 0;
}