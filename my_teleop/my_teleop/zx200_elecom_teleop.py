import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy, JointState
from com3_msgs.msg import JointCmd

class ZX200ElecomTeleop(Node):
    def __init__(self):
        super().__init__('zx200_elecom_controller_teleop')

        self.subscription = self.create_subscription( Joy, 'joy', self.joy_callback, 10)
        # Unityから現在の関節角度を受け取る
        self.joint_state_sub = self.create_subscription(
                    JointState,
                    '/zx200/joint_states',
                    self.joint_state_callback,
                    10
                )
        self.pub_front = self.create_publisher( JointCmd, '/zx200/front_cmd', 10)
        
        self.target_swing = 0.0
        self.target_boom = 0.0
        self.target_arm = 0.0
        self.target_bucket = 0.0
        
        self.current_axes = [0.0] * 8

        # 入力に対する速度の倍率・感度
        # 動きを敏感にしたい場合：0.002 ~ 0.005
        # 動きを精密にしたい場合：0.0005などに変更
        self.speed_scale = 0.00075

        self.deadzone = 0.1

        self.initial_pose_acquired = False

        self.limits = {
                    'boom': (-1.22, 0.96),
                    'arm' : (0.79, 2.53),
                    'bucket' : (-0.61, 2.37)
                }

        self.timer = self.create_timer(0.001, self.timer_callback)

        self.get_logger().info('zx200 elecom teleop node started. waiting for input')

    def joy_callback( self, msg):
        self.current_axes = msg.axes

    def joint_state_callback( self, msg: JointState):
        if self.initial_pose_acquired:
            return
        try:
            swing_idx = msg.name.index('swing_joint')
            boom_idx = msg.name.index('boom_joint')
            arm_idx = msg.name.index('arm_joint')
            bucket_idx = msg.name.index('bucket_joint')

            self.target_swing = msg.position[swing_idx]
            self.target_boom = msg.position[boom_idx]
            self.target_arm = msg.position[arm_idx]
            self.target_bucket = msg.position[bucket_idx]

            self.initial_pose_acquired = True
            self.get_logger().info('Initial pose acquired! Safe to operate.')

        except ValueError:
            pass
    def apply_deadzone(self, value):
        if abs(value) < self.deadzone:
            return 0.0
        return value

    def clamp(self, value, min_val, max_val):
        return max(min_val, min(value,max_val))

    def timer_callback( self):
        if not self.initial_pose_acquired:
            return
        if len(self.current_axes) < 4:
            return

        # 1. 上部旋回(左ステック左右: axes[0])
        swing_input = self.apply_deadzone(self.current_axes[0])
        self.target_swing += swing_input * self.speed_scale

        # 2. アーム(左ステック上下: axes[1])
        arm_input = self.apply_deadzone(self.current_axes[1])
        self.target_arm -= arm_input * self.speed_scale
        self.target_arm = self.clamp(self.target_arm, self.limits['arm'][0], self.limits['arm'][1])

        # 3. バケット(右ステック左右: axes[2])
        bucket_input = self.apply_deadzone(self.current_axes[2])
        self.target_bucket += bucket_input * self.speed_scale
        self.target_bucket = self.clamp(self.target_bucket, self.limits['bucket'][0], self.limits['bucket'][1])
       
        # 4. ブーム(右ステック上下: axes[3])
        boom_input = self.apply_deadzone(self.current_axes[3])
        self.target_boom += boom_input * self.speed_scale
        self.target_boom = self.clamp(self.target_boom, self.limits['boom'][0], self.limits['boom'][1])

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
    node = ZX200ElecomTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

