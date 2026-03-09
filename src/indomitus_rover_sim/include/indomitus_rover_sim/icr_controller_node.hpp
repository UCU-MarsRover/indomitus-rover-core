#pragma once

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>

class ICRController : public rclcpp::Node {
public:
    static constexpr double L = 1.06;
    static constexpr double W = 0.61;
    static constexpr double WHEEL_RADIUS = 0.15;
    static constexpr double STEER_MAX = M_PI;

    const std::array<std::pair<double,double>, 4> wheel_positions = {{
        {  L/2,  W/2 },
        {  L/2, -W/2 },
        { -L/2,  W/2 },
        { -L/2, -W/2 },
    }};

    ICRController();
    ~ICRController() = default;

private:
    void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg);

    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr steer_pub_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr drive_pub_;
};