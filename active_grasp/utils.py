from geometry_msgs.msg import PoseStamped
import rospy

import active_grasp.msg
from robot_utils.ros.conversions import *


class CartesianPoseControllerClient:
    def __init__(self, topic="/command"):
        self.target_pub = rospy.Publisher(topic, PoseStamped, queue_size=10)

    def send_target(self, pose):
        msg = to_pose_stamped_msg(pose, "panda_link0")
        self.target_pub.publish(msg)


class AABBox:
    def __init__(self, bbox_min, bbox_max):
        self.min = bbox_min
        self.max = bbox_max

    def is_inside(self, p):
        return np.all(p > self.min) and np.all(p < self.max)


def from_bbox_msg(msg):
    aabb_min = from_point_msg(msg.min)
    aabb_max = from_point_msg(msg.max)
    return AABBox(aabb_min, aabb_max)


def to_bbox_msg(bbox):
    msg = active_grasp.msg.AABBox()
    msg.min = to_point_msg(bbox.min)
    msg.max = to_point_msg(bbox.max)
    return msg