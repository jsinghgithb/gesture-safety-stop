import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


class TurtleReactor(Node):
    def __init__(self):
        super().__init__('turtle_reactor')
        self.subscription = self.create_subscription(
            Bool, 'gesture_event', self.gesture_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        self.moving_cmd = Twist()
        self.moving_cmd.linear.x = 1.0
        self.moving_cmd.angular.z = 0.5

        self.stop_cmd = Twist()

        self.timer = self.create_timer(0.1, self.publish_current_state)
        self.is_stopped = False

    def gesture_callback(self, msg):
        if msg.data:
            self.is_stopped = True
            self.get_logger().info('Reactor: STOPPING turtle')
        else:
            self.is_stopped = False

    def publish_current_state(self):
        if self.is_stopped:
            self.cmd_pub.publish(self.stop_cmd)
        else:
            self.cmd_pub.publish(self.moving_cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleReactor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()