import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class CancelOrder(Node):
    def __init__(self):
        super().__init__('cancel_order')
        self.publisher_ = self.create_publisher(String, 'cancel_order', 10)
        input("Press ENTER to cancel current order")
        msg = String()
        msg.data = "cancel"
        self.publisher_.publish(msg)
        self.get_logger().info("Cancel signal sent")

def main(args=None):
    rclpy.init(args=args)
    node = CancelOrder()
    rclpy.spin_once(node, timeout_sec=1)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
