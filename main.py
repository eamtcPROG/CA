import matplotlib.pylab as plt
from math import sqrt
from math import floor

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Standard English letter frequencies (as counts, typical running text)
STANDARD_ENGLISH_FREQUENCY = {
    'E': 127, 'T': 91, 'A': 82, 'O': 75, 'I': 70, 'N': 67, 'S': 63, 'H': 61,
    'R': 60, 'D': 43, 'L': 40, 'C': 28, 'U': 28, 'M': 24, 'W': 24, 'F': 22,
    'G': 20, 'Y': 20, 'P': 19, 'B': 15, 'V': 10, 'K': 8, 'J': 2, 'X': 2,
    'Q': 1, 'Z': 1,
}


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
    plt.bar(frequencies.keys(), frequencies.values())
    plt.show()

def compute_frequency_english():
    with open('english_words.txt', 'r') as f:
        text = f.read().upper().replace(' ', '').replace('\n', '')
    return frequency_analysis(text)

def get_substrings(text, min_n=3):
    text = text.upper().replace(' ', '')
    result = []
    n = min_n
    while True:
        if len(text) - n + 1 < 2:
            break
        counts = {}
        for i in range(len(text) - n + 1):
            sub = text[i : i + n]
            counts[sub] = counts.get(sub, 0) + 1
        repeated = [sub for sub, count in counts.items() if count > 1]
        if not repeated:
            break
        result.extend(repeated)
        n += 1
    # Keep only longest version of each repeat: drop any substring contained in another
    deduped = [
        s for s in result
        if not any(s != other and s in other for other in result)
    ]
    return deduped

def get_distance_between_substrings(text, substrings):
    text = text.upper().replace(' ', '')
    distances = {}
    for sub in substrings:
        positions = [i for i in range(len(text) - len(sub) + 1) if text[i : i + len(sub)] == sub]
        distances[sub] = [positions[j + 1] - positions[j] for j in range(len(positions) - 1)]
    return distances


def get_factors(number):
    factors = []
    n = number
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def get_factors_of_distance(distances):
    result = {}
    for substring, dist_list in distances.items():
        result[substring] = [{d: get_factors(d)} for d in dist_list]
    return result

def get_most_frequent_factor(factors):
    factor_count = {}
    for factor in factors:
        factor_count[factor] = factor_count.get(factor, 0) + 1
    return max(factor_count, key=factor_count.get)


def structure_to_array(data):
    result = []
    for key in data:
        for d in data[key]:
            for factors in d.values():
                result.extend(factors)
    return result

def compute_string_based_length(text, n):
    """For each m in 1..n, split text into m streams. result[m-1] = list of m strings."""
    result = []
    for m in range(1, n + 1):
        streams = [[] for _ in range(m)]
        for i, char in enumerate(text):
            if char in ALPHABET:
                streams[i % m].append(char)
        result.append([''.join(s) for s in streams])
    return result

def caesar_decrypt(cipher_text, key):
    plain_text = ''

    for c in cipher_text:
        index = ALPHABET.find(c)
        index = (index - key) % len(ALPHABET)
        plain_text = plain_text + ALPHABET[index]

    return plain_text



def frequency_diff(frequency, general_frequency):
    """Sum of absolute differences between normalized distributions. Lower = better match."""
    total_a = sum(frequency.values()) or 1
    total_b = sum(general_frequency.values()) or 1
    diff = 0.0
    for letter in ALPHABET:
        p_a = frequency.get(letter, 0) / total_a
        p_b = general_frequency.get(letter, 0) / total_b
        diff += abs(p_a - p_b)
    return diff


def correlation_score(frequency, general_frequency):
    """Dot product of normalized distributions. Higher = better match to English."""
    total_obs = sum(frequency.values()) or 1
    total_exp = sum(general_frequency.values()) or 1
    score = 0.0
    for letter in ALPHABET:
        obs = frequency.get(letter, 0) / total_obs
        exp = general_frequency.get(letter, 0) / total_exp
        score += obs * exp
    return score

def decrypt_for_each_letter(cipher_text, general_frequency):
    """Return the key letter(s) that had the best frequency match (correlation with English)."""
    scores = {}
    for key in range(len(ALPHABET)):
        plain_text = caesar_decrypt(cipher_text, key)
        frequency = frequency_analysis(plain_text)
        scores[key] = correlation_score(frequency, general_frequency)
    best_score = max(scores.values())  # higher correlation = better
    return [ALPHABET[k] for k in range(len(ALPHABET)) if scores[k] == best_score]

def get_possible_keys(streams, general_frequency):
    """For each stream (one per key position), return the best key letter(s). Returns list of lists."""
    result = []
    for stream in streams:
        letters = decrypt_for_each_letter(stream, general_frequency)
        result.append(letters)
    return result

if __name__ == '__main__':
    plain_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND THE DOG JUMPS OVER THE FOX AND THE FOX JUMPS OVER THE DOG"
    # Repeat to get longer ciphertext so frequency-based key recovery is reliable (~17 chars/stream is too few)
    plain_text = (plain_text + " ") * 2
    key = "HELPER"

    encrypted_text = encrypt(plain_text, key)
    print("Original plaintext:", plain_text)
    print("Key:", key)
    print("Encrypted text:", encrypted_text)
    decrypted_text = decrypt(encrypted_text, key)
    print("Decrypted text:", decrypted_text)

    frequency = frequency_analysis(encrypted_text)

    english_frequency = compute_frequency_english()
    print(english_frequency)
    # plot_distribution(frequency)
    # plot_distribution(english_frequency)

    substrings = get_substrings(encrypted_text)
    print(substrings)

    distances = get_distance_between_substrings(encrypted_text, substrings)
    print(distances)

    distances_factors = get_factors_of_distance(distances)
    print(distances_factors)

    factors = structure_to_array(distances_factors)
    print(factors)

    k_length = get_most_frequent_factor(factors)
    print(k_length)

    string_based_length = compute_string_based_length(encrypted_text, k_length)
    print(string_based_length)

    # Streams for the estimated key length (m = k_length)
    streams_for_key = string_based_length[k_length - 1]
    keys = get_possible_keys(streams_for_key, STANDARD_ENGLISH_FREQUENCY)
    print("Possible key letter(s) per position:", keys)
    print("Recovered key (first candidate per position):", "".join(c[0] for c in keys))