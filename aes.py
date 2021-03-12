from BitVector import BitVector
from constants import Constants
from utils import Utils
from typing import *
from key import Key

class AES:

    def __init__(self, input_string: str, key : Key):
        self.expanded_key = key

    def encrypt(self, input_string: str) -> str:
        # 0th round
        assert len(input_string) == 16, "Input to be encrypted must be 16 characters"
        ascii_input_arr = AES.generate_ascii_int_array_from_string(input_string)
        zeroth_round_int_array = Utils.xor_operation_on_int_array(ascii_input_arr,
                                                                  self.expanded_key.get_round_key(0))
        zeroth_round_state_matrix = Utils.convert_1d_arr_to_2d_column_major_state_matrix(zeroth_round_int_array)
        # print(f'Round 1 Input matrix: {Utils.convert_int_state_matrix_to_hex(zeroth_round_state_matrix)}')

    # round 1 - 9
    def perform_generic_round(self, prev_round_state_matrix : List[List[int]]) -> List[List[int]]:
        substitute_state_matrix = Utils.byte_substitution_sbox_for_matrix(prev_round_state_matrix)
        # print(f'Round 1 sbox substituted matrix: {Utils.convert_int_state_matrix_to_hex(substitute_state_matrix)}')
        left_shift_state_matrix = Utils.shift_left_row_state_matrix(substitute_state_matrix)
        # print(f'Round 1 left shifted matrix: {Utils.convert_int_state_matrix_to_hex(left_shift_state_matrix)}')







    @staticmethod
    def generate_ascii_int_array_from_string(plaintext_string: str) -> List[int]:
        size_adjusted_string = plaintext_string
        if len(plaintext_string) > 16:
            size_adjusted_string = plaintext_string[0:16]
        elif len(plaintext_string) < 16:
            size_adjusted_string = plaintext_string.ljust(16, '\0')  # pad string to the right with 0's

        ascii_array = [ord(size_adjusted_string[x]) for x in range(16)]
        print(f'Original string: {size_adjusted_string}\nString in Int: {ascii_array}')
        return ascii_array


AES("Two One Nine Two",Key("Thats my Kung Fu"))
