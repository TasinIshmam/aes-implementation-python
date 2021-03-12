
from BitVector import BitVector
from constants import Constants
from typing import *


class Utils:

    @staticmethod
    def convert_int_array_to_hex_array(int_array):
        return [ hex(value) for idx,value in enumerate(int_array)]

    @staticmethod
    def xor_operation_on_int_array(op1, op2):
        if len(op1) != len(op2):
            raise Exception("Array sizes do not match for bitwise operation")

        xored_bitvector_array = \
            [BitVector(intVal=op1[x],size=8).__xor__(BitVector(intVal=op2[x],size=8)) for x in range(len(op1))]

        # print([item.intValue() for item in xored_bitvector_array])
        return [item.intValue() for item in xored_bitvector_array]

    @staticmethod
    def byte_substitution_sbox(int_array):
        substituted_array = []
        for x in range(len(int_array)):
            substituted_int = Constants.sbox[int_array[x]]
            substituted_array.append(substituted_int)
        return substituted_array

    # Coverts (16) len 1d array into column major 4x4 matrix
    @staticmethod
    def convert_1d_arr_to_2d_column_major_state_matrix(int_arr):
        assert len(int_arr) == 16, "Input must be of length 16"
        state_matrix = zeros = [[0] * 4 for _ in range(4)]
        idx = 0
        for i in range(4):
            for j in range(4):
                state_matrix[j][i] = int_arr[idx]
                idx += 1
        return state_matrix

    @staticmethod
    def xor_operation_on_state_matrix(matrix1, matrix2):
        assert len(matrix1) == 4 and len(matrix2) == 4 and len(matrix1[0]) == 4 and len(matrix2[0]) == 4\
            , "Matrix used has invalid size"

        updated_matrix = [[] for i in range(4)]
        for i in range(4):
            updated_matrix[i] = Utils.xor_operation_on_int_array(matrix1[i], matrix2[i])

        return updated_matrix

    @staticmethod
    def convert_int_state_matrix_to_hex(matrix):
        assert len(matrix) == 4 and len(matrix[0]) == 4, "Matrix used has invalid size"

        hex_matrix = [[] for i in range(4)]
        for i in range(4):
            hex_matrix[i] = Utils.convert_int_array_to_hex_array(matrix[i])
        return hex_matrix

    @staticmethod
    def byte_substitution_sbox_for_matrix(matrix):
        assert len(matrix) == 4 and len(matrix[0]) == 4, "Matrix used has invalid size"

        substitute_matrix = [[] for i in range(4)]
        for i in range(4):
            substitute_matrix[i] = Utils.byte_substitution_sbox(matrix[i])
        return substitute_matrix

    @staticmethod
    def shift_left_row_state_matrix(state_matrix: List[List[int]]) -> List[List[int]]:
        assert len(state_matrix) == 4 and len(state_matrix[0]) == 4, "Matrix used has invalid size"

        state_matrix[1][0], state_matrix[1][1], state_matrix[1][2], state_matrix[1][3] = state_matrix[1][1], \
                                                                                         state_matrix[1][2], \
                                                                                         state_matrix[1][3], \
                                                                                         state_matrix[1][0]

        state_matrix[2][0], state_matrix[2][1], state_matrix[2][2], state_matrix[2][3] = state_matrix[2][2], \
                                                                                         state_matrix[2][3], \
                                                                                         state_matrix[2][0], \
                                                                                         state_matrix[2][1]

        state_matrix[3][0], state_matrix[3][1], state_matrix[3][2], state_matrix[3][3] = state_matrix[3][3], \
                                                                                         state_matrix[3][0], \
                                                                                         state_matrix[3][1], \
                                                                                         state_matrix[3][2]
        return state_matrix
