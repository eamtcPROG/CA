ALPHABET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encrypt(plain_text, key):
    plain_text = plain_text.upper().replace(' ', '')
    key = key.upper().replace(' ', '')

    cipher_text = ''
    key_index = 0

    for character in plain_text:
        index = (ALPHABET.find(character)+ALPHABET.find(key[key_index])) % len(ALPHABET)
        cipher_text = cipher_text + ALPHABET[index]

        key_index = key_index + 1

        if key_index == len(key):
            key_index = 0

    return cipher_text

def decrypt(cipher_text, key):

    cipher_text = cipher_text.upper().replace(' ', '')
    key = key.upper().replace(' ', '')

    plain_text = ''
    key_index = 0

    for character in cipher_text:
        index = (ALPHABET.find(character)-ALPHABET.find(key[key_index])) % len(ALPHABET)
        plain_text = plain_text + ALPHABET[index]

        key_index = key_index + 1

        if key_index == len(key):
            key_index = 0

    return plain_text

if __name__ == '__main__':
    plain_text = input("Enter the plain text: ")
    key = input("Enter the key: ")
    encrypted_text = encrypt(plain_text, key)
    decrypted_text = decrypt(encrypted_text, key)

    print("Encrypted text: ", encrypted_text)
    print("Decrypted text: ", decrypted_text)