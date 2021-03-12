
from BitVector import BitVector

class Utils:

    @staticmethod
    def print_int_array_in_hex(int_array):
        print([ hex(value) for idx,value in enumerate(int_array)])

    @staticmethod
    def xor_operation_on_int_array(op1, op2):
        if len(op1) != len(op2):
            raise Exception("Array sizes do not match for bitwise operation")

        xored_bitvector_array = [ BitVector(intVal=op1[x],size=8).__xor__(BitVector(intVal=op2[x],size=8)) for x in range(len(op1))]

        # print([item.intValue() for item in xored_bitvector_array])
        return [item.intValue() for item in xored_bitvector_array]

