import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from com3_msgs.msg import JointCmd

class ZX200PS5Teleop(Node):
    def __init__(self):
        super().__init__('zx200_ps5_teleop')

        self.subscription = self.create_subscription( Joy, 'joy', self.joy_callback, 10)

        self.pub_front = self.create_publisher( JointCmd, '/zx200/front_cmd', 10)
        
        self.target_swing = 0.0
        self.target_boom = 0.0
        self.target_arm = 0.0
        self.target_bucket = 0.0

        self.current_axes = [0.0] * 8

        self.speed_scale = 0.001

        self.timer = self.create_timer(0.001, self.timer_callback)

    def joy_callback( self, msg):
        self.current_axes = msg.axes

    def timer_callback( self):
        # 1. 上部旋回(左ステック左右: axes[0])
        self.target_swing += self.current_axes[0] * self.speed_scale

        # 2. アーム(左ステック上下: axes[1])
        self.target_arm -= self.current_axes[1] * self.speed_scale

        # 3. バケット(右ステック左右: axes[3])
        self.target_bucket += self.current_axes[3] * self.speed_scale
       
        # 4. ブーム(右ステック上下: axes[4])
        self.target_boom += self.current_axes[4] * self.speed_scale

        msg = JointCmd()

        msg.joint_name = [ 'swing_joint', 'boom_joint', 'arm_joint', 'bucket_joint']

        msg.position = [
                float( self.target_swing),
                float( self.target_boom),
                float( self.target_arm),
                float( self.target_bucket)
                ]

        self.pub_front.publish( msg)

def main(args=None):
    rclpy.init(args=args)
    node = ZX200PS5Teleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

