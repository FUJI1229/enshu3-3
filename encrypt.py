import util
import obfuscator
import insert

def xor_encrypt(data, key):
    data_bytes = data.encode('utf-8')
    key_bytes = key.encode('utf-8')
    encrypted_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data_bytes)])
    return encrypted_bytes


def xor_encrypt_to_c_literal(data, key):
    data_bytes = data.encode('ascii')
    key_bytes = key.encode('ascii')
    encrypted_bytes = [b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data_bytes)]
    c_string = ''.join(f'\\x{b:02x}' for b in encrypted_bytes)
    return c_string


def apply_xor_encryption(code, xor_pairs):
    xor_map = {}
    for i in range(0, len(xor_pairs), 2):
        original = xor_pairs[i]
        key = xor_pairs[i + 1]
        encrypted = xor_encrypt_to_c_literal(original, key)
        xor_map[original] = (encrypted, key)
    decrypt_func_name = util.generate_random_func_name()
    code = obfuscator.xor_obfuscate_literals(code, xor_map, decrypt_func_name)
    code = insert.insert_decryption_function(code, decrypt_func_name)
    return code