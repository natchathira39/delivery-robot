import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import threading

LOCATIONS = {
    "home": (0, 0),
    "kitchen": (1, 0),
    "table1": (2, 1),
    "table2": (2, 2),
    "table3": (2, 3)
}

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.state = "IDLE"
        self.cancelled = False
        self.kitchen_confirmed = False
        self.table_confirmed = False

        self.create_subscription(String, 'new_order', self.order_callback, 10)
        self.create_subscription(String, 'kitchen_confirm', self.kitchen_confirm_callback, 10)
        self.create_subscription(String, 'table_confirm', self.table_confirm_callback, 10)
        self.create_subscription(String, 'cancel_order', self.cancel_callback, 10)

        self.status_pub = self.create_publisher(String, 'robot_status', 10)
        self.get_logger().info("Robot Ready. Waiting for orders...")

    def publish_status(self, status):
        msg = String()
        msg.data = status
        self.status_pub.publish(msg)
        self.get_logger().info(status)

    def cancel_callback(self, msg):
        self.cancelled = True
        self.get_logger().info("Cancellation Received")

    def kitchen_confirm_callback(self, msg):
        self.kitchen_confirmed = True
        self.get_logger().info("Kitchen Confirmation Received")

    def table_confirm_callback(self, msg):
        self.table_confirmed = True
        self.get_logger().info("Table Confirmation Received")

    def wait_for_confirmation(self, confirm_type, timeout=30):
        self.publish_status(f"Waiting for {confirm_type} confirmation...")
        start = time.time()
        while time.time() - start < timeout:
            time.sleep(0.1)
            if self.cancelled:
                return "cancelled"
            if confirm_type == "kitchen" and self.kitchen_confirmed:
                self.kitchen_confirmed = False
                return "confirmed"
            if confirm_type == "table" and self.table_confirmed:
                self.table_confirmed = False
                return "confirmed"
        return "timeout"

    def move_to(self, location):
        self.publish_status(f"Moving to {location}")
        time.sleep(1)

    def order_callback(self, msg):
        thread = threading.Thread(
            target=self.run_order,
            args=(msg.data,)
        )
        thread.start()

    def run_order(self, data):
        tables = [t.strip() for t in data.split(",")]
        self.cancelled = False
        self.kitchen_confirmed = False
        self.table_confirmed = False

        self.publish_status(f"Order Received: {tables}")

        self.state = "GO_TO_KITCHEN"
        self.move_to("Kitchen")

        if self.cancelled:
            self.publish_status("Cancelled on way to Kitchen. Returning Home.")
            self.move_to("Home")
            self.state = "IDLE"
            return

        self.state = "WAIT_KITCHEN_CONFIRM"
        result = self.wait_for_confirmation("kitchen")

        if result in ("cancelled", "timeout"):
            self.publish_status(f"Kitchen {result}. Returning Home.")
            self.move_to("Home")
            self.state = "IDLE"
            return

        self.publish_status("Food Collected from Kitchen")

        for table in tables:
            if table not in LOCATIONS:
                self.publish_status(f"Unknown table {table}, skipping.")
                continue

            self.state = "GO_TO_TABLE"
            self.move_to(table)

            if self.cancelled:
                self.publish_status(f"Order cancelled for {table}. Skipping.")
                self.cancelled = False
                continue

            self.state = "WAIT_TABLE_CONFIRM"
            result = self.wait_for_confirmation("table")

            if result == "confirmed":
                self.publish_status(f"Delivered to {table}")
            elif result == "timeout":
                self.publish_status(f"No confirmation at {table}. Skipping.")
            elif result == "cancelled":
                self.publish_status(f"Cancelled at {table}. Skipping.")
                self.cancelled = False

        self.state = "RETURN_KITCHEN"
        self.move_to("Kitchen")
        self.state = "RETURN_HOME"
        self.move_to("Home")
        self.publish_status("All deliveries done. Back Home.")
        self.state = "IDLE"


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
