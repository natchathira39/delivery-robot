**Restaurant Butler Robot - ROS2**

A ROS2-based butler robot that collects food from the kitchen and delivers to tables with full confirmation, timeout, and cancellation handling.

**Package Structure**
butler_robot/
├── butler_robot/
│   ├── robot_controller.py   # State machine + main logic
│   ├── order_manager.py      # Publishes orders
│   ├── confirmation_node.py  # Sends kitchen/table confirmations
│   └── cancel_order.py       # Sends cancellation signal
├── setup.py
└── package.xml

## Locations
| Location | Coordinates |
|----------|-------------|
| Home     | (0, 0)      |
| Kitchen  | (1, 0)      |
| Table1   | (2, 1)      |
| Table2   | (2, 2)      |
| Table3   | (2, 3)      |

## State Machine
IDLE → GO_TO_KITCHEN → WAIT_KITCHEN_CONFIRM → GO_TO_TABLE → WAIT_TABLE_CONFIRM → RETURN_KITCHEN → RETURN_HOME

## 📡 ROS2 Topics
| Topic | Type | Purpose |
|-------|------|---------|
| `/new_order` | String | Send table order |
| `/kitchen_confirm` | String | Kitchen confirmation |
| `/table_confirm` | String | Table confirmation |
| `/cancel_order` | String | Cancel current order |
| `/robot_status` | String | Robot status updates |

## ⚙️ Setup & Run

### Prerequisites
- Ubuntu 22.04
- ROS2 Humble

### Build
```bash
cd ~/butler_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

### Run (4 terminals)
```bash
# Terminal 1
ros2 run butler_robot robot_controller

# Terminal 2
ros2 run butler_robot confirmation_node

# Terminal 3
ros2 run butler_robot order_manager

# Terminal 4 (only for cancellation scenarios)
ros2 run butler_robot cancel_order
```

## Scenarios Tested

| Scenario | Description | Result |
|----------|-------------|--------|
| 1 | Single order, full confirmation | Pass |
| 2 | Kitchen timeout, return home | Pass |
| 3a | No kitchen confirm, return home |  Pass |
| 3b | No table confirm, skip table | Pass |
| 4 | Cancel during delivery | Pass |
| 5 | Multiple tables, all confirmed | Pass |
| 6 | Multiple tables, skip unconfirmed | Pass |
| 7 | Multiple tables, cancel one |  Pass |

## Key ROS2 Concepts Used
- Publishers & Subscribers
- Multi-threaded executor
- Multiple nodes communicating via topics
- State machine design pattern
