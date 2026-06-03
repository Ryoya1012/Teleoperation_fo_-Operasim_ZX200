import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyTurtleTwoStick(Node):
    def __init__(self):
        super().__init__('joy_to_turtle_twostick')

        self.subscription = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

    def joy_callback(self, msg):
        twist = Twist()

        twist.linear.x = msg.axes[0]*2.0
        twist.angular.z = msg.axes[3]*2.0

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = JoyTurtleTwoStick()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
