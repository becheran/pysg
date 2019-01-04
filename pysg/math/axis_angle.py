import numpy as np


class AxisAngle(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, axis_list):
        if len(axis_list) != 3:
            raise Exception('Array must be length 3 to create axis_angle form list')
        return cls(axis_list[0], axis_list[1], axis_list[2])

    def to_list(self):
        return [self.x, self.y, self.z]

    # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/angleToQuaternion/index.htm
    def to_quaternion(self):
        axis = np.array([self.x, self.y, self.z])
        angle = np.sqrt(axis.dot(axis))
        if angle > 0:
            axis /= angle
        else:
            axis = np.array([1, 0, 0])
            angle = 0
        s = np.math.sin(angle / 2.0)
        axis *= s
        w = np.math.cos(angle / 2.0)
        return [axis[0], axis[1], axis[2], w]
