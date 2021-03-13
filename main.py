from aes import AES
from key import Key
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


if __name__ == "__main__":
    key_string = input("Enter key: ")
    text_to_be_encrypted = input("Enter text to be encrypted: ")

    # Expand key and instantiate AES module
    key = Key(key_string)
    aes = AES(key)

    split_text = [text_to_be_encrypted[i:i+16] for i in range(0, len(text_to_be_encrypted), 16)]

    print("-----------Encrypting-----------")
    cyphertext_arr = []
    for text_fragment in split_text:
        cyphertext_for_fragment = aes.encrypt(text_fragment)
        print(f'Input Text: {text_fragment}\nCyphertext: {cyphertext_for_fragment}\n\n')
        cyphertext_arr.append(cyphertext_for_fragment)

    print("-----------Decrypting-----------")
    decrypted_text_arr = []
    for cyphertext_fragment in cyphertext_arr:
        decrypted_text_fragment = aes.decrypt(cyphertext_fragment)
        print(f'CypherText: {cyphertext_fragment}\nDecrypted Plaintext: {decrypted_text_fragment}\n\n')
        decrypted_text_arr.append(decrypted_text_fragment)

    cyphertext_full = "".join(cyphertext_arr)
    print(f'Cyphertext: {cyphertext_full}')

    decrypted_text_full = "".join(decrypted_text_arr).replace('\0', "")
    print(f'Decrpyted Text: {decrypted_text_full}')