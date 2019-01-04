from unittest import TestCase

from src.scene.vector3 import Vector3
import numpy as np


class TestVector3(TestCase):
    def test_sub(self):
        v1 = Vector3(-0.1964498, 0.6910764, -0.1814247)
        v2 = Vector3(0.23, 0.13, 0.288)
        sub = v1 - v2
        self.assertTrue(np.allclose(sub.to_list(), [-0.4264498, 0.5610764, -0.4694247], atol=1.e-4))
