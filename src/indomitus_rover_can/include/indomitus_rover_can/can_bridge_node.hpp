#include <string>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
// #include "std_msgs/msg/..."

namespace indomitus_rover_can {

class CanBridgeNode : public rclcpp::Node {
public:
    explicit CanBridgeNode(const rclcpp::NodeOptions& options);
    ~CanBridgeNode();
private:
    void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg);

    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub_;
    std::string can_interface_;
    bool use_sim_;
};

} // indomitus_rover_can