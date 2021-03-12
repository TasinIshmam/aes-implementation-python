
from BitVector import BitVector
from constants import Constants
from utils import Utils
import copy


class Key:

    KEY_EXPANSIONS = 10  # 11 sets of keys including original.

    def __init__(self, key_string):
        self.key_string = key_string
        self.key_int_array = Key.generate_key_from_string(key_string)  # Array of ints. Eg - [75, 22..]
        self.expanded_key_int_array = [[self.key_int_array]]  # array of arrays.

        Key.generate_new_round_key(self.key_int_array, 1)

    @staticmethod
    def generate_new_round_key(prev_round_key_int_array, round_no):
        prev_round_root_word = prev_round_key_int_array[12:16]
        updated_root_word = Key.g_function_on_root_word(prev_round_root_word, round_no)

        # generate each word of the new round key
        first_word = Utils.xor_operation_on_int_array(updated_root_word, prev_round_key_int_array[0:4])
        second_word = Utils.xor_operation_on_int_array(first_word, prev_round_key_int_array[4:8])
        third_word = Utils.xor_operation_on_int_array(second_word, prev_round_key_int_array[8:12])
        fourth_word = Utils.xor_operation_on_int_array(third_word, prev_round_key_int_array[12:16])

        new_round_key = first_word + second_word + third_word + fourth_word
        return new_round_key

    @staticmethod
    def g_function_on_root_word(root_word, round_no):
        if not (1 <= round_no <= 10):
            raise Exception("Invalid round used for generate_round_key")

        # circular byte left shift
        shifted_root_word = Key.circular_byte_left_shift(root_word)
        # byte substitution
        byte_substituted_root_word = Key.byte_substitution_sbox(shifted_root_word)
        # adding round constant
        round_constant_int = Constants.round_constants[round_no]
        round_constant_bitvector = BitVector(intVal=round_constant_int, size=8)
        root_word_significant_byte_bitvector = BitVector(intVal=byte_substituted_root_word[0], size=8)
        updated_root_word_significant_byte_bitvector = root_word_significant_byte_bitvector.__xor__(round_constant_bitvector)

        # only most significant byte changes for round constant addition.
        byte_substituted_root_word[0] = updated_root_word_significant_byte_bitvector.intValue()

        return byte_substituted_root_word

    @staticmethod
    def circular_byte_left_shift(root_word_int_array):
        return [root_word_int_array[1], root_word_int_array[2], root_word_int_array[3], root_word_int_array[0]]

    @staticmethod
    def byte_substitution_sbox(root_word_int_array):
        substituted_array = []
        for x in range(4):
            substituted_int = Constants.sbox[root_word_int_array[x]]
            substituted_array.append(substituted_int)
        return substituted_array


    @staticmethod
    def generate_key_from_string(key_string):
        size_adjusted_string = key_string
        if len(key_string) > 16:
            size_adjusted_string = key_string[0:16]
        elif len(key_string) < 16:
            size_adjusted_string = key_string.ljust(16,'\0')    # pad string to the right with 0's

        key = [ord(size_adjusted_string[x]) for x in range(16) ]
        print(f'Original Key: {size_adjusted_string}\nKey in Int: {key}')
        return key


# print(BitVector(intVal=0x34, size=8).get_bitvector_in_hex())

Key("Thats my Kung Fu")
