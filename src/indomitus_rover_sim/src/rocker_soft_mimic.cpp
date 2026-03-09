#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

class RockerSoftMimic : public rclcpp::Node
{
public:
  RockerSoftMimic() : Node("rocker_soft_mimic")
  {
    joint_state_sub_ = this->create_subscription<sensor_msgs::msg::JointState>(
      "/joint_states", 10,
      std::bind(&RockerSoftMimic::jointStateCallback, this, std::placeholders::_1));

    r_rocker_cmd_pub_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(
      "/r_rocker_position_controller/commands", 10);
  }

private:
  void jointStateCallback(const sensor_msgs::msg::JointState::SharedPtr msg)
  {
    double l_rocker_pos = 0.0;
    bool found = false;

    for (size_t i = 0; i < msg->name.size(); ++i) {
      if (msg->name[i] == "l_rocker_joint") {
        l_rocker_pos = msg->position[i];
        found = true;
        break;
      }
    }

    if (!found) return;

    auto cmd_msg = std_msgs::msg::Float64MultiArray();
    cmd_msg.data.push_back(-l_rocker_pos);
    r_rocker_cmd_pub_->publish(cmd_msg);
  }

  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_state_sub_;
  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr r_rocker_cmd_pub_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<RockerSoftMimic>());
  rclcpp::shutdown();
  return 0;
}
