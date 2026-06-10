Restaurant Butler Robot - ROS2
Overview

This project implements a Restaurant Butler Robot using ROS2 Humble.

ROS Nodes
robot_controller
order_manager
confirmation_node
cancel_order
Locations
Home
Kitchen
Table1
Table2
Table3
State Machine

HOME → KITCHEN → TABLE → HOME

Features
Single order delivery
Kitchen confirmation handling
Table confirmation handling
Order cancellation
Multiple table delivery
Skip unconfirmed table
Skip cancelled table
Topics
new_order
kitchen_confirm
cancel_order
Tested Scenarios
Single order delivery
Kitchen timeout
Table timeout
Cancellation during delivery
Multiple table delivery
Skip unconfirmed table
Skip cancelled table
