from BitVector import BitVector
from constants import Constants
from utils import Utils
from typing import *
from key import Key

class AES:

    def __init__(self, input_string: str, key : Key):
        assert len(input_string) == 16, "Input to be encrypted must be 16 characters"
        self.input_string = input_string
        self.ascii_input_arr = AES.generate_ascii_int_array_from_string(self.input_string)
        self.expanded_key = key
        # 0th round
        self.first_round_state_int_arr = Utils.xor_operation_on_int_array(self.ascii_input_arr,self.expanded_key.get_round_key(0))





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





