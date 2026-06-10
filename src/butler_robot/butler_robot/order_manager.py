import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class OrderManager(Node):
    def __init__(self):
        super().__init__('order_manager')
        self.publisher_ = self.create_publisher(String, 'new_order', 10)
        tables = input("Enter tables (e.g. table1 or table1,table2,table3): ")
        msg = String()
        msg.data = tables
        self.publisher_.publish(msg)
        self.get_logger().info(f'Order Sent: {tables}')

def main(args=None):
    rclpy.init(args=args)
    node = OrderManager()
    rclpy.spin_once(node, timeout_sec=1)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
