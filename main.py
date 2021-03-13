from aes import AES
from key import Key

# initialize logger
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # Change level to logging.DEBUG for detailed computation


if __name__ == "__main__":
    key_string = input("Enter key: ")
    text_to_be_encrypted = input("Enter text to be encrypted: ")

    # Expand key and instantiate AES module
    key = Key(key_string)
    aes = AES(key)

    split_text = [text_to_be_encrypted[i:i+16] for i in range(0, len(text_to_be_encrypted), 16)]

    logging.info("-----------Encrypting-----------\n")
    cyphertext_arr = []
    for text_fragment in split_text:
        cyphertext_for_fragment = aes.encrypt(text_fragment)
        logging.info(f'Input Text: {text_fragment}\nCyphertext: {cyphertext_for_fragment}\n')
        cyphertext_arr.append(cyphertext_for_fragment)

    logging.info("-----------Decrypting-----------\n")
    decrypted_text_arr = []
    for cyphertext_fragment in cyphertext_arr:
        decrypted_text_fragment = aes.decrypt(cyphertext_fragment)
        logging.info(f'CypherText: {cyphertext_fragment}\nDecrypted Plaintext: {decrypted_text_fragment}\n')
        decrypted_text_arr.append(decrypted_text_fragment)

    logging.info("-----------Final Result-----------\n")
    cyphertext_full = "".join(cyphertext_arr)
    logging.info(f'Cyphertext: {cyphertext_full}')

    decrypted_text_full = "".join(decrypted_text_arr).replace('\0', "")  # remove placeholder null characters
    logging.info(f'Decrpyted Plaintext: {decrypted_text_full}')