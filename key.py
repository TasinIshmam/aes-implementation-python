
from BitVector import BitVector
from constants import Constants
from utils import Utils
from typing import *
import copy


class Key:

    NO_OF_ROUNDS = 10  # NO_OF_ROUNDS + 1 keys needed including original. So 'NO_OF_ROUNDS' key expansions are needed.

    def __init__(self, key_string : str):
        self.key_string = key_string
        self.key_int_array = Key.generate_key_from_string(key_string)  # Array of ints. Eg - [75, 22..]
        self.expanded_key_int_array = [self.key_int_array]  # array of arrays.

        for round_no in range(1, Key.NO_OF_ROUNDS + 1):
            new_round_key = Key.generate_new_round_key(self.expanded_key_int_array[round_no-1], round_no)
            print(f'Key for Round: {round_no} in Hex is: {Utils.convert_int_array_to_hex_array(new_round_key)}')
            self.expanded_key_int_array.append(new_round_key)

    # Returns an int array of ASCII values of a specific round's key
    def get_round_key(self, round_no : int) -> List[int]:
        if not (0 <= round_no <= Key.NO_OF_ROUNDS):
            raise Exception("Invalid round number specified")
        return self.expanded_key_int_array[round_no]

    @staticmethod
    def generate_new_round_key(prev_round_key_int_array : List[int], round_no : int) -> List[int]:
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
    def g_function_on_root_word(root_word: List[int], round_no: int) -> List[int]:
        if not (1 <= round_no <= Key.NO_OF_ROUNDS):
            raise Exception("Invalid round used for generate_round_key")

        # circular byte left shift
        shifted_root_word = Key.circular_byte_left_shift(root_word)
        # byte substitution
        byte_substituted_root_word = Utils.byte_substitution_sbox(shifted_root_word)
        # adding round constant
        round_constant_int = Constants.round_constants[round_no]
        round_constant_bitvector = BitVector(intVal=round_constant_int, size=8)
        root_word_significant_byte_bitvector = BitVector(intVal=byte_substituted_root_word[0], size=8)
        updated_root_word_significant_byte_bitvector = root_word_significant_byte_bitvector.__xor__(round_constant_bitvector)

        # only most significant byte changes for round constant addition.
        byte_substituted_root_word[0] = updated_root_word_significant_byte_bitvector.intValue()

        return byte_substituted_root_word

    @staticmethod
    def circular_byte_left_shift(root_word_int_array: List[int]) -> List[int]:
        return [root_word_int_array[1], root_word_int_array[2], root_word_int_array[3], root_word_int_array[0]]

    @staticmethod
    def generate_key_from_string(key_string: str) -> List[int]:
        size_adjusted_string = key_string
        if len(key_string) > 16:
            size_adjusted_string = key_string[0:16]
        elif len(key_string) < 16:
            size_adjusted_string = key_string.ljust(16,'\0')    # pad string to the right with 0's

        key = [ord(size_adjusted_string[x]) for x in range(16) ]
        print(f'Original Key: {size_adjusted_string}\nKey in Int: {key}')
        return key


# print(BitVector(intVal=0x34, size=8).get_bitvector_in_hex())

# Key("Thats my Kung Fu")
