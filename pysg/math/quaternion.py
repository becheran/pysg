import numpy as np

from src.scene.vector3 import Vector3


class Quaternion(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @classmethod
    def from_list(cls, quaternion_list):
        if len(quaternion_list) != 4:
            raise Exception('Array must be length 4 to create quaternion form list')
        return cls(quaternion_list[0], quaternion_list[1], quaternion_list[2], quaternion_list[3])

    @classmethod
    def identity(cls,):
        return cls(0, 0, 0, 1)

    def to_list(self):
        return [self.x, self.y, self.z, self.w]

    # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/
    def to_axis_angle(self):
        angle = 2 * np.math.acos(self.w)
        sqrt = np.math.sqrt(1 - self.w * self.w)
        if sqrt < 0.001:
            return angle, 0, 0
        else:
            return (self.x / sqrt) * angle, (self.y / sqrt) * angle, (self.z / sqrt) * angle

    # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/
    def to_euler_angles(self):
        t = self.x * self.y + self.z * self.w
        if t > 0.499:  # singularity at north pole
            x = 2 * np.math.atan2(self.x, self.w)
            y = np.math.pi / 2
            z = 0
        elif t < -0.499:  # singularity at south pole
            x = -2 * np.math.atan2(self.x, self.w)
            y = - np.math.pi / 2
            z = 0
        else:
            sx = self.x * self.x
            sy = self.y * self.y
            sz = self.z * self.z
            x = np.math.atan2(2 * self.y * self.w - 2 * self.x * self.z, 1 - 2 * sy - 2 * sz)
            y = np.math.asin(2 * self.x * self.y + 2 * self.z * self.w)
            z = np.math.atan2(2 * self.x * self.w - 2 * self.y * self.z, 1 - 2 * sx - 2 * sz)
        return x, y, z

    # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
    def to_rotation_matrix(self):
        xx = self.x * self.x
        xy = self.x * self.y
        xz = self.x * self.z
        xw = self.x * self.w
        yy = self.y * self.y
        yz = self.y * self.z
        yw = self.y * self.w
        zz = self.z * self.z
        zw = self.z * self.w

        m00 = 1 - 2 * (yy + zz)
        m01 = 2 * (xy - zw)
        m02 = 2 * (xz + yw)

        m10 = 2 * (xy + zw)
        m11 = 1 - 2 * (xx + zz)
        m12 = 2 * (yz - xw)

        m20 = 2 * (xz - yw)
        m21 = 2 * (yz + xw)
        m22 = 1 - 2 * (xx + yy)

        return m00, m01, m02, m10, m11, m12, m20, m21, m22

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z) + "," + str(self.w)

    def __mul__(self, other):
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        return Quaternion(x, y, z, w)

    def __iter__(self):
        return iter(self.to_list())

    def __rmul__(self, other):
        return self.__mul__(other)

    def inverse(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def rotate(self, point):
        q_point = Quaternion(point.x, point.y, point.z, 0)
        rotated = self * q_point * self.inverse()
        return Vector3(rotated.x, rotated.y, rotated.z)
