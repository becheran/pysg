from unittest import TestCase
import numpy as np

from src.scene.transform import Transform


class TestTransform(TestCase):
    def test_transform_conversion(self):
        parent_global = Transform(23.84, 18.18, 8.73, -0.1964498, 0.6910764, -0.1814247, 0.6714953)
        child_global = Transform(2.238, 81.27, 28.17, 0.627765, 0.3268382, 0.5890927, 0.3899457)
        child_local = Transform(-48.70543, 44.6657, -21.39307, 0.03174144, -0.051847, 0.9643597, 0.2575166)
        calculated_child_local = child_global.to_local_transform(parent_global)
        calculated_child_global = child_local.to_global_transform(parent_global)
        print(calculated_child_global) #TODO REMOVE ME
        self.assertTrue(np.allclose(calculated_child_local.to_list(), child_local.to_list(), atol=1.e-4))
        self.assertTrue(np.allclose(calculated_child_global.to_list(), child_global.to_list(), atol=1.e-4))
