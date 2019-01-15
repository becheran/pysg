from pysg.math import quaternion_are_equal


class CustomAssertions:
    def assertQuaternionAreEqual(self, q1, q2):
        if not quaternion_are_equal(q1, q2):
            raise AssertionError('Quaternion q1(%s) and q2(%s) are not equal!' % (q1, q2))
