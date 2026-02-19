import os
import itertools

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


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

def frequency_analysis(text):
    # the text we analyse
    text = text.upper().replace(' ', '')

    # we use a dictionary to store the letter-frequency pair
    letter_frequencies = {}

    # initialize the dictionary (of course with 0 frequencies)
    for letter in ALPHABET:
        letter_frequencies[letter] = 0

    # let's consider the text we want to analyse
    for letter in text:
        if letter in ALPHABET:
            letter_frequencies[letter] += 1

    return letter_frequencies


def plot_distribution(frequencies):
    import matplotlib.pylab as plt
    plt.bar(frequencies.keys(), frequencies.values())
    plt.show()



if __name__ == '__main__':
    plain_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND THE DOG JUMPS OVER THE FOX AND THE FOX JUMPS OVER THE DOG"
    key = "SECRET"

    encrypted_text = encrypt(plain_text, key)
    print("Original plaintext:", plain_text)
    print("Key:", key)
    print("Encrypted text:", encrypted_text)

    frequency_analysis = frequency_analysis(encrypted_text)
    print("Frequency analysis:", frequency_analysis)
    plot_distribution(frequency_analysis)