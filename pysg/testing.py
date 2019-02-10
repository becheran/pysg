from pyrr import Quaternion

from pysg.pyrr_extensions import quaternion_are_equal


class CustomAssertions:
    def assertQuaternionAreEqual(self, q1: Quaternion, q2: Quaternion, epsilon: float = 1e-12) -> None:
        if not quaternion_are_equal(q1, q2, epsilon=epsilon):
            raise AssertionError('Quaternion q1(%s) and q2(%s) are not equal!' % (q1, q2))
