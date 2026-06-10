import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ConfirmationNode(Node):
    def __init__(self):
        super().__init__('confirmation_node')
        self.kitchen_pub = self.create_publisher(String, 'kitchen_confirm', 10)
        self.table_pub = self.create_publisher(String, 'table_confirm', 10)

        while rclpy.ok():
            choice = input("Send confirmation (k=kitchen, t=table, q=quit): ")
            msg = String()
            msg.data = "confirmed"
            if choice == "k":
                self.kitchen_pub.publish(msg)
                self.get_logger().info("Kitchen Confirmation Sent")
            elif choice == "t":
                self.table_pub.publish(msg)
                self.get_logger().info("Table Confirmation Sent")
            elif choice == "q":
                break

def main(args=None):
    rclpy.init(args=args)
    node = ConfirmationNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
