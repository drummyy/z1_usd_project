#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from sensor_msgs.msg import JointState
import time


class Z1Bridge(Node):
    def __init__(self):
        super().__init__('z1_bridge')

        self.create_subscription(
            JointTrajectory, '/joint_trajectory', self.traj_cb, 10
        )

        self.cmd_pub = self.create_publisher(JointState, '/joint_command', 10)

        self.trajectory = None
        self.current_idx = 0
        self.start_time = None

        self.create_timer(0.02, self.control_loop)
        self.get_logger().info('Z1 Bridge ready, waiting for trajectory...')

    def traj_cb(self, msg):
        self.trajectory = msg
        self.current_idx = 0
        self.start_time = time.time()
        self.get_logger().info(f'Got trajectory: {len(msg.points)} points')

    def control_loop(self):
        if self.trajectory is None:
            return

        elapsed = time.time() - self.start_time
        points = self.trajectory.points

        # Advance waypoint index based on time
        while self.current_idx < len(points):
            wp_time = (
                points[self.current_idx].time_from_start.sec
                + points[self.current_idx].time_from_start.nanosec / 1e9
            )
            if wp_time > elapsed:
                break
            self.current_idx += 1

        # Trajectory complete
        if self.current_idx >= len(points):
            positions = list(points[-1].positions)
            self.publish_cmd(positions)
            self.get_logger().info('Trajectory complete!')
            self.trajectory = None
            return

        # Interpolate
        idx = self.current_idx
        curr = points[idx]
        curr_t = curr.time_from_start.sec + curr.time_from_start.nanosec / 1e9

        if idx > 0:
            prev = points[idx - 1]
            prev_t = prev.time_from_start.sec + prev.time_from_start.nanosec / 1e9
            dt = curr_t - prev_t
            alpha = (elapsed - prev_t) / dt if dt > 0 else 1.0
            alpha = max(0.0, min(1.0, alpha))
            positions = [
                (1 - alpha) * p + alpha * c
                for p, c in zip(prev.positions, curr.positions)
            ]
        else:
            positions = list(curr.positions)

        self.publish_cmd(positions)

    def publish_cmd(self, positions):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(self.trajectory.joint_names) if self.trajectory else []
        msg.position = positions
        self.cmd_pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(Z1Bridge())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
