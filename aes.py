from BitVector import BitVector
from constants import Constants
from utils import Utils
from typing import *
from key import Key
import logging

class AES:

    def __init__(self, key: Key):
        self.expanded_key = key

    def encrypt(self, input_string: str) -> str:
        # 0th round
        assert len(input_string) <= 16, "Input to be encrypted must be 16 characters or less"
        ascii_input_arr = AES.generate_ascii_int_array_from_string(input_string)
        zeroth_round_int_array = Utils.xor_operation_on_int_array(ascii_input_arr,
                                                                  self.expanded_key.get_round_key(0))
        zeroth_round_state_matrix = Utils.convert_1d_arr_to_2d_column_major_state_matrix(zeroth_round_int_array)
        # logging.debug(f'Round 1 Input matrix: {Utils.convert_int_state_matrix_to_hex_matrix(zeroth_round_state_matrix)}')

        round_output = zeroth_round_state_matrix
        for round_no in range(1, 11):
            round_output = self.perform_encryption_round(round_output, round_no)

        ciphertext = Utils.convert_2d_column_major_state_matrix_to_1d_arr(round_output)
        ciphertext_string = ''.join(chr(i) for i in ciphertext)
        logging.debug(f'----------Cyphertext---------:\nHex: {Utils.convert_int_array_to_hex_array(ciphertext)}')
        logging.debug(f'String: {ciphertext_string}')
        return ciphertext_string

    def decrypt(self, input_string: str) -> str:
        assert len(input_string) == 16, "Input to be decrypted must be 16 characters"
        ascii_input_arr = AES.generate_ascii_int_array_from_string(input_string)
        zeroth_round_int_array = Utils.xor_operation_on_int_array(ascii_input_arr,
                                                                  self.expanded_key.get_round_key(10))
        zeroth_round_state_matrix = Utils.convert_1d_arr_to_2d_column_major_state_matrix(zeroth_round_int_array)
        logging.debug(
            f'Decryption Round 1 Input matrix: {Utils.convert_int_state_matrix_to_hex_matrix(zeroth_round_state_matrix)}')

        round_output = zeroth_round_state_matrix
        for round_no in range(1, 11):
            round_output = self.perform_decryption_round(round_output, round_no)

        plaintext = Utils.convert_2d_column_major_state_matrix_to_1d_arr(round_output)
        plaintext_string = ''.join(chr(i) for i in plaintext)
        logging.debug(f'----------Plaintext---------:\nHex: {Utils.convert_int_array_to_hex_array(plaintext)}')
        logging.debug(f'String: {plaintext_string}')
        return plaintext_string

    # round 1 - 10
    def perform_decryption_round(self, prev_round_state_matrix: List[List[int]], round_no: int) -> List[List[int]]:
        assert 1 <= round_no <= 10, "Invalid round_no for generic round"

        # perform inverse shift row
        right_shift_state_matrix = Utils.shift_right_row_state_matrix(prev_round_state_matrix)
        logging.debug(
            f'Decryption Round {round_no} right shifted matrix: {Utils.convert_int_state_matrix_to_hex_matrix(right_shift_state_matrix)}')

        # perform inverse substitution bytes
        substitute_state_matrix = Utils.byte_substitution_inverse_sbox_for_matrix(right_shift_state_matrix)
        logging.debug(
            f'Decryption Round {round_no} inverse sbox substituted matrix: {Utils.convert_int_state_matrix_to_hex_matrix(substitute_state_matrix)}')

        # add round key
        round_key_matrix = Utils.convert_1d_arr_to_2d_column_major_state_matrix(
            self.expanded_key.get_round_key(10 - round_no))
        round_key_added_state_matrix = Utils.xor_operation_on_state_matrix(substitute_state_matrix, round_key_matrix)
        logging.debug(
            f'Decryption Round {round_no} round key added matrix: {Utils.convert_int_state_matrix_to_hex_matrix(round_key_added_state_matrix)}')

        if 1 <= round_no <= 9:
            # perform inverse mix column
            mix_col_state_matrix = Utils.matrix_multiply_for_bitvectors(Constants.inv_mixer,
                                                                        Utils.convert_int_state_matrix_to_bitvector_matrix(
                                                                            round_key_added_state_matrix))
            logging.debug(
                f'Decryption Round {round_no} inverse column mixed matrix: {Utils.convert_int_state_matrix_to_hex_matrix(mix_col_state_matrix)}')
        elif round_no == 10:
            logging.debug("Skipping column mixing for final round")
            mix_col_state_matrix = round_key_added_state_matrix  # skip for round 10

        return mix_col_state_matrix

    # Round 1-10
    def perform_encryption_round(self, prev_round_state_matrix: List[List[int]], round_no: int) -> List[List[int]]:
        assert 1 <= round_no <= 10, "Invalid round_no for generic round"

        # perform substitution bytes
        substitute_state_matrix = Utils.byte_substitution_sbox_for_matrix(prev_round_state_matrix)
        logging.debug(
            f'Round {round_no} sbox substituted matrix: {Utils.convert_int_state_matrix_to_hex_matrix(substitute_state_matrix)}')

        # perform shift row
        left_shift_state_matrix = Utils.shift_left_row_state_matrix(substitute_state_matrix)
        logging.debug(
            f'Round {round_no} left shifted matrix: {Utils.convert_int_state_matrix_to_hex_matrix(left_shift_state_matrix)}')

        if 1 <= round_no <= 9:
            # perform mix column
            mix_col_state_matrix = Utils.matrix_multiply_for_bitvectors(Constants.mixer,
                                                                        Utils.convert_int_state_matrix_to_bitvector_matrix(
                                                                            left_shift_state_matrix))
            logging.debug(
                f'Round {round_no} column mixed matrix: {Utils.convert_int_state_matrix_to_hex_matrix(mix_col_state_matrix)}')
        elif round_no == 10:
            logging.debug("Skipping column mixing for final round")
            mix_col_state_matrix = left_shift_state_matrix  # skip for round 10

        # add round key
        round_key_added_matrix = Utils.xor_operation_on_state_matrix(mix_col_state_matrix,
                                                                     Utils.convert_1d_arr_to_2d_column_major_state_matrix(
                                                                         self.expanded_key.get_round_key(round_no)))
        logging.debug(
            f'Round {round_no} round key added matrix: {Utils.convert_int_state_matrix_to_hex_matrix(round_key_added_matrix)}')

        return round_key_added_matrix

    @staticmethod
    def generate_ascii_int_array_from_string(plaintext_string: str) -> List[int]:
        size_adjusted_string = plaintext_string
        if len(plaintext_string) > 16:
            size_adjusted_string = plaintext_string[0:16]
        elif len(plaintext_string) < 16:
            size_adjusted_string = plaintext_string.ljust(16, '\0')  # pad string to the right with 0's

        ascii_array = [ord(size_adjusted_string[x]) for x in range(16)]
        logging.debug(f'Original string: {size_adjusted_string}\nString in Int: {ascii_array}')
        return ascii_array



