
from BitVector import BitVector
from constants import Constants

class Utils:

    @staticmethod
    def convert_int_array_to_hex_array(int_array):
        return [ hex(value) for idx,value in enumerate(int_array)]

    @staticmethod
    def xor_operation_on_int_array(op1, op2):
        if len(op1) != len(op2):
            raise Exception("Array sizes do not match for bitwise operation")

        xored_bitvector_array = [ BitVector(intVal=op1[x],size=8).__xor__(BitVector(intVal=op2[x],size=8)) for x in range(len(op1))]

        # print([item.intValue() for item in xored_bitvector_array])
        return [item.intValue() for item in xored_bitvector_array]

    @staticmethod
    def byte_substitution_sbox(int_array):
        substituted_array = []
        for x in range(len(int_array)):
            substituted_int = Constants.sbox[int_array[x]]
            substituted_array.append(substituted_int)
        return substituted_array

