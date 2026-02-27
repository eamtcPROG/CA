import secrets
import struct


KEY_BYTES = 32
NONCE_BYTES = 8
MASK_32 = (1 << 32) - 1 
MASK_64 = (1 << 64) - 1

# Constant for the Salsa20 expansion 256-bit key | for 128-bit key, use "expand 16-byte k"
SALSA20_EXPANSION_CONSTANT = b"expand 32-byte k"


def rotate_left_32(x, n):
    x &= MASK_32
    return ((x << n) | (x >> (32 - n))) & MASK_32


def quarter_round(y, a, b, c, d):
    y[b] ^= rotate_left_32((y[a] + y[d]) & MASK_32, 7)
    y[c] ^= rotate_left_32((y[b] + y[a]) & MASK_32, 9)
    y[d] ^= rotate_left_32((y[c] + y[b]) & MASK_32, 13)
    y[a] ^= rotate_left_32((y[d] + y[c]) & MASK_32, 18)


def compute_block(expansion_constant, key, nonce, counter):
    
    c0, c1, c2, c3 = struct.unpack("<4I", expansion_constant)
    k = struct.unpack("<8I", key)
    n0, n1 = struct.unpack("<2I", nonce)
    ctr0 = counter & MASK_32
    ctr1 = (counter >> 32) & MASK_32

    y = [
        c0, k[0], k[1], k[2],
        k[3], c1, n0, n1,
        ctr0, ctr1, c2, k[4],
        k[5], k[6], k[7], c3,
    ]

    z = y.copy()
    for _ in range(10):
        # column rounds
        quarter_round(z, 0, 4, 8, 12)
        quarter_round(z, 5, 9, 13, 1)
        quarter_round(z, 10, 14, 2, 6)
        quarter_round(z, 15, 3, 7, 11)
        # row rounds
        quarter_round(z, 0, 1, 2, 3)
        quarter_round(z, 5, 6, 7, 4)
        quarter_round(z, 10, 11, 8, 9)
        quarter_round(z, 15, 12, 13, 14)

    for i in range(16):
        z[i] = (z[i] + y[i]) & MASK_32
    return struct.pack("<16I", *z)


def generate_key_stream(key, nonce, length):
    stream = bytearray()
    counter = 0
    while length > 0:
        block = compute_block(
            SALSA20_EXPANSION_CONSTANT, key, nonce, counter
        )
        take = min(64, length)
        stream.extend(block[:take])
        length -= take
        counter += 1
    return bytes(stream)


def generate_key():
    return secrets.token_bytes(KEY_BYTES)


def generate_nonce(counter = 1):
    return (counter & MASK_64).to_bytes(8, "little")


def encrypt(text,key,nonce):
    if len(key) != KEY_BYTES:
        raise ValueError(f"key must be {KEY_BYTES} bytes (256-bit)")
    if len(nonce) != NONCE_BYTES:
        raise ValueError(f"nonce must be {NONCE_BYTES} bytes (64-bit)")

    stream = generate_key_stream(key, nonce, len(text))
    return bytes(a ^ b for a, b in zip(text, stream))


def decrypt(text,key,nonce):
    return encrypt(text, key, nonce)


def bytes_to_binary(data):
    return "".join(format(byte, "08b") for byte in data)


if __name__ == "__main__":
    key = generate_key()
    nonce = generate_nonce(1)
    plaintext = b"Secret message: My name is Mihai, and I'm a student at the UTM"

    cipher = encrypt(plaintext, key, nonce)
    decrypted = decrypt(cipher, key, nonce)

    print("Key:", bytes_to_binary(key))
    print("Nonce:", bytes_to_binary(nonce))
    print("Cipher text:", bytes_to_binary(cipher))
    print("Decrypted text:", decrypted.decode('utf-8'))
    nonce = generate_nonce(2)
    cipher = encrypt(plaintext, key, nonce)
    decrypted = decrypt(cipher, key, nonce)
    print("Cipher text:", bytes_to_binary(cipher))
    print("Decrypted text:", decrypted.decode('utf-8'))
