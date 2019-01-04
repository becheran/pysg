import numpy as np


class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, vector3_list):
        return cls(vector3_list[0], vector3_list[1], vector3_list[2])

    def to_list(self):
        return [self.x, self.y, self.z]

    def magnitude(self):
        return np.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag
        self.z /= mag

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iter__(self):
        return iter(self.to_list())

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)
