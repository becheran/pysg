from enum import Enum

from src.scene.rotation.axis_angle import AxisAngle
from src.scene.rotation.euler import Euler
from src.scene.rotation.quaternion import Quaternion
from src.scene.rotation.rotation_matrix import RotationMatrix


class RotationType(Enum):
    EULER = 0
    QUATERNION = 1
    AXIS_ANGLE = 2
    ROTATION_MATRIX = 4
    SPARSE_ROTATION_MATRIX = 5


def rotation_type_length(rot_type):
    if rot_type == RotationType.EULER or rot_type == RotationType.AXIS_ANGLE:
        return 3
    elif rot_type == RotationType.QUATERNION:
        return 4
    elif rot_type == RotationType.SPARSE_ROTATION_MATRIX:
        return 6
    elif rot_type == RotationType.ROTATION_MATRIX:
        return 9
    else:
        raise Exception('Rotation type ' + str(rot_type) + ' not implemented yet!')


def rotation_identity(rot_type):
    if rot_type == RotationType.EULER:
        return [0, 0, 0]
    elif rot_type == RotationType.AXIS_ANGLE:
        return [0, 0, 0]
    elif rot_type == RotationType.QUATERNION:
        return [0, 0, 0, 1]
    elif rot_type == RotationType.SPARSE_ROTATION_MATRIX:
        return [1, 0, 0, 0, 1, 0]
    elif rot_type == RotationType.ROTATION_MATRIX:
        return [1, 0, 0, 0, 1, 0, 0, 0, 1]
    else:
        raise Exception('Rotation type ' + str(rot_type) + ' not implemented yet!')


def convert_vector(input_vector, input_type, output_type):
    input_type_len = rotation_type_length(input_type)

    if len(input_vector) % input_type_len != 0:
        raise Exception('Input must be multiple of ' + str(input_type_len) + '. But is ' + str(len(input_vector)))
    if input_type == output_type:
        return input_vector
    else:
        converted = []
        for i in range(0, int(len(input_vector) / input_type_len)):
            in_rot = input_vector[i * input_type_len:i * input_type_len + input_type_len]
            out_rot = None
            if input_type == RotationType.EULER:
                if output_type == RotationType.QUATERNION:
                    out_rot = Euler.from_list(in_rot).to_quaternion()
            elif input_type == RotationType.AXIS_ANGLE:
                if output_type == RotationType.QUATERNION:
                    out_rot = AxisAngle.from_list(in_rot).to_quaternion()
            elif input_type == RotationType.ROTATION_MATRIX:
                matrix = RotationMatrix.from_list(in_rot)
                matrix.normalize()
                if output_type == RotationType.QUATERNION:
                    out_rot = matrix.to_quaternion()
            elif input_type == RotationType.SPARSE_ROTATION_MATRIX:
                sparse_matrix = RotationMatrix.orthonormalize_sparse_matrix(in_rot)
                matrix = RotationMatrix.from_sparse_matrix(sparse_matrix)
                if output_type == RotationType.QUATERNION:
                    out_rot = matrix.to_quaternion()
            elif input_type == RotationType.QUATERNION:
                quaternion = Quaternion.from_list(in_rot)
                if output_type == RotationType.AXIS_ANGLE:
                    out_rot = quaternion.to_axis_angle()
                elif output_type == RotationType.ROTATION_MATRIX:
                    out_rot = quaternion.to_rotation_matrix()
                elif output_type == RotationType.EULER:
                    out_rot = quaternion.to_euler_angles()
                elif output_type == RotationType.SPARSE_ROTATION_MATRIX:
                    out_rot = quaternion.to_rotation_matrix()
                    out_rot = out_rot[0:6]
            else:
                raise Exception('Rotation type ' + str(input_type) + ' not implemented yet!')

            if out_rot is None:
                raise Exception('Conversion not successfully... Not implemented yet!')
            else:
                converted += out_rot
        return converted
