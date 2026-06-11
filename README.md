**Restaurant Butler Robot using ROS2**

**Executive Summary**

This project implements a ROS2-based Butler Robot designed for restaurant delivery operations. The robot receives customer orders, collects food from the kitchen, delivers to one or more tables, processes confirmations, handles cancellations, and returns safely to its home position.

The implementation focuses on modular ROS2 node architecture, event-driven communication, timeout handling, and state-machine-based decision making.

---

**Design Philosophy**

The system was intentionally designed as a distributed ROS2 application rather than a single monolithic program.

Each responsibility was isolated into an independent node:

* Order generation
* Robot control
* Confirmation handling
* Cancellation handling

This approach improves maintainability, scalability, and fault isolation.

The Robot Controller acts as the central decision-making component and implements the complete delivery workflow.


**Key Engineering Decisions**

**State Machine Approach**

A state machine was selected because restaurant delivery operations naturally consist of discrete operational states.

Advantages:

* Predictable behaviour
* Easy debugging
* Clear transition rules
* Simplified exception handling

**Timeout-Based Safety**

Timeout mechanisms were implemented to prevent indefinite waiting at kitchen and table locations.

This ensures the robot always reaches a safe terminal state even when confirmations are not received.

### Event-Driven Communication

ROS2 Publisher-Subscriber communication was chosen to decouple robot behaviour from user interaction.

Orders, confirmations, and cancellations are treated as asynchronous events.

This architecture closely resembles real-world robotic systems.
