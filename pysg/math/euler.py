import numpy as np


class Euler(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, euler_list):
        if len(euler_list) != 3:
            raise Exception('Array must be length 3 to create euler form list')
        return cls(euler_list[0], euler_list[1], euler_list[2])

    def to_list(self):
        return [self.x, self.y, self.z]

    # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/index.htm
    def to_quaternion(self):
        c1 = np.math.cos(self.x / 2.0)
        s1 = np.math.sin(self.x / 2.0)
        c2 = np.math.cos(self.y / 2.0)
        s2 = np.math.sin(self.y / 2.0)
        c3 = np.math.cos(self.z / 2.0)
        s3 = np.math.sin(self.z / 2.0)
        c1c2 = c1 * c2
        s1s2 = s1 * s2
        w = c1c2 * c3 - s1s2 * s3
        x = c1c2 * s3 + s1s2 * c3
        y = s1 * c2 * c3 + c1 * s2 * s3
        z = c1 * s2 * c3 - s1 * c2 * s3
        return x, y, z, w
