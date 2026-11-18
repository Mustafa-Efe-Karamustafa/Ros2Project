import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from ros_gz_interfaces.msg import Entity, EntityWrench

FORCE_TOPIC = '/world/pool/wrench/persistent'
CLEAR_TOPIC = '/world/pool/wrench/clear'


PHASES = (
    ('İleri', 5.0, 11.0),
    ('Bekle', 2.0, 0.0),
    ('Geri', 5.0, -11.0),
    ('Test bitti', float('inf'), 0.0),
)


class DriveTest(Node):
    def __init__(self):
        super().__init__('test_surusu')
        self.vehicle = Entity(name='auv', type=Entity.MODEL)
        self.force_publisher = self.create_publisher(EntityWrench, FORCE_TOPIC, 10)
        self.clear_publisher = self.create_publisher(Entity, CLEAR_TOPIC, 10)
        self.phases = iter(PHASES)
        self.phase_end_time = 0.0
        self.timer = self.create_timer(0.02, self.step)

    def step(self):
        sim_time = self.get_clock().now().nanoseconds / 1e9
        if sim_time < self.phase_end_time:
            return
        if not (self.force_publisher.get_subscription_count() and self.clear_publisher.get_subscription_count()):
            return

        label, duration, force = next(self.phases)
        self.phase_end_time = sim_time + duration
        if force:
            command = EntityWrench(entity=self.vehicle)
            command.wrench.force.x = force
            self.force_publisher.publish(command)
        else:
            self.clear_publisher.publish(self.vehicle)
        self.get_logger().info(f'{label} | X kuvveti {force:+g} N')


def main():
    rclpy.init()
    node = DriveTest()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
